# 07. Advanced Querying, Filtering, and Operators

## 🎯 Goal of This Chapter
By the end of this chapter, you will be able to perform complex queries in Sequelize. You will learn to use query operators (`Op`) for filtering, select specific columns (projection), sort results, and implement offset-based pagination using the `findAndCountAll` API.

---

## 🤔 Why This Topic Matters
Real-world applications rarely fetch all columns or rows from a table. Users search for keywords, filter by price ranges, sort items by rating, and read data page-by-page. 

If you do not implement querying, sorting, and pagination at the **database level**, your application will:
* Fetch megabytes of unnecessary data over the network.
* Overload server memory by loading thousands of rows.
* Expose sensitive fields like password hashes in HTTP responses.

---

## 🧠 Core Concept

### 1. Attributes (Projection)
In SQL, you select specific columns using `SELECT name, email FROM users;`. In Sequelize, you restrict the fields fetched using the `attributes` option. You can also exclude specific fields (like `password`).

### 2. Operators (`Op`)
Sequelize exposes database symbols (like `>`, `<`, `LIKE`, `IN`) under the **`Op`** object. Importing `Op` allows you to write advanced search criteria.

### 3. Sorting
Sorting uses the `order` array, where you define the column name and direction (`ASC` or `DESC`).

### 4. Pagination
Pagination divides data into chunks. Sequelize achieves this with two options:
* `limit`: The number of records to retrieve.
* `offset`: The number of records to skip before starting to retrieve.

---

## 🏗 Mental Model / Internal Working

### How Operators map to SQL
When Sequelize parses a `where` object containing `Op` keys, the Query Generator matches the key to its SQL operator string:

| Sequelize Operator | SQL Equivalent | Example Code | Generated SQL |
| :--- | :--- | :--- | :--- |
| `[Op.eq]` | `=` | `age: { [Op.eq]: 25 }` | `age = 25` |
| `[Op.gt]` | `>` | `age: { [Op.gt]: 18 }` | `age > 18` |
| `[Op.between]` | `BETWEEN` | `price: { [Op.between]: [10, 50] }` | `price BETWEEN 10 AND 50` |
| `[Op.like]` | `LIKE` | `title: { [Op.like]: '%Node%' }` | `title LIKE '%Node%'` |
| `[Op.in]` | `IN` | `role: { [Op.in]: ['admin', 'manager'] }` | `role IN ('admin', 'manager')` |
| `[Op.or]` | `OR` | `[Op.or]: [{ age: 10 }, { age: 12 }]` | `(age = 10 OR age = 12)` |

---

## 🌍 Real-World Analogy
Think of database querying as using a **Vending Machine**:
* **Attributes** is like selecting to show only the label and price of the soda cans, hiding internal serial numbers.
* **Operators** are the filters: *"show me drinks that are cold AND cost less than $3"*.
* **Pagination** is how the items are arranged: since they can't fit all drinks on the front display shelf, they display the first 10 items (limit), and to see more, you push a button to scroll/skip past them (offset).

---

## ⚙️ Syntax / API / Core Usage

### Excluded Attributes Projection
```javascript
const users = await User.findAll({
  attributes: { exclude: ['password'] } // Fetch all fields EXCEPT the password hash
});
```

### Complex Filtering with `Op`
```javascript
const { Op } = require('sequelize');

const activeAdmins = await User.findAll({
  where: {
    status: 'active',
    role: {
      [Op.in]: ['admin', 'manager']
    },
    age: {
      [Op.gte]: 21
    }
  }
});
```

---

## 💻 Practical Examples

### Example 1: E-commerce Product Search Endpoint
Here is a realistic Express controller method that allows users to search, filter by price range, sort, and paginate through products.

```javascript
// src/controllers/productController.js
const { Op } = require('sequelize');
const Product = require('../models/Product');

module.exports = {
  getProducts: async (req, res) => {
    try {
      // 1. Destructure query parameters with fallback defaults
      let { search, minPrice, maxPrice, sortBy, order, page, limit } = req.query;

      page = parseInt(page) || 1;
      limit = parseInt(limit) || 10;
      const offset = (page - 1) * limit;

      // 2. Build dynamic where filter clause
      const whereClause = {
        isActive: true // Always filter out inactive products
      };

      if (search) {
        whereClause.name = {
          [Op.like]: `%${search}%` // Case-insensitive search (default behavior in MySQL collation)
        };
      }

      if (minPrice || maxPrice) {
        whereClause.price = {};
        if (minPrice) whereClause.price[Op.gte] = parseFloat(minPrice);
        if (maxPrice) whereClause.price[Op.lte] = parseFloat(maxPrice);
      }

      // 3. Define sorting parameters
      const validSortFields = ['price', 'createdAt', 'rating'];
      const sortField = validSortFields.includes(sortBy) ? sortBy : 'createdAt';
      const sortOrder = order === 'asc' ? 'ASC' : 'DESC';

      // 4. Query the database using findAndCountAll
      // This returns { count: TotalCountMatches, rows: ArrayOfResults }
      const { count, rows } = await Product.findAndCountAll({
        where: whereClause,
        attributes: ['id', 'name', 'price', 'rating', 'createdAt'], // Projection
        order: [[sortField, sortOrder]],
        limit,
        offset
      });

      // 5. Calculate total pages for metadata response
      const totalPages = Math.ceil(count / limit);

      return res.status(200).json({
        data: rows,
        pagination: {
          totalItems: count,
          totalPages,
          currentPage: page,
          itemsPerPage: limit
        }
      });
    } catch (error) {
      return res.status(500).json({ error: error.message });
    }
  }
};
```

---

## 🔄 Flow Diagram

### How `findAndCountAll` Executes
When you call `findAndCountAll({ limit: 10, offset: 20 })`, Sequelize triggers **two SQL queries** in parallel:

```text
                  Product.findAndCountAll()
                             │
              ┌──────────────┴──────────────┐
              ▼                             ▼
       [Query 1: Count]             [Query 2: Data]
       SELECT COUNT(*)              SELECT id, name, price 
       FROM products                FROM products
       WHERE isActive = true;       WHERE isActive = true
                                    ORDER BY price ASC
                                    LIMIT 10 OFFSET 20;
              │                             │
              ▼                             ▼
         Count: 145                     Rows: [10 items]
              │                             │
              └──────────────┬──────────────┘
                             ▼
                    Combine into Object:
               { count: 145, rows: [...] }
```

---

## 🧪 Common Interview Questions

### Q1: What is the benefit of `findAndCountAll` over running `findAll` and then checking `array.length`?
* **Answer**: `findAll` with limit and offset only returns the items on that specific page (e.g., 10 rows). Checking `array.length` would return `10`, hiding the total count of products in the database. `findAndCountAll` executes a separate `COUNT(*)` query without limit/offset to determine the total number of records matching the criteria, which is necessary to compute total pages in frontend pagination displays.

### Q2: Why is the `Op` object used instead of plain string keys?
* **Answer**: Using ES6 Symbols (like `[Op.gt]`) prevents key collision conflicts with database column names. It also prevents developers from injecting raw SQL fragments inside key strings, ensuring that all query variables are properly escaped by the ORM's parameterization engine.

### Q3: What is the difference between `Op.like` and `Op.iLike`, and which is used in MySQL?
* **Answer**: 
  * `Op.like` maps to standard SQL `LIKE`. In MySQL, the default table collation (e.g. `utf8mb4_0900_ai_ci`) is case-insensitive (signified by `_ci`). Therefore, `Op.like` acts as a case-insensitive search by default in MySQL.
  * `Op.iLike` maps to `ILIKE` in PostgreSQL (which forces case-insensitivity on case-sensitive databases). MySQL does not support `ILIKE` syntax, so running `Op.iLike` on a MySQL connection will throw a SQL syntax error. Always use `Op.like` in MySQL.

---

## ⚠️ Common Mistakes / Pitfalls
* **N+1 count queries on heavy tables**: Calling `findAndCountAll` on huge tables (millions of rows) with complex joins can slow down performance because running `COUNT(*)` forces the database to count all match indexes, which is highly resource-intensive.
* **Negative Offset errors**: Calculating offset values as `(page - 1) * limit` without validation. If a client sends `page=0`, the offset calculation yields a negative number `(-1 * 10 = -10)`, causing the database server to throw a query syntax error.

---

## ✅ Best Practices
* **Enforce Limits**: Never allow users to supply arbitrary limits without constraints. If a user requests `limit=1000000`, it can crash your server's memory. Implement a maximum limit override:
  ```javascript
  const limit = Math.min(parseInt(req.query.limit) || 10, 100); // Caps limit at 100 max
  ```
* **Index Sorted Columns**: If your application queries tables sorting by fields like `price` or `createdAt` regularly, ensure you add indexes to those fields in your migrations to maintain sub-millisecond query performance.

---

## 📝 Quick Recap
* Project columns using the `attributes` block to select specific fields and hide sensitive columns.
* Import the `Op` object from Sequelize to perform complex comparisons (`>`, `<`, `IN`, `LIKE`, `AND/OR`).
* Order results using the nested array formatting syntax: `order: [['columnName', 'ASC']]`.
* Implement paginated lists using `limit` (page size) and `offset` (page skip count) calculations inside `findAndCountAll`.

---

## 🔗 Navigation
Previous : [06_basic_crud_operations.md](./06_basic_crud_operations.md) | Index : [00_index.md](./00_index.md) | Next : [08_validations_constraints_and_hooks.md](./08_validations_constraints_and_hooks.md)
