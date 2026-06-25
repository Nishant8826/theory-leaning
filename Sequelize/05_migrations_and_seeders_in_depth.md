# 05. Migrations and Seeders in Depth

## 🎯 Goal of This Chapter
By the end of this chapter, you will understand how to manage your database schema and initial data records professionally. You will learn to use migrations as version control for database schemas, write reversible migration scripts, and seed databases with static or mock data using the Sequelize CLI.

---

## 🤔 Why This Topic Matters
In professional software development, you cannot manually alter production databases or run `sync()` scripts. If you deploy a new version of your application that requires a new database table or an added column, you need a safe, automated way to execute that change.

**Migrations** act as Git commits for database schemas. They allow developers to coordinate schema updates safely, track changes over time, and easily rollback if a deployment fails. **Seeders** complement this by populating databases with default lookup data (like roles) or test mock data automatically.

---

## 🧠 Core Concept

### Database Migrations
A **Migration** is a JavaScript file containing two functions:
1. `up`: Defines the changes to apply to the database (e.g., creating a table, adding a column).
2. `down`: Defines how to undo those exact changes (e.g., dropping a table, deleting a column).

### Database Seeders
A **Seeder** is a script used to populate database tables with initial records. Like migrations, seeders have `up` (to insert data) and `down` (to delete data) methods.

### The `queryInterface` Object
Inside migrations and seeders, you do not use model classes (like `User`). Instead, you use the low-level **`queryInterface`** object provided by Sequelize, which contains helper methods for direct SQL-like schema modifications:
* `queryInterface.createTable()`
* `queryInterface.dropTable()`
* `queryInterface.addColumn()`
* `queryInterface.removeColumn()`
* `queryInterface.bulkInsert()`
* `queryInterface.bulkDelete()`

---

## 🏗 Mental Model / Internal Working

### How Sequelize Tracks Executed Migrations
How does Sequelize know which migration files to execute when you type `npx sequelize-cli db:migrate`?

1. When you run migrations for the first time, Sequelize creates a metadata table in your database called **`SequelizeMeta`**. This table has a single column: `name`.
2. When you execute migrations, Sequelize scans your local `migrations/` folder.
3. It checks the `SequelizeMeta` table to see which migration filenames are already listed there.
4. Sequelize executes the `up` method of **only** the local files that are *not* present in `SequelizeMeta`.
5. Upon successful execution, it inserts the filename into `SequelizeMeta`.
6. When rolling back (`db:migrate:undo`), Sequelize reads the last row in `SequelizeMeta`, runs its `down` function, and deletes that filename row from the table.

---

## 🌍 Real-World Analogy
Think of migrations as **Instruction Sheets** in a Lego manual:
* Step 1: "Add a grey baseboard." (`up` builds the board, `down` removes it).
* Step 2: "Place a red brick on top." (`up` adds the brick, `down` pulls it off).
* If you tell the helper to build (run `db:migrate`), they look at the completed stamps inside their logbook (`SequelizeMeta`) and execute only the steps they haven't finished yet. If they need to take apart the model (run `db:migrate:undo`), they undo the last step they did.

---

## ⚙️ Syntax / API / Core Usage

### Essential CLI Commands

```bash
# 1. Generate a new migration file
npx sequelize-cli migration:generate --name create-users

# 2. Run all pending migrations
npx sequelize-cli db:migrate

# 3. Rollback the most recent migration step
npx sequelize-cli db:migrate:undo

# 4. Rollback all executed migrations
npx sequelize-cli db:migrate:undo:all

# 5. Generate a new seeder file
npx sequelize-cli seed:generate --name default-admin

# 6. Execute all seeders
npx sequelize-cli db:seed:all

# 7. Undo the last seeder operation
npx sequelize-cli db:seed:undo
```

---

## 💻 Practical Examples

### Example 1: Creating a Table Migration
Generate the migration using `npx sequelize-cli migration:generate --name create-users-table`. Open the generated file in `src/migrations/` and edit it:

```javascript
// src/migrations/[timestamp]-create-users-table.js
'use strict';

module.exports = {
  // Executed when running db:migrate
  up: async (queryInterface, Sequelize) => {
    await queryInterface.createTable('users', {
      id: {
        type: Sequelize.INTEGER,
        primaryKey: true,
        autoIncrement: true,
        allowNull: false
      },
      username: {
        type: Sequelize.STRING(50),
        allowNull: false,
        unique: true
      },
      email: {
        type: Sequelize.STRING,
        allowNull: false,
        unique: true
      },
      createdAt: {
        type: Sequelize.DATE,
        allowNull: false,
        defaultValue: Sequelize.literal('CURRENT_TIMESTAMP')
      },
      updatedAt: {
        type: Sequelize.DATE,
        allowNull: false,
        defaultValue: Sequelize.literal('CURRENT_TIMESTAMP')
      }
    });
  },

  // Executed when running db:migrate:undo
  down: async (queryInterface, Sequelize) => {
    await queryInterface.dropTable('users');
  }
};
```

### Example 2: Modifying an Existing Table (Adding a Column)
If you need to add a column in the future, **do not edit the original migration**. Create a new one:
`npx sequelize-cli migration:generate --name add-role-to-users`

```javascript
// src/migrations/[timestamp]-add-role-to-users.js
'use strict';

module.exports = {
  up: async (queryInterface, Sequelize) => {
    await queryInterface.addColumn('users', 'role', {
      type: Sequelize.STRING(20),
      defaultValue: 'user',
      allowNull: false
    });
  },

  down: async (queryInterface, Sequelize) => {
    await queryInterface.removeColumn('users', 'role');
  }
};
```

### Example 3: Writing a Seeder File
Generate the seeder using `npx sequelize-cli seed:generate --name demo-users`.

```javascript
// src/seeders/[timestamp]-demo-users.js
'use strict';

module.exports = {
  up: async (queryInterface, Sequelize) => {
    await queryInterface.bulkInsert('users', [
      {
        username: 'alice_dev',
        email: 'alice@example.com',
        role: 'admin',
        createdAt: new Date(),
        updatedAt: new Date()
      },
      {
        username: 'bob_user',
        email: 'bob@example.com',
        role: 'user',
        createdAt: new Date(),
        updatedAt: new Date()
      }
    ], {});
  },

  down: async (queryInterface, Sequelize) => {
    // Delete all records from users table where email matches our seeds
    await queryInterface.bulkDelete('users', {
      email: ['alice@example.com', 'bob@example.com']
    }, {});
  }
};
```

---

## 🔄 Flow Diagram

### Migration Verification Flow

```text
               User runs: db:migrate
                         │
                         ▼
             Create SequelizeMeta table 
                  if not exists
                         │
                         ▼
             Scan migrations/ directory 
             & read file names
                         │
                         ▼
             Compare list with names in
               SequelizeMeta table
                         │
                         ▼
            Are there local files not
              listed in database?
               /              \
             NO               YES
             /                  \
            v                    v
      Database is up-to-date   For each pending file (in order):
                               1. Run the up() method
                               2. Save filename to SequelizeMeta
```

---

## 🧪 Common Interview Questions

### Q1: What is the `SequelizeMeta` table and what is its role?
* **Answer**: `SequelizeMeta` is a metadata table managed by Sequelize. It stores the filenames of all migrations that have been successfully run. Sequelize reads this table to ensure it only runs new migration scripts, preventing previously run migrations from executing again and corrupting existing data.

### Q2: Why must you write a `down` method in every migration?
* **Answer**: The `down` method is the escape hatch. If a deployment fails or a database change causes problems in production, you must be able to safely rollback the database schema. Without a `down` method, you cannot run `db:migrate:undo`, leaving your database in a broken state that is difficult to restore.

### Q3: Should models and migrations match?
* **Answer**: Yes. The current state of your code's Model files (`User.js`) must mirror the current state of the database schemas generated by your compiled migrations list. If they do not match, Sequelize models will query fields that do not exist, resulting in runtime SQL syntax errors.

---

## ⚠️ Common Mistakes / Pitfalls
* **Editing Committed Migration Files**: Once a migration file has run in any environment (dev, staging, prod), **never edit it**. The filename is stored in `SequelizeMeta` on other servers, meaning Sequelize will bypass your modifications on those servers, creating schema inconsistencies.
* **Forgetting `await` inside `up`/`down` methods**: If you omit `await` or fail to return promise statements, Sequelize CLI completes the execution process before the database finishes running the SQL query, leading to incomplete schemas or random database lock failures.

---

## ✅ Best Practices
* **Migrations must be immutable**: If you make a mistake in a migration, write a brand new migration to fix it (e.g. `modify-column-x`) rather than changing a historical migration file.
* **Keep migrations small**: Each migration file should focus on one task (e.g., creating one table or modifying a set of related columns). This makes debugging, reviews, and rollbacks clean and simple.

---

## 📝 Quick Recap
* Migrations are version control for database schemas, executing step-by-step updates.
* Every migration needs an `up` method (to apply changes) and a `down` method (to rollback changes).
* The `SequelizeMeta` table tracks which migration files have already been run.
* Seeders populate database tables with lookup, static, or mockup records.

---

## 🔗 Navigation
Previous : [04_models_definition_and_synchronization.md](./04_models_definition_and_synchronization.md) | Index : [00_index.md](./00_index.md) | Next : [06_basic_crud_operations.md](./06_basic_crud_operations.md)
