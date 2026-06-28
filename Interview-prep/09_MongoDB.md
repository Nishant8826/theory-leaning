# 🚀 Interview Preparation - MongoDB

> **Domain:** NoSQL Databases / Backend Development  
> **Level:** Beginner to Expert  
> **Target Role:** Software Engineer / Senior Engineer / Database Engineer

---

## 🟢 Beginner Level

### ❓ Q1. **What is MongoDB and how does it compare to relational databases?**

<details>
<summary><b>👀 Show Answer</b></summary>

* **MongoDB:**
  - A document-oriented NoSQL database.
  - Stores data as flexible, schema-less BSON (Binary JSON) documents.
  - Relations are handled via nested sub-documents (embedding) or reference IDs.
  - Built-in support for scaling out (sharding) and high availability (replica sets).
* **Comparison with Relational Databases:**

| Relational (SQL) | MongoDB (NoSQL) |
| :--- | :--- |
| Database | Database |
| Table | Collection |
| Row | Document |
| Column | Field |
| Join | Reference / `$lookup` |

> 💡 **Interviewer Focus:** Ensure the candidate highlights the flexibility of document models vs the rigid schemas of relational databases, and explains when to choose one over the other.

</details>

<hr/>

### ❓ Q2. **What is BSON and how does it differ from JSON?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **JSON (JavaScript Object Notation):**
  - A lightweight, text-based data interchange format.
  - Supports basic types: string, number, boolean, null, object, and array.
- **BSON (Binary JSON):**
  - A binary-serialized representation of JSON documents.
  - Faster to parse and scan because it encodes length prefixes for elements.
  - Supports additional data types not present in standard JSON, such as `Date`, `ObjectId`, `Decimal128` (high precision numbers), `Binary data` (images/files), and `Double`.

> 💡 **Interviewer Focus:** Knowing that BSON enables faster indexing and search traversals, and provides database-specific datatypes.

</details>

<hr/>

### ❓ Q3. **How do you insert documents in MongoDB?**

<details>
<summary><b>👀 Show Answer</b></summary>

MongoDB provides write operations to insert documents into collections:
- **`insertOne(document)`**: Inserts a single document.
- **`insertMany([documents])`**: Inserts an array of documents.

```javascript
// Inserting a single user
db.users.insertOne({
  name: "Nishant",
  email: "nishant@example.com",
  createdAt: new Date()
});
```

> 💡 **Interviewer Focus:** Mention that if the `_id` field is omitted from the document, MongoDB automatically generates a unique `ObjectId` for it before writing it to disk.

</details>

<hr/>

### ❓ Q4. **What is the `_id` field and how is it generated?**

<details>
<summary><b>👀 Show Answer</b></summary>

In MongoDB, every document requires a unique `_id` field that acts as its primary key. If not provided, MongoDB automatically generates an **`ObjectId`** (a 12-byte identifier):
- **4 bytes:** Unix timestamp representing the document's creation time.
- **5 bytes:** Random value unique to the machine and process.
- **3 bytes:** Incrementing counter, starting with a random value.

> 💡 **Interviewer Focus:** Since the first 4 bytes encode a timestamp, you can extract the creation time of a document directly from its `ObjectId` without storing a separate `createdAt` field.

</details>

<hr/>

### ❓ Q5. **How do you perform basic query filtering in MongoDB?**

<details>
<summary><b>👀 Show Answer</b></summary>

Querying is performed using JSON-like filter documents passed to the `find()` method:
- **Equality:** `{ status: "ACTIVE" }`
- **Operators:**
  - `$gt` (greater than), `$lt` (less than), `$gte`, `$lte`.
  - `$in` (matches any value in an array), `$nin`.
  - `$or`, `$and` (logical operators).

```javascript
// Find active users older than 25
db.users.find({
  status: "ACTIVE",
  age: { $gt: 25 }
});
```

> 💡 **Interviewer Focus:** Familiarity with standard query operator prefixes and nested object filtering syntax.

</details>

<hr/>

### ❓ Q6. **What is the difference between `find()` and `findOne()`?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **`find(filter)`:** 
  - Returns a **cursor** (a pointer to the result set).
  - Does not load all documents into memory instantly; you iterate through the cursor (e.g., using `.toArray()`, `.next()`, or `.forEach()`).
- **`findOne(filter)`:**
  - Returns the **actual document object** itself (the first one matching the query filter).
  - Returns `null` if no match is found.

> 💡 **Interviewer Focus:** Understanding that cursors optimize memory by lazy loading query results.

</details>

<hr/>

### ❓ Q7. **How do you update documents in MongoDB?**

<details>
<summary><b>👀 Show Answer</b></summary>

Updates are performed using `updateOne(filter, update, options)` or `updateMany(filter, update, options)`. You must use atomic update operators:
- **`$set`**: Sets the value of a field.
- **`$unset`**: Deletes a field from the document.
- **`$inc`**: Increments a numeric field by a specified value.
- **`$push`**: Appends an item to an array field.

```javascript
// Increment user's score by 10
db.users.updateOne(
  { _id: ObjectId("60c72b2f9b1d8b2bad000001") },
  { $inc: { score: 10 } }
);
```

> 💡 **Interviewer Focus:** Emphasize that omitting update operators (like `$set`) when modifying documents in older MongoDB versions would overwrite the *entire* document with the new object.

</details>

<hr/>

### ❓ Q8. **How do you delete documents in MongoDB?**

<details>
<summary><b>👀 Show Answer</b></summary>

Documents are deleted using:
- **`deleteOne(filter)`**: Deletes the first document matching the filter.
- **`deleteMany(filter)`**: Deletes all documents matching the filter.

> 💡 **Interviewer Focus:** Explain that deletes are permanent and should be executed with caution; many systems use soft-deletes (`deleted: true`) instead.

</details>

<hr/>

### ❓ Q9. **What is the purpose of the `$lookup` aggregation stage?**

<details>
<summary><b>👀 Show Answer</b></summary>

The `$lookup` stage performs a left outer join to another collection in the same database, pulling matching documents into an array field.

```javascript
db.orders.aggregate([
  {
    $lookup: {
      from: "users",             // Target collection
      localField: "userId",      // Field in orders
      foreignField: "_id",       // Field in users
      as: "customerDetails"      // Array output field
    }
  }
]);
```

> 💡 **Interviewer Focus:** Point out that `$lookup` is resource-intensive because MongoDB is not designed for relational joins. Encourage embedding data if joins are required frequently.

</details>

<hr/>

### ❓ Q10. **Explain embedded documents vs references in MongoDB.**

<details>
<summary><b>👀 Show Answer</b></summary>

- **Embedded Documents (Denormalization):**
  - Storing related data directly inside a single document as a nested object or array.
  - Pros: High read performance (fetched in a single query/I/O operation).
  - Cons: Redundant data, document size limits (max 16MB).
- **References (Normalization):**
  - Storing a pointer (usually the target document's `_id`) to link records across collections.
  - Pros: Prevents data redundancy, works well for unbounded 1-to-many relationships.
  - Cons: Requires multiple queries or `$lookup` joins, reducing read speeds.

> 💡 **Interviewer Focus:** The 16MB document size limit as a primary driver for choosing references over embedding.

</details>

<hr/>

### ❓ Q11. **What is MongoDB Compass?**

<details>
<summary><b>👀 Show Answer</b></summary>

MongoDB Compass is the official Graphical User Interface (GUI) for MongoDB. It allows users to visually analyze schemas, build queries and aggregation pipelines, inspect query execution plans (explain), construct indexes, and inspect collection statistics without executing shell terminal scripts.

> 💡 **Interviewer Focus:** Practical utility for querying databases visually and using visual pipeline builders.

</details>

<hr/>

### ❓ Q12. **What does the upsert option do in an update statement?**

<details>
<summary><b>👀 Show Answer</b></summary>

The `upsert` option (boolean) tells MongoDB:
- If a document matches the query filter, update it.
- If no document matches the filter, insert a new document combining the query filter fields and the update modifications.

```javascript
db.users.updateOne(
  { email: "new@example.com" },
  { $set: { name: "New User" } },
  { upsert: true } // Inserts if email not found
);
```

> 💡 **Interviewer Focus:** Saving query roundtrips by consolidating checking and inserting logic into a single database operation.

</details>

<hr/>

### ❓ Q13. **How do you perform text searches in MongoDB?**

<details>
<summary><b>👀 Show Answer</b></summary>

To perform text searches:
1. Create a `text` index on the target string fields.
2. Query using the `$text` operator with the `$search` parameter.

```javascript
// Step 1: Create index
db.articles.createIndex({ content: "text" });

// Step 2: Query
db.articles.find({ $text: { $search: "database scaling" } });
```

> 💡 **Interviewer Focus:** Limit of one text index per collection, and sorting results by match quality using the `$meta: "textScore"` metadata projection.

</details>

<hr/>

### ❓ Q14. **What is a cursor in MongoDB and how do you configure its limit and skip?**

<details>
<summary><b>👀 Show Answer</b></summary>

A cursor is a pointer to the result set of a query. Applications fetch results page-by-page by appending:
- **`limit(N)`**: Sets the maximum number of documents returned.
- **`skip(N)`**: Skips the first N matching documents.

```javascript
// Pagination: page 3 with 10 documents per page
db.products.find().skip(20).limit(10);
```

> 💡 **Interviewer Focus:** Note that `skip(N)` has linear $O(N)$ scanning performance overhead on large collections; suggest keyset pagination (using criteria filters like `_id > lastId`) for large datasets.

</details>

<hr/>

### ❓ Q15. **What is the default port number of MongoDB?**

<details>
<summary><b>👀 Show Answer</b></summary>

The default port number for `mongod` and `mongos` processes is **`27017`**.

> 💡 **Interviewer Focus:** Basic security: changing default ports and blocking public access.

</details>

<hr/>

### ❓ Q16. **What is the difference between countDocuments() and estimatedDocumentCount()?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **`estimatedDocumentCount()`**: Retrieves the total count of documents in a collection directly from the metadata (statistics). It does not scan data or evaluate filters, making it $O(1)$ fast, but it can be slightly inaccurate if the collection had unclean shut downs.
- **`countDocuments(filter)`**: Executes an actual aggregation scan of the collection, counting records that match the query filter. It is $O(N)$ slower but guarantees absolute accuracy.

> 💡 **Interviewer Focus:** Performance differences. Use `estimatedDocumentCount()` for fast, generic total count indicators on metadata dashboards.

</details>

<hr/>

### ❓ Q17. **What is the difference between $set and $push?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **`$set`**: Updates the value of a specific scalar field, or adds the field to the document if it does not exist.
- **`$push`**: Appends a value to an array field. If the field is missing, it creates the array and appends the value.

> 💡 **Interviewer Focus:** Correct application of array manipulation operators vs value override operators.

</details>

<hr/>

### ❓ Q18. **What does the projection argument do in find()?**

<details>
<summary><b>👀 Show Answer</b></summary>

Projection limits the fields returned from documents to reduce network bandwidth.
- `1` (or `true`): Include the field in output.
- `0` (or `false`): Exclude the field.

```javascript
// Return only name and email (exclude other fields, _id is included by default unless set to 0)
db.users.find({ status: "ACTIVE" }, { name: 1, email: 1, _id: 0 });
```

> 💡 **Interviewer Focus:** Network payload optimization by querying only what is required.

</details>

<hr/>

### ❓ Q19. **What is a collection in MongoDB?**

<details>
<summary><b>👀 Show Answer</b></summary>

A collection is a grouping of MongoDB BSON documents. It is the NoSQL equivalent of a relational database table. Collections do not enforce structure by default, meaning documents inside a single collection can have different fields.

> 💡 **Interviewer Focus:** Basic layout terminology.

</details>

<hr/>

### ❓ Q20. **Can a document contain different fields from another document in the same collection?**

<details>
<summary><b>👀 Show Answer</b></summary>

Yes. MongoDB is natively **schema-less** (or has dynamic schema). This allows documents to store custom fields depending on context, making it ideal for polymorphic data shapes.

> 💡 **Interviewer Focus:** Dynamic data structures support.

</details>

<hr/>

### ❓ Q21. **What is the maximum size limit for a single BSON document?**

<details>
<summary><b>👀 Show Answer</b></summary>

The maximum size limit for a single BSON document in MongoDB is **`16MB`**. This prevents extreme memory usage and keeps data packets manageable.

> 💡 **Interviewer Focus:** Schema designs: using references when array nesting risks exceeding this limit.

</details>

<hr/>

### ❓ Q22. **What is the role of the mongod process?**

<details>
<summary><b>👀 Show Answer</b></summary>

`mongod` is the primary daemon process for the MongoDB system. It handles data access requests, manages write logs and data files, and runs background maintenance tasks.

> 💡 **Interviewer Focus:** Database engine hosting.

</details>

<hr/>

### ❓ Q23. **What is the role of the mongos process?**

<details>
<summary><b>👀 Show Answer</b></summary>

`mongos` is the routing service for MongoDB sharded clusters. It acts as an entry point for applications, directing queries to the correct physical shard holding the requested data by consulting config servers.

> 💡 **Interviewer Focus:** Sharded architecture layout.

</details>

<hr/>

### ❓ Q24. **How do you sort query results in ascending or descending order?**

<details>
<summary><b>👀 Show Answer</b></summary>

Append `.sort()` to the query cursor passing column priorities:
- `1`: Ascending order.
- `-1`: Descending order.

```javascript
db.products.find().sort({ price: 1, createdAt: -1 });
```

> 💡 **Interviewer Focus:** Index matching rules for sorting.

</details>

<hr/>

### ❓ Q25. **What is the difference between $or and $in operators?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **`$in`**: Compares a single field against a list of possible values (shorthand for single-field OR).
- **`$or`**: Evaluates multiple logical conditions across *different* fields.

```sql
-- Single field: Use $in
db.users.find({ country: { $in: ["US", "IN"] } });

-- Multi-field: Use $or
db.users.find({ $or: [{ status: "ACTIVE" }, { age: { $gt: 50 } }] });
```

> 💡 **Interviewer Focus:** Selecting optimal query operators for clean schema parsing.

</details>

<hr/>

## 🟡 Intermediate Level

### ❓ Q26. **Explain the MongoDB Aggregation Framework and its common stages.**

<details>
<summary><b>👀 Show Answer</b></summary>

The Aggregation Framework is a data processing pipeline where documents enter a multi-stage pipeline that transforms them into aggregated results.
- **Common Stages:**
  - **`$match`**: Filters documents (similar to `WHERE` in SQL).
  - **`$group`**: Groups documents by a specified key and runs aggregates (similar to `GROUP BY` and `SUM/AVG`).
  - **`$project`**: Selects, renames, or creates new fields in output documents.
  - **`$sort`**: Sorts documents.
  - **`$limit`** & **`$skip`**: Paginated boundaries.
  - **`$unwind`**: Deconstructs an array field from input documents to output a document for each element.

```javascript
db.sales.aggregate([
  { $match: { status: "COMPLETED" } },
  { $group: { _id: "$category", totalSales: { $sum: "$amount" } } }
]);
```

> 💡 **Interviewer Focus:** Pipeline optimization: always place `$match` and `$sort` stages at the very beginning of the pipeline to take advantage of indexes.

</details>

<hr/>

### ❓ Q27. **What is the ESR (Equality, Sort, Range) rule for Compound Indexes?**

<details>
<summary><b>👀 Show Answer</b></summary>

When designing compound indexes in MongoDB to optimize queries containing filtering and sorting, you must order the columns in the index according to the **ESR rule**:
1. **E - Equality:** Place columns checked for exact equality matches first (e.g., `{ status: "ACTIVE" }`).
2. **S - Sort:** Place sorting columns next (e.g., `{ sort: { createdAt: -1 } }`). This allows the index to satisfy the sort without a CPU-heavy in-memory sort (blocking sort).
3. **R - Range:** Place columns checked for range conditions (e.g., `{ price: { $gt: 100 } }`) last. If a range column is placed before a sort column, the index cannot be used for sorting.

> 💡 **Interviewer Focus:** How placing range filters before sort columns forces MongoDB to perform an expensive in-memory sort.

</details>

<hr/>

### ❓ Q28. **What is a Multikey Index and how does it index arrays?**

<details>
<summary><b>👀 Show Answer</b></summary>

A **Multikey Index** is automatically created when you index a field that contains an array value.
- MongoDB creates index key entries for *every single element* in the array.
- This allows queries to efficiently search for documents containing specific array elements.
- **Restriction:** You cannot create a compound multikey index where *more than one* of the indexed fields is an array (to prevent Cartesian product growth of index entries).

> 💡 **Interviewer Focus:** The index size overhead of multikey indexes, as each array item generates a separate entry in the index tree.

</details>

<hr/>

### ❓ Q29. **What is a TTL (Time-To-Live) Index and how does it work?**

<details>
<summary><b>👀 Show Answer</b></summary>

A TTL index is a single-field index that automatically deletes documents from a collection after a certain amount of time.
- Created on a date field using the `expireAfterSeconds` option.
- A background thread reads this index and deletes expired documents once every 60 seconds.
- **Use cases:** User sessions, verification codes, event logs, and temporary caches.

```javascript
// Automatically delete session logs after 1 hour (3600 seconds)
db.sessions.createIndex(
  { createdAt: 1 },
  { expireAfterSeconds: 3600 }
);
```

> 💡 **Interviewer Focus:** Note that TTL deletes are background tasks and do not guarantee instant deletion exactly at the second of expiration under high write loads.

</details>

<hr/>

### ❓ Q30. **What is the difference between a Partial Index and a Sparse Index?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **Sparse Index:**
  - Only contains entries for documents that *actually contain the indexed field* (even if the field value is null).
  - Saves index storage space when fields are missing from most documents.
- **Partial Index:**
  - A more powerful, generic feature (introduced in MongoDB 3.2).
  - Uses a filter expression (`partialFilterExpression`) to index only documents that meet a specific criteria.
  - Can evaluate complex queries, not just the existence of a field.

```javascript
// Partial index: only index usernames for active users
db.users.createIndex(
  { username: 1 },
  { partialFilterExpression: { status: "ACTIVE" } }
);
```

> 💡 **Interviewer Focus:** Partial indexes are highly recommended over sparse indexes because they offer query filtering optimization.

</details>

<hr/>

### ❓ Q31. **How do you handle ACID transactions in MongoDB?**

<details>
<summary><b>👀 Show Answer</b></summary>

MongoDB introduced **Multi-Document ACID Transactions** in version 4.0 (extended to sharded clusters in 4.2).
- They use Logical Sessions (`client.startSession()`).
- Follow the standard database transactional model: `startTransaction()`, `commitTransaction()`, and `abortTransaction()`.
- **Note:** Transactions have write lock performance overhead. In document databases, you should model your schema (via nesting) so that atomic operations can be executed on a *single* document, reducing the need for multi-document transactions.

> 💡 **Interviewer Focus:** Emphasize that single-document writes in MongoDB are natively atomic, so transactions should only be used when modifying multiple separate collections.

</details>

<hr/>

### ❓ Q32. **What does the `$unwind` stage do in an aggregation pipeline?**

<details>
<summary><b>👀 Show Answer</b></summary>

The `$unwind` stage splits an array field within a document, outputting a separate copy of the document for each element in the array.

- **Example Input:** `{ _id: 1, item: "Shirt", sizes: ["S", "M"] }`
- **Output of `$unwind: "$sizes"`:**
  1. `{ _id: 1, item: "Shirt", sizes: "S" }`
  2. `{ _id: 1, item: "Shirt", sizes: "M" }`

> 💡 **Interviewer Focus:** Essential for performing grouping calculations on array data (e.g., getting total counts of nested items).

</details>

<hr/>

### ❓ Q33. **What is a Capped Collection and what are its features?**

<details>
<summary><b>👀 Show Answer</b></summary>

Capped collections are fixed-size collections that insert data in natural insertion order.
- Once the allocated maximum size/document limit is reached, they overwrite the oldest documents automatically (acting as a circular buffer).
- Updates that increase document size are not allowed.
- Cannot delete documents manually (you must drop the entire collection).
- **Use cases:** Real-time logging, transaction logs, and caching.

> 💡 **Interviewer Focus:** Mention that Capped Collections support Tailable Cursors, which are used by MongoDB internally to tail replication logs (oplog).

</details>

<hr/>

### ❓ Q34. **What is the difference between $merge and $out stages in aggregation?**

<details>
<summary><b>👀 Show Answer</b></summary>

Both output aggregation results to a target collection:
- **`$out`**: Creates a new collection or completely overwrites an existing collection. It performs an atomic replace operation, meaning the original collection is unavailable briefly.
- **`$merge`**: Merges pipeline output into an existing collection (inserts new documents, updates matched records, ignores unmatched). It supports upsert/merge logic without dropping the target collection.

> 💡 **Interviewer Focus:** Using `$merge` for incremental materializations in reporting systems.

</details>

<hr/>

### ❓ Q35. **Explain the differences between single-field indexes and compound indexes.**

<details>
<summary><b>👀 Show Answer</b></summary>

- **Single-Field Index:** Indexes a single field (e.g. `{ age: 1 }`). Optimizes queries filtering on that specific column.
- **Compound Index:** Indexes multiple fields in a defined sequence (e.g. `{ last_name: 1, first_name: 1 }`). It speeds up queries filtering on prefixes of the index key (following the Left-to-Right rule).

> 💡 **Interviewer Focus:** Minimizing index count overhead by utilizing prefix patterns of compound indexes.

</details>

<hr/>

### ❓ Q36. **What is a Text Index in MongoDB, and what are its limitations?**

<details>
<summary><b>👀 Show Answer</b></summary>

A text index indexes string fields for search capabilities.
- **Limitations:**
  - Only **one** text index is permitted per collection.
  - They consume significant storage space and slow down writes.
  - Do not support complex full-text searches (like fuzzy matching, auto-suggestions) well; use external search engines like ElasticSearch or MongoDB Atlas Search for advanced features.

> 💡 **Interviewer Focus:** Recognizing architecture boundaries of text indexing.

</details>

<hr/>

### ❓ Q37. **What is the difference between referencing and embedding when handling a 1-to-Many relationship?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **Embedding:** Store child array documents inside the parent document. Recommended if the child count is bounded (e.g., `< 100` items) and parent/children are read together.
- **Referencing:** Store the child `_id`s in the parent or parent `_id` in the children. Mandatory if the relationship is unbounded (e.g., users to logs) to prevent exceeding the 16MB document size limit.

> 💡 **Interviewer Focus:** Array growth rate analysis.

</details>

<hr/>

### ❓ Q38. **How does MongoDB support geolocation queries?**

<details>
<summary><b>👀 Show Answer</b></summary>

MongoDB supports coordinate indexing and querying:
1. Store location using GeoJSON formats: `{ type: "Point", coordinates: [ longitude, latitude ] }`.
2. Create a `2dsphere` index on the field.
3. Query using operators like `$near`, `$geoWithin`, or `$geoIntersects`.

```javascript
db.stores.find({
  location: {
    $near: {
      $geometry: { type: "Point", coordinates: [ 77.2, 28.6 ] },
      $maxDistance: 5000 // meters
    }
  }
});
```

> 💡 **Interviewer Focus:** Ordering of coordinates (longitude first, then latitude) in GeoJSON specifications.

</details>

<hr/>

### ❓ Q39. **What is DBRef in MongoDB and how does it compare to manual references?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **Manual Reference:** Storing a standard `_id` to link collections. The application must know which collection the reference links to.
- **DBRef:** A sub-document format containing the database name (`$db`), collection name (`$ref`), and reference ID (`$id`).
- **Comparison:** DBRef is bulkier. Manual references are preferred unless documents link to varying collections dynamically.

> 💡 **Interviewer Focus:** Selecting manual references over DBRefs by default for simpler schema formats.

</details>

<hr/>

### ❓ Q40. **What is index prefix matching?**

<details>
<summary><b>👀 Show Answer</b></summary>

Index prefixes are the initial subsets of a compound index. For an index `{ a: 1, b: 1, c: 1 }`, the prefixes are `{ a: 1 }` and `{ a: 1, b: 1 }`. MongoDB can use this single index to satisfy queries filtering on `{ a }` or `{ a, b }`, eliminating the need to build separate indexes for them.

> 💡 **Interviewer Focus:** Reducing indexing duplication.

</details>

<hr/>

### ❓ Q41. **How do you rename a field in a MongoDB collection?**

<details>
<summary><b>👀 Show Answer</b></summary>

Use the `$rename` update operator within `updateMany()`:

```javascript
db.users.updateMany({}, { $rename: { "nickname": "username" } });
```

> 💡 **Interviewer Focus:** Point out that `$rename` executes atomically but must write to all target documents, causing lock latency on large tables.

</details>

<hr/>

### ❓ Q42. **What does the $elemMatch operator do in queries?**

<details>
<summary><b>👀 Show Answer</b></summary>

`$elemMatch` matches documents where *at least one* element in an array meets **all** specified query conditions. Without `$elemMatch`, conditions can match across *different* array elements.

```javascript
// Matches if one single score element is both > 80 and < 90
db.students.find({ scores: { $elemMatch: { $gt: 80, $lt: 90 } } });
```

> 💡 **Interviewer Focus:** Array element query isolation.

</details>

<hr/>

### ❓ Q43. **What is the role of the system.profile collection?**

<details>
<summary><b>👀 Show Answer</b></summary>

The `system.profile` collection stores query profiling metrics when database profiling is active. It records slow queries, command options, execution times, and resource utilization.

> 💡 **Interviewer Focus:** Analyzing database query bottlenecks.

</details>

<hr/>

### ❓ Q44. **How do you configure database logging for slow queries?**

<details>
<summary><b>👀 Show Answer</b></summary>

Configure the system profiler:
- **`db.setProfilingLevel(level, options)`**:
  - Level `0`: Profiler off.
  - Level `1`: Log slow operations (default threshold `slowms` is 100ms).
  - Level `2`: Log all operations.

```javascript
// Log queries slower than 50ms
db.setProfilingLevel(1, { slowms: 50 });
```

> 💡 **Interviewer Focus:** Slow query thresholds customization.

</details>

<hr/>

### ❓ Q45. **What is the difference between standard indexes and hashed indexes?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **Standard Index (B-Tree):** Indexes values in sorted order. Supports equality, range queries (`$gt`, `$lt`), and sorting operations.
- **Hashed Index:** Indexes the MD5 hash of values. Supports only equality matches (`$eq`), but distributes keys uniformly across partitions. Essential for hashed sharding keys.

> 💡 **Interviewer Focus:** Hashed indexes do not support range scans.

</details>

<hr/>

### ❓ Q46. **How does the $facet stage work in MongoDB aggregation?**

<details>
<summary><b>👀 Show Answer</b></summary>

The `$facet` stage allows executing multiple parallel aggregation pipelines within a single stage on the same input documents.
- Useful for generating multi-faceted dashboards or search interfaces (e.g. counting products by category, price ranges, and status in a single query).

> 💡 **Interviewer Focus:** Parallel pipeline executions and memory bounds.

</details>

<hr/>

### ❓ Q47. **What is schema validation in MongoDB?**

<details>
<summary><b>👀 Show Answer</b></summary>

MongoDB supports enforcing structure on writes using JSON Schema validator rules defined on collections.

```javascript
db.createCollection("users", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["email", "age"],
      properties: {
        email: { bsonType: "string" },
        age: { bsonType: "int", minimum: 18 }
      }
    }
  }
});
```

> 💡 **Interviewer Focus:** Balancing dynamic schema capabilities with structural integrity requirements.

</details>

<hr/>

### ❓ Q48. **What are view collections in MongoDB?**

<details>
<summary><b>👀 Show Answer</b></summary>

View collections are read-only virtual collections defined by an aggregation pipeline on a source collection. They execute their pipeline dynamically when read and do not support insert/update writes.

> 💡 **Interviewer Focus:** Read abstractions and data access boundaries.

</details>

<hr/>

### ❓ Q49. **How do you perform case-insensitive index searches?**

<details>
<summary><b>👀 Show Answer</b></summary>

By defining a custom collation (e.g., strength `1` or `2`) when creating the index and matching that collation settings inside your query document.

```javascript
// Create index with case-insensitive collation
db.users.createIndex({ username: 1 }, { collation: { locale: "en", strength: 2 } });

// Query matching the same collation
db.users.find({ username: "john" }).collation({ locale: "en", strength: 2 });
```

> 💡 **Interviewer Focus:** Correct collation configuration matching to utilize indexes.

</details>

<hr/>

### ❓ Q50. **What is a covered query in MongoDB?**

<details>
<summary><b>👀 Show Answer</b></summary>

A covered query is a query where:
1. All filtered fields are part of an index.
2. All projected fields are also part of the same index (with `_id` explicitly excluded).
- The query execution plan reads values directly from the index tree without loading documents from disk pages (`totalDocsExamined = 0`).

> 💡 **Interviewer Focus:** Optimizing read latency by eliminating disk fetching steps.

</details>

<hr/>

## 🔴 Advanced Level

### ❓ Q51. **How does Replica Set election and high availability work in MongoDB?**

<details>
<summary><b>👀 Show Answer</b></summary>

A replica set is a cluster of `mongod` instances hosting the same data. It typically consists of 1 Primary node and multiple Secondary nodes.
- **Primary:** Receives all write operations and records them to the replication log (**oplog**).
- **Secondary:** Replicates the oplog asynchronously to maintain matching data states.
- **Elections:** 
  - Nodes send heartbeats once every 2 seconds.
  - If the Primary is unreachable for 10 seconds, secondaries initiate an election.
  - Nodes vote for a new Primary based on criteria: (1) network connectivity, (2) priority, (3) replication progress (most up-to-date oplog is preferred).
  - Requires a majority of voting members to elect a new Primary.

> 💡 **Interviewer Focus:** Emphasize that if a network partition splits the replica set, the partition containing the **majority** of nodes remains functional, while the minority partition steps down its Primary to secondary status to prevent split-brain issues.

</details>

<hr/>

### ❓ Q52. **Explain Write Concern vs. Read Concern in MongoDB.**

<details>
<summary><b>👀 Show Answer</b></summary>

These settings control data durability and consistency across replica sets.
- **Write Concern (`w`):** Controls write success confirmation requirements.
  - `w: 1` (Default): Confirmed once written to the local Primary. Fast, but risks data loss if the Primary crashes before replicating.
  - `w: majority`: Confirmed only after written to a majority of voting replica nodes. Protects against rollbacks on replica failures.
  - `j: true`: Confirmed only after written to the on-disk journal file, guaranteeing durability on power failures.
- **Read Concern:** Controls what version of data secondary nodes can return.
  - `local`/`available`: Returns the node's local data state instantly (risks returning dirty data that might get rolled back).
  - `majority`: Returns data committed by a majority of nodes. Prevents reading dirty data.
  - `linearizable`: Guarantees the node queries the Primary to verify it is still the actual Primary before returning data, preventing stale reads from split-brain scenarios.

> 💡 **Interviewer Focus:** Transaction consistency settings and balancing latency overhead against consistency safety.

</details>

<hr/>

### ❓ Q53. **How does sharding work in MongoDB and how do you choose a Shard Key?**

<details>
<summary><b>👀 Show Answer</b></summary>

Sharding distributes collection data across multiple separate database servers (shards) to support horizontal scaling.
- **Architecture:**
  - **mongos**: Query router intercepting application queries.
  - **Config Servers**: Store cluster metadata and chunk routing tables.
  - **Shards**: Individual database instances holding data partitions.
- **Choosing a Shard Key:**
  - The shard key determines how data is partitioned.
  - A good shard key must have:
    1. **High Cardinality:** A large number of distinct values to distribute data evenly.
    2. **Low Frequency:** Prevents hot-spotting (writing to a single shard because one key value dominates the data volume).
    3. **Non-monotonically increasing:** Do not use auto-incrementing IDs or current timestamps as the shard key; this causes all writes to target the same shard (the last one), defeating parallel write performance goals.

> 💡 **Interviewer Focus:** Identifying hot-spots and resolving unbalanced chunk distributions.

</details>

<hr/>

### ❓ Q54. **How do you diagnose query performance using `explain()`?**

<details>
<summary><b>👀 Show Answer</b></summary>

Appending `.explain("executionStats")` to a query provides detailed execution stats:
- **`stage`**:
  - **`COLLSCAN`**: Full collection scan (no index used). Bad.
  - **`IXSCAN`**: Index scan. Good.
  - **`FETCH`**: Retrieving actual documents from disk using index pointers.
  - **`SORT`**: In-memory sort (blocking sort). Bad.
- **Key Metrics:**
  - `nReturned`: Number of documents returned by the query.
  - `totalKeysExamined`: Number of index keys inspected.
  - `totalDocsExamined`: Number of actual documents read from disk.
  - **Goal:** Ideally, `totalKeysExamined` should match `nReturned`, and `totalDocsExamined` should be minimized (or 0 for covered queries).

> 💡 **Interviewer Focus:** Interpreting explain plan hierarchies and identifying when queries trigger memory-heavy sorting stages.

</details>

<hr/>

### ❓ Q55. **Explain document-level locking in the WiredTiger storage engine.**

<details>
<summary><b>👀 Show Answer</b></summary>

WiredTiger (MongoDB's default engine since 3.2) uses **optimistic concurrency control** and document-level locking.
- Under WiredTiger, write operations acquire lock handles at the individual **document level**, not the entire collection or database.
- Multiple transactions can write to the same collection simultaneously as long as they target different documents.
- If two transactions modify the exact same document, one encounters a write conflict and is retried automatically by WiredTiger.

> 💡 **Interviewer Focus:** Contrasting WiredTiger's document locking with MMAPv1's collection/database locking.

</details>

<hr/>

### ❓ Q56. **How does GridFS work and when should you use it?**

<details>
<summary><b>👀 Show Answer</b></summary>

GridFS is a system specification for storing files that exceed the BSON document limit of 16MB.
- **Mechanism:** It splits the target file into chunks (default 255KB) and stores them across two collections:
  1. `fs.files`: Holds file metadata (filename, upload date, size).
  2. `fs.chunks`: Holds the binary data chunks linked via `files_id`.
- **When to use:** Use GridFS when storing large assets directly in the database (e.g., media files, PDFs) while needing query access to file segments without loading the entire file into RAM.
- **Alternative:** Generally, storing large binary objects in AWS S3 and saving S3 links in MongoDB is preferred in production.

> 💡 **Interviewer Focus:** Performance impacts. GridFS queries can clog database I/O compared to object storage services.

</details>

<hr/>

### ❓ Q57. **What is the difference between Ranged Sharding and Hashed Sharding?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **Ranged Sharding:** Partitions data based on range values of the shard key.
  - Pros: Optimizes range query performance since contiguous values reside on the same shard.
  - Cons: Monotonic keys cause hot-spot writes.
- **Hashed Sharding:** Computes an MD5 hash of the shard key value to determine the partition.
  - Pros: Evenly distributes writes across shards, avoiding hot-spots.
  - Cons: Range queries must scatter-gather to all shards since contiguous data is scattered.

> 💡 **Interviewer Focus:** Selecting sharding strategies depending on read-intensive range queries vs high-volume write workloads.

</details>

<hr/>

### ❓ Q58. **Explain the collation property in MongoDB.**

<details>
<summary><b>👀 Show Answer</b></summary>

Collation defines the rules for comparing and sorting character strings (case sensitivity, accent sensitivity, numeric ordering) in queries.
- Defined by locale parameters:
  - `locale`: Geographic region identifier (e.g., `"en"`, `"fr"`).
  - `strength`: Level of comparison strictness (`1` treats base characters equal, ignoring case/accents; `2` checks accents but ignores case; `3` checks case and accents).

> 💡 **Interviewer Focus:** Matching query collation with index collation to utilize indexes.

</details>

<hr/>

### ❓ Q59. **How do you optimize an aggregation pipeline containing multiple stages?**

<details>
<summary><b>👀 Show Answer</b></summary>

Optimization strategies:
1. **Match/Sort First:** Place `$match` and `$sort` stages at the very beginning of the pipeline to leverage indexes.
2. **Filter early:** Use `$project`, `$filter`, and `$limit` early to reduce document counts and sizes passing through subsequent stages.
3. **Avoid redundant $unwind:** `$unwind` dramatically expands the document count; perform filtering on arrays before unwinding them.

> 💡 **Interviewer Focus:** Aggregation memory limits (default 100MB per stage restriction) and utilizing the `allowDiskUse` option.

</details>

<hr/>

### ❓ Q60. **What is the WiredTiger cache eviction policy?**

<details>
<summary><b>👀 Show Answer</b></summary>

WiredTiger reserves RAM (default 50% of (RAM - 1GB)) to cache hot pages.
- **Eviction mechanism:** Background threads monitor dirty pages (modified pages not on disk) and total cache occupancy.
- If total cache occupancy exceeds 80%, or dirty pages exceed 20%, eviction threads begin writing dirty pages to disk and freeing clean pages to make room. If occupancy spikes above 95%, user write threads are blocked and forced to perform eviction themselves (throttling).

> 💡 **Interviewer Focus:** Eviction queue bottlenecks and disk I/O latency.

</details>

<hr/>

### ❓ Q61. **What is replication lag, and how do you monitor it?**

<details>
<summary><b>👀 Show Answer</b></summary>

Replication lag is the delay between a write operation on the Primary node and the application of that write on a Secondary node.
- **Monitoring:** Run `rs.status()` or `rs.printSecondaryReplicationInfo()` in the Mongo Shell. It lists the optime (oplog timestamp) of each secondary node compared to the primary.

> 💡 **Interviewer Focus:** Minimizing write concern lag and tuning oplog size budgets.

</details>

<hr/>

### ❓ Q62. **Explain the difference between linearizable and majority read concern.**

<details>
<summary><b>👀 Show Answer</b></summary>

- **`majority`**: Reads data committed by a majority of nodes. Fast, but if the queried node has been partitioned, it could return stale data that is no longer valid on the actual primary.
- **`linearizable`**: Guarantees the node queries a quorum (majority) of nodes *during* the read operation to verify it is still the actual Primary before returning data. Prevents reading stale data on network splits at the cost of high read latency.

> 💡 **Interviewer Focus:** Real-time data consistency guarantees on partitioned networks.

</details>

<hr/>

### ❓ Q63. **What is the role of Arbiter nodes in replica sets?**

<details>
<summary><b>👀 Show Answer</b></summary>

Arbiters are replica set members that do not host data. Their sole purpose is to participate in primary node elections to break ties and establish a quorum.
- **Pros:** Saves storage/compute costs compared to spinning up a full secondary node.
- **Cons:** Cannot be promoted to Primary and do not provide read scaling.

> 💡 **Interviewer Focus:** Maintaining odd member counts (minimum 3 voting members) in clusters cost-effectively.

</details>

<hr/>

### ❓ Q64. **Explain how MongoDB handles write operations under a split-brain scenario.**

<details>
<summary><b>👀 Show Answer</b></summary>

If a network partition splits a 3-node replica set into a minority partition (1 node) and a majority partition (2 nodes):
- The Primary in the minority partition notices it cannot communicate with a majority of nodes.
- It immediately steps down to secondary status, stopping write operations in that partition.
- The majority partition elects a new Primary and processes writes.
- **Resolution:** When the partition heals, the minority node syncs from the new primary, rolling back any uncommitted writes that did not satisfy `w: majority`.

> 💡 **Interviewer Focus:** Rollback logs parsing and the importance of using `w: majority` write concern.

</details>

<hr/>

### ❓ Q65. **What is the difference between index build processes: Foreground vs Background?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **Foreground (Legacy default):** Blocks all read and write operations on the database/collection during the build. Fast, but causes application downtime.
- **Background (Legacy alternative):** Runs in the background, allowing database operations to continue at the cost of slower index creation.
- **Modern (MongoDB 4.2+):** Uses a hybrid model where indexes are built using an optimized lock-free design, eliminating foreground block behaviors.

> 💡 **Interviewer Focus:** Performance tuning and zero-downtime index deployments.

</details>

<hr/>

### ❓ Q66. **What is a covering index and how do you verify if a query uses it?**

<details>
<summary><b>👀 Show Answer</b></summary>

Verify using `.explain("executionStats")`:
- Look for an execution stage `IXSCAN` without a subsequent `FETCH` stage.
- `totalDocsExamined` must be `0`, indicating no disk documents were loaded.

> 💡 **Interviewer Focus:** Tuning index properties and projection parameters (explicitly setting `_id: 0` unless included in the index).

</details>

<hr/>

### ❓ Q67. **Explain how transaction retry logic works in MongoDB application drivers.**

<details>
<summary><b>👀 Show Answer</b></summary>

Modern MongoDB drivers implement retryable writes and transactions:
- If a write encounter a network drop or primary failover error, the driver automatically resubmits the write operation once to the elected primary.
- For transactions, drivers wrap execution block logic in helper utilities (`withTransaction()`) that handle transient write conflicts and abort errors by retrying the transaction block.

> 💡 **Interviewer Focus:** Driver-level error abstraction.

</details>

<hr/>

### ❓ Q68. **What does the $facet stage accomplish in an aggregation pipeline?**

<details>
<summary><b>👀 Show Answer</b></summary>

It executes multiple, independent aggregation pipelines (facets) in parallel on the same set of input documents. The outputs of these parallel pipelines are returned as arrays inside a single document.

> 💡 **Interviewer Focus:** Multi-dimensional reporting and search metrics dashboards queries.

</details>

<hr/>

### ❓ Q69. **What is the write path of a document to disk under WiredTiger?**

<details>
<summary><b>👀 Show Answer</b></summary>

1. Write is registered in the in-memory **WiredTiger Cache**.
2. Write details are appended sequentially to the **Journal Log** on disk (ensuring crash safety).
3. The server sends confirmation back to the client.
4. Dirty pages in cache are consolidated and written to main collection data files on disk during background **Checkpoint** operations (every 60 seconds).

> 💡 **Interviewer Focus:** Separating journaling durability from checkpoint flushes.

</details>

<hr/>

### ❓ Q70. **How do you configure schema validation using JSON Schema?**

<details>
<summary><b>👀 Show Answer</b></summary>

Create or modify collections using the `validator` parameter:
- **`validationLevel`**: `strict` (validates all inserts/updates) vs `moderate` (validates existing active records only).
- **`validationAction`**: `error` (rejects invalid writes) vs `warn` (logs violation but accepts write).

> 💡 **Interviewer Focus:** Transitioning schema-less databases to validated structures.

</details>

<hr/>

### ❓ Q71. **What is the difference between read preference and read concern?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **Read Preference:** Controls **where** the driver routes read queries (e.g. `primary`, `secondary`, `nearest`).
- **Read Concern:** Controls **what consistency** level the queried node uses to filter returned data (e.g. `local`, `majority`, `linearizable`).

> 💡 **Interviewer Focus:** Clean categorization of routing routing parameters vs data freshness parameters.

</details>

<hr/>

### ❓ Q72. **How do you monitor index usage in MongoDB?**

<details>
<summary><b>👀 Show Answer</b></summary>

Use the `$indexStats` aggregation stage:
- It returns metadata statistics for each index in the collection, including the number of times (`ops`) the index was chosen by the query optimizer.
- Unused indexes (`ops = 0` over long periods) should be dropped to save write I/O and RAM.

> 💡 **Interviewer Focus:** Clean indexes hygiene.

</details>

<hr/>

### ❓ Q73. **Explain the difference between sparse indexes and partial indexes.**

<details>
<summary><b>👀 Show Answer</b></summary>

- **Sparse Index:** Indexes only documents containing the indexed field. It cannot evaluate custom fields values or filters.
- **Partial Index:** Uses a `partialFilterExpression` query filter. It can index a subset of documents based on complex conditions (e.g., `{ age: { $gt: 21 } }`), saving significant storage.

> 💡 **Interviewer Focus:** Partial indexes are more powerful and preferred for selective indexing.

</details>

<hr/>

### ❓ Q74. **What is the impact of index keys size on index efficiency?**

<details>
<summary><b>👀 Show Answer</b></summary>

Large index keys (like indexing long strings or full text) increase the physical memory size of the index tree.
- Since B-Tree pages hold fewer keys, the index consumes more RAM.
- If indexes do not fit entirely in the WiredTiger cache RAM, pages must be swapped out of disk constantemente (cache thrashing), which degrades write and read performance.

> 💡 **Interviewer Focus:** Cache fitting optimization.

</details>

<hr/>

### ❓ Q75. **How does MongoDB handle concurrent connections?**

<details>
<summary><b>👀 Show Answer</b></summary>

MongoDB uses a thread-per-connection execution model (with connection pooling pools).
- High concurrent connection counts consume significant host system memory and thread scheduling context-switching overhead.
- Deploying connection pooling middleware (like HAProxy or application-level pools) helps limit active threads on database servers.

> 💡 **Interviewer Focus:** Thread scheduling overheads.

</details>

<hr/>

## 🟣 Expert Level

### ❓ Q76. **Explain the WiredTiger Ticketing System and how it manages write queue saturation.**

<details>
<summary><b>👀 Show Answer</b></summary>

WiredTiger controls concurrent execution internally using a ticketing system to prevent thread exhaustion.
- **Tickets Allocation:**
  - It maintains a pool of read tickets (default 128) and write tickets (default 128).
  - Every incoming read or write operation must acquire a ticket before entering the WiredTiger execution engine.
- **Saturation Behavior:**
  - Under heavy concurrency or slow disk write performance, operations hold tickets longer.
  - When the ticket pool is exhausted, new requests must wait in a queue, causing application latency spikes.
  - You can monitor this state via `db.serverStatus().wiredTiger.concurrentTransactions`.

> 💡 **Interviewer Focus:** Differentiating application-layer connection exhaustion from storage-layer ticket exhaustion.

</details>

<hr/>

### ❓ Q77. **Explain Causal Consistency and how it ensures read-your-own-writes.**

<details>
<summary><b>👀 Show Answer</b></summary>

In distributed replica set environments, reading from secondaries can result in reading stale data due to replication lag. **Causal Consistency** solves this.
- **Mechanism:**
  - Uses logical clocks (**Cluster Time**) to order events causally.
  - When a write completes, the server returns an operation token indicating the transaction time.
  - For subsequent reads, the client sends this token. The secondary node blocks execution of the read until its oplog replication catches up to that specific cluster time.
  - This guarantees **Read-Your-Own-Writes** and **Monotonic Reads** consistency without requiring expensive reads from the Primary.

> 💡 **Interviewer Focus:** How logical cluster clocks prevent replica lag reading anomalies.

</details>

<hr/>

### ❓ Q78. **Explain the internals of WiredTiger Cache Eviction and Checkpointing.**

<details>
<summary><b>👀 Show Answer</b></summary>

WiredTiger does not sync data to files on disk during every write.
- **Journaling:** Writes are logged sequentially to the journal file for crash safety.
- **In-Memory Cache:** Actual document updates are written to WiredTiger's in-memory cache.
- **Checkpointing:** 
  - Every 60 seconds (or once 2GB of journal is written), a checkpoint thread runs.
  - It writes all dirty pages from cache to the main collection files on disk.
- **Cache Eviction:** 
  - Background threads monitor cache usage.
  - If dirty data exceeds 20% of cache size, or total data in cache exceeds 80%, eviction threads begin pushing clean pages out of memory and writing dirty pages to disk, slowing down user write threads if eviction cannot keep up.

> 💡 **Interviewer Focus:** WiredTiger memory sizing rules (default is 50% of (RAM - 1GB)) and avoiding memory starvation under containerized configurations.

</details>

<hr/>

### ❓ Q79. **How do you choose a Shard Key to prevent Jumbo Chunks and Hot Spots?**

<details>
<summary><b>👀 Show Answer</b></summary>

A poorly selected shard key can result in **Jumbo Chunks**—chunks of data that exceed the maximum chunk size (default 64MB) and cannot be split because all documents share the exact same shard key value.
- **Preventing Hot Spots & Jumbo Chunks:**
  - Do not use low-cardinality keys (like `gender` or `status`).
  - Do not use monotonic keys (like timestamp or auto-incrementing ID).
  - **Solution: Compound Shard Keys.** Combine a high-cardinality field with a functional field (e.g., `{ tenantId: 1, userId: 1 }` or `{ hashed_id: "hashed" }`).
  - Hashing the key distributes writes uniformly across all shards, though it degrades range query performance.

> 💡 **Interviewer Focus:** Balancing write distribution (hashed keys) vs range query performance (ranged keys).

</details>

<hr/>

### ❓ Q80. **What are Change Streams and how do they capture real-time write events?**

<details>
<summary><b>👀 Show Answer</b></summary>

Change Streams allow applications to access real-time data changes without the complexity of tailing the oplog.
- **How they work:**
  - They rely on the replica set **oplog** (operations log).
  - When a change occurs, the stream emits a change event document to the listening application.
  - **Resumability:** Every change event contains a resume token (`_data`). If the connection drops, the client reconnects passing this token to resume reading changes exactly where it left off, preventing data loss.
  - Can be filtered and transformed inside MongoDB using aggregation stages before sending to the client.

> 💡 **Interviewer Focus:** Resumability architecture and oplog retention rules in production.

</details>

<hr/>

### ❓ Q81. **Explain the initial sync vs oplog tailing replication mechanism.**

<details>
<summary><b>👀 Show Answer</b></summary>

When a new node joins a replica set:
1. **Initial Sync:**
   - The node copies all database data from a sync source node collection-by-collection.
   - During data copying, it records all incoming writes in its local buffer.
   - It builds indexes on the copied collections.
   - It applies the buffered writes to catch up.
2. **Oplog Tailing:**
   - Once synchronized, the secondary node queries the sync source node's `local.oplog.rs` collection using a tailable cursor.
   - It applies the write events asynchronously in a local worker pool thread model to stay in sync.

> 💡 **Interviewer Focus:** Thread pooling replication mechanisms and replication log size constraints.

</details>

<hr/>

### ❓ Q82. **Explain how WiredTiger handles page locks and concurrent page access.**

<details>
<summary><b>👀 Show Answer</b></summary>

WiredTiger does not use traditional spinlocks for reader concurrency:
- It utilizes **hazard pointers** to coordinate access to in-memory pages.
- When a thread accesses an in-memory page, it registers a hazard pointer on it.
- Eviction or modification threads cannot modify or reclaim a page that has active hazard pointers, ensuring lock-free reader concurrency without mutex block bottlenecks.

> 💡 **Interviewer Focus:** Hazard pointer patterns in transaction concurrency.

</details>

<hr/>

### ❓ Q83. **How do you troubleshoot index bloat in MongoDB?**

<details>
<summary><b>👀 Show Answer</b></summary>

Index bloat occurs when high write/delete volumes create fragmented index pages.
- **Troubleshooting:**
  - Check collection statistics using `db.collection.stats()`. Compare logical index size vs actual disk index size.
  - **Resolution:** Run the **`compact`** command on the collection to rebuild indexes and defragment page allocation: `db.runCommand({ compact: "collectionName" });`
  - Note: In replica sets, run `compact` on secondaries first before triggering failover to avoid production write blocks.

> 💡 **Interviewer Focus:** compact command performance overhead and replica set rolling configurations.

</details>

<hr/>

### ❓ Q84. **How do you design a schema to avoid the Unbounded Array anti-pattern?**

<details>
<summary><b>👀 Show Answer</b></summary>

An unbounded array grows indefinitely (e.g. storing all comments inside a single post document). This risks exceeding the 16MB BSON size limit and degrades performance because the database must read/write the entire array.
- **Alternative Patterns:**
  - **Bucket Pattern:** Group records into bounded array documents (e.g. storing 100 comments per document).
  - **Referencing:** Store comments in a separate collection, with each comment document containing a reference ID (`postId`) pointing to the parent.

> 💡 **Interviewer Focus:** Document limit constraints and memory loading optimization.

</details>

<hr/>

### ❓ Q85. **Explain the impact of write concerns on replication performance and safety.**

<details>
<summary><b>👀 Show Answer</b></summary>

Write concern defines the confirmation requirements for write operations:
- **`w: 1`**: Confirm once written to the primary node. Low write latency, but risks data rollback if the primary crashes before replicating writes.
- **`w: majority`**: Confirm once written to a majority of voting replica set nodes. Protects against rollbacks at the cost of network latency round-trips.
- **`j: true`**: Write must be flushed to the journal on disk before confirmation, guaranteeing durability but increasing latency.

> 💡 **Interviewer Focus:** Balancing network-latency trade-offs against absolute data safety.

</details>

<hr/>

### ❓ Q86. **How does MongoDB handle schema migration in high-traffic production databases with zero downtime?**

<details>
<summary><b>👀 Show Answer</b></summary>

Since MongoDB is schema-less:
- Do not execute database-level queries to update all historical documents at once; this blocks connections and slows performance.
- **Lazy Migration Strategy:**
  - Modify application code to handle both old and new schema structures dynamically.
  - When a document is read, assign default values for missing new fields.
  - Write documents in the new schema format during standard user update operations.
  - Run a background script to update remaining un-migrated records in small, throttle batches.

> 💡 **Interviewer Focus:** Lazy validation code designs and throttling batch updates.

</details>

<hr/>

### ❓ Q87. **Explain the implementation of two-phase commit inside MongoDB transactions.**

<details>
<summary><b>👀 Show Answer</b></summary>

For transactions spanning multiple shards:
- The `mongos` router acts as the **Transaction Coordinator**.
- It uses a **Two-Phase Commit (2PC)** process, logging state changes to a coordinator log collection.
- It prepares the transaction on all target shards, votes on feasibility, and sends commits. If a coordinator drops mid-transaction, backup recovery sessions reconcile states using session transaction tokens.

> 💡 **Interviewer Focus:** Distributed transaction coordinator logic.

</details>

<hr/>

### ❓ Q88. **What is the performance cost of using MongoDB as a queue system?**

<details>
<summary><b>👀 Show Answer</b></summary>

Using collections as queues (e.g. `findAndModify` querying for status and updating it) causes performance bottlenecks:
- It creates high write lock contention on the same index key values.
- High delete volumes lead to page fragmentation (index bloat) and cache thrashing.
- Recommend using dedicated queuing systems (RabbitMQ, SQS, Redis) for fast operations.

> 💡 **Interviewer Focus:** Identifying database model anti-patterns.

</details>

<hr/>

### ❓ Q89. **How does MongoDB sharding handle split chunk operations during high write volume?**

<details>
<summary><b>👀 Show Answer</b></summary>

When a chunk size grows beyond the limit (64MB):
1. The shard hosting the chunk splits it into two chunks by updating metadata on config servers.
2. The config server lock changes.
3. The balancer process runs, planning migration to balance chunk counts across shards.
4. If write volumes are high, the balancer's block migrations can cause replication lag and slow queries.

> 💡 **Interviewer Focus:** Balancing metrics during high write bursts.

</details>

<hr/>

### ❓ Q90. **Explain how election timeouts affect primary node failover latency.**

<details>
<summary><b>👀 Show Answer</b></summary>

- **`electionTimeoutMillis`** (default 10,000ms): The time secondaries wait before initiating a primary election.
- Lowering this value decreases failover latency, but can trigger false elections on transient network drops, causing system instability.

> 💡 **Interviewer Focus:** Tuning network heartbeat parameters.

</details>

<hr/>

### ❓ Q91. **What is the difference between $lookup using local/foreign fields vs custom pipeline lookups?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **Local/Foreign Field:** Performs a simple left outer join. Internal optimization translates this to a fast index search.
- **Custom Pipeline Lookup:** Allows executing complex aggregation stages (filtering, calculations) inside the joined collection using variables (`let`). It is more powerful but slower because it can bypass index paths if not structured carefully.

> 💡 **Interviewer Focus:** Pipeline variables mapping performance.

</details>

<hr/>

### ❓ Q92. **How does the WiredTiger storage engine write dirty pages to disk during checkpoints?**

<details>
<summary><b>👀 Show Answer</b></summary>

During checkpoints (every 60s):
- WiredTiger writes snapshots of dirty pages to disk using a **Copy-on-Write** mechanism.
- Instead of overwriting existing data blocks in-place, it writes changes to new disk blocks and updates tree pointers atomically. This prevents file corruption on power failures.

> 💡 **Interviewer Focus:** Structural integrity crash recovery designs.

</details>

<hr/>

### ❓ Q93. **What is the difference between statement-based replication and row-based replication (oplog)?**

<details>
<summary><b>👀 Show Answer</b></summary>

MongoDB's **oplog** is statement-independent:
- It stores **idempotent operations** (e.g. converting updates into exact `$set` operations of properties with precise values, rather than incremental `$inc` queries).
- Replicating idempotent events ensures that executing the oplog multiple times yields identical results.

> 💡 **Interviewer Focus:** Oplog idempotency design patterns.

</details>

<hr/>

### ❓ Q94. **Explain how databases handle lock upgrades and lock escalation in collections.**

<details>
<summary><b>👀 Show Answer</b></summary>

WiredTiger does not escalate locks because it uses document-level locking based on optimistic concurrency control.
- If lock conflicts occur, threads retry transaction steps instead of locking parent collection layers, preventing concurrency bottlenecks.

> 💡 **Interviewer Focus:** Concurrency benefits of optimistic lock engines.

</details>

<hr/>

### ❓ Q95. **What is doublewrite buffer / journaling in WiredTiger?**

<details>
<summary><b>👀 Show Answer</b></summary>

WiredTiger writes transactions sequentially to the **Journal file** on disk before returning success. The journal acts as the recovery log to reconstruct changes since the last checkpoint during startup recovery.

> 💡 **Interviewer Focus:** Durability guarantees.

</details>

<hr/>

### ❓ Q96. **How does MongoDB handle scale limitations on ObjectID?**

<details>
<summary><b>👀 Show Answer</b></summary>

The 12-byte `ObjectId` structure is highly scalable:
- The 4-byte timestamp resets on integer overflow far in the future.
- Machine/process IDs (5-bytes) and incrementing counters (3-bytes) allow up to 16 million unique IDs per second per process, preventing collision bottlenecks.

> 💡 **Interviewer Focus:** ObjectId components.

</details>

<hr/>

### ❓ Q97. **Explain how transaction isolation levels are enforced under WiredTiger.**

<details>
<summary><b>👀 Show Answer</b></summary>

MongoDB transactions support **Snapshot Isolation**:
- It reads data from a transaction snapshot matching the start transaction time.
- Write conflicts are detected when writing to the same document, triggering transaction aborts and retries.

> 💡 **Interviewer Focus:** Lock-free read concurrency.

</details>

<hr/>

### ❓ Q98. **How does distributed sharding affect aggregation queries scatter-gather?**

<details>
<summary><b>👀 Show Answer</b></summary>

Aggregations are split:
- **`mongos`** sends stages to all shards.
- Shards perform local matching/grouping (`$match`, `$group`).
- Results are returned to `mongos`, which executes final consolidation and sorting before returning data.

> 💡 **Interviewer Focus:** Coordinator overhead.

</details>

<hr/>

### ❓ Q99. **Explain WiredTiger delete space fragmentation reuse.**

<details>
<summary><b>👀 Show Answer</b></summary>

When documents are deleted, WiredTiger does not release disk space to the OS.
- Instead, it marks the page blocks as free and records them in internal lists.
- Subsequent inserts reuse these free blocks. To reclaim disk space, run the `compact` command.

> 💡 **Interviewer Focus:** Database storage management.

</details>

<hr/>

### ❓ Q100. **How do you optimize MongoDB for write-heavy high-throughput ingestion workloads?**

<details>
<summary><b>👀 Show Answer</b></summary>

1. Use **`bulkWrite()`** to batch operations.
2. Index only required fields (avoid unused indexes).
3. Select hashed sharding to distribute writes.
4. Disable write concern journals (`j: false`) if data loss during crash is acceptable.

> 💡 **Interviewer Focus:** Minimizing disk I/O bottlenecks.

</details>

<hr/>

### 🧭 Navigation

| ⬅️ Previous | 🏠 Index | ➡️ Next |
| :--- | :---: | ---: |
| [⬅️ SQL](./08_SQL.md) | [Home](./00_Index.md) | [➡️ AWS](./10_AWS.md) |
