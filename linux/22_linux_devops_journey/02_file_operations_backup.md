# 1. Scenario: Emergency File Backup Before Deployment

## 2. Real-world Context
Your team is deploying a critical update to the main web application database configuration. Before overwriting the old configurations, standard procedure dictates you must create a backup copy of the existing files. If the new deployment breaks the app, you will need to quickly restore the old configurations from this backup.

## 3. Objective
Locate current configuration files, create secure backups, and move an outdated file to an archive directory.

## 4. Step-by-step Solution

### Prerequisite: Setting up the Practice Environment
*If you are practicing on a fresh Linux instance, the required directory and files won't exist yet. Run this command to create the mock environment before starting:*

```bash
sudo mkdir -p /var/www/html/backend
cd /var/www/html/backend
sudo touch database.yml secrets.env old_startup.sh temp_debug.log
```
* **What:** Creates the `/var/www/html/backend` directory and generates several empty text files inside it.
* **Why:** We need these mock files to exist so you can practice copying, moving, and removing them without errors.
* **How:** `sudo mkdir -p` creates the directory tree. `cd` navigates into it. `sudo touch` creates empty versions of the target files.
* **Impact:** Prepares the starting state, ensuring your practice closely mirrors a real-world server deployment scenario.

**Step 1: Check your current directory to ensure you are in the application root**
```bash
pwd
```
* **What:** Prints the current working directory path.
* **Why:** You must absolutely confirm you are in the correct application folder before altering configurations.
* **How:** Simply typing `pwd` returns the absolute path.
* **Impact:** Prevents catastrophic mistakes like backing up or deleting files from the wrong environment (e.g., Staging vs. Production).

**Step 2: Create an archive folder for the backup**
```bash
mkdir backup_v1
```
* **What:** Creates a directory named `backup_v1`.
* **Why:** You need a designated place to store the old files safely.
* **How:** `mkdir [name]` creates a folder in the current directory.
* **Impact:** Keeps the workspace organized, ensuring rollback files are easy to find during an incident.

**Step 3: Copy multiple configuration files into the backup folder**
```bash
cp database.yml secrets.env backup_v1/
```
* **What:** Copies two sensitive target files into the `backup_v1` directory at once.
* **Why:** To preserve exactly how the environment was running before the new code drops.
* **How:** `cp [file1] [file2] [destination]` allows multiple source files to flow into one folder.
* **Impact:** This is your safety net. If the deployment fails, these files save the company from downtime.

**Step 4: Move an obsolete script completely out of the active folder**
```bash
mv old_startup.sh backup_v1/
```
* **What:** Moves the old script out of the current folder and places it into the backup.
* **Why:** We no longer want the system to accidentally execute this outdated startup script.
* **How:** `mv [file] [destination]` shifts the file instead of duplicating it.
* **Impact:** Ensures clean system initialization by removing deprecated scripts from the active path.

**Step 5: Safely remove a risky temporary file**
```bash
rm temp_debug.log
```
* **What:** Deletes the specific file `temp_debug.log`.
* **Why:** Temporary debug logs can sometimes contain sensitive passwords or customer data and must be cleaned up.
* **How:** `rm [file]` deletes it permanently.
* **Impact:** Enhances security by clearing out accidental local data leakage.

## 6. Expected Output
```text
$ pwd
/var/www/html/backend
$ mkdir backup_v1
$ cp database.yml secrets.env backup_v1/
$ mv old_startup.sh backup_v1/
$ rm temp_debug.log
$ ls backup_v1/
database.yml  old_startup.sh  secrets.env
```

## 7. Tips / Best Practices
* **Never skip backups:** Running a deploy without taking a manual or automated snapshot of the state is the #1 cause of extended downtime.
* **Interactive rm:** If you are nervous about deleting files, run `rm -i filename`. It will prompt you `rm: remove regular file 'filename'?` for safety.
* **Timestamped backups:** In real life, name your backups with dates: `mkdir backup_20260403`.

## 8. Interview Questions
1. **Q:** What does `pwd` stand for and why is it used?
   **A:** It stands for "print working directory." It's used to verify exactly where you are in the filesystem hierarchy.
2. **Q:** What happens if you run `cp folder_name backup_folder/` without any flags?
   **A:** It will throw an error because you cannot copy a directory without the `-r` (recursive) flag.
3. **Q:** How can you force `rm` to ask you yes/no before deleting every single file?
   **A:** By using the `-i` (interactive) flag: `rm -i file.txt`.

---
[⬅️ Previous: 01_linux_basics_file_management](01_linux_basics_file_management.md) | [Next ➡️: 03_permissions_and_ownership](03_permissions_and_ownership.md)
