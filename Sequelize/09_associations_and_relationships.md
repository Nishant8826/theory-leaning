# 09. Associations and Relationships

## 🎯 Goal of This Chapter
By the end of this chapter, you will understand how to model and configure relationships between tables in Sequelize. You will learn the mechanics of One-to-One, One-to-Many, and Many-to-Many associations, where foreign keys are located, and how to structure your model code to keep associations organized.

---

## 🤔 Why This Topic Matters
Real-world data is relational. A user has a profile; a user writes blog posts; a post has many tags. If you do not define associations correctly:
* Your database will lack referential integrity (e.g. posts can refer to user IDs that don't exist, creating "orphaned records").
* You won't be able to fetch related data in a single clean query, forcing you to write slow, manual database lookups.
* Many-to-Many junctions will require manual management, increasing bugs.

---

## 🧠 Core Concept

Sequelize defines relationships using four helper methods:
1. **`hasOne`**: Establishes a 1:1 relationship where the foreign key is in the target model.
2. **`belongsTo`**: Establishes a relationship where the foreign key is in the source model itself. Used to complete 1:1 and 1:M relationships.
3. **`hasMany`**: Establishes a 1:M relationship where the foreign key is in the target model.
4. **`belongsToMany`**: Establishes a M:N (Many-to-Many) relationship using a junction table (joins table) defined in the `through` option.

### Where does the Foreign Key Go?
This is the most important rule of ORM associations:
* **The model containing the `belongsTo` method always holds the Foreign Key column.**

---

## 🏗 Mental Model / Internal Working

### 1. One-to-One (1:1)
* **Example**: A `User` has one `Profile`.
* **Model Association**:
  ```javascript
  User.hasOne(Profile, { foreignKey: 'userId' });
  Profile.belongsTo(User, { foreignKey: 'userId' });
  ```
* **Database Layout**: The `profiles` table contains the column `userId`.

### 2. One-to-Many (1:M)
* **Example**: A `User` has many `Posts`.
* **Model Association**:
  ```javascript
  User.hasMany(Post, { foreignKey: 'userId' });
  Post.belongsTo(User, { foreignKey: 'userId' });
  ```
* **Database Layout**: The `posts` table contains the column `userId`.

### 3. Many-to-Many (M:N)
* **Example**: A `Post` has many `Tags`, and a `Tag` belongs to many `Posts`.
* **Model Association**:
  ```javascript
  Post.belongsToMany(Tag, { through: 'PostTags', foreignKey: 'postId' });
  Tag.belongsToMany(Post, { through: 'PostTags', foreignKey: 'tagId' });
  ```
* **Database Layout**: A third table called `PostTags` is created. It contains two columns: `postId` and `tagId` (a junction table).

---

## 🌍 Real-World Analogy
Think of relationships as **Family Connections**:
* **One-to-One**: A husband and a wife. They are connected directly. If one has the ring, they are linked.
* **One-to-Many**: A mother and her children. The children must point to their mother (each child has their mother's name printed on their birth certificate — the **foreign key**). The mother does not print children's names on her ID; the link exists on the children's side.
* **Many-to-Many**: Authors and books. An author writes many books; a book is co-authored by many authors. To represent this, the library catalog has a separate index cabinet card (the **junction table**) where every card says: *"Book X is linked to Author Y"*.

---

## ⚙️ Syntax / API / Core Usage

### The Association Pattern (`models/index.js`)
To avoid circular dependency imports when declaring relationships, the standard industry pattern is to write an `associate` method inside each model class, and call them sequentially in a central bootstrapping file (`models/index.js`).

#### Step 1: Model Associate Declaration
```javascript
// src/models/Post.js
const { Model, DataTypes } = require('sequelize');

class Post extends Model {
  // Class method to define relationships
  static associate(models) {
    // A Post belongs to a User
    Post.belongsTo(models.User, { foreignKey: 'userId', as: 'author' });
    
    // A Post has many Comments
    Post.hasMany(models.Comment, { foreignKey: 'postId', as: 'comments' });
  }
}
Post.init({
  title: DataTypes.STRING,
  content: DataTypes.TEXT
}, { sequelize, modelName: 'Post' });
```

#### Step 2: Loader Setup
The index file imports all models, reads their class properties, and runs the `associate` methods:

```javascript
// src/models/index.js
const sequelize = require('../config/database');
const User = require('./User');
const Post = require('./Post');
const Comment = require('./Comment');
const Tag = require('./Tag');

const models = { User, Post, Comment, Tag };

// Run associate methods to link tables
Object.keys(models).forEach(modelName => {
  if (models[modelName].associate) {
    models[modelName].associate(models);
  }
});

models.sequelize = sequelize;

module.exports = models;
```

---

## 💻 Practical Examples

### Writing Migrations for Associated Tables
When creating migrations for related tables, you must ensure the dependent tables (holding the foreign keys) are created **after** their parent tables, and foreign key constraints are declared correctly.

#### User Table Migration (Parent)
```javascript
await queryInterface.createTable('users', {
  id: { type: Sequelize.INTEGER, primaryKey: true, autoIncrement: true }
});
```

#### Post Table Migration (Child - holding `userId` foreign key)
```javascript
// src/migrations/[timestamp]-create-posts-table.js
module.exports = {
  up: async (queryInterface, Sequelize) => {
    await queryInterface.createTable('posts', {
      id: { type: Sequelize.INTEGER, primaryKey: true, autoIncrement: true },
      title: { type: Sequelize.STRING, allowNull: false },
      userId: {
        type: Sequelize.INTEGER,
        allowNull: false,
        // Establish foreign key constraint at database level
        references: {
          model: 'users', // Name of target table in DB
          key: 'id'       // Target column
        },
        onUpdate: 'CASCADE',
        onDelete: 'CASCADE' // If user is deleted, delete all their posts automatically
      }
    });
  },
  down: async (queryInterface) => {
    await queryInterface.dropTable('posts');
  }
};
```

---

## 🔄 Flow Diagram

### Relationship Entity Diagram

```text
  +------------------+                   +--------------------+
  |      users       |                   |      profiles      |
  |  - id (PK)       | 1 <─────────────> |  - id (PK)         |
  |                  |        1          |  - userId (FK)     |
  +--------+---------+                   +--------------------+
           |
           | 1
           |
           | Many
           v
  +------------------+                   +--------------------+
  |      posts       | Many <──────────> |      PostTags      |
  |  - id (PK)       |         PostTags  |  - postId (FK-PK)  |
  |  - userId (FK)   |                   |  - tagId (FK-PK)   |
  +------------------+                   +---------+----------+
                                                   |
                                                   | Many
                                                   |
                                                   v
                                         +--------------------+
                                         |        tags        |
                                         |  - id (PK)         |
                                         |  - name            |
                                         +--------------------+
```

---

## 🧪 Common Interview Questions

### Q1: What is the difference between `hasOne` and `belongsTo`?
* **Answer**: 
  * `hasOne` means the target table holds the foreign key pointer. (e.g., `User.hasOne(Profile)` means the `profiles` table has a `userId` column).
  * `belongsTo` means the source table holds the foreign key pointer. (e.g., `Profile.belongsTo(User)` means the `profiles` table contains the `userId` column).

### Q2: What do the cascade rules `onDelete: 'CASCADE'` and `onUpdate: 'CASCADE'` mean?
* **Answer**: 
  * `onDelete: 'CASCADE'` means that if a row in the parent table (e.g. `users`) is deleted, all matching child records (e.g. `posts` written by that user) will be deleted by the database automatically.
  * `onUpdate: 'CASCADE'` means that if a parent primary key changes (rare), the foreign key columns in all matching child rows will update automatically to maintain the relationship.

### Q3: Why is it important to define associations on BOTH sides of a relationship?
* **Answer**: Defining the association on both models enables bidirectionality. It tells Sequelize how to query relations in both directions. For example, if you only define `User.hasMany(Post)`, you can query a user with their posts, but you cannot query a post and include details about its author because Post doesn't know it belongs to User.

---

## ⚠️ Common Mistakes / Pitfalls
* **Forgetting Foreign Keys in Migrations**: Defining associations in your JS models, but forgetting to write the `references` block in migration scripts. Without the migration configuration, the database server will not enforce foreign key checks, leading to orphaned database rows.
* **Dialect Table Pluralization mismatches**: In migrations, the target model name in `references` refers to the actual SQL table name (usually lowercase and pluralized: e.g. `'users'`). If you write the model class name (`'User'`), the migration will fail on databases like PostgreSQL and MySQL (on Linux servers) because table names are case-sensitive.

---

## ✅ Best Practices
* **Define `as` aliases explicitly**: Use the `as` alias option (e.g. `{ as: 'author' }`) to make queries readable and descriptive.
* **Always specify foreignKey keys**: Do not let Sequelize auto-calculate foreign keys (which results in names like `UserId` or `user_id` depending on defaults). Define it explicitly in association blocks to stay aligned with migration files.

---

## 📝 Quick Recap
* Use `hasOne`/`belongsTo` for 1:1, `hasMany`/`belongsTo` for 1:M, and `belongsToMany` for M:N relations.
* The model defining the `belongsTo` association always contains the foreign key column.
* Many-to-Many relationships require a junction table, configured via the `through` property.
* Declare relationships inside model class `associate` methods, and bootstrap them centrally inside `models/index.js`.

---

## 🔗 Navigation
Previous : [08_validations_constraints_and_hooks.md](./08_validations_constraints_and_hooks.md) | Index : [00_index.md](./00_index.md) | Next : [10_eager_and_lazy_loading.md](./10_eager_and_lazy_loading.md)
