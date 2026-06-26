# 🧩 Sequelize + Node.js + Express – Complete Revision Guide

Welcome to the ultimate Sequelize ORM master revision guide. This file serves as a comprehensive, high-density study hub compiling the core architectural models, essential commands, code syntaxes, best practices, and interview-ready concepts covered across all chapters of this course. By expanding the key concepts in detail, this guide serves as a fully self-contained reference sheet, allowing you to revise the entire database module quickly without opening the individual lesson files.

---

## 📌 Module Navigation

* [01. Introduction to ORM and Sequelize](#01-introduction-to-orm-and-sequelize)
* [02. Sequelize Architecture and Mental Model](#02-sequelize-architecture-and-mental-model)
* [03. Project Setup and Configuration](#03-project-setup-and-configuration)
* [04. Model Definition and Synchronization](#04-model-definition-and-synchronization)
* [05. Migrations and Seeders in Depth](#05-migrations-and-seeders-in-depth)
* [06. Basic CRUD Operations](#06-basic-crud-operations)
* [07. Advanced Querying, Filtering, and Operators](#07-advanced-querying-filtering-and-operators)
* [08. Validations, Constraints, and Hooks](#08-validations-constraints-and-hooks)
* [09. Associations and Relationships](#09-associations-and-relationships)
* [10. Eager and Lazy Loading](#10-eager-and-lazy-loading)
* [11. Transactions in Depth](#11-transactions-in-depth)
* [12. Paranoid Tables and Scopes](#12-paranoid-tables-and-scopes)
* [13. Model Methods and Advanced Patterns](#13-model-methods-and-advanced-patterns)
* [14. Error Handling and Production Practices](#14-error-handling-and-production-practices)
* [15. Common Mistakes and Interview Prep](#15-common-mistakes-and-interview-prep)

---

## 01. Introduction to ORM and Sequelize

🔗 **Full Lesson:** [01_introduction_to_orm_and_sequelize.md](./01_introduction_to_orm_and_sequelize.md)

* **Why It Exists**: Eliminates raw SQL string boilerplate, handles database-specific dialects automatically, and protects applications from SQL injection using parameterization.
* **Key Concepts**:
  * **Tabular-Object Mapping**: Maps database tables to JavaScript classes (Models), table rows to class instances, and columns to object properties.
  * **Active Record Pattern**: Model instances represent data rows and carry database operations (like `.save()` or `.destroy()`), coupling schema representation with persistence methods.
  * **Dynamic SQL Generation**: Calls like `User.findAll()` compile into parameterized SQL in the background. User values are separated from query syntax automatically to prevent SQL Injection.
  * **Object Hydration**: The process of translating raw, flat SQL database arrays into rich JavaScript model objects decorated with instance helper methods.
  * **ORM vs. Query Builder vs. Driver**: Drivers (e.g., `mysql2`) send raw SQL. Query Builders (e.g., `Knex.js`) programmatically build SQL strings but return flat JSON. ORMs provide validation, hooks, associations, and mapping.
  * **Dialect Agnosticism**: Abstracts the underlying database dialect. The developer writes the same JavaScript code, and Sequelize compiles it to the correct SQL grammar of the connected database.

### Key Commands / Code Example:
```javascript
// Plain SQL comparison using mysql2 raw driver vs. Sequelize ORM
// Raw mysql2:
const [rows] = await connection.execute('SELECT id, name FROM users WHERE id = ?', [1]);
const rawUser = rows[0];

// Sequelize ORM:
const user = await User.findByPk(1, { attributes: ['id', 'name'] }); // returns rich class instance
```

> [!IMPORTANT]
> Do not treat the ORM as magic. You must still understand SQL to prevent generating slow or multiple queries in the background.

---

## 02. Sequelize Architecture and Mental Model

🔗 **Full Lesson:** [02_sequelize_architecture_and_mental_model.md](./02_sequelize_architecture_and_mental_model.md)

* **Why It Exists**: Manages connection resources efficiently and defines the interface pattern (Active Record) used to interact with database records.
* **Key Concepts**:
  * **Sequelize Layers**: User API (Models) ➡️ Query Generator (compiler) ➡️ Connection Pool (socket manager) ➡️ Dialect Adapter (translator) ➡️ Database.
  * **Query Execution Lifecycle**: Model schema validation checks ➡️ SQL string compilation ➡️ Leasing a socket connection from the pool ➡️ Execution on database ➡️ Deserializing raw row outputs to class instances.
  * **Connection Pooling**: Keeps a set of open socket connections to avoid network handshakes (TCP/SSL) for each query.
    * `max`: Max concurrent connections allowed.
    * `min`: Min idle connections maintained in the pool.
    * `acquire`: Max milliseconds to wait for an available socket before throwing a connection error.
    * `idle`: Max milliseconds a connection can sit idle before being closed.
  * **Dialects**: Translation adapters (e.g., `mysql`, `postgres`, `sqlite`) that compile standard Sequelize functions into database-specific SQL dialects.
  * **Singleton Pattern**: Reusing a single `new Sequelize()` instance across the entire application to prevent running out of database connections.

### Key Commands / Code Example:
```javascript
// Configuring connection pools during Sequelize initialization
const sequelize = new Sequelize('db', 'user', 'pass', {
  host: 'localhost',
  dialect: 'mysql',
  pool: { 
    max: 10,       // Max connections in pool
    min: 2,        // Min idle connections
    acquire: 30000, // Connection wait timeout
    idle: 10000    // Idle socket timeout
  }
});
```

> [!IMPORTANT]
> Always export a single, shared Sequelize instance from your config folder to avoid leaking connection sockets under server loads.

---

## 03. Project Setup and Configuration

🔗 **Full Lesson:** [03_project_setup_and_configuration.md](./03_project_setup_and_configuration.md)

* **Why It Exists**: Establishes directory organization and configures environments (development, testing, production) securely using environmental variables.
* **Key Concepts**:
  * **Environment Isolation**: Storing configurations in `.env` and loading them via `dotenv` dynamically based on `NODE_ENV`.
  * **Dialect Drivers**: The core `sequelize` library needs a separate driver (e.g., `mysql2`) to communicate with the database over socket connections.
  * **CLI Path Customization**: Using `.sequelizerc` to map CLI target folders (`migrations`, `seeders`, `models`) into the standard `src/` directory.
  * **Database Validation**: Running `sequelize.authenticate()` at app startup to confirm that the database credentials are valid and the server is reachable.
  * **Dynamic JavaScript Config**: Using a `.js` database configuration file instead of a static `.json` configuration file, allowing environment variables to be loaded dynamically.

### Key Commands / Code Example:
```bash
# 1. Install dependencies
npm install sequelize mysql2 dotenv
# 2. Run Sequelize CLI setup in your project
npx sequelize-cli init
# 3. Verify database connection in code
await sequelize.authenticate();
```

> [!IMPORTANT]
> Never commit your local `.env` file to version control. Commit an `.env.example` file instead.

---

## 04. Model Definition and Synchronization

🔗 **Full Lesson:** [04_models_definition_and_synchronization.md](./04_models_definition_and_synchronization.md)

* **Why It Exists**: Maps JavaScript class structures to physical tables, manages column types, and initializes base tables.
* **Key Concepts**:
  * **Class Syntax (Modern)**: Models inherit from the `Model` superclass and are initialized using the `init(attributes, options)` static method.
  * **Attribute DataTypes Mapping**: Mapping JS primitives to specific database types, such as `DataTypes.STRING`, `DataTypes.INTEGER`, `DataTypes.ENUM`, `DataTypes.UUID`, and `DataTypes.JSON`.
  * **Common Constraints**: Enforcing rules at the schema level: `allowNull: false`, `unique: true`, `defaultValue`, and `primaryKey`.
  * **Synchronization Modes**:
    * `sync()`: Creates the table if it does not exist.
    * `sync({ force: true })`: Runs destructive `DROP TABLE IF EXISTS` and recreates the tables.
    * `sync({ alter: true })`: Reads current columns and runs `ALTER TABLE` statements to match models.
  * **Model Configuration Keys**: Configuring parameters like `tableName`, `underscored` (camelCase to snake_case column mapping), and `timestamps`.

### Key Commands / Code Example:
```javascript
// Modern model definition setup
class Product extends Model {}
Product.init({
  name: { type: DataTypes.STRING, allowNull: false, unique: true },
  price: { type: DataTypes.DECIMAL(10, 2), defaultValue: 0.00 }
}, { 
  sequelize, 
  modelName: 'Product', 
  tableName: 'products' 
});
```

> [!IMPORTANT]
> Never use `sync({ force: true })` or `sync({ alter: true })` in production. They can cause catastrophic data loss or database locks. Use migrations instead.

---

## 05. Migrations and Seeders in Depth

🔗 **Full Lesson:** [05_migrations_and_seeders_in_depth.md](./05_migrations_and_seeders_in_depth.md)

* **Why It Exists**: Enforces Git-like version control on databases, enabling trackable schema updates and populating datasets.
* **Key Concepts**:
  * **`SequelizeMeta`**: A metadata table automatically managed in the database to record the filenames of all executed migrations to prevent duplicates.
  * **Reversibility**: Every migration needs an `up` function (applies change) and a `down` function (reverts change) using the low-level `queryInterface` object.
  * **QueryInterface Methods**: Used instead of models: `createTable`, `dropTable`, `addColumn`, `removeColumn`, `bulkInsert`, `bulkDelete`.
  * **Seeders**: Scripts to populate the database with default lookup values (e.g. roles, settings) or mock data.
  * **Immutable Migration Rule**: Already executed migration files must never be edited; schema changes must be applied via a new migration file.
  * **Awaiting Promises**: In async migrations, every query Interface command must be awaited to prevent the CLI runner from completing before the database finishes writing.

### Key Commands / Code Example:
```bash
# Generate a migration file
npx sequelize-cli migration:generate --name add-role-to-users
# Execute all pending migrations
npx sequelize-cli db:migrate
# Rollback the last migration
npx sequelize-cli db:migrate:undo
```

> [!IMPORTANT]
> Migrations are immutable. Once a migration script has been run on a database, never edit it. Write a new migration file to apply changes.

---

## 06. Basic CRUD Operations

🔗 **Full Lesson:** [06_basic_crud_operations.md](./06_basic_crud_operations.md)

* **Why It Exists**: Performs standard database interactions (Create, Read, Update, Delete) inside API routes.
* **Key Concepts**:
  * **Class vs. Instance Methods**:
    * **Class Methods** (`Model.create`, `Model.findAll`, `Model.update`): Call directly on the class. `update` and `destroy` are bulk operations.
    * **Instance Methods** (`instance.save`, `instance.destroy`, `instance.update`): Call on a retrieved row object.
  * **Object Hydration Bypass**: Passing `{ raw: true }` skips model instance creation, returning plain JSON. This uses less memory for read-only listings.
  * **Update Query Counts**: Hydrated updates (fetch ➡️ edit ➡️ `.save()`) take **2 queries** (1 SELECT + 1 UPDATE) but run validations and hooks. Direct updates (`Model.update()`) take **1 query** (1 UPDATE) but bypass hooks.
  * **API Return Values**: `findAll()` returns an array (always truthy, check `.length === 0`). `findOne()` and `findByPk()` return `null` on a query miss. `update()` and `destroy()` return stats (affected rows count).

### Key Commands / Code Example:
```javascript
// 1. Direct 1-query update (fast, bypasses hooks)
await User.update({ isActive: false }, { where: { role: 'guest' } });

// 2. Hydrated 2-query update (slow, triggers hooks and validations)
const user = await User.findByPk(1);
if (user) {
  user.email = 'new@email.com';
  await user.save();
}
```

> [!IMPORTANT]
> `Model.findAll()` always returns an array. If no matches are found, it returns `[]` (which is truthy), not `null`. Check `results.length === 0` to confirm it is empty.

---

## 07. Advanced Querying, Filtering, and Operators

🔗 **Full Lesson:** [07_advanced_querying_filtering_and_operators.md](./07_advanced_querying_filtering_and_operators.md)

* **Why It Exists**: Restricts, sorts, filters, and paginates datasets at the database level to optimize network payloads.
* **Key Concepts**:
  * **Projection (Attributes)**: Restricting retrieved columns to minimize bandwidth and exclude sensitive fields: `{ attributes: { exclude: ['password'] } }`.
  * **Query Operators (`Op`)**: Importing the `Op` object to perform complex operations (e.g. `[Op.or]`, `[Op.between]`, `[Op.like]`, `[Op.in]`).
  * **Case Sensitivity in Search**: `Op.like` is case-insensitive in MySQL by default due to default table collation settings. MySQL does not support `Op.iLike` (which is Postgres-only).
  * **Offset Pagination**: Utilizing `limit` (max records to return) and `offset` (records to skip) inside `Model.findAndCountAll()` to build paginated APIs.
  * **Complex Logical Nesting**: Combining multiple conditional arrays using `[Op.and]` and `[Op.or]` to construct complex, nested logical boolean checks.
  * **Sorting Syntax**: Sorting rows using the nested array formatting syntax: `order: [['columnName', 'ASC']]`.

### Key Commands / Code Example:
```javascript
const { Op } = require('sequelize');
const { count, rows } = await Product.findAndCountAll({
  where: {
    price: { [Op.between]: [10, 50] },
    name: { [Op.like]: '%Laptop%' }
  },
  order: [['price', 'ASC']],
  limit: 10,
  offset: 0
});
```

> [!IMPORTANT]
> Always validate and cap pagination limit inputs (e.g., `Math.min(limit, 100)`) to prevent client requests from crashing server memory.

---

## 08. Validations, Constraints, and Hooks

🔗 **Full Lesson:** [08_validations_constraints_and_hooks.md](./08_validations_constraints_and_hooks.md)

* **Why It Exists**: Guarantees data validation before writing to disk and automates recurring tasks (such as password hashing).
* **Key Concepts**:
  * **Model-Level Validations (JS)**: Checked in Node.js memory *before* compiling queries. Fails early without hitting the database (e.g. `isEmail: true`).
  * **Database-Level Constraints (DB)**: Hard limits enforced by the database engine (e.g. `allowNull: false`, `unique: true`).
  * **Custom Validators**: Asynchronous or synchronous custom validation methods defined on field configurations.
  * **Lifecycle Hooks**: Automatic event triggers: `beforeValidate` ➡️ **VALIDATE** ➡️ `afterValidate` ➡️ `beforeSave` ➡️ **SQL WRITE** ➡️ `afterSave`.
  * **Bulk operations & Hooks**: Bulk writes bypass individual instance hooks by default unless `{ individualHooks: true }` is enabled.
  * **Changed Attribute Checks**: Using `instance.changed('fieldName')` inside hooks to run actions only if specific attributes were modified (e.g. hashing a password only when the password field is updated).

### Key Commands / Code Example:
```javascript
// Model configuration with validation rules and hooks
User.init({
  email: { type: DataTypes.STRING, validate: { isEmail: true } }
}, {
  sequelize,
  hooks: {
    beforeSave: async (user) => {
      if (user.changed('password')) {
        user.password = await bcrypt.hash(user.password, 10);
      }
    }
  }
});
```

> [!IMPORTANT]
> Asynchronous hooks must use `async/await` or return a promise. If not, Sequelize will execute queries before the hook finishes (e.g. saving a plain-text password before hashing completes).

---

## 09. Associations and Relationships

🔗 **Full Lesson:** [09_associations_and_relationships.md](./09_associations_and_relationships.md)

* **Why It Exists**: Models relational links (1:1, 1:M, M:N) between tables, ensuring integrity using Foreign Keys.
* **Key Concepts**:
  * **Association Types**:
    * **One-to-One**: `hasOne` / `belongsTo` (Foreign key in target table).
    * **One-to-Many**: `hasMany` / `belongsTo` (Foreign key in child table).
    * **Many-to-Many**: `belongsToMany` through a junction table.
  * **Foreign Key Location**: The model calling **`belongsTo`** always holds the foreign key column.
  * **Referential Integrity**: Declaring `references` and cascade rules (`onDelete: 'CASCADE'`) in migration files to prevent orphaned database records.
  * **Bootstrap Loader**: Declaring `associate(models)` methods on model classes and initializing them centrally in `models/index.js` to avoid import loops.
  * **Cascade Rules**: Setting database action handlers like `onDelete: 'CASCADE'` and `onUpdate: 'CASCADE'` to keep dependent child rows synced.
  * **Custom Aliases**: Using the `as` property to name association keys in query results (e.g. including posts `as: 'articles'`).

### Key Commands / Code Example:
```javascript
// User has many Posts (Post table will hold 'userId')
User.hasMany(Post, { foreignKey: 'userId', as: 'posts' });
Post.belongsTo(User, { foreignKey: 'userId', as: 'author' });

// Many-to-Many: Post has many Tags through PostTags junction table
Post.belongsToMany(Tag, { through: 'PostTags', foreignKey: 'postId' });
Tag.belongsToMany(Post, { through: 'PostTags', foreignKey: 'tagId' });
```

> [!IMPORTANT]
> Always define foreign key parameters explicitly in both models to prevent Sequelize from generating duplicate key columns.

---

## 10. Eager and Lazy Loading

🔗 **Full Lesson:** [10_eager_and_lazy_loading.md](./10_eager_and_lazy_loading.md)

* **Why It Exists**: Controls when and how associated tables are queried to optimize database performance.
* **Key Concepts**:
  * **Lazy Loading**: Fetches the parent first, then calls generated getter methods (e.g. `await user.getPosts()`) to run subqueries later.
  * **Eager Loading**: Fetches parent and children together in 1 SQL query using `include` (combines tables using SQL `JOIN` statements).
  * **The N+1 Query Problem**: Triggering lazy loading queries inside loops, resulting in 1 parent query + N individual child queries.
  * **Nested Includes**: Joining multiple levels (e.g. User ➡️ Posts ➡️ Comments).
  * **Required Join Filter**: Setting `required: true` converts the default `LEFT OUTER JOIN` into an `INNER JOIN`, filtering out parent records that do not contain matching children.
  * **Eager Loading Hydration Bypass**: Combining `raw: true` and `nest: true` options to retrieve nested arrays as plain JavaScript objects.
  * **Association Queries**: Running filters directly inside includes using `where` keys.

### Key Commands / Code Example:
```javascript
// Eager loading with alias projection (fixes N+1 problem)
const users = await User.findAll({
  include: [{
    model: Post,
    as: 'posts',
    attributes: ['id', 'title'] // Fetch only necessary columns
  }]
});
```

> [!IMPORTANT]
> Eagerly load fields using explicit projections (`attributes`) to avoid fetching unused heavy text fields over the network.

---

## 11. Transactions in Depth

🔗 **Full Lesson:** [11_transactions_in_depth.md](./11_transactions_in_depth.md)

* **Why It Exists**: Enforces atomic writes across multiple tables so they either succeed together or roll back together during failures.
* **Key Concepts**:
  * **ACID Compliance**: Enforcing Atomicity (all or nothing), Consistency, Isolation (hidden modifications), and Durability (permanence on disk).
  * **Managed Transactions (Recommended)**: Pass a callback to `sequelize.transaction()`. Commits and rollbacks are handled automatically based on execution success.
  * **Unmanaged Transactions**: Manual execution control requiring developers to call `t.commit()` and `t.rollback()`.
  * **Pessimistic Concurrency Control**: Using row locks (`lock: transaction.LOCK.UPDATE`) to queue concurrent write requests on the same row, preventing double-spending race conditions.
  * **Transaction Scope Leaks**: Leaving out `{ transaction: t }` in one of the nested queries, causing that query to run outside the transaction.
  * **Side Effects Guard**: Executing non-database tasks (like stripe charges or email dispatch APIs) only *after* transactions successfully commit.

### Key Commands / Code Example:
```javascript
// Managed transaction implementation
await sequelize.transaction(async (t) => {
  // Pass transaction object to ALL queries in the block
  const user = await User.create({ username: 'bob' }, { transaction: t });
  await Profile.create({ userId: user.id, bio: 'Dev' }, { transaction: t });
});
```

> [!IMPORTANT]
> If you forget to pass `{ transaction: t }` to any query inside the transaction callback, it runs on a separate connection outside the transaction, bypasses rollbacks, and can lock the database.

---

## 12. Paranoid Tables and Scopes

🔗 **Full Lesson:** [12_paranoid_tables_and_scopes.md](./12_paranoid_tables_and_scopes.md)

* **Why It Exists**: Prevents destructive data loss using soft deletes, and packages reusable query parameters inside models.
* **Key Concepts**:
  * **Paranoid Tables (Soft Delete)**: `destroy()` updates a `deletedAt` column instead of deleting the row. Active queries automatically filter out soft-deleted records (`WHERE deletedAt IS NULL`).
  * **Hard Deletes**: Bypassing soft deletes using the `{ force: true }` option.
  * **Default Scopes**: Query configurations merged into **every** query run on that model. Bypassed using `.unscoped()`.
  * **Named Scopes**: Reusable query rules called programmatically via `.scope('scopeName')`.
  * **Restoring Rows**: Re-enabling soft-deleted records in code by calling `.restore()` on the model instance.
  * **Scope Chaining**: Applying multiple scopes sequentially using array lists, e.g. `User.scope(['active', 'recent']).findAll()`.

### Key Commands / Code Example:
```javascript
// Model options setup:
timestamps: true,
paranoid: true, // Enables soft delete
defaultScope: { where: { status: 'published' } },
scopes: { popular: { where: { views: { [Op.gt]: 1000 } } } }

// Querying using scopes and bypassing soft deletes:
const activePopular = await Post.scope('popular').findAll({ paranoid: false });
```

> [!IMPORTANT]
> Keep `defaultScope` rules simple. Complicated default scopes can cause unexpected issues during update and delete operations.

---

## 13. Model Methods and Advanced Patterns

🔗 **Full Lesson:** [13_model_methods_and_advanced_patterns.md](./13_model_methods_and_advanced_patterns.md)

* **Why It Exists**: Encapsulates data logic within models and decouples queries from HTTP routes in enterprise applications.
* **Key Concepts**:
  * **Instance Methods**: Defined on the class prototype. They have access to `this` (the row values). Useful for actions like checking passwords (`bcrypt.compare`).
  * **Class Methods**: Static methods defined on the model class. Useful for custom query shortcuts.
  * **`toJSON()` Override**: Automatically invoked by Express serialization (`res.json()`). Overriding it lets you strip sensitive fields (like passwords) from all API outputs.
  * **Service/Repository Layers**: Decoupling code logic: Route ➡️ Controller (HTTP handling) ➡️ Service (business logic) ➡️ Repository (database queries) ➡️ Model.
  * **Arrow Function Gotcha**: Using arrow functions `() => {}` inside model definitions breaks `this` context binding, making it impossible to access object variables.
  * **Architecture Boundaries**: Keep Services free of HTTP objects (`req`, `res`) and Repositories free of business logic.

### Key Commands / Code Example:
```javascript
class User extends Model {
  // 1. Instance method (Accesses 'this' row values)
  async comparePassword(password) { return await bcrypt.compare(password, this.password); }
  
  // 2. toJSON override (Strip passwords from responses)
  toJSON() {
    const values = { ...this.get() };
    delete values.password;
    return values;
  }
}
```

> [!IMPORTANT]
> Never use arrow functions when defining model methods, as they do not bind the instance context `this`.

---

## 14. Error Handling and Production Practices

🔗 **Full Lesson:** [14_error_handling_and_production_practices.md](./14_error_handling_and_production_practices.md)

* **Why It Exists**: Gracefully maps database errors into secure, user-friendly JSON responses, and optimizes production database queries.
* **Key Concepts**:
  * **SequelizeBaseError**: The root class of all database exceptions.
  * **ValidationError mapping**: Catching validation and unique constraint failures to return clean field messages to the client instead of raw SQL dump logs.
  * **Database Indexing**: Explicitly indexing foreign keys and columns used in `WHERE`, `ORDER BY`, or `JOIN` statements in migration files to optimize query speed.
  * **Environment Logging**: Disabling SQL terminal logging in production configs to secure data and improve performance.
  * **Centralized Express Error pipeline**: Error handling middlewares must be placed at the very bottom of the Express app routing definition list.
  * **Connection Pool Tuning**: Preventing acquire timeouts during traffic peaks by increasing `max` pool count.

### Key Commands / Code Example:
```javascript
// Central Express error handling middleware check
if (err instanceof ValidationError) {
  const errors = err.errors.map(e => ({ field: e.path, message: e.message }));
  return res.status(400).json({ error: 'ValidationError', details: errors });
}
```

> [!IMPORTANT]
> Databases do not automatically index foreign keys. You must explicitly add indexes in migration scripts to maintain query performance under loads.

---

## 15. Common Mistakes and Interview Prep

🔗 **Full Lesson:** [15_common_mistakes_and_interview_prep.md](./15_common_mistakes_and_interview_prep.md)

* **Why It Exists**: Resolves production anti-patterns, covers senior-level scenarios, and structures large MVC codebases.
* **Key Concepts**:
  * **SQL Injection Prevention**: Using replacements or bind variables in raw queries instead of string concatenation.
  * **Bulk Query Speed Tuning**: Passing `{ validate: false, hooks: false }` inside `bulkCreate` to bypass validators and hooks, accelerating bulk updates.
  * **Replication Configurations**: Splitting database queries automatically: routing writes (`create`, `update`) to a master database, and reads (`findAll`) to database replica servers.
  * **Cross-Environment Drifts**: Ensuring matching local and production database engines (e.g. avoiding SQLite in development if production is MySQL, because table casing and constraints behave differently).
  * **Pessimistic vs. Optimistic Locking**: Optimistic locks use a version column to prevent concurrent overwrites. Pessimistic locks (`LOCK.UPDATE`) block row edits at the database level.
  * **Cursor-based Pagination**: Bypassing offset page drift bottlenecks by querying items greater than a specific ID cursor.

### Key Commands / Code Example:
```javascript
// Safe parameterization of raw SQL queries
await sequelize.query(
  'SELECT * FROM users WHERE email = :userEmail',
  { 
    replacements: { userEmail: req.query.email }, 
    type: QueryTypes.SELECT 
  }
);
```

> [!IMPORTANT]
> Perform external side effects (like sending emails or charging cards) after transactions commit, never inside transaction blocks.

---

## 🚀 30-Minute Quick Revision Section

### 1. Sequelize Mental Model in 10 Bullets
1. **Model Registration**: Model classes define schemas in-memory but do not touch the database until synced or migrated.
2. **Dynamic Compilation**: The Query Generator translates JS arrays and filters into parameterized raw SQL queries.
3. **Dialect Routing**: Dialect engines (adapters) format SQL statements to match target databases (MySQL, Postgres, SQLite).
4. **Connection Pooling**: Connections are leased from a shared pool to run queries and returned immediately.
5. **Database constraints**: Constraints (Not Null, Unique) are checked by the database engine during query runs.
6. **Hydration**: Raw rows returned from the database are wrapped (hydrated) into Sequelize instances.
7. **Active Record**: Hydrated objects hold operational methods like `.save()` and `.destroy()` pointing to their own DB keys.
8. **Validations run in JS**: Model validations evaluate conditions in Node memory, stopping before queries hit networks.
9. **Hooks act as Triggers**: Callbacks hook into lifecycle events, enabling operations like hashing passwords.
10. **JSON Serialization**: `res.json()` calls the `toJSON()` override to strip sensitive fields before sending responses.

---

### 2. Most Important Commands / APIs to Remember

#### CLI Operations
* `npx sequelize-cli init` - Initialize project setup.
* `npx sequelize-cli migration:generate --name add-column` - Create migration template.
* `npx sequelize-cli db:migrate` - Execute pending database changes.
* `npx sequelize-cli db:migrate:undo` - Revert the latest database migration step.
* `npx sequelize-cli seed:generate --name demo-data` - Create a new seeder.
* `npx sequelize-cli db:seed:all` - Run all seeders.

#### Key Query APIs
* `Model.create({ data })` - Insert record.
* `Model.findAll({ where: { key: value } })` - Query multiple matching records.
* `Model.findByPk(primaryKey)` - Query one record by ID.
* `Model.findOne({ where: { email } })` - Query first matching record.
* `Model.findAndCountAll({ limit, offset })` - Query paginated rows and total count.
* `Model.update({ fields }, { where })` - Bulk update.
* `instance.save()` - Update fetched instance attributes.
* `instance.destroy()` - Delete record (soft delete if paranoid is enabled).
* `instance.restore()` - Recover soft-deleted paranoid row.

#### Association and Transaction APIs
* `User.hasMany(Post, { foreignKey: 'userId' })` - Define 1:M.
* `Post.belongsTo(User, { foreignKey: 'userId' })` - Complete 1:M link.
* `sequelize.transaction(async (t) => { ... })` - Start a managed database transaction.

---

### 3. Most Important Interview Concepts

#### sync vs alter vs migrations
* `sync({ force: true })` drops tables before recreating them. Never run in production.
* `sync({ alter: true })` modifies columns dynamically, which can fail if current data violates new rules.
* **Migrations** are version-controlled, step-by-step schema modifications. They are the only production-safe choice.

#### Model vs Migration
* Models represent the schema inside JavaScript memory for query generation.
* Migrations represent the physical schema changes in the database. They must match to avoid syntax errors.

#### Hooks and Validations
* Validations run in JS memory first. Hooks run at lifecycle events (before/after validate, save, create).
* Bulk operations bypass hooks by default unless `{ individualHooks: true }` is enabled.

#### Associations and Eager Loading
* `belongsTo` maps the foreign key on the source table.
* Eager loading uses `include` to run JOIN queries. Lazy loading runs subqueries later, causing N+1 loop issues.

#### Transactions
* Enforce ACID properties across operations.
* Always pass `{ transaction: t }` to queries inside transaction blocks.

#### Paranoid Tables
* Implement soft deletes, setting a `deletedAt` field instead of deleting rows. Bypassed with `paranoid: false`.

#### Scopes
* Package reusable queries. Default scopes run automatically; named scopes run via `.scope()`.

#### Performance and N+1 Queries
* Resolve N+1 queries by using eager loading JOINs.
* Use `{ raw: true }` to skip hydration for read-only listings.
* Add indexes to foreign keys and columns used in WHERE filters or ORDER sorting.

---

### 4. Common Mistakes to Avoid
1. **Syncing in Production**: Running `sequelize.sync({ force: true })` in live environments, deleting customer data.
2. **Connection Spikes**: Initializing multiple Sequelize instances instead of sharing a single instance, exhausting database connections.
3. **Lazy Loading in Loops**: Querying relations inside loops, triggering N+1 query performance issues.
4. **Missing Transactions**: Executing dependent write queries without using transactions, leaving databases in inconsistent states.
5. **No Indexes on Foreign Keys**: Forgetting to add indexes to foreign key columns, causing queries to slow down over time.
6. **Leaking Stack Traces**: Returning raw database error stacks to clients, exposing system details to security threats.
7. **Modifying Ran Migrations**: Editing old migrations instead of generating a new one to apply schema updates.

---

### 5. Recommended Learning Order for Revision
1. **Architecture Basics**: Study the Active Record pattern, connection pool configuration, and query execution lifecycle.
2. **Models & Setup**: Review model definition, data types, and model synchronization rules.
3. **Migrations**: Master creating, running, and undoing migrations and seeders using the CLI.
4. **CRUD & Operators**: Memorize the core query methods and operator symbols.
5. **Associations & Performance**: Study table relationships, eager vs lazy loading, and solving N+1 query loops.
6. **Transactions**: Practice managed transactions, passing transaction objects, and row locking.
7. **Error Handling & Production**: Study mapping validation errors in middleware, indexing foreign keys, and disabling query logs.

---

Previous : [00_index.md](./00_index.md) | Index : [00_index.md](./00_index.md) | Next : [01_introduction_to_orm_and_sequelize.md](./01_introduction_to_orm_and_sequelize.md)
