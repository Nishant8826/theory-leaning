# Sequelize ORM

## What is it?
Sequelize is a modern, promise-based Object-Relational Mapper (ORM) for Node.js. It supports relational databases like PostgreSQL, MySQL, MariaDB, SQLite, and Microsoft SQL Server. It maps database tables directly to JavaScript classes (Models) and provides features for validating data, managing transactions, running migrations, and defining relationships.

## Why do we need it?
Writing raw SQL queries in application code can be difficult to manage. Developers have to manually sanitize inputs to prevent SQL Injection, map result arrays back to JS objects, and manage connection pools. Sequelize handles these tasks automatically, providing a structured, type-safe API to interact with databases, making backend applications easier to write, scale, and test.

```
Without ORM (Raw SQL):
Client Request ──> Manual Input Sanitization ──> Raw SQL query string ──> Execute 
               ──> Map row array to JS objects (High boilerplate, error-prone)

With Sequelize ORM (Active Record):
Client Request ──> Model.findOne({ where: { id } }) ──> Auto parameterization ──> Execute
               ──> Return Sequelize Model Instance (Rich OOP methods, highly clean)
```

## How does it work?
Sequelize uses the **Active Record** pattern. 
1. **Model Representation**: Every table is mapped to a Model class, and every row in that table is represented as an instance of that class.
2. **Dynamic SQL Generation**: When you execute a query (like `User.findAll()`), Sequelize translates the method arguments into a parameterized SQL statement, passes it to the database driver, and parses the returned rows into model instances.
3. **Connection Pooling**: Sequelize manages a pool of database connections internally, recycling active sockets to handle high-concurrency requests efficiently.
4. **Migrations**: Track schema modifications over time using version-controlled JS files, allowing database environments to stay synchronized.

### Hinglish Explanation of Core Working:
* **Model Representation (Tabular to Object Mapping)**: Har database table ko hum ek JS class (Model) se connect karte hain. Jab database se ek line (row) read hoti hai, toh Sequelize usey ek standard JS object (instance) bana deta hai, jise hum code mein easily dot notation (jaise `user.name`) se read/update kar sakte hain.
* **Dynamic SQL Generation (Query Translation)**: Jab aap `User.findAll()` run karte hain, toh aapko manual SQL likhne ki zaroorat nahi hoti. Sequelize is method call ko background mein dynamic `SELECT * FROM users;` query mein convert kar deta hai aur security ke liye values ko auto-sanitize/parameterize karta hai.
* **Connection Pooling (Connection Management)**: Database se har query par ek new network connection socket banana slow aur heavy hota hai. Sequelize pehle se kuch active connections ka ek group (pool) bana kar rakhta hai. Jab query aati hai, tab usi pool se ek connection query chalane ke liye de deta hai aur run hone ke baad socket wapas pool mein return ho jata hai.
* **Migrations (Database Version Control)**: Database design ko build-by-build safely modify karne ka tarika. Agar aapko table mein new columns add karne hain ya schemas badalne hain, toh JS version-controlled files use hoti hain taaki production servers aur local developers ka database sync rahe.

## Impact
* **Application Architecture**: Strongly model-driven, organizing data models and tables into clean class files.
* **Performance**: Adds translation overhead compared to raw SQL query builders. If associations are loaded incorrectly, it can trigger performance issues like the N+1 query problem.
* **Maintainability**: Centralizes validations, hooks, and relationships, making codebase changes clean and predictable.
* **Scalability**: Transaction management and read-replica replication support help applications scale.

## Real World Example
In a multi-user blog application, when a user creates a post, Sequelize checks that the post title is valid, appends the user's ID as a foreign key, and saves the post within a database transaction. If the database save fails, the transaction rolls back, preventing orphaned data records.

## Syntax
* **Initialization**:
```javascript
const { Sequelize } = require('sequelize');
const sequelize = new Sequelize('database', 'username', 'password', { host: 'localhost', dialect: 'postgres' });
```
* **Defining Model**:
```javascript
class User extends Model {}
User.init({ username: DataTypes.STRING }, { sequelize, modelName: 'User' });
```
* **Creating Associations**:
```javascript
User.hasMany(Post, { foreignKey: 'userId' });
Post.belongsTo(User, { foreignKey: 'userId' });
```

## Data Types in Sequelize

Sequelize provides a wide range of data types to map JavaScript variables directly to database column types. These are accessed via the `DataTypes` object.

### Common Data Types & Database Mapping

| Sequelize Type | JavaScript Type | PostgreSQL Type | MySQL Type | Description & Use Case |
| :--- | :--- | :--- | :--- | :--- |
| `DataTypes.STRING` | `string` | `VARCHAR(255)` | `VARCHAR(255)` | Short text columns (titles, names, email). Length restrict karne ke liye `DataTypes.STRING(100)` use karein. |
| `DataTypes.TEXT` | `string` | `TEXT` | `TEXT` | Long text blobs (blog content, description, comments). |
| `DataTypes.INTEGER` | `number` | `INTEGER` | `INT` | Standard integers. Can be signed/unsigned (MySQL). |
| `DataTypes.BOOLEAN` | `boolean` | `BOOLEAN` | `TINYINT(1)` | True/False values (isActive, isVerified). |
| `DataTypes.DATE` | `Date` | `TIMESTAMP WITH TIME ZONE` | `DATETIME` | Date and time (timestamps, birthdates). |
| `DataTypes.UUID` | `string` | `UUID` | `CHAR(36)` | Universally Unique Identifiers. `DataTypes.UUIDV4` automatically generates values. |
| `DataTypes.ENUM` | `string` | `USER_DEFINED` | `ENUM` | Standardizes value to a predefined set. e.g., `DataTypes.ENUM('admin', 'user', 'guest')`. |
| `DataTypes.JSON` | `object`/`array` | `JSON` | `JSON` | Saves raw JSON object formatting. |
| `DataTypes.JSONB` | `object`/`array` | `JSONB` | N/A (Postgres only) | Binary JSON. Faster queries and supports indexing. |
| `DataTypes.ARRAY(...)` | `array` | `ARRAY` | N/A (Postgres only) | Array of another DataType, e.g., `DataTypes.ARRAY(DataTypes.STRING)`. |

### Hinglish Explanation of Data Types:
* **Datatypes Ka Kaam**: Jab aap schema (table design) define karte hain, toh database ko batana padta hai ki kis column mein kis tarah ka data store hoga. `DataTypes.STRING` short text ke liye hota hai, jabki `DataTypes.TEXT` lambi descriptions ke liye.
* **Auto Validation**: Sequelize data types database level par table schema create karne ke sath-sath Javascript level par data validation bhi karte hain. Agar integer column mein string bhejoge toh query run hone se pehle hi errors catch ho jayenge.
* **UUID (Universally Unique Identifier)**: Standard auto-incrementing ID (1, 2, 3...) ke badle high-security system mein UUIDV4 use kiya jata hai (jaise `4a7b9e1c-5d2f-4e0a-8b8c-1e2f3a4b5c6d`), jisse database records guessing and scraping tools ke liye protected rehte hain.

## Code Examples

### 1. Database Connection and Model Definition
```javascript
// db/sequelize.js
const { Sequelize, DataTypes, Model } = require('sequelize');

const sequelize = new Sequelize(
  process.env.DB_NAME || 'my_db',
  process.env.DB_USER || 'postgres',
  process.env.DB_PASS || 'password',
  {
    host: process.env.DB_HOST || 'localhost',
    port: process.env.DB_PORT || 5432,
    dialect: 'postgres',
    logging: process.env.NODE_ENV === 'development' ? console.log : false,
    pool: {
      max: 10,
      min: 0,
      acquire: 30000,
      idle: 10000
    }
  }
);

class User extends Model {}
User.init({
  id: {
    type: DataTypes.UUID,
    defaultValue: DataTypes.UUIDV4,
    primaryKey: true
  },
  email: {
    type: DataTypes.STRING,
    allowNull: false,
    unique: true,
    validate: {
      isEmail: true
    }
  },
  username: {
    type: DataTypes.STRING,
    allowNull: false,
    validate: {
      len: [3, 30]
    }
  }
}, {
  sequelize,
  modelName: 'User',
  tableName: 'users',
  timestamps: true,
  indexes: [{ unique: true, fields: ['email'] }]
});

class Post extends Model {}
Post.init({
  id: {
    type: DataTypes.INTEGER,
    autoIncrement: true,
    primaryKey: true
  },
  title: {
    type: DataTypes.STRING,
    allowNull: false
  },
  content: {
    type: DataTypes.TEXT,
    allowNull: false
  }
}, {
  sequelize,
  modelName: 'Post',
  tableName: 'posts',
  timestamps: true
});

// Associations Setup
User.hasMany(Post, { as: 'posts', foreignKey: 'userId', onDelete: 'CASCADE' });
Post.belongsTo(User, { as: 'author', foreignKey: 'userId' });

module.exports = { sequelize, User, Post };
```

### 2. Complete CRUD Operations (Create, Read, Update, Delete) & Eager Loading

Sequelize allows you to execute standard CRUD operations using async/await syntax. Here is a fully fleshed-out controller demonstrating all actions, along with eager loading and proper error handling.

#### Hinglish Explanation of CRUD Methods:
* **Create (Data Insert)**: Database mein new entry daalne ke liye hum `.create()` call karte hain jo database mein row insert karke model ka instance return karta hai. Multiple entries ek saath insert karne ke liye `.bulkCreate()` use hota hai.
* **Read (Data Retrieval)**: Table se data read karne ke liye `.findByPk()` (primary key search), `.findOne()` (single match search), aur `.findAll()` (multiple entries match) methods hote hain. Custom filter lagane ke liye `where` block use kiya jata hai.
* **Update (Data Modification)**: Kisi existing record ko change karne ke do tareeqe hote hain: direct query level update `.update()` call karke (fast execution, returns count), ya object instance retrieve karke uske fields edit karna aur `.save()` call karna (triggers hooks, triggers instance validation).
* **Delete (Data Removal)**: Entry delete karne ke liye `.destroy()` call karte hain. Isme `where` filter lagana zaroori hai, varna table ka data clean ho sakta hai!

```javascript
// controllers/post-controller.js
const { User, Post } = require('../db/sequelize');
const { Op } = require('sequelize'); // Import operators for search queries

// 1. CREATE: Create a New Post
exports.createPost = async (req, res, next) => {
  try {
    const { title, content, userId } = req.body;

    // Create record in the database
    const newPost = await Post.create({
      title,
      content,
      userId
    });

    res.status(201).json({
      success: true,
      message: 'Post created successfully',
      data: newPost
    });
  } catch (err) {
    next(err);
  }
};

// 2. READ: Get All Posts (with Pagination, Searching & Eager Loading)
exports.getPosts = async (req, res, next) => {
  try {
    const { page = 1, limit = 10, search = '' } = req.query;
    const offset = (page - 1) * limit;

    const queryOptions = {
      limit: parseInt(limit),
      offset: parseInt(offset),
      order: [['createdAt', 'DESC']],
      // Eager Load association to prevent N+1 query loops
      include: [{
        model: User,
        as: 'author',
        attributes: ['id', 'username', 'email']
      }]
    };

    // If search term is provided, filter by title using iLike (Postgres) or Like operator
    if (search) {
      queryOptions.where = {
        title: {
          [Op.iLike]: `%${search}%` // Case-insensitive matching
        }
      };
    }

    const { count, rows: posts } = await Post.findAndCountAll(queryOptions);

    res.json({
      totalItems: count,
      totalPages: Math.ceil(count / limit),
      currentPage: parseInt(page),
      posts
    });
  } catch (err) {
    next(err);
  }
};

// 3. READ: Get a Single Post by ID
exports.getPostById = async (req, res, next) => {
  try {
    const { id } = req.params;

    const post = await Post.findByPk(id, {
      include: [{
        model: User,
        as: 'author',
        attributes: ['id', 'username', 'email']
      }]
    });

    if (!post) {
      return res.status(404).json({ success: false, message: 'Post not found' });
    }

    res.json({ success: true, data: post });
  } catch (err) {
    next(err);
  }
};

// 4. UPDATE: Update a Post (Method A: Direct Model Update)
exports.updatePostDirectly = async (req, res, next) => {
  try {
    const { id } = req.params;
    const { title, content } = req.body;

    // Runs a single UPDATE query directly at the database level
    const [updatedRowsCount] = await Post.update(
      { title, content },
      { where: { id } }
    );

    if (updatedRowsCount === 0) {
      return res.status(404).json({ success: false, message: 'Post not found or no changes made' });
    }

    res.json({ success: true, message: 'Post updated successfully' });
  } catch (err) {
    next(err);
  }
};

// 5. UPDATE: Update a Post (Method B: Instance-Level Save - triggers hooks & model validation)
exports.updatePostInstance = async (req, res, next) => {
  try {
    const { id } = req.params;
    const { title, content } = req.body;

    // Fetch the instance first
    const post = await Post.findByPk(id);
    if (!post) {
      return res.status(404).json({ success: false, message: 'Post not found' });
    }

    // Set properties and call save()
    post.title = title || post.title;
    post.content = content || post.content;
    await post.save(); // Automatically runs UPDATE query containing only changed fields

    res.json({ success: true, message: 'Post updated successfully', data: post });
  } catch (err) {
    next(err);
  }
};

// 6. DELETE: Delete a Post
exports.deletePost = async (req, res, next) => {
  try {
    const { id } = req.params;

    // Delete query: DELETE FROM posts WHERE id = id
    const deletedRowsCount = await Post.destroy({
      where: { id }
    });

    if (deletedRowsCount === 0) {
      return res.status(404).json({ success: false, message: 'Post not found' });
    }

    res.json({ success: true, message: 'Post deleted successfully' });
  } catch (err) {
    next(err);
  }
};
```

### 3. Managed Transactions
```javascript
// services/user-registration.js
const { sequelize, User, Post } = require('../db/sequelize');

exports.registerUserAndCreateWelcomePost = async (userData, welcomePostData) => {
  // Use a managed transaction. If any database write fails, the entire transaction rolls back automatically.
  return sequelize.transaction(async (t) => {
    
    const user = await User.create(userData, { transaction: t });
    
    const postData = {
      ...welcomePostData,
      userId: user.id
    };
    
    const post = await Post.create(postData, { transaction: t });
    
    return { user, post };
  });
};
```

## Best Practices
* **Always Use Eager Loading (`include`)**: When querying lists of records that require related data, always use eager loading to fetch everything in a single `JOIN` query, avoiding the N+1 query problem.
* **Define Indexes Explicitly**: Add database indexes to columns that are frequently used in `where` filters or search conditions to improve lookup speeds.
* **Keep Database Dialects abstract**: Avoid writing dialect-specific raw queries. Rely on Sequelize's query generator methods to keep dialet-switching possible.

## Common Mistakes
* **Executing Queries in Loops (The N+1 Anti-Pattern)**: Running database queries inside map loops. For example, fetching a list of posts, and then looping over them to fetch each author. This triggers dozens of network requests, slowing down the event loop. Use eager loading (`include`) instead.
* **Forgetting Transactions on Multi-Step Operations**: Updating account balances or creating related orders without wrapping the writes in a transaction. If one write fails, it leaves orphaned or corrupted records in the database.

## Interview Questions & Answers

### Q: What is the N+1 Query Problem in Sequelize and how can you resolve it?
**A**: The N+1 Query Problem occurs when the application runs one query to fetch parent records, and then runs a separate query (N queries) for each parent record to fetch related data. For example, fetching 100 posts, and then running 100 queries to get the author for each post. This can be resolved by using Eager Loading (the `include` option) in your initial query, forcing Sequelize to fetch all related data in a single SQL query using a `JOIN` statement.

### Q: Explain the difference between managed and unmanaged transactions in Sequelize.
**A**: An **unmanaged transaction** requires you to manually commit or roll back the transaction:
```javascript
const t = await sequelize.transaction();
try {
  await User.create(data, { transaction: t });
  await t.commit();
} catch (err) {
  await t.rollback();
}
```
A **managed transaction** handles commits and rollbacks automatically. You pass a callback containing your queries to `sequelize.transaction()`, and it commits if the callback resolves or rolls back if an error is thrown.

### Q: Why should you avoid using `.sync({ force: true })` in production environments?
**A**: Using `{ force: true }` drops tables and recreates them, deleting all existing data in the process. In production, you should manage database schemas using version-controlled migrations (`sequelize-cli`) to apply updates safely without losing data.

## Summary
Sequelize ORM simplifies database interactions in Node.js using the Active Record pattern. Managing model definitions, validations, transactions, and eager loading (`include`) ensures secure, structured, and performant database architectures.

---
Previous : [40_ORM_Concepts.md](40_ORM_Concepts.md) | Index : [00_index.md](00_index.md) | Next : [41_Redis.md](41_Redis.md)
