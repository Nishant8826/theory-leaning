# 1. Scenario: Setting Up the App Workspace

## 2. Real-world Context
You are a junior system administrator. A new web application called "Payment Gateway" is being deployed today. You need to create an organized folder structure for the application code, copy over a default configuration file from a template, rename it, and remove old temporary deployment files that are taking up space.

## 3. Objective
Set up the correct folder structure, securely move and copy necessary files, and clean up the environment without accidentally deleting system files.

## 4. Step-by-step Solution

### Prerequisite: Setting up a Dummy Template
*If you are practicing on a fresh Linux instance, the template file we need to copy later (`/etc/template/nginx.conf`) won't exist yet. Run this command before starting the main exercise:*

```bash
sudo mkdir -p /etc/template
sudo bash -c 'cat <<EOF > /etc/template/nginx.conf
worker_processes auto;

events {
    worker_connections 1024;
}

http {
    server {
        listen       80;
        server_name  localhost;

        location / {
            proxy_pass http://127.0.0.1:8080;
        }
    }
}
EOF'
```
* **What:** Creates an `/etc/template` directory and generates a basic NGINX configuration file inside it.
* **Why:** We need this dummy template file to exist on the server so that the copy (`cp`) command in Step 3 succeeds without error.
* **How:** `sudo mkdir -p` creates the folder with root permissions. `sudo bash -c 'cat <<EOF > ...'` uses a heredoc to elegantly write multiple lines directly into a protected system file block.
* **Impact:** Prepares the environment properly, guaranteeing that the learning commands operate identical to a real production system.

**Step 1: Create the main project directory**
```bash
mkdir -p /opt/payment-app/config
```
* **What:** Creates a new folder named `payment-app` with a subfolder `config`.
* **Why:** The app needs a dedicated, isolated space for its code and configuration.
* **How:** `mkdir` creates directories. The `-p` flag creates parent directories if they don't exist.
* **Impact:** Ensures the application is cleanly separated from other software on the server, which is crucial for maintenance.

**Step 2: Navigate into the new directory**
```bash
cd /opt/payment-app
```
* **What:** Changes your current working location to the newly created folder.
* **Why:** You need to work directly inside this folder for your next operations.
* **How:** `cd [path]` moves you to the specified path.
* **Impact:** Prevents you from accidentally modifying files in the wrong location.

**Step 3: Copy the template configuration file**
```bash
cp /etc/template/nginx.conf ./config/
```
* **What:** Copies a configuration template into your app's `config` folder.
* **Why:** Rather than writing a config from scratch, start with an approved company template to avoid syntax errors.
* **How:** `cp [source] [destination]`. The `./` means "current folder."
* **Impact:** Standardization. Using approved templates reduces production bugs.

**Step 4: Rename the copied config file**
```bash
mv ./config/nginx.conf ./config/payment.conf
```
* **What:** Changes the name of the file from `nginx.conf` to `payment.conf`.
* **Why:** We need an app-specific name so it doesn't conflict with other services.
* **How:** `mv [old_name] [new_name]` effectively renames the file.
* **Impact:** Prevents configuration overlap and server crashes caused by duplicate generic filenames.

**Step 5: Verify the folder contents**
```bash
ls -l ./config/
```
* **What:** Lists the contents of the `config` folder in long format.
* **Why:** To visually verify that the file was successfully copied and renamed.
* **How:** `ls` lists files, `-l` shows detailed info like size and dates.
* **Impact:** Trust but verify. Always check your work in production before proceeding.

**Step 6: Remove the old temporary files**
```bash
rm -rf /tmp/payment-old-deploy
```
* **What:** Deletes a directory containing old deployment data explicitly.
* **Why:** Old files consume disk space and can cause confusion during rollbacks.
* **How:** `rm` removes files. `-r` means recursive (for folders), `-f` forces deletion without asking.
* **Impact:** Keeps the server clean. (Warning: use with extreme caution in root directories!)

## 6. Expected Output
```text
$ mkdir -p /opt/payment-app/config
$ cd /opt/payment-app
$ cp /etc/template/nginx.conf ./config/
$ mv ./config/nginx.conf ./config/payment.conf
$ ls -l ./config/
total 4
-rw-r--r-- 1 sysadmin sysadmin 1024 Oct 24 10:00 payment.conf
$ rm -rf /tmp/payment-old-deploy
```

## 7. Tips / Best Practices
* **Avoid `rm -rf /`:** Never run forceful recursive deletions on root paths. Always double-check your target path.
* **Use `mkdir -p`:** It saves time by creating an entire folder tree at once without errors if the parent doesn't exist.
* **Relative paths:** Be mindful of using `./` and `../`. When in doubt, prefer absolute paths (like `/opt/payment-app`) to avoid executing commands in the wrong directory.

## 8. Interview Questions
1. **Q:** What does the `-p` flag do in the `mkdir` command?
   **A:** It creates any missing parent directories required by the path provided, preventing "directory not found" errors.
2. **Q:** How can you copy a file and preserve its original permissions?
   **A:** By using the `cp -p` command.
3. **Q:** What is the difference between `cp` and `mv`?
   **A:** `cp` duplicates the file, leaving the original intact. `mv` relocates or renames the file, removing the original from its source.

---
[Next ➡️: 02_file_operations_backup](02_file_operations_backup.md)
