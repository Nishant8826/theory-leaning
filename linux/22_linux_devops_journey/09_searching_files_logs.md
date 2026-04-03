# 1. Scenario: Hunting Down Hacked Files

## 2. Real-world Context
Your server has triggered a security alert. A malicious bot may have uploaded a hidden payload. You have been tasked to find all `.js` files that were modified within the last 24 hours anywhere in the sprawling `/var/www/html` folder. Additionally, you need to search deeply inside those files to see if the phrase "eval(base64" has been injected.

## 3. Objective
Utilize advanced searching tools to locate files based on specific attributes (like time modified), and perform recursive text searches across an entire filesystem.

## 4. Step-by-step Solution

### Prerequisite: Setting up the Practice Environment
*To practice hunting for malicious files, let's inject a fake "hacked" JavaScript file into a web directory structure:*

```bash
sudo mkdir -p /var/www/html/core
sudo mkdir -p /var/www/html/assets
sudo touch /var/www/html/core/login.js
sudo bash -c 'cat <<EOF > /var/www/html/assets/obfuscated_temp.js
// basic script
run(eval(base64_decode(x)));
EOF'
```
* **What:** Creates web directories and generates a few `.js` files, actively inserting a mock malicious `eval(base64` string into one of them.
* **Why:** The `find` and `grep -rn` commands require these files and specific string contents to exist in order to successfully "discover" them.
* **How:** `mkdir` builds the folder tree, `touch` creates a benign recently-modified file, and a heredoc writes the "malicious" string into another file.
* **Impact:** Safely replicates a compromised web server scenario to test forensic search techniques.

**Step 1: Find all files modified within the last 1 day**
```bash
find /var/www/html -mtime -1
```
* **What:** Crawls through the server folder and dumps paths of any file altered recently.
* **Why:** A hacker modifies code files. Locating recently altered targets dramatically narrows down the investigation.
* **How:** `find [path]` executes the search. `-mtime -1` means modified time is less than 1 day ago.
* **Impact:** Rapid forensic discovery. This command alone saves hours of manual checking.

**Step 2: Filter the find command to ONLY lookup JavaScript files**
```bash
find /var/www/html -name "*.js" -mtime -1
```
* **What:** Combines search parameters so only files ending in `.js` that were changed in the last 24 hours appear.
* **Why:** You don't care about logs or images right now, only javascript code.
* **How:** `-name` searches by a file pattern. `*.js` captures everything ending in `.js`. Always quote the pattern so the shell doesn't misinterpret the `*`.
* **Impact:** Precision searching, isolating dangerous scripts.

**Step 3: Recursively grep a folder for malicious text**
```bash
grep -rn "eval(base64" /var/www/html/
```
* **What:** Scans inside *every* file inside the HTML folder looking for the exact malicious string.
* **Why:** Sometimes time modifications can be masked. If we know exactly what malicious code looks like, we can hunt it by its content instead of its filename.
* **How:** `grep` searches text. `-r` means recursively dig into every folder. `-n` prints the exact line number where the string was found!
* **Impact:** Provides the exact File Path AND Line Number where the vulnerability exists. Developer fix time becomes 30 seconds.

**Step 4: Real-time trailing of the active system authentication log**
```bash
sudo tail -f /var/log/auth.log | grep Failed
```
* **What:** Monitors the authentication log live on screen, spitting out only new lines where a login "Failed".
* **Why:** Since the system might currently be under a brute-force attack, you need to actively watch the unauthorized attempts as they happen.
* **How:** `tail -f` (follow) watches a file update in real-time. Piped to `grep`, it filters the live stream.
* **Impact:** Dynamic incident response. You can watch the attacker fail while you formulate defense protocols.

## 6. Expected Output
```text
$ find /var/www/html -name "*.js" -mtime -1
/var/www/html/core/login.js
/var/www/html/assets/obfuscated_temp.js

$ grep -rn "eval(base64" /var/www/html/
/var/www/html/assets/obfuscated_temp.js:42: run(eval(base64_decode(x)));

$ sudo tail -f /var/log/auth.log | grep Failed
Oct 27 15:02:11 devserver sshd[1204]: Failed password for invalid user root
Oct 27 15:02:14 devserver sshd[1205]: Failed password for admin
```

## 7. Tips / Best Practices
* **Don't search from Root (`/`):** Running `find / -name "*.txt"` forces the system to literally check millions of system-critical files, lagging the server. Always narrow the search path if possible.
* **Delete old logs:** You can combine `find` with executing actions. E.g., `find /var/log -name "*.log" -mtime +30 -exec rm {} \;` will automatically delete log files older than 30 days!
* **Case insensitive grep:** `grep -ri "password"` finds passwords regardless of capitalization, recursively.

## 8. Interview Questions
1. **Q:** How do you search a directory and all subdirectories for a file named `backup.zip`?
   **A:** `find /dir/path -name "backup.zip"`
2. **Q:** What is the purpose of the `-r` and `-n` flags in `grep -rn "error" /var/log`?
   **A:** `-r` causes grep to recursively look inside all nested files in the directory. `-n` prints the line number where the matching text was found in each file.
3. **Q:** How does `tail -f` differ from a regular `tail` command?
   **A:** A regular `tail` command prints the last 10 lines and exits. `tail -f` actively "follows" the file, continuously streaming new lines to the screen as they are written.

---
[⬅️ Previous: 08_text_processing](08_text_processing.md) | [Next ➡️: 10_network_troubleshooting](10_network_troubleshooting.md)
