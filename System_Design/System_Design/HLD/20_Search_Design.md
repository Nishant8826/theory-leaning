# 📌 Search Design

## 🧠 Concept Explanation (Story Format)

You type "node js redis tutorial" in YouTube search. In 200ms, you get thousands of relevant results, ranked by relevance, with typo tolerance and personalization.

How? Not with `SELECT * FROM videos WHERE title LIKE '%node%'`! That would scan billions of rows and take minutes.

YouTube uses specialized search infrastructure. We use **Elasticsearch** — a distributed search engine designed specifically for fast full-text search.

Think of Elasticsearch as a "search index" — like a book's index at the back. Instead of reading every page to find "Redis", the index tells you: "Redis is on pages 45, 200, 670". Elasticsearch builds this index for all your data.

---

## 🏗️ Basic Design (Naive)

```javascript
// ❌ SQL LIKE query for search — terrible at scale
app.get('/search', async (req, res) => {
  const { q } = req.query;
  
  // This will do a FULL TABLE SCAN on millions of rows!
  const results = await db.query(
    'SELECT * FROM posts WHERE content LIKE $1 OR title LIKE $2',
    [`%${q}%`, `%${q}%`]
  );
  
  res.json(results.rows);
});

// Problems:
// - No fuzzy matching: "reids" won't find "redis"
// - No ranking: All results treated equally
// - Very slow: 5+ seconds for millions of rows
// - No stemming: "running" won't find "run"
// - No language awareness
```

---

## ⚡ Optimized Design

```
User types search query
         ↓
React App (debounced input)
         ↓
Node.js API
         ↓
[Elasticsearch] ← Specialized search engine
  - Instant full-text search
  - Fuzzy matching (typos)
  - Relevance ranking (TF-IDF + BM25)
  - Filters and aggregations
  - Autocomplete suggestions
  - Personalization via boosting
         ↓
Returns ranked results in <100ms

Sync process (separate from search):
[Node.js API] → writes to [PostgreSQL/MongoDB]
                       ↓ (async via queue/event)
             [Elasticsearch Indexer]  ← keeps search index updated
```

---

## 🔍 Key Components

### Elasticsearch Basics

```javascript
const { Client } = require('@elastic/elasticsearch');
const client = new Client({ node: process.env.ELASTICSEARCH_URL });

// 1. CREATE INDEX (define schema/mapping)
await client.indices.create({
  index: 'posts',
  mappings: {
    properties: {
      title: { type: 'text', analyzer: 'english' },     // Full-text, English stemming
      content: { type: 'text', analyzer: 'english' },
      userId: { type: 'keyword' },  // Exact match only
      tags: { type: 'keyword' },    // Exact match, for filtering
      likesCount: { type: 'integer' },
      createdAt: { type: 'date' },
      location: { type: 'geo_point' }  // For location-based search
    }
  }
});

// 2. INDEX A DOCUMENT (add/update data)
await client.index({
  index: 'posts',
  id: post.id,
  document: {
    title: post.title,
    content: post.content,
    userId: post.userId,
    tags: post.tags,
    likesCount: post.likes,
    createdAt: post.createdAt
  }
});

// 3. SEARCH
const results = await client.search({
  index: 'posts',
  query: {
    bool: {
      must: [
        {
          multi_match: {
            query: 'node redis caching tutorial',
            fields: ['title^3', 'content^1', 'tags^2'],  // Title matches are 3x more important
            fuzziness: 'AUTO',  // Handle typos: "reids" → "redis"
            operator: 'or'      // Match any word (not all)
          }
        }
      ],
      filter: [
        { range: { likesCount: { gte: 10 } } },  // Only popular posts
        { range: { createdAt: { gte: 'now-1y' } } }  // Last year only
      ],
      should: [
        { term: { userId: currentUser.id } }  // Boost user's own content
      ]
    }
  },
  sort: [
    { _score: { order: 'desc' } },  // Relevance first
    { createdAt: { order: 'desc' } }  // Then newest
  ],
  from: 0, size: 20  // Pagination
});

const hits = results.hits.hits.map(hit => ({
  ...hit._source,
  score: hit._score
}));
```

### Autocomplete / Suggestions

```javascript
// Create an index with completion suggester for autocomplete
await client.indices.create({
  index: 'autocomplete',
  mappings: {
    properties: {
      suggest: {
        type: 'completion',
        analyzer: 'simple'
      }
    }
  }
});

// Index terms for autocomplete
await client.index({
  index: 'autocomplete',
  document: {
    suggest: {
      input: ['Node.js', 'Node', 'Nodejs'],  // All ways user might type it
      weight: 100  // Higher weight = higher in suggestions
    }
  }
});

// Get suggestions
const suggestions = await client.search({
  index: 'autocomplete',
  suggest: {
    post_suggest: {
      prefix: req.query.q,  // What user has typed so far
      completion: {
        field: 'suggest',
        size: 10,  // Return top 10 suggestions
        fuzzy: { fuzziness: 1 }  // Allow 1 typo
      }
    }
  }
});

const options = suggestions.suggest.post_suggest[0].options
  .map(option => option.text);
```

### Keeping Search Index in Sync

```javascript
// Strategy: Use events to update Elasticsearch when data changes

// Option 1: Dual write in service (simple but tight coupling)
class PostService {
  async createPost(data) {
    const post = await db.collection('posts').insertOne(data);
    
    // Also index in Elasticsearch
    await elasticsearch.index({ index: 'posts', id: post.id, document: data });
    
    return post;
  }
  
  async updatePost(postId, updates) {
    await db.collection('posts').updateOne({ _id: postId }, { $set: updates });
    await elasticsearch.update({ index: 'posts', id: postId, doc: updates });
  }
  
  async deletePost(postId) {
    await db.collection('posts').deleteOne({ _id: postId });
    await elasticsearch.delete({ index: 'posts', id: postId });
  }
}

// Option 2: Event-driven sync (better — Elasticsearch out of critical path)
// Create post → DB → emit 'post.created' event → Queue → Elasticsearch Indexer worker

// Option 3: MongoDB Change Streams (elegant)
const changeStream = db.collection('posts').watch();

changeStream.on('change', async (change) => {
  if (change.operationType === 'insert') {
    await elasticsearch.index({ index: 'posts', id: change.documentKey._id.toString(), document: change.fullDocument });
  }
  if (change.operationType === 'update') {
    await elasticsearch.update({ index: 'posts', id: change.documentKey._id.toString(), doc: change.updateDescription.updatedFields });
  }
  if (change.operationType === 'delete') {
    await elasticsearch.delete({ index: 'posts', id: change.documentKey._id.toString() });
  }
});
```

---

## ⚖️ Trade-offs

| Elasticsearch | PostgreSQL Full-Text | MongoDB Full-Text |
|--------------|---------------------|------------------|
| Very fast search | Decent for simple cases | Basic search |
| Rich query language | SQL familiar | Limited |
| Fuzzy matching | No | No |
| Distributed | Single node (complex distributed) | Yes |
| Eventually consistent | ACID | ACID |
| Extra infrastructure | No extra | No extra |
| Complex to maintain | Simple | Simple |

**Rule:** Use PostgreSQL FTS for simple search (<10M records). Use Elasticsearch for complex search at scale.

---

## 📊 Scalability Discussion

### Elasticsearch Architecture

```
Elasticsearch Cluster:

[Node 1 - Master + Data]  [Node 2 - Data]  [Node 3 - Data]
         ↑                       ↑                  ↑
         └──────────── Shard 0 ──┘
                       Shard 1 ─────────────────────┘
                       Shard 2 ─────────────────────┘

Index "posts" split into 3 shards:
- Shard 0: Posts A-F
- Shard 1: Posts G-M  
- Shard 2: Posts N-Z

Search queries run in parallel on all shards → fast!
Add more nodes → add more shards → scales horizontally
```

### Search API Route Design

```javascript
// Complete search endpoint with all features

app.get('/api/search', authenticate, async (req, res) => {
  const { 
    q,           // Search query
    type,        // 'posts', 'users', 'tags'
    page = 1,
    limit = 20,
    sort = 'relevance', // 'relevance', 'recent', 'popular'
    from_date,
    to_date,
    location     // For location-based search
  } = req.query;
  
  const from = (page - 1) * limit;
  
  // Build Elasticsearch query
  const query = {
    bool: {
      must: q ? [{ multi_match: { query: q, fields: ['title^3', 'content', 'tags^2'], fuzziness: 'AUTO' } }] : [{ match_all: {} }],
      filter: []
    }
  };
  
  if (from_date || to_date) {
    query.bool.filter.push({ range: { createdAt: { gte: from_date, lte: to_date } } });
  }
  
  const sortOption = {
    relevance: [{ _score: 'desc' }],
    recent: [{ createdAt: 'desc' }],
    popular: [{ likesCount: 'desc' }]
  }[sort];
  
  const results = await elasticsearch.search({
    index: type || 'posts',
    query,
    sort: sortOption,
    from, size: parseInt(limit),
    highlight: {
      fields: { title: {}, content: { fragment_size: 150, number_of_fragments: 1 } }
    }
  });
  
  // Track search for analytics + personalization
  await redis.lpush(`user:${req.user.id}:recent_searches`, q);
  await redis.ltrim(`user:${req.user.id}:recent_searches`, 0, 9); // Keep last 10
  
  res.json({
    total: results.hits.total.value,
    results: results.hits.hits.map(h => ({ ...h._source, highlight: h.highlight })),
    page, limit
  });
});
```

---

## 💼 Interview Questions (WITH SOLUTIONS)

### Q1: Why can't we use SQL LIKE queries for search at scale?

**Solution:**
SQL `LIKE '%query%'` has fundamental limitations:
1. **No index usage:** `LIKE '%redis%'` (wildcard at start) → full table scan on every query
2. **No relevance ranking:** All matching rows treated equally
3. **No fuzzy matching:** "reids" won't find "redis" — exact substring only
4. **No stemming:** "running" won't find "run" or "runs"
5. **Slow:** 1 second for 1M rows → unusable for user-facing search

For up to ~10M records with simple needs → **PostgreSQL Full-Text Search** (GIN index + `tsvector`) is acceptable.
For complex search, large scale, or great UX → **Elasticsearch**.

---

### Q2: How does Elasticsearch make search so fast?

**Solution:**
Elasticsearch uses an **inverted index** — the core data structure of all search engines.

```
Documents:
Doc 1: "Redis is a fast cache"
Doc 2: "Cache makes systems fast"
Doc 3: "Redis improves performance"

Inverted Index:
"redis"       → [Doc 1, Doc 3]
"is"          → [Doc 1]
"a"           → [Doc 1]
"fast"        → [Doc 1, Doc 2]
"cache"       → [Doc 1, Doc 2]
"makes"       → [Doc 2]
"systems"     → [Doc 2]
"improves"    → [Doc 3]
"performance" → [Doc 3]
```

Query "redis fast":
- Look up "redis" → [Doc 1, Doc 3]
- Look up "fast" → [Doc 1, Doc 2]
- Intersection/union based on operator
- Doc 1 appears in both → highest relevance!

This lookup is O(1) per term — no table scan!

---

### Q3: What is TF-IDF and how does Elasticsearch use it for ranking?

**Solution:**
**TF-IDF** determines how relevant a document is to a query:

**TF (Term Frequency):** How often the search term appears in the document.
- Document with "Redis" 10 times is more relevant than one with "Redis" once.

**IDF (Inverse Document Frequency):** How rare the term is across all documents.
- "Redis" appears in 1,000 documents → more specific, higher IDF
- "the" appears in 1,000,000 documents → very common, lower IDF
- Common words like "the", "is" have low IDF → less impact on ranking

**Score = TF × IDF**

Elasticsearch uses BM25 (an improved version of TF-IDF) by default.

Additionally, you can boost specific fields:
```javascript
// Title match is 3x more important than content match
fields: ['title^3', 'content^1']
```

---

### Q4: How do you implement search-as-you-type (autocomplete)?

**Solution:**
Two approaches:

**1. Prefix search (simplest):**
```javascript
// As user types "no" → search for posts starting with "no"
const results = await client.search({
  index: 'posts',
  query: {
    prefix: { title: req.query.q }  // Prefix match
  }
});
```

**2. Completion Suggester (best for autocomplete):**
- Special data structure optimized for prefix lookups
- Returns suggestions in <10ms
- Pre-built for this use case

```javascript
// Index with completion field
const results = await client.search({
  index: 'search-suggestions',
  suggest: {
    title_suggest: {
      prefix: req.query.q,
      completion: { field: 'suggest', size: 10, fuzzy: { fuzziness: 1 } }
    }
  }
});
```

**3. Ngram tokenizer:**
- Pre-indexes substrings: "redis" → ["r", "re", "red", "redi", "redis"]
- Every prefix is instantly searchable
- Higher index size but fastest lookup

---

### Q5: How do you keep Elasticsearch in sync with your primary database?

**Solution:**
**Recommended: Event-driven sync**

```javascript
// 1. Application publishes events to queue (SQS/Bull)
async function createPost(data) {
  const post = await mongoDB.collection('posts').insertOne(data);
  
  // Publish event (don't wait — keeps API fast!)
  await searchIndexQueue.add('index_post', { postId: post.id, action: 'create' });
  
  return post;
}

// 2. Elasticsearch Indexer Worker (separate process)
searchIndexQueue.process('index_post', async (job) => {
  const { postId, action } = job.data;
  
  if (action === 'create' || action === 'update') {
    const post = await mongoDB.collection('posts').findOne({ _id: postId });
    await elasticsearch.index({ index: 'posts', id: postId, document: post });
  }
  
  if (action === 'delete') {
    await elasticsearch.delete({ index: 'posts', id: postId });
  }
});

// 3. For bulk initial indexing (when setting up Elasticsearch):
async function bulkIndexAllPosts() {
  const batchSize = 1000;
  let skip = 0;
  
  while (true) {
    const posts = await mongoDB.collection('posts').find().skip(skip).limit(batchSize).toArray();
    if (posts.length === 0) break;
    
    const operations = posts.flatMap(post => [
      { index: { _index: 'posts', _id: post._id.toString() } },
      post
    ]);
    
    await elasticsearch.bulk({ operations });
    skip += batchSize;
    console.log(`Indexed ${skip} posts...`);
  }
}
```

---

## 🧩 Practice Problems (WITH SOLUTIONS)

### Problem 1: Design search for a Twitter-like app (tweets, users, hashtags)

**Solution:**
```javascript
// Three search indexes:

// 1. Tweets index
await elasticsearch.indices.create({
  index: 'tweets',
  mappings: {
    properties: {
      content: { type: 'text', analyzer: 'english' },
      userId: { type: 'keyword' },
      username: { type: 'keyword' },
      hashtags: { type: 'keyword' },    // For exact hashtag filtering
      mentions: { type: 'keyword' },
      likesCount: { type: 'integer' },
      isRetweet: { type: 'boolean' },
      createdAt: { type: 'date' },
      // Suggest for autocomplete
      suggest: { type: 'completion' }
    }
  }
});

// 2. Users index
await elasticsearch.indices.create({
  index: 'users',
  mappings: {
    properties: {
      username: { type: 'keyword' },
      name: { type: 'text', analyzer: 'standard' },
      bio: { type: 'text', analyzer: 'english' },
      followersCount: { type: 'integer' },
      isVerified: { type: 'boolean' }
    }
  }
});

// Search endpoint
app.get('/api/search', async (req, res) => {
  const { q, type = 'all' } = req.query;
  
  const searches = [];
  
  if (type === 'all' || type === 'tweets') {
    searches.push(client.search({
      index: 'tweets',
      query: {
        bool: {
          should: [
            { match: { content: { query: q, boost: 1 } } },
            { term: { hashtags: { value: q.replace('#', '').toLowerCase(), boost: 3 } } }
          ]
        }
      },
      size: 20
    }));
  }
  
  if (type === 'all' || type === 'users') {
    searches.push(client.search({
      index: 'users',
      query: {
        bool: {
          should: [
            { match: { name: { query: q, boost: 2 } } },
            { prefix: { username: { value: q.toLowerCase(), boost: 3 } } }
          ],
          should: [{ term: { isVerified: true } }]  // Boost verified accounts
        }
      },
      sort: [{ _score: 'desc' }, { followersCount: 'desc' }],
      size: 10
    }));
  }
  
  const results = await Promise.all(searches);
  res.json({ tweets: results[0]?.hits.hits, users: results[1]?.hits.hits });
});
```

---

### Problem 2: Search is slow during peak hours. How do you scale Elasticsearch?

**Solution:**
```
Diagnosis:
1. Check ES cluster health: GET /_cluster/health
   - red: some shards not allocated (critical!)
   - yellow: replicas not assigned (check immediately)
   - green: all good

2. Check hot threads: GET /_nodes/hot_threads
   - Find which queries are slowest

3. Check index stats: GET /posts/_stats
   - Look for large segment count (merge needed?)

Scaling solutions:

1. Horizontal scaling: Add more ES nodes
   - More nodes = more shards = parallel search
   - Start with 3 nodes, scale to 10+ at peak

2. Increase replicas during peak:
   PUT /posts/_settings
   { "index": { "number_of_replicas": 3 } }
   - More replicas = more copies to serve read traffic
   - Query any replica (ES load balances automatically)

3. Cache frequent searches in Redis:
   const cacheKey = `search:${JSON.stringify(query)}`;
   const cached = await redis.get(cacheKey);
   if (cached) return JSON.parse(cached);
   // ... do ES search ...
   await redis.setex(cacheKey, 60, JSON.stringify(results)); // Cache 1 minute

4. Optimize mapping:
   - Set doc_values: false for fields you never sort/aggregate
   - Set store: false for large text fields you don't need to retrieve
   - Use keyword instead of text for exact-match-only fields

5. AWS OpenSearch Service:
   - Managed Elasticsearch (no ops overhead)
   - Auto-scaling with Ultra Warm nodes for cost efficiency
```

---

### Navigation
**Prev:** [19_Content_Delivery_Network.md](19_Content_Delivery_Network.md) | **Index:** [00_Index.md](../00_Index.md) | **Next:** [21_Logging_and_Monitoring.md](21_Logging_and_Monitoring.md)
