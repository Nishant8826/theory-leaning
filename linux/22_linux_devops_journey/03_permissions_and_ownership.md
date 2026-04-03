# 1. Scenario: Locking Down Sensitive SSH Keys

## 2. Real-world Context
A developer on your team accidentally uploaded an API access key to the server and left the permissions completely open. Currently, any user logged into the entire Linux machine can view the secret key. Security policy dictates that private keys must be readable ONLY by the application user.

## 3. Objective
Change the owner of the sensitive file to the correct user and restrict its read/write permissions to prevent unauthorized access.

## 4. Step-by-step Solution

**Step 1: Check current permissions and ownership**
```bash
ls -l api_secret.key
```
* **What:** Examines the read, write, and execute permissions of the file, as well as who owns it.
* **Why:** You need to know how exposed the file actually is.
* **How:** `ls -l` outputs a 10-character permission string (like `-rw-rw-rw-`) and the user/group owners.
* **Impact:** Auditing is the first step in security. You must know the baseline before fixing it.

**Step 2: Change ownership to the designated application user**
```bash
sudo chown appuser:appgroup api_secret.key
```
* **What:** Changes the owner to `appuser` and the group to `appgroup`.
* **Why:** The developer uploaded it, so they own it. The actual application user needs ownership to utilize the key.
* **How:** `chown [user]:[group] [file]`. `sudo` is required to give away ownership.
* **Impact:** Guarantees that the backend app has the right credentials to attach the key at runtime while blocking standard users.

**Step 3: Restrict permissions to the owner only (Absolute Mode)**
```bash
sudo chmod 600 api_secret.key
```
* **What:** Gives read (4) and write (2) permissions to the owner ONLY, and zero access to group or others.
* **Why:** A private key must remain private. No other process or user should be allowed to view it.
* **How:** `chmod 600` means Owner gets `4 + 2` (6), Group gets `0`, Others get `0`.
* **Impact:** Immediate compliance with security policies. Without 600 or 400 permissions, SSH and many AWS tools will actively refuse to use a key!

**Step 4: Verify the changes applied correctly**
```bash
ls -l api_secret.key
```
* **What:** Checks the final state of the file attributes.
* **Why:** Never assume a command worked perfectly without checking, especially for security tasks.
* **How:** `ls -l`.
* **Impact:** Let's you confirm the file now looks like `-rw------- 1 appuser appgroup ...`.

## 6. Expected Output
```text
$ ls -l api_secret.key
-rw-rw-r-- 1 developer developer 2048 Oct 25 11:00 api_secret.key
$ sudo chown appuser:appgroup api_secret.key
$ sudo chmod 600 api_secret.key
$ ls -l api_secret.key
-rw------- 1 appuser appgroup 2048 Oct 25 11:00 api_secret.key
```

## 7. Tips / Best Practices
* **Understanding Numbers:** `4` is Read, `2` is Write, `1` is Execute. Add them up per category (Owner, Group, Others). `755` means owner gets 7 (read/write/execute), group gets 5 (read/execute), others get 5.
* **Permissions on Folders:** For a user to `cd` into a directory, they MUST have the Execute (`1`) permission on that folder!
* **chmod +x:** If you write a bash script, use `chmod +x script.sh` to make it easily executable.

## 8. Interview Questions
1. **Q:** What does the permission `-rwxr-xr--` mean numerically?
   **A:** 754. Owner has read, write, execute (4+2+1=7), Group has read, execute (4+0+1=5), Others have read only (4).
2. **Q:** Why do some commands require `sudo`?
   **A:** `sudo` allows a permitted user to execute a command as the superuser (root). Tasks like changing another user's file ownership require root privileges.
3. **Q:** What is the difference between `chown` and `chmod`?
   **A:** `chown` changes WHO owns the file. `chmod` changes WHAT permissions users have on the file.
