# 1. Scenario: Archiving Application Source Code for Transfer

## 2. Real-world Context
You have a legacy frontend codebase sitting on an old server. Before decommissioning the server, you need to download all the website's source code to your local machine. Downloading thousands of small HTML, CSS, and JS files over the network individually would be extremely slow. You must compress the entire folder into a single, compact archive file first.

## 3. Objective
Use Linux archiving tools to bundle a large directory into a single compressed `.tar.gz` file for efficient off-server transfer.

## 4. Step-by-step Solution

### Prerequisite: Setting up the Practice Environment
*To practice compressing a large directory, let's create a simulated legacy application folder:*

```bash
sudo mkdir -p /var/www/legacy-app/css
sudo bash -c 'cat <<EOF > /var/www/legacy-app/index.html
<html><body>Hello World</body></html>
EOF'
sudo touch /var/www/legacy-app/css/style.css
sudo fallocate -l 500M /var/www/legacy-app/dummy_data.bin || sudo truncate -s 500M /var/www/legacy-app/dummy_data.bin
```
* **What:** Creates the `/var/www/legacy-app` directory structure and uses `fallocate` or `truncate` to create a 500MB dummy file inside it.
* **Why:** We need a realistically sized folder to compress so that the `tar` command has something substantial to work with and the output matches the expected 500M size.
* **How:** `mkdir` creates the folders, `cat` writes a mock HTML file, and `fallocate`/`truncate` allocates 500MB of space for a dummy binary file.
* **Impact:** Mocks a legacy web application, ensuring the compression exercise provides realistic feedback and sizes.

**Step 1: Check the folder size before compressing**
```bash
du -sh /var/www/legacy-app
```
* **What:** Checks the total size of the application directory contents.
* **Why:** You need an estimate of the size so you can ensure you have enough free disk space to store the compressed archive.
* **How:** `du` calculates directory size, `-s` summarizes, `-h` is human format.
* **Impact:** Prevents you from accidentally exhausting disk space by creating massive archive files blindly.

**Step 2: Create a compressed archive of the folder**
```bash
tar -czvf legacy-app-backup.tar.gz /var/www/legacy-app
```
* **What:** Zips and bundles the entire folder into a single file named `legacy-app-backup.tar.gz`.
* **Why:** A single file is drastically faster to transfer than 10,000 separate text files. The compression saves bandwidth.
* **How:** `tar` tape archive tool. `-c` = create, `-z` = compress with gzip, `-v` = verbose (show files on screen), `-f` = filename follows.
* **Impact:** The standard way everything in Linux is bundled—from application source code to database backups.

**Step 3: Verify the archive was created properly**
```bash
ls -lh legacy-app-backup.tar.gz
```
* **What:** Lists the new compressed file to verify its size.
* **Why:** Check if compression actually resulted in a smaller file size, guaranteeing success.
* **How:** List with human readable sizes.
* **Impact:** Gives confidence the bundle is ready for the network transfer.

**Step 4: (Optional Test) Extract the file to ensure it's not corrupt**
```bash
tar -xzvf legacy-app-backup.tar.gz -C /tmp/test-extract
```
* **What:** Unzips the generated file into a temporary `/tmp/test-extract` folder.
* **Why:** A backup is only useful if it can be successfully restored. Checking it prevents finding out it's broken a year later.
* **How:** `-x` = extract. The `-C` flag explicitly tells tar WHERE to put the extracted contents.
* **Impact:** Assures the integrity of the mission-critical archiving process.

## 6. Expected Output
```text
$ du -sh /var/www/legacy-app
500M    /var/www/legacy-app

$ tar -czvf legacy-app-backup.tar.gz /var/www/legacy-app
/var/www/legacy-app/
/var/www/legacy-app/index.html
/var/www/legacy-app/css/style.css
...

$ ls -lh legacy-app-backup.tar.gz
-rw-r--r-- 1 root root 120M Oct 27 09:00 legacy-app-backup.tar.gz
```

## 7. Tips / Best Practices
* **Know your flags:**
  `-c` = Create
  `-x` = Extract
  `-z` = Gzip (small size, makes `.tar.gz`)
  `-j` = Bzip2 (smaller size, makes `.tar.bz2`)
  `-f` = MUST be the last flag because the filename comes immediately after it!
* **Zip equivalent:** `zip` and `unzip` are also available in Linux, but `tar` is natively supported across all POSIX servers and preserves Linux-specific file permissions better.

## 8. Interview Questions
1. **Q:** What does `tar -czvf` mean?
   **A:** Create a new archive (`-c`), compress using GZip (`-z`), print output verbosely (`-v`), and write it to the specified filename (`-f`).
2. **Q:** How do you unzip an archive file named `data.tar.gz`?
   **A:** You extract it using `tar -xzvf data.tar.gz`.
3. **Q:** Why do we compress logs or folders before transferring them using SCP or SFTP?
   **A:** Transferring one single large file is vastly quicker than transferring thousands of tiny files because it drastically reduces network protocol overhead and I/O wait times.
