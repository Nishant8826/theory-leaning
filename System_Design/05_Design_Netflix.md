# 🏗️ Case Study: Netflix (Video Streaming)

## 📋 Requirements

**Functional:**
- Users can browse and search for movies/shows
- Users can stream video (adaptive bitrate)
- Continue watching from where you left off
- Personalized recommendations
- Multiple user profiles per account
- Downloads for offline viewing
- Multiple device support

**Non-Functional:**
- 230M subscribers, 100M+ hours streamed daily
- Video quality adapts to bandwidth (240p to 4K)
- < 2 second startup time
- 99.99% availability
- Global scale (190+ countries)

---

## 📊 Capacity Estimation

```
Content:
  Netflix has ~6,000 titles
  Each title in 10+ formats/resolutions: 6,000 × 10 = 60,000 video files
  Average file size: 10GB
  Total video storage: 60,000 × 10GB = 600TB (manageable!)
  
Streaming:
  100M hours/day = 4.1M concurrent streams
  Average bitrate: 5 Mbps
  Total bandwidth: 4.1M × 5Mbps = 20.5 Tbps!
  → This is why CDN is critical — Netflix is ~35% of US internet traffic!

User events (plays, pauses, seeks): ~10M events/sec → Kafka handles this
```

---

## 🏗️ High Level Architecture

```
[Users worldwide]
       ↓
[Netflix CDN (Open Connect)] ← Billions of video bytes!
       ↓ (only for API calls)
[AWS CloudFront]
       ↓
[API Gateway + Load Balancer]
       ↓
┌─────────────────────────────────────────────────────────────┐
│                     MICROSERVICES                            │
│  [User Service]       [Auth Service]    [Profile Service]   │
│  [Content Service]    [Search Service]  [Recommendation Svc]│
│  [Streaming Service]  [Billing Service] [Analytics Service] │
└─────────────────────────────────────────────────────────────┘
       ↓
[PostgreSQL] [Cassandra] [Redis] [Elasticsearch] [Kafka] [S3]
```

---

## 🎬 Video Upload and Processing Pipeline

```javascript
// Content Ops uploads raw video
// AWS Step Functions orchestrates the pipeline

// 1. Raw video upload to S3
app.post('/api/admin/content/upload-url', authenticateAdmin, async (req, res) => {
  const { title, contentType } = req.body;
  const contentId = uuidv4();
  
  const uploadUrl = s3.getSignedUrl('putObject', {
    Bucket: process.env.RAW_VIDEO_BUCKET,
    Key: `raw/${contentId}/original.${getExtension(contentType)}`,
    ContentType: contentType,
    Expires: 3600 // 1 hour to upload
  });
  
  await db.query(
    'INSERT INTO content (id, title, status) VALUES ($1, $2, $3)',
    [contentId, title, 'uploading']
  );
  
  res.json({ contentId, uploadUrl });
});

// 2. S3 trigger → Start Step Functions workflow
// (Configured in AWS Console/CDK)

// 3. Transcoding function (runs in parallel for all resolutions!)
async function transcodeVideo(contentId, resolution, targetBitrate) {
  const inputKey = `raw/${contentId}/original.mp4`;
  const outputKey = `processed/${contentId}/${resolution}p/`;
  
  // AWS Elastic Transcoder or MediaConvert
  const job = await mediaConvert.createJob({
    Role: process.env.MEDIA_CONVERT_ROLE,
    Settings: {
      Inputs: [{ FileInput: `s3://${process.env.RAW_BUCKET}/${inputKey}` }],
      OutputGroups: [{
        Name: 'HLS',
        OutputGroupSettings: {
          Type: 'HLS_GROUP_SETTINGS',
          HlsGroupSettings: {
            SegmentLength: 6, // 6-second HLS segments
            Destination: `s3://${process.env.CDN_BUCKET}/${outputKey}`
          }
        },
        Outputs: [{
          VideoDescription: {
            Width: resolutionMap[resolution].width,
            Height: resolutionMap[resolution].height,
            CodecSettings: {
              Codec: 'H_264',
              H264Settings: {
                Bitrate: targetBitrate,
                FramerateDenominator: 1,
                FramerateNumerator: 24
              }
            }
          },
          AudioDescriptions: [{
            CodecSettings: { Codec: 'AAC', AacSettings: { Bitrate: 128000 } }
          }],
          ContainerSettings: { Container: 'M3U8' }
        }]
      }]
    }
  }).promise();
  
  return { jobId: job.Job.Id, status: 'transcoding' };
}

// Generate master playlist (m3u8) that includes all quality variants
async function generateMasterPlaylist(contentId, availableResolutions) {
  const manifestContent = `
#EXTM3U
#EXT-X-VERSION:3

${availableResolutions.map(({ resolution, bitrate, url }) => `
#EXT-X-STREAM-INF:BANDWIDTH=${bitrate},RESOLUTION=${resolution}
${url}`).join('\n')}
`.trim();
  
  await s3.putObject({
    Bucket: process.env.CDN_BUCKET,
    Key: `processed/${contentId}/master.m3u8`,
    Body: manifestContent,
    ContentType: 'application/x-mpegURL'
  }).promise();
}

// 4. After transcoding complete → Update database
async function onTranscodingComplete(contentId) {
  await db.query('UPDATE content SET status = $1 WHERE id = $2', ['ready', contentId]);
  await elasticsearch.index({
    index: 'content',
    id: contentId,
    document: await getContentMetadata(contentId)
  });
  
  // Trigger thumbnail generation
  await lambdaClient.invoke({
    FunctionName: 'generate-thumbnails',
    Payload: JSON.stringify({ contentId })
  }).promise();
}
```

---

## 📺 Video Streaming with Adaptive Bitrate

```javascript
// Streaming Service — Returns HLS manifest and signed URLs

app.get('/api/stream/:contentId', authenticate, async (req, res) => {
  const { contentId } = req.params;
  
  // Verify user has subscription
  const subscription = await subscriptionService.getActiveSubscription(req.user.id);
  if (!subscription) return res.status(403).json({ error: 'No active subscription' });
  
  // Get content metadata
  const content = await db.query('SELECT * FROM content WHERE id = $1 AND status = $2', 
    [contentId, 'ready']);
  if (!content.rows[0]) return res.status(404).json({ error: 'Content not found' });
  
  // Check geo-restrictions
  const userCountry = getCountryFromIP(req.ip);
  if (content.rows[0].restricted_countries?.includes(userCountry)) {
    return res.status(403).json({ error: 'Not available in your region' });
  }
  
  // Generate signed CloudFront URL for the master playlist
  // This allows client to access the HLS files without being authenticated per request
  const manifestKey = `processed/${contentId}/master.m3u8`;
  
  const signedUrl = cloudfront.getSignedUrl({
    url: `${process.env.CDN_URL}/${manifestKey}`,
    keypairId: process.env.CF_KEY_PAIR_ID,
    privateKey: process.env.CF_PRIVATE_KEY,
    expires: Math.floor(Date.now() / 1000) + 3600 // 1 hour
  });
  
  // Record stream start event
  await kafkaProducer.send({
    topic: 'stream-events',
    messages: [{ value: JSON.stringify({ event: 'stream_started', userId: req.user.id, contentId, timestamp: Date.now() }) }]
  });
  
  // Update watch history
  await updateWatchHistory(req.user.id, contentId, req.params.profileId);
  
  res.json({
    streamUrl: signedUrl,  // Master m3u8 playlist
    subtitleTracks: await getSubtitleTracks(contentId, req.user.preferredLanguage),
    audioTracks: await getAudioTracks(contentId)
  });
});

// HLS Player (React Native / Web) handles adaptive streaming automatically:
// - Starts at low quality, monitors bandwidth
// - Upgrades quality when bandwidth allows
// - Degrades quality when bandwidth drops
// - All handled by HLS.js (web) or AVPlayer (iOS)

// Update watch position
app.post('/api/watch-history/position', authenticate, async (req, res) => {
  const { contentId, profileId, position, duration } = req.body;
  
  // Upsert watch position (Redis for low latency, persist to DB periodically)
  await redis.hset(`watch:${req.user.id}:${profileId}`, contentId, JSON.stringify({
    position,
    duration,
    updatedAt: Date.now()
  }));
  
  // If > 90% watched → mark as completed
  if (position / duration > 0.9) {
    await db.query(
      'INSERT INTO completed_content (user_id, profile_id, content_id) VALUES ($1, $2, $3) ON CONFLICT DO NOTHING',
      [req.user.id, profileId, contentId]
    );
  }
  
  res.status(204).send();
});

// Get continue watching list
app.get('/api/continue-watching', authenticate, async (req, res) => {
  const { profileId } = req.query;
  
  // Get from Redis (fast!) then enrich with content details
  const watchData = await redis.hgetall(`watch:${req.user.id}:${profileId}`);
  
  const contentIds = Object.keys(watchData)
    .map(id => ({ id, ...JSON.parse(watchData[id]) }))
    .filter(w => w.position / w.duration < 0.9) // Not fully watched
    .sort((a, b) => b.updatedAt - a.updatedAt)   // Most recently watched
    .slice(0, 20);
  
  const contentDetails = await getContentByIds(contentIds.map(c => c.id));
  
  res.json(contentIds.map((item, i) => ({
    ...contentDetails[i],
    position: item.position,
    duration: item.duration,
    percentWatched: Math.round((item.position / item.duration) * 100)
  })));
});
```

---

## 🎯 Recommendation System

```javascript
// AI-powered recommendation using collaborative filtering

// Collect viewing events for ML training
const viewingEvents = [
  { userId, contentId, watchedPercent, rating, timestamp },
  // ...
];

// Two approaches:
// 1. Collaborative Filtering: "Users like you also watched..."
// 2. Content-Based: "Because you watched Action movies..."

// Real Netflix uses both + many other signals

class RecommendationService {
  async getPersonalizedFeed(userId, profileId, limit = 20) {
    const cacheKey = `recommendations:${userId}:${profileId}`;
    
    // Check Redis cache (recommendations computed by ML job, cached for 1 hour)
    const cached = await redis.get(cacheKey);
    if (cached) return JSON.parse(cached);
    
    // Fetch pre-computed recommendations from Cassandra
    // (ML model runs every hour, stores results)
    const recs = await cassandra.execute(
      'SELECT content_id, score FROM user_recommendations WHERE user_id = ? AND profile_id = ? ORDER BY score DESC LIMIT ?',
      [userId, profileId, limit]
    );
    
    // Fetch content details
    const contentIds = recs.rows.map(r => r.content_id);
    const contentDetails = await getContentByIds(contentIds);
    
    const result = recs.rows.map((rec, i) => ({
      ...contentDetails[i],
      recommendationScore: rec.score
    }));
    
    // Cache for 1 hour
    await redis.setex(cacheKey, 3600, JSON.stringify(result));
    
    return result;
  }
  
  // Simple collaborative filtering (simplified version)
  async computeRecommendations(userId) {
    // Get user's watch history and ratings
    const userHistory = await db.query(
      'SELECT content_id, watch_percent, rating FROM watch_events WHERE user_id = $1',
      [userId]
    );
    
    // Get genres the user likes
    const likedGenres = await db.query(
      'SELECT genres FROM content WHERE id = ANY($1) AND watch_percent > 70',
      [userHistory.rows.map(h => h.content_id)]
    );
    
    // Find similar content
    const recommendations = await db.query(
      'SELECT id, title FROM content WHERE genres && $1::text[] AND id != ALL($2) ORDER BY rating DESC LIMIT 50',
      [likedGenres.map(g => g.genres), userHistory.rows.map(h => h.content_id)]
    );
    
    return recommendations.rows;
  }
}

// Trending content (globally)
async function getTrendingContent() {
  const cacheKey = 'trending:global';
  
  const cached = await redis.get(cacheKey);
  if (cached) return JSON.parse(cached);
  
  // Compute from last 24h events in Cassandra
  const trending = await cassandra.execute(
    'SELECT content_id, COUNT(*) as views FROM stream_events WHERE timestamp > ? GROUP BY content_id ORDER BY views DESC LIMIT 20',
    [Date.now() - 24 * 60 * 60 * 1000]
  );
  
  const result = await getContentByIds(trending.rows.map(r => r.content_id));
  await redis.setex(cacheKey, 300, JSON.stringify(result)); // Cache 5 minutes
  
  return result;
}
```

---

## 🔍 Content Search

```javascript
// Elasticsearch for content search

// Index content
await elasticsearch.index({
  index: 'content',
  id: contentId,
  document: {
    title: 'Stranger Things',
    description: 'When...',
    genres: ['Drama', 'Sci-Fi', 'Horror'],
    cast: ['Winona Ryder', 'David Harbour'],
    director: 'The Duffer Brothers',
    year: 2016,
    rating: 8.7,
    maturityRating: 'TV-14',
    tags: ['supernatural', '80s', 'small town']
  }
});

app.get('/api/search', async (req, res) => {
  const { q, genre, year, rating, page = 1, limit = 20 } = req.query;
  
  const query = {
    bool: {
      must: q ? [{
        multi_match: {
          query: q,
          fields: ['title^3', 'description', 'cast^2', 'director^2', 'tags'],
          fuzziness: 'AUTO'
        }
      }] : [{ match_all: {} }],
      filter: [
        ...(genre ? [{ term: { genres: genre } }] : []),
        ...(year ? [{ term: { year: parseInt(year) } }] : []),
        ...(rating ? [{ range: { rating: { gte: parseFloat(rating) } } }] : [])
      ]
    }
  };
  
  const results = await elasticsearch.search({
    index: 'content',
    query,
    sort: q ? [{ _score: 'desc' }] : [{ rating: 'desc' }],
    from: (page - 1) * limit,
    size: limit
  });
  
  res.json({
    results: results.hits.hits.map(h => h._source),
    total: results.hits.total.value,
    page, limit
  });
});
```

---

## 🗄️ Database Choices

```
PostgreSQL (RDS):
  - users, subscriptions, billing, profiles
  - Content metadata (titles, descriptions, rights)
  - Watch history (user_id + content_id + position)
  
Cassandra:
  - Stream events (10M events/sec!)
  - Pre-computed recommendations (high read throughput)
  - User activity feeds
  
Redis (ElastiCache):
  - Session data, JWT tokens
  - Continue watching positions (fast writes/reads)
  - Recommendation cache (1 hour TTL)
  - Trending content (5 min TTL)
  
Elasticsearch:
  - Content search with full-text, filters, facets
  
S3:
  - Raw video files
  - Processed HLS segments
  - Thumbnails
  - Subtitles (SRT/VTT files)
  
Kafka:
  - Stream events (plays, pauses, seeks, quality changes)
  - Input to ML recommendation pipelines
```

---

## 🎯 Interview Discussion Points

### Key Design Decisions

1. **CDN Strategy (Most Important):**
   Netflix built their OWN CDN called Open Connect. They place servers inside ISPs to cache popular content locally. When you watch Stranger Things, video comes from a server 10ms away, not from AWS!
   
   For your design: Use AWS CloudFront with S3. CloudFront has 400+ edge locations globally.

2. **Adaptive Bitrate Streaming (HLS):**
   Video divided into 6-second segments. Multiple quality versions. Client's HLS player monitors network and switches quality automatically. Buffer 30 seconds ahead. Smooth streaming even on variable connections.

3. **Video Processing Pipeline:**
   Raw upload → Transcoding (parallel for all resolutions) → CDN distribution. Use AWS MediaConvert or Elastic Transcoder. Step Functions for pipeline orchestration.

4. **Recommendation System:**
   ML models (collaborative + content-based filtering) run offline (hourly). Results stored in Cassandra. Served from Redis cache. Netflix invests $1B+ in recommendations — it drives 80% of what's watched.

5. **Database for Events:**
   Cassandra (not PostgreSQL) for stream events. Write-optimized. 10M events/sec is unreachable with relational DB.

---

### Navigation
**Prev:** [04_Design_Uber.md](04_Design_Uber.md) | **Index:** [00_Index.md](00_Index.md) | **Next:** [06_Design_Twitter.md](06_Design_Twitter.md)
