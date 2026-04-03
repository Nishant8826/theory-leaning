# 1. Scenario: Hardening a Fresh Web Server

## 2. Real-world Context
Your company just provisioned a completely blank Ubuntu server facing the public internet. Before deploying the application code, you need to execute a basic server setup to establish security. Hackers scan the internet 24/7 for open servers. You must install a firewall to block all traffic except web (HTTP/HTTPS) and remote management (SSH).

## 3. Objective
Initialize an Uncomplicated Firewall (UFW), allow specific traffic ports, block everything else, and verify the active ruleset.

## 4. Step-by-step Solution

### Prerequisite: Setting up the Practice Environment
*To practice configuring the Uncomplicated Firewall (UFW), we first need to ensure the firewall software is installed and completely disabled so we have a clean slate:*

```bash
sudo apt update && sudo apt install -y ufw
sudo ufw --force reset
sudo ufw disable
```
* **What:** Installs the firewall, aggressively resets any existing rules to factory defaults, and disables it.
* **Why:** It is extremely dangerous to experiment with firewalls blindly. This ensures the firewall starts deactivated and completely empty, matching the blank-slate scenario perfectly.
* **How:** `--force reset` deletes everything without asking for confirmation, and `disable` effectively turns the packet filtering kernel module off safely.
* **Impact:** Provides a secure, zero-state environment for you to safely build up your incoming firewall rules from scratch.

**Step 1: Check the default firewall status**
```bash
sudo ufw status
```
* **What:** Asks the Uncomplicated Firewall for its current state.
* **Why:** Before modifying security perimeters, you must know if existing rules are already active to prevent accidentally overwriting them.
* **How:** `ufw status`.
* **Impact:** Determines the current attack surface of the machine (usually "inactive" by default on fresh images).

**Step 2: Explicitly allow SSH connections (CRITICAL)**
```bash
sudo ufw allow OpenSSH
```
* **What:** Informs the firewall to strictly allow incoming traffic on Port 22 (SSH).
* **Why:** If you turn on a firewall *before* explicitly allowing SSH, the firewall will block your own terminal connection. You will be permanently locked out of your newly created server!
* **How:** `ufw allow [service/port]`.
* **Impact:** Secures your access lifeline before shutting the rest of the doors.

**Step 3: Allow standard web traffic**
```bash
sudo ufw allow 'Nginx Full'
```
* **What:** Allows incoming traffic for HTTP (Port 80) and HTTPS (Port 443).
* **Why:** The fundamental purpose of this server is to host a website for public users.
* **How:** `Nginx Full` is an application profile ufw recognizes. You could equivalently type `sudo ufw allow 80` and `sudo ufw allow 443`.
* **Impact:** Exposes only the exact ports the business strictly requires to operate.

**Step 4: Enable the firewall**
```bash
sudo ufw enable
```
* **What:** Activates the firewall and enforces the rule system. By default, it blocks *all* incoming connections that don't match the rules you just wrote.
* **Why:** A firewall ruleset is useless until activated.
* **How:** Type `ufw enable` and press `y` to confirm.
* **Impact:** Immediately secures the server from port-scanning script kiddies and external database-probing attacks.

## 6. Expected Output
```text
$ sudo ufw status
Status: inactive

$ sudo ufw allow OpenSSH
Rule added
Rule added (v6)

$ sudo ufw allow 'Nginx Full'
Rule added
Rule added (v6)

$ sudo ufw enable
Command may disrupt existing ssh connections. Proceed with operation (y|n)? y
Firewall is active and enabled on system startup

$ sudo ufw status
Status: active
To                         Action      From
--                         ------      ----
OpenSSH                    ALLOW       Anywhere
Nginx Full                 ALLOW       Anywhere
```

## 7. Tips / Best Practices
* **Never use root:** A basic setup also includes setting up a new standard user with sudo privileges, and disabling SSH login for the `root` account entirely inside `/etc/ssh/sshd_config`.
* **UFW Profiles:** You can see what software profiles UFW knows about by running `sudo ufw app list`.
* **AWS Security Groups vs UFW:** In the cloud (AWS), you have Cloud Firewalls (Security Groups). A true DevOps setup uses *both*—the Security Group blocks traffic at the cloud perimeter, and UFW provides a secondary defense layer inside the OS itself.

## 8. Interview Questions
1. **Q:** Why is it absolutely vital to run `ufw allow ssh` BEFORE running `ufw enable`?
   **A:** Enabling UFW defaults to dropping all undocumented incoming connections. If SSH isn't documented, your current connection gets severed, locking you permanently out of remote access.
2. **Q:** What is the difference between port 80 and 443?
   **A:** HTTP operates on port 80 (unencrypted). HTTPS operates on port 443 (encrypted with SSL/TLS certificates).
3. **Q:** Does UFW replace `iptables`?
   **A:** No, UFW (Uncomplicated Firewall) is simply a user-friendly frontend command-line interface that manipulates the extremely complex underlying `iptables`/`nftables` rules in the Linux kernel on your behalf.

## 9. DevOps Insight
Deploying firewalls manually via UFW is excellent for single-server sysadmin work. However, in DevOps, infrastructure is defined as "Code" (IaC). DevOps engineers use tools like HashiCorp Terraform to construct firewall rules (like AWS Security Groups) via structured `.tf` files. The concepts (Ports, Ingress, Allow/Deny) remain identical; only the tooling changes from Bash commands to declarative code.
