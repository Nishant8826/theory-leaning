# Apache Web Server

---

## 1. What

**Apache** (officially the Apache HTTP Server) is the "A" in XAMPP. It is the core software that makes XAMPP act as a web server.

A web server is a program that sits on a computer, listens for incoming network requests (like "Hey, send me your homepage!"), and responds by serving files (like HTML documents, images, or JSON data).

---

## 2. Why

### The Problem:
If you build a React app and export an `index.html` file, you could technically just double-click it and open it in Chrome via the `file://` protocol. 
However, the `file://` protocol severely limits browser features due to security. You cannot make API calls (CORS issues), use service workers, or process PHP files without a real HTTP connection.

### The Solution:
Apache provides that HTTP protocol. It acts just like a real public website server, but it runs securely inside your local network. It allows your browser to communicate with your local files using `http://localhost`, perfectly mimicking a real website.

---

## 3. How

### How Apache Works in XAMPP:

1. **Listening:** When started via the XAMPP Control Panel, Apache continuously listens to Port **80** (for regular HTTP) and Port **443** (for secure HTTPS).
2. **Receiving Request:** Your browser sends an HTTP GET request to `localhost:80`.
3. **Routing Document:** Apache looks at its configuration file (`httpd.conf`), which dictates that `localhost` corresponds to the `C:\xampp\htdocs` directory.
4. **Processing (if needed):** 
   - If the request is for an `.html` or `.jpg` file, Apache just sends the file directly.
   - If the request is for a `.php` file, Apache says "I don't know how to read PHP! Let me pass this to the PHP Engine." PHP processes the file, hands the generated HTML back to Apache.
5. **Responding:** Apache sends the final HTTP Response back to the browser.

---

## 4. Implementation

### Understanding `htdocs`

The core location for Apache in XAMPP is the Document Root. By default, it is the `htdocs` folder.

```
C:\xampp\
  ├── apache\       (The server software files)
  ├── mysql\        (The database software files)
  ├── php\          (The PHP engine files)
  └── htdocs\       (YOUR WORKSPACE - The Document Root)
       ├── index.php      -> Loads at http://localhost/
       └── my_project/    
            └── api.php   -> Loads at http://localhost/my_project/api.php
```

### Modifying Apache Ports (Troubleshooting)

A very common issue is that starting Apache fails because "Port 80 is already in use" (often by Skype or Windows IIS).

To fix this:
1. Open XAMPP Control Panel.
2. Click **Config** next to Apache, select **httpd.conf**.
3. Press `Ctrl+F` and find `Listen 80`. Change it to `Listen 8080`.
4. Find `ServerName localhost:80`. Change it to `ServerName localhost:8080`.
5. Save the file and restart Apache.
6. You now access your sites via `http://localhost:8080/`.

---

## 5. Impact

Apache is the foundational pillar of the web. Historically, it powered over 70% of the entire internet! While NGINX is now more popular for high-traffic sites, Apache remains the standard for basic setups, shared hosting (like GoDaddy), and local development bundles like XAMPP.

Understanding how Apache routes requests through `htdocs` is crucial for understanding how the World Wide Web fundamentally operates.

---

## 6. Summary

- **Apache** is the HTTP web server inside XAMPP.
- It listens for requests on Port 80 and 443.
- It serves static files directly, and hands dynamic files (PHP) to the appropriate processor.
- Its root folder is called **`htdocs`**.
- It allows you to run a true HTTP server environment mirroring real-world web hosting directly from your hard drive.

---

**Prev:** [01_introduction_to_xampp.md](./01_introduction_to_xampp.md) | **Next:** [03_mysql_and_mariadb.md](./03_mysql_and_mariadb.md)
