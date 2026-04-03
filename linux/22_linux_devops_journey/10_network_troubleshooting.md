# 1. Scenario: Backend Cannot Connect to Database

## 2. Real-world Context
Your frontend developer states the website is loading, but the dashboard is failing to retrieve user data. The web server (Backend Application) is trying to talk to the Backend Database over the network but is failing. You must determine if this is an application bug, a firewalled port, or a total network outage between the two servers.

## 3. Objective
Diagnose network connectivity, check DNS resolution, make direct HTTP requests to APIs, and view open ports on your server.

## 4. Step-by-step Solution

### Prerequisite: Setting up the Practice Environment
*Since we cannot physically control remote firewalls safely, this exercise relies heavily on live networking concepts. However, we can start a dummy local HTTP server so your `curl` command hits something:*

```bash
python3 -m http.server 8080 &
sleep 2
```
* **What:** Starts a basic local HTTP server on port 8080 in the background.
* **Why:** So that the `curl` and `netstat` commands in the scenario actually have a local listening service to successfully interact with and discover.
* **How:** Python's built-in `http.server` module instantly binds to port 8080 and serves the current directory without needing full configuration.
* **Impact:** Simulates a running backend application, giving your network diagnostic commands a real local socket to test.

**Step 1: Check basic network reachability**
```bash
ping db.internal-company.com
```
* **What:** Sends small ICMP packet requests to the database server asking "Are you alive?"
* **Why:** This is the most fundamental test. If it fails, the server is offline or network routing is broken. If it succeeds, the machine is online, but the database *application* might be down.
* **How:** `ping [hostname or IP]`. Press `Ctrl+C` to stop it.
* **Impact:** Instantly divides network problems from application problems.

**Step 2: Test API endpoints directly from the server**
```bash
curl -I http://localhost:8080/health
```
* **What:** Acts as a command-line web browser, hitting a URL to see the HTTP response code (e.g., 200 OK or 502 Bad Gateway).
* **Why:** You need to know if the backend service is actually successfully running on the local machine before blaming the remote database.
* **How:** `curl` fetches data. The `-I` flag fetches ONLY the headers instead of the HTML page.
* **Impact:** Verifies application health directly at the source, bypassing load balancers.

**Step 3: Check which ports are actively listening on your machine**
```bash
sudo netstat -tulpn | grep LISTEN
```
* **What:** Lists all active network sockets and the applications controlling them.
* **Why:** To accept traffic, your backend MUST be actively listening on port 8080. If it's not listed here, the service crashed.
* **How:** `netstat` lists connections. `-t` TCP, `-u` UDP, `-l` listening, `-p` show process name, `-n` show numbers.
* **Impact:** Confirms whether your software successfully bound to a port.

**Step 4: Check if an external port is open via Telnet / NC**
```bash
nc -vz 10.0.1.55 5432
```
* **What:** Attempts a TCP connection to the database IP (`10.0.1.55`) on PostgreSQL port (`5432`).
* **Why:** `ping` might work, but the specific port might be blocked by a Firewall.
* **How:** `nc` is Netcat. `-v` provides verbose output. `-z` scans without sending payloads.
* **Impact:** The ultimate confirmation. If `nc` succeeds, the network is perfect, and the bug is inside the code.

## 6. Expected Output
```text
$ ping db.internal-company.com
PING db.internal (10.0.1.55) 56(84) bytes of data.
64 bytes from 10.0.1.55: icmp_seq=1 ttl=64 time=0.8 ms

$ curl -I http://localhost:8080/health
HTTP/1.1 500 Internal Server Error

$ nc -vz 10.0.1.55 5432
Connection to 10.0.1.55 5432 port [tcp/postgresql] succeeded!
```

## 7. Tips / Best Practices
* **Pinging is blocked:** Corporate firewalls often block Ping (ICMP). A failed ping doesn't mean the server is dead, rely on `nc` or `curl`.
* **Troubleshooting path:** Always start looking locally (`netstat`) and move outwards (`nc`, `curl`).

## 8. Interview Questions
1. **Q:** What is `curl` used for in DevOps?
   **A:** To transfer data over network protocols, heavily used to test APIs directly from the server CLI.
2. **Q:** If `ping` fails, but `curl` succeeds, what does that mean?
   **A:** The database server is alive but blocks ICMP ping packets intentionally for security.

## 9. DevOps Insight
Understanding networking bridges the gap between SysAdmins and DevOps. In AWS, network bugs are usually Security Group or Subnet misconfigurations. Combining `curl` and `nc` allows Jenkins or GitLab CI/CD pipelines to run automated health checks instantly after deploying infrastructure.
