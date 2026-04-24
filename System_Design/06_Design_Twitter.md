# 🏗️ Case Study: Twitter (Social Feed)

## 📋 Requirements

**Functional:**
- Users can post tweets (280 characters)
- Users can follow/unfollow others
- Home timeline shows tweets from followed users
- Likes, retweets, replies
- Trending hashtags
- Search (tweets, users, hashtags)
- Notifications (likes, follows, retweets)

**Non-Functional:**
- 200M daily active users
- 500M tweets per day
- 200K tweets per second (peak, World Cup etc.)
- Timeline loads in < 500ms
- 99.99% availability

---

## 📊 Capacity Estimation

```
Tweets/day: 500M = ~5,800 tweets/sec (avg), 200K/sec (peak!)
Reads: 200M users × 30 visits/day × 20 tweets/visit = 120B timeline reads/day
  = ~1.4M timeline reads/sec!

Read:Write ratio = 1.4M / 5,800 = ~240:1 (extremely read-heavy!)
→ Optimize aggressively for reads

Tweet size: 140 bytes (text) + 500 bytes (metadata) = ~640 bytes
500M × 640 = 320GB/day of tweet data
1 year: ~117TB

The core challenge: Pre-computing 200M users' timelines efficiently
```

---

## 🏗️ High Level Architecture

```
[Twitter Web/App]
      ↓
[CloudFront CDN] → [Static assets]
      ↓
[AWS API Gateway + ALB]
      ↓
┌──────────────────────────────────────────────────────────────┐
│                      MICROSERVICES                           │
│                                                             │
│  [Tweet Service]       [User Service]   [Follow Service]    │
│  [Timeline Service]    [Search Service] [Notification Svc]  │
│  [Hashtag Service]     [Media Service]  [Trend Service]     │
└──────────────────────────────────────────────────────────────┘
      ↓
[PostgreSQL]  [Redis]  [Kafka]  [Elasticsearch]  [S3]
              ↑
     (Most critical — stores pre-computed timelines!)
```

---

## 🐦 Tweet Service

```javascript
// Tweet Service

app.post('/api/tweets', authenticate, rateLimitTweets, async (req, res) => {
  const { content, replyToId, retweetId, mediaIds = [] } = req.body;
  
  // Validate
  if (!content && !retweetId && mediaIds.length === 0) {
    return res.status(400).json({ error: 'Tweet must have content or media' });
  }
  if (content && content.length > 280) {
    return res.status(400).json({ error: 'Tweet exceeds 280 characters' });
  }
  
  // Extract hashtags and mentions
  const hashtags = (content?.match(/#[\w]+/g) || []).map(h => h.slice(1).toLowerCase());
  const mentions = (content?.match(/@[\w]+/g) || []).map(m => m.slice(1).toLowerCase());
  
  // Create tweet
  const tweet = await db.query(
    'INSERT INTO tweets (user_id, content, reply_to_id, retweet_of_id) VALUES ($1, $2, $3, $4) RETURNING *',
    [req.user.id, content, replyToId, retweetId]
  );
  
  // Update user tweet count
  await db.query('UPDATE users SET tweet_count = tweet_count + 1 WHERE id = $1', [req.user.id]);
  
  // Link media
  if (mediaIds.length > 0) {
    await db.query(
      'UPDATE media SET tweet_id = $1 WHERE id = ANY($2) AND user_id = $3',
      [tweet.rows[0].id, mediaIds, req.user.id]
    );
  }
  
  // If retweet: Update original tweet count
  if (retweetId) {
    await db.query('UPDATE tweets SET retweet_count = retweet_count + 1 WHERE id = $1', [retweetId]);
  }
  
  // Fan-out to followers (async)
  await kafkaProducer.send({
    topic: 'tweet-fanout',
    messages: [{
      key: req.user.id,
      value: JSON.stringify({ tweetId: tweet.rows[0].id, userId: req.user.id, hashtags, mentions })
    }]
  });
  
  // Process hashtags
  if (hashtags.length > 0) {
    processHashtags(tweet.rows[0].id, hashtags).catch(console.error);
  }
  
  // Send mention notifications
  if (mentions.length > 0) {
    notifyMentions(mentions, tweet.rows[0].id, req.user.id).catch(console.error);
  }
  
  res.status(201).json(tweet.rows[0]);
});
```

---

## 📰 Timeline Service (Core Design Challenge)

```javascript
// This is the hardest part of Twitter at scale!

class TimelineService {
  // Push approach: When you tweet, push to all followers' timelines
  async fanOutTweet(tweetId, userId) {
    const user = await userService.getUser(userId);
    
    // Decision: Is this user a "celebrity"?
    const CELEBRITY_THRESHOLD = 1_000_000; // 1M followers
    
    if (user.followerCount > CELEBRITY_THRESHOLD) {
      // Celebrity: Don't fan-out. Pull their tweets at read time.
      await redis.zadd('celebrity_users', user.followerCount, userId);
      return;
    }
    
    // Regular user: Fan-out to all followers
    let offset = 0;
    const BATCH_SIZE = 1000;
    
    while (true) {
      const followers = await db.query(
        'SELECT follower_id FROM follows WHERE following_id = $1 LIMIT $2 OFFSET $3',
        [userId, BATCH_SIZE, offset]
      );
      
      if (followers.rows.length === 0) break;
      
      const pipeline = redis.pipeline();
      followers.rows.forEach(({ follower_id }) => {
        // Add tweet to follower's home timeline (sorted set by timestamp)
        pipeline.zadd(`timeline:${follower_id}`, Date.now(), tweetId);
        // Keep only latest 1000 tweets in timeline
        pipeline.zremrangebyrank(`timeline:${follower_id}`, 0, -1001);
        // Set TTL if user hasn't been active
        pipeline.expire(`timeline:${follower_id}`, 7 * 24 * 60 * 60); // 7 days
      });
      
      await pipeline.exec();
      
      offset += BATCH_SIZE;
      if (followers.rows.length < BATCH_SIZE) break;
    }
  }
  
  // Read timeline (hybrid approach)
  async getHomeTimeline(userId, cursor = null, limit = 20) {
    // 1. Get pre-computed timeline from Redis
    const maxScore = cursor ? parseFloat(cursor) : '+inf';
    
    const cachedTweetIds = await redis.zrevrangebyscore(
      `timeline:${userId}`,
      maxScore,
      '-inf',
      'WITHSCORES',
      'LIMIT', 0, limit
    );
    
    let tweetIds = [];
    let scores = [];
    for (let i = 0; i < cachedTweetIds.length; i += 2) {
      tweetIds.push(cachedTweetIds[i]);
      scores.push(cachedTweetIds[i + 1]);
    }
    
    // 2. Pull celebrity tweets (not in pre-computed timeline)
    const followingCelebrities = await this.getUserFollowedCelebrities(userId);
    
    if (followingCelebrities.length > 0) {
      const celebTweets = await db.query(
        'SELECT id, created_at FROM tweets WHERE user_id = ANY($1) AND created_at < $2 ORDER BY created_at DESC LIMIT $3',
        [followingCelebrities, cursor ? new Date(parseFloat(cursor)) : new Date(), limit]
      );
      
      tweetIds = [...tweetIds, ...celebTweets.rows.map(t => t.id)];
    }
    
    if (tweetIds.length === 0) {
      // Timeline empty/expired — rebuild from DB
      return this.rebuildTimeline(userId, limit);
    }
    
    // 3. Fetch full tweet data
    const tweets = await this.getTweetsByIds(tweetIds);
    
    // Sort by timestamp (merge pre-computed + celebrity)
    tweets.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));
    
    const paginatedTweets = tweets.slice(0, limit);
    const nextCursor = paginatedTweets.length === limit 
      ? new Date(paginatedTweets[paginatedTweets.length - 1].createdAt).getTime().toString()
      : null;
    
    return { tweets: paginatedTweets, nextCursor, hasMore: !!nextCursor };
  }
  
  // Rebuild timeline for user (cache miss or cold start)
  async rebuildTimeline(userId, limit = 1000) {
    const following = await db.query(
      'SELECT following_id FROM follows WHERE follower_id = $1',
      [userId]
    );
    
    const followingIds = following.rows.map(r => r.following_id);
    
    const tweets = await db.query(
      'SELECT id, created_at FROM tweets WHERE user_id = ANY($1) AND created_at > NOW() - INTERVAL \'7 days\' ORDER BY created_at DESC LIMIT $2',
      [followingIds, limit]
    );
    
    if (tweets.rows.length > 0) {
      const pipeline = redis.pipeline();
      tweets.rows.forEach(tweet => {
        pipeline.zadd(`timeline:${userId}`, new Date(tweet.created_at).getTime(), tweet.id);
      });
      pipeline.expire(`timeline:${userId}`, 7 * 24 * 60 * 60);
      await pipeline.exec();
    }
    
    return this.getHomeTimeline(userId);
  }
  
  async getUserFollowedCelebrities(userId) {
    const allFollowing = await db.query(
      'SELECT following_id FROM follows WHERE follower_id = $1',
      [userId]
    );
    
    const celebrities = await redis.smembers('celebrity_users');
    const celebritySet = new Set(celebrities);
    
    return allFollowing.rows
      .map(r => r.following_id)
      .filter(id => celebritySet.has(id));
  }
}

// Kafka consumer for fan-out
const tweetFanoutConsumer = kafka.consumer({ groupId: 'tweet-fanout-group' });

await tweetFanoutConsumer.subscribe({ topic: 'tweet-fanout' });

await tweetFanoutConsumer.run({
  partitionsConsumedConcurrently: 3,
  eachMessage: async ({ topic, partition, message }) => {
    const { tweetId, userId, hashtags } = JSON.parse(message.value.toString());
    await timelineService.fanOutTweet(tweetId, userId);
  }
});
```

---

## ❤️ Likes and Retweets

```javascript
// Optimized for 57K likes/sec

app.post('/api/tweets/:id/like', authenticate, async (req, res) => {
  const { id: tweetId } = req.params;
  const userId = req.user.id;
  
  // Atomic: Add to set (returns 1 if added, 0 if already existed)
  const added = await redis.sadd(`tweet:${tweetId}:likers`, userId);
  
  if (added === 0) {
    // Already liked → unlike
    await redis.srem(`tweet:${tweetId}:likers`, userId);
    await redis.decr(`tweet:${tweetId}:likes`);
    
    // Queue DB update
    await likesQueue.add({ tweetId, userId, action: 'unlike' });
    
    return res.json({ liked: false, likeCount: await redis.get(`tweet:${tweetId}:likes`) });
  }
  
  const likeCount = await redis.incr(`tweet:${tweetId}:likes`);
  
  // Queue DB update (async, non-blocking)
  await likesQueue.add({ tweetId, userId, action: 'like' });
  
  // Notify tweet author (async)
  notificationService.notifyLike(tweetId, userId).catch(() => {});
  
  res.json({ liked: true, likeCount });
});

// Retweet
app.post('/api/tweets/:id/retweet', authenticate, async (req, res) => {
  const { id: tweetId } = req.params;
  const userId = req.user.id;
  
  // Check if already retweeted
  const existing = await db.query(
    'SELECT id FROM tweets WHERE user_id = $1 AND retweet_of_id = $2',
    [userId, tweetId]
  );
  
  if (existing.rows[0]) {
    // Undo retweet
    await db.query('DELETE FROM tweets WHERE id = $1', [existing.rows[0].id]);
    await db.query('UPDATE tweets SET retweet_count = retweet_count - 1 WHERE id = $1', [tweetId]);
    return res.json({ retweeted: false });
  }
  
  // Create retweet
  const retweet = await db.query(
    'INSERT INTO tweets (user_id, retweet_of_id) VALUES ($1, $2) RETURNING id',
    [userId, tweetId]
  );
  
  await db.query('UPDATE tweets SET retweet_count = retweet_count + 1 WHERE id = $1', [tweetId]);
  
  // Fan out to retweeter's followers
  await kafkaProducer.send({
    topic: 'tweet-fanout',
    messages: [{ value: JSON.stringify({ tweetId: retweet.rows[0].id, userId }) }]
  });
  
  res.json({ retweeted: true });
});
```

---

## 🔥 Trending Hashtags

```javascript
// Real-time trending computation

// When tweet is created with hashtags:
async function processHashtags(tweetId, hashtags) {
  const now = Date.now();
  const windowKey = `trends:${Math.floor(now / (60 * 60 * 1000))}`; // Hourly bucket
  
  const pipeline = redis.pipeline();
  hashtags.forEach(hashtag => {
    // Increment in sorted set (score = count)
    pipeline.zincrby(windowKey, 1, hashtag);
    pipeline.expire(windowKey, 2 * 60 * 60); // Keep 2 hours
  });
  await pipeline.exec();
}

// Get trending hashtags
app.get('/api/trending', async (req, res) => {
  const cacheKey = 'trending:hashtags:global';
  
  const cached = await redis.get(cacheKey);
  if (cached) return res.json(JSON.parse(cached));
  
  // Aggregate last 24 hours of hourly buckets
  const now = Date.now();
  const hourlyKeys = Array.from({ length: 24 }, (_, i) => 
    `trends:${Math.floor((now - i * 60 * 60 * 1000) / (60 * 60 * 1000))}`
  );
  
  // Union all hourly sorted sets
  const tempKey = `trends:union:${Date.now()}`;
  await redis.zunionstore(tempKey, hourlyKeys.length, ...hourlyKeys);
  
  const trending = await redis.zrevrangebyscore(tempKey, '+inf', '-inf', 'WITHSCORES', 'LIMIT', 0, 10);
  await redis.del(tempKey);
  
  const result = [];
  for (let i = 0; i < trending.length; i += 2) {
    result.push({ hashtag: trending[i], count: parseInt(trending[i + 1]) });
  }
  
  await redis.setex(cacheKey, 60, JSON.stringify(result)); // Cache 1 minute
  
  res.json(result);
});
```

---

## 🔍 Search

```javascript
// Elasticsearch for tweet and user search

// Index tweets as they're created
kafkaConsumer.on('tweet-created', async (tweet) => {
  await elasticsearch.index({
    index: 'tweets',
    id: tweet.id,
    document: {
      content: tweet.content,
      userId: tweet.userId,
      username: tweet.username,
      hashtags: tweet.hashtags,
      likeCount: tweet.likeCount,
      retweetCount: tweet.retweetCount,
      createdAt: tweet.createdAt
    }
  });
});

app.get('/api/search', async (req, res) => {
  const { q, type = 'tweets', page = 1, limit = 20 } = req.query;
  
  if (type === 'tweets') {
    const results = await elasticsearch.search({
      index: 'tweets',
      query: {
        bool: {
          must: [{ match: { content: { query: q, operator: 'and' } } }],
          should: [{ match_phrase: { content: q } }]
        }
      },
      sort: [{ likeCount: 'desc' }, { createdAt: 'desc' }],
      from: (page - 1) * limit, size: limit
    });
    
    return res.json({ tweets: results.hits.hits.map(h => h._source), total: results.hits.total.value });
  }
  
  if (type === 'users') {
    const results = await elasticsearch.search({
      index: 'users',
      query: {
        bool: {
          should: [
            { match_phrase_prefix: { username: q } },
            { match: { displayName: q } }
          ]
        }
      },
      sort: [{ followerCount: 'desc' }],
      size: limit
    });
    
    return res.json({ users: results.hits.hits.map(h => h._source) });
  }
});
```

---

## 🎯 Interview Discussion Points

### Key Design Decisions

1. **The Celebrity Problem (Core Twitter Challenge):**
   - Cardi B tweets → 70M followers need it in their timeline
   - Push model: 70M Redis writes = too slow
   - Solution: Mark users with >1M followers as "celebrities"
   - Regular fan-out for normal users
   - Pull celebrity tweets at read time (merge with pre-computed timeline)

2. **Timeline Pre-computation:**
   - User's home timeline = Redis sorted set of tweet IDs
   - Score = tweet timestamp
   - Fan-out on write: When you tweet, add to all followers' Redis sets
   - Keeps read path fast (just get from Redis)

3. **Scale Numbers:**
   - Pre-computed timelines: 200M users × 1000 tweet IDs × 8 bytes = 1.6TB Redis
   - With replication: ~5TB Redis — expensive but enables 1.4M reads/sec!

4. **Trending:**
   - Per-hour counters in Redis sorted sets
   - Union and score hourly buckets to get 24h trends
   - Region-specific trending by maintaining separate keys per country

5. **Eventual Consistency:**
   - New tweet appears in followers' feeds within ~2-5 seconds (fan-out takes time)
   - Twitter is OK with this! Users don't notice 2-second delay.

---

### Navigation
**Prev:** [05_Design_Netflix.md](05_Design_Netflix.md) | **Index:** [00_Index.md](00_Index.md) | **Next:** [07_Design_Dropbox.md](07_Design_Dropbox.md)
