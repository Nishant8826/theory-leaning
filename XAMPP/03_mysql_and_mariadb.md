# MySQL and MariaDB

---

## 1. What

**MySQL** / **MariaDB** represent the "M" in XAMPP. They are **Relational Database Management Systems (RDBMS)**.

- **Relational:** Data is stored in structured tables (rows and columns) that are related to one another.
- **DBMS:** The software that lets you write, read, update, and delete that data efficiently and safely.

*Note: Originally, XAMPP shipped with MySQL. Since version 5.5.30, XAMPP uses MariaDB (a drop-in replacement created by the original developers of MySQL after MySQL was acquired by Oracle). For all practical purposes, commands and code are identical, so the terms are often used interchangeably.*

---

## 2. Why

### The Problem:
Web applications need state. If users register for an account, create posts, or add items to a shopping cart, that data must be saved permanently. You *could* save this in giant `.txt` files or `.json` files, but reading from massive text files is incredibly slow, insecure, and breaks instantly if two users try to save data at the exact same millisecond.

### The Solution:
Databases exist to handle massive amounts of data operations simultaneously, quickly, and securely. MySQL is optimized to look up specific records out of millions in a fraction of a second utilizing SQL (Structured Query Language).

---

## 3. How

### How MySQL Works Internally:

1. **Service Startup:** You click "Start" next to MySQL in the XAMPP Control Panel.
2. **Daemon Listening:** The `mysqld.exe` background process runs and listens on Port **3306**.
3. **Connection:** A client (like your PHP script, Node.js backend, or a GUI tool) mathematically establishes a connection using credentials (`localhost`, `root`, `""` [blank password]).
4. **Execution:** The client says `SELECT * FROM users;`
5. **Return:** The MySQL Engine processes the SQL command, fetches data from the hard drive, and returns it as a data structure to the client.

---

## 4. Implementation

To interact with the local MySQL database, you typically use a backend language. 

### Connecting via Node.js (TypeScript)

If you are building a modern API with Next.js or Express locally, you can easily connect directly to XAMPP's database.

```ts
// Mandatory installation: npm install mysql2
import mysql from 'mysql2/promise';

async function connectToXamppDB() {
  // Creating a connection to the XAMPP MySQL daemon 
  const connection = await mysql.createConnection({
    host: 'localhost',      // XAMPP runs locally
    user: 'root',           // Default XAMPP username
    password: '',           // Default XAMPP password is blank!
    database: 'my_project'  // Name of the DB you created
  });

  try {
    // Write standard SQL
    const [rows, fields] = await connection.execute('SELECT * FROM users');
    console.log("Database Results:", rows);
    return rows;
  } catch (error) {
    console.error("Database Error:", error);
  } finally {
    await connection.end(); // close the connection
  }
}
```

---

## 5. Impact

Relational Databases power the overwhelming majority of the internet (ecommerce, social media, banking).
By having MySQL bundled in XAMPP, developers can test complex SQL structures, table relationships (foreign keys), and heavy data operations entirely offline with zero cost and zero latency.

---

## 6. Summary

- **MySQL/MariaDB** is the database system inside XAMPP.
- It stores structured data in tables and uses SQL to interact with it.
- In XAMPP, the server runs on Port **3306**.
- The default credentials for a fresh XAMPP installation are username: **root** with **no password**.
- Never connect to a database directly from a React Client Component; use an API or a Next.js Server Component.

---

**Prev:** [02_apache_server.md](./02_apache_server.md) | **Next:** [04_php_processor.md](./04_php_processor.md)
