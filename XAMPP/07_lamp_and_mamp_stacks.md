# MAMP and LAMP Stacks

---

## 1. What

If WAMP is for Windows, the other acronyms define environments for the other major operating systems:

- **MAMP:** **M**ac, **A**pache, **M**ySQL, **P**HP.
- **LAMP:** **L**inux, **A**pache, **M**ySQL, **P**HP.

*Note: Like WAMP, MAMP is an actual packaged application you can download. LAMP typically isn't a packaged downloaded app; rather, it refers to the architectural design of configuring these tools manually on a Linux server.*

---

## 2. Why

### The Problem:
macOS handles background networking processes differently than Windows. Apple also builds its own web servers natively into macOS for other features. You need a dedicated graphical environment that handles macOS permissions, firewall requests, and folder routing (`/Applications/`) without conflicting with Apple's system roots.

### The Solution:
**MAMP** provides a gorgeous, Mac-native graphical interface to bind Apache ports gracefully inside macOS environments. 
**LAMP** defines the absolute production industry standard. 90% of PHP/MySQL websites deployed to live physical servers on the internet are running on a LAMP architecture.

---

## 3. How

### How MAMP Works (macOS):
MAMP installs itself cleanly into `/Applications/MAMP`. 
Because macOS often runs services on port 80 natively, MAMP safely defaults to running Apache on port **8888** and MySQL on port **8889**. Every time you type `localhost` into a Mac browser, you use `http://localhost:8888`. Its Document Root is `/Applications/MAMP/htdocs`.

### How LAMP Works (Linux):
Instead of clicking a `.dmg` or `.exe`, a developer provisions a fresh Ubuntu Linux server and types commands:
```bash
sudo apt update
sudo apt install apache2
sudo apt install mysql-server
sudo apt install php libapache2-mod-php php-mysql
```
There is no GUI here. The server is strictly configured through the terminal. Document root is `/var/www/html`.

---

## 4. Implementation

### Changing Ports in MAMP to Match XAMPP (Port 80)
If you switch from a PC to a Mac, you might hate typing `:8888`.
1. Open MAMP Pro or standard MAMP interface.
2. Click **Preferences** -> **Ports**.
3. Click the button to "Set Web & MySQL ports to 80 & 3306".
4. You will now be required to enter your Mac password every time you start MAMP (because binding to port 80 requires administrator privileges on macOS!).

---

## 5. Impact

MAMP was incredibly popular in the early 2010s Mac community because of its exceptionally clean GUI and premium tools (MAMP Pro) for mocking local `.dev` domain names (e.g. typing `http://myproject.test` instead of `localhost`). 

LAMP is still the backbone of internet deployment. Learning how a local MAMP/XAMPP server behaves prepares you perfectly for administering a real live production Linux server.

---

## 6. Summary

- **MAMP** is a Mac-specific bundled software for Apache/MySQL/PHP.
- It defaults to ports `8888` (Apache) and `8889` (MySQL) to avoid macOS root permission conflicts.
- **LAMP** is the Linux architectural standard, typically configured purely via terminal command line.
- Frontends like React and Next.js compensate for cross-platform team differences (Port 80 vs 8888) using environment variables (`.env`).

---

**Prev:** [06_wamp_stack.md](./06_wamp_stack.md) | **Next:** [08_docker_vs_xampp.md](./08_docker_vs_xampp.md)
