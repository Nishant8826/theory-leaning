# PHP Processor

---

## 1. What

**PHP** (PHP: Hypertext Preprocessor) is the "P" in XAMPP. It is a server-side scripting language explicitly designed for web development.

Unlike JavaScript (which traditionally runs in the browser), PHP runs on the **server backend**.

---

## 2. Why

### The Problem:
Static HTML pages cannot change dynamically based on who is logged in, what the time is, or what is in a database. To build dynamic applications (like Facebook or WordPress), you need a language that can evaluate logic on the server *before* sending the page to the user.

### The Solution:
PHP acts as the middleman. It connects to the MySQL database, processes form submissions, handles user sessions/cookies, and outputs standard HTML/JSON to the Apache server, which then delivers it to the user.

---

## 3. How

### How PHP Works in XAMPP:

1. A user visits `http://localhost/dashboard.php`.
2. **Apache** intercepts the request. It sees the `.php` extension.
3. Apache passes the file to the **PHP Engine** (which was installed via XAMPP).
4. The PHP Engine reads the file top-to-bottom.
5. If it sees `<?php ... ?>` tags, it executes that programming logic (e.g., query a database).
6. It substitutes the executed logic into final output (usually HTML text).
7. PHP hands the final text back to Apache.
8. Apache sends the text over the network to the browser.
9. **Crucial:** The browser *never* sees the actual raw PHP code. It only sees the final HTML.

---

## 4. Implementation

### Writing a Basic API in PHP inside XAMPP

While you can use PHP to print HTML, in modern development (using React/Next.js for the frontend), PHP is primarily used to build REST APIs that output JSON data.

1. Navigate to your XAMPP installation, usually `C:\xampp\htdocs\`.
2. Create a folder named `api` and a file named `users.php`.

```php
<?php
// C:\xampp\htdocs\api\users.php

// 1. Allow modern frontends to read this data (CORS)
header("Access-Control-Allow-Origin: *");
header("Content-Type: application/json; charset=UTF-8");

// 2. Connect to XAMPP's MySQL Database
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "my_project";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
  // If failed, send a JSON error
  echo json_encode(["status" => "error", "message" => "Connection failed"]);
  exit();
}

// 3. Query the database
$sql = "SELECT id, name, email FROM users";
$result = $conn->query($sql);

$users = [];

if ($result->num_rows > 0) {
  // Fetch each row and push it to the array
  while($row = $result->fetch_assoc()) {
    $users[] = $row;
  }
}

// 4. Send the result back as highly readable JSON
echo json_encode([
    "status" => "success",
    "data" => $users
]);

$conn->close();
?>
```

---

## 5. Impact

PHP powers nearly 77% of all websites on the internet whose server-side programming language is known (mostly because of WordPress). XAMPP provides the easiest pathway to testing WordPress themes and plugins locally because it auto-configures the exact Apache/PHP/MySQL trinity that WordPress requires.

---

## 6. Summary

- **PHP** is the scripting language processor bundled inside XAMPP.
- It intercepts files ending in `.php` that are loaded through Apache.
- It executes server-side logic before any data is sent to the user's browser.
- Modern architectures increasingly use PHP merely to output formatting JSON APIs, letting React handle the HTML rendering UI.
- Next.js can fully replace PHP's role while still utilizing XAMPP's MySQL database.

---

**Prev:** [03_mysql_and_mariadb.md](./03_mysql_and_mariadb.md) | **Next:** [05_phpmyadmin.md](./05_phpmyadmin.md)
