# 03. Project Setup and Configuration

## 🎯 Goal of This Chapter
By the end of this chapter, you will know how to initialize a Node.js and Express application, install Sequelize along with database dialect drivers, set up environment-based configurations using environment variables, and initialize the Sequelize Command Line Interface (CLI).

---

## 🤔 Why This Topic Matters
A messy database setup is a major source of production bugs. Issues like exposed database passwords in Git repositories, mismatched settings between developer machines and production servers, or missing drivers can crash deployments. Setting up a clean, structured project with environment-based configurations is the foundation of any production-ready application.

---

## 🧠 Core Concept
To use Sequelize, your project needs three parts:
1. **Sequelize Core**: The main ORM package (`sequelize`).
2. **Database Dialect Driver**: Low-level database connector library (e.g. `mysql2` for MySQL, `pg` for PostgreSQL) that Sequelize uses under the hood to send raw commands.
3. **Sequelize CLI**: A developer command line tool used to generate boilerplate files for models, migrations, and seeders.

Instead of writing static configuration files like `config.json` (which doesn't support reading environment variables out-of-the-box), modern backend applications use a dynamic JavaScript configuration file (like `config.js` or `database.js`) that reads values from `.env`.

---

## 🏗 Mental Model / Internal Working

### Project Directory Structure
A typical Express + Sequelize project structure looks like this:

```text
my-express-app/
├── src/
│   ├── config/
│   │   └── database.js   # DB connection instance & pool setup
│   ├── models/
│   │   └── index.js      # Bootstraps models and registers relationships
│   ├── app.js            # Express application setup
│   └── server.js         # Starts the HTTP server & database connection test
├── .env                  # Local environment variables (gitignored)
├── .env.example          # Sample environment variables (safe to commit)
├── package.json
└── .sequelizerc          # Directs Sequelize CLI to use specific source directories
```

---

## 🌍 Real-World Analogy
Setting up your project is like setting up a **Smart Home Central Controller**:
* The **Express app** is the house itself.
* The **Database** is the electrical power grid outside.
* The **Sequelize Instance** is the main circuit breaker.
* The **`.env` file** is the wall socket adapter configuration that ensures you plug in the correct voltages (host, user, password) depending on whether you are in India, the US, or Europe (development, testing, or production environments).

---

## ⚙️ Syntax / API / Core Usage

### 1. Installation Commands
To start, initialize your package and install dependencies:

```bash
# Initialize Node.js project
npm init -y

# Install Express, Sequelize, and dotenv
npm install express sequelize dotenv

# Install the dialect driver (MySQL example)
npm install mysql2

# Install Sequelize CLI as a dev dependency
npm install --save-dev sequelize-cli
```

### 2. Configure the CLI using `.sequelizerc`
Create a `.sequelizerc` file in your root folder. This file instructs the CLI to place its generated folders inside our standard project structure (`src/`) instead of the root directory.

```javascript
// .sequelizerc
const path = require('path');

module.exports = {
  'config': path.resolve('src', 'config', 'database.js'),
  'models-path': path.resolve('src', 'models'),
  'seeders-path': path.resolve('src', 'seeders'),
  'migrations-path': path.resolve('src', 'migrations')
};
```

---

## 💻 Practical Examples

### Step 1: Create the `.env` File
Create a `.env` file in the root directory to store database connection details:

```env
PORT=3000
NODE_ENV=development

DB_USER=root
DB_PASSWORD=mysecurepassword
DB_NAME=mysql_learning_db
DB_HOST=127.0.0.1
DB_PORT=3306
```

### Step 2: Create the Database Configuration File
Create the dynamic database configuration file `src/config/database.js`:

```javascript
// src/config/database.js
require('dotenv').config();

module.exports = {
  development: {
    username: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    database: process.env.DB_NAME,
    host: process.env.DB_HOST,
    port: process.env.DB_PORT || 3306,
    dialect: 'mysql',
    logging: console.log, // Logs SQL queries in development terminal
    pool: {
      max: 5,
      min: 0,
      acquire: 30000,
      idle: 10000
    }
  },
  test: {
    username: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    database: 'test_db',
    host: process.env.DB_HOST,
    port: process.env.DB_PORT || 3306,
    dialect: 'mysql',
    logging: false // Mute SQL logging during test runs
  },
  production: {
    username: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    database: process.env.DB_NAME,
    host: process.env.DB_HOST,
    port: process.env.DB_PORT || 3306,
    dialect: 'mysql',
    logging: false,
    pool: {
      max: 20, // Increase max connection pool size for production loads
      min: 2,
      acquire: 30000,
      idle: 10000
    }
  }
};
```

### Step 3: Create the Express Server File
Create `src/server.js` to initialize the Express app and test the database connection socket at startup:

```javascript
// src/server.js
const express = require('express');
const { Sequelize } = require('sequelize');
const dbConfig = require('./config/database');

const app = express();
const PORT = process.env.PORT || 3000;
const env = process.env.NODE_ENV || 'development';

// Parse JSON bodies
app.use(express.json());

// Initialize Sequelize with current environment configuration
const currentConfig = dbConfig[env];
const sequelize = new Sequelize(
  currentConfig.database,
  currentConfig.username,
  currentConfig.password,
  currentConfig
);

// Middleware/Endpoint to check health status
app.get('/health', async (req, res) => {
  try {
    // Authenticate checks if Sequelize can connect to the database
    await sequelize.authenticate();
    res.status(200).json({
      status: 'success',
      message: 'Database connection has been established successfully.'
    });
  } catch (error) {
    res.status(500).json({
      status: 'error',
      message: 'Unable to connect to the database.',
      details: error.message
    });
  }
});

app.listen(PORT, () => {
  console.log(`Server running in ${env} mode on port ${PORT}`);
});
```

---

## 🔄 Flow Diagram

### Application Startup Flow

```text
                     +----------------------+
                     |  Start: node server  |
                     +----------+-----------+
                                |
                                v
                     +----------------------+
                     |  Load .env settings  |
                     +----------+-----------+
                                |
                                v
                     +----------------------+
                     |  Match Config for    |
                     |  NODE_ENV            |
                     +----------+-----------+
                                |
                                v
                     +----------------------+
                     | Instantiate          |
                     | new Sequelize()      |
                     +----------+-----------+
                                |
                                v
                     +----------------------+
                     | Run:                 |
                     | authenticate()       |
                     +----------+-----------+
                                |
                      /------------------\
                     /                    \
            [Success]                      [Fail]
                /                            \
               v                              v
      +------------------+           +------------------+
      | Express listens  |           | Throw Database   |
      | on port          |           | Connection Error |
      +------------------+           +------------------+
```

---

## 🧪 Common Interview Questions

### Q1: Why is `sequelize.authenticate()` used?
* **Answer**: `sequelize.authenticate()` tests the connection by executing a simple, harmless query (like `SELECT 1+1` or similar). It validates that the network credentials (host, username, password) are correct and that the database server is running and reachable.

### Q2: Why do we use `.sequelizerc`?
* **Answer**: By default, the Sequelize CLI generates folder structures in the root directory. To keep a clean source-code architecture, we write a `.sequelizerc` file to map CLI targets (migrations, seeders, configs, models) directly into our modular `src/` directory.

### Q3: Why is using environment variables better than committing a JSON configuration file?
* **Answer**: 
  1. **Security**: Storing hardcoded secrets in version control (like GitHub) is a massive security vulnerability.
  2. **Flexibility**: Environment variables let the application scale without editing source code. Local developers, automated test suites, and cloud deployment pipelines can use different credentials by simply setting different environment variables.

---

## ⚠️ Common Mistakes / Pitfalls
* **Exposing Secret Files**: Forgetting to add `.env` to your `.gitignore` file. If committed, your database credentials will be public.
* **Missing Dialect Driver**: Running `npm install sequelize` but forgetting to run `npm install mysql2`. This will throw the runtime error: `Error: Please install mysql2 package manually`.

---

## ✅ Best Practices
* **Create an `.env.example` file**: Create a mock `.env.example` file containing empty variables (e.g. `DB_USER=`) and commit it to git so other developers know which keys are required to run the app.
* **Mute Logging in Production**: Ensure SQL logging is set to `false` in production config. Logging thousands of SQL queries to console in production degrades performance and clutters server log files.

---

## 📝 Quick Recap
* Installing Sequelize requires installing the core `sequelize` package plus the driver (`mysql2` as default driver, `pg`, etc.).
* Use a dynamic JavaScript configuration file to parse environment variables from `.env`.
* Run `sequelize.authenticate()` at app startup to verify database credentials before accepting requests.
* Use a `.sequelizerc` file to organize directories inside the `src/` directory.

---

## 🔗 Navigation
Previous : [02_sequelize_architecture_and_mental_model.md](./02_sequelize_architecture_and_mental_model.md) | Index : [00_index.md](./00_index.md) | Next : [04_models_definition_and_synchronization.md](./04_models_definition_and_synchronization.md)
