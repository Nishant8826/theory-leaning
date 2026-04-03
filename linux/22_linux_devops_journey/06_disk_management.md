# 1. Scenario: Server Disk is 100% Full

## 2. Real-world Context
Your database has abruptly crashed with a "No space left on device" error message. The entire company website is down because no data can be written. You logged onto the server and must immediately determine which hard drive partition is full, and locate the bloated file taking up all the room.

## 3. Objective
Check system disk space, identify the full partition, and track down the largest subdirectories eating up storage.

## 4. Step-by-step Solution

### Prerequisite: Setting up the Practice Environment
*To practice locating large files, let's create a simulated large log file safely inside the `/var/log` directory:*

```bash
sudo mkdir -p /var/log
sudo truncate -s 48G /var/log/nginx-error.log
```
* **What:** Uses the `truncate` command to instantly create a simulated 48-Gigabyte file named `nginx-error.log`.
* **Why:** We need a large target file to exist so the `ls -S` commands actually have a massive file to discover and sort.
* **How:** The `truncate -s 48G` command creates a "sparse file" which pretends to be 48GB in size to `ls`, without actually consuming real hard drive space (Note: `du -sh` might show 0 usage unless run as `du -sh --apparent-size`). 
* **Impact:** Safely mimics a critical storage failure scenario without actually filling your server's disk.

**Step 1: Check overall disk space on all mounted filesystems**
```bash
df -h
```
* **What:** Displays the available and used disk space of all your drives.
* **Why:** You need to know exactly which disk partition is hitting 100% usage before you can fix it.
* **How:** `df` stands for Disk Free. The `-h` flag makes sizes "human readable" (Megabytes, Gigabytes) rather than raw blocks.
* **Impact:** In one glance, you find out if it's the root (`/`) directory or a separate attached mount (like `/data`).

**Step 2: Navigate to the full partition**
```bash
cd /var
```
* **What:** Changes your directory to the `/var` folder, which is where logs heavily accumulate.
* **Why:** Assuming `df -h` showed the root partition is full, `/var` is statistically the most likely culprit.
* **How:** Basic navigation.
* **Impact:** Puts you in position to start pinpointing the fat files.

**Step 3: Find the largest directories inside /var**
```bash
sudo du -sh *
```
* **What:** Evaluates the total size of every folder and file in your current location.
* **Why:** You know `/var` is big, but is it the database folder, the docker folder, or the log folder causing the issue?
* **How:** `du` means Disk Usage. `-s` means summarize (don't list every file inside, just total), `-h` means human readable, `*` means check everything here.
* **Impact:** Instantly targets the exact application causing the storage leak.

**Step 4: Drill down further to find the explicit file**
```bash
cd log
ls -lhSr
```
* **What:** Changes to the `log` folder and lists files sorted by size.
* **Why:** If the `log` folder showed 50GB worth of usage, you need to find the specific 50GB file.
* **How:** `ls -l` is list. `-h` is human readable. `-S` sorts by size. `-r` reverses it so the LARGEST file is at the very bottom (closest to your eyes).
* **Impact:** You discover `nginx-error.log` is suddenly 48GB. You found the killer!

**Step 5: Empty the heavy log file to restore service**
```bash
> nginx-error.log
```
* **What:** Truncates the file to 0 bytes without deleting the actual file itself.
* **Why:** If you use `rm` to delete the file, Nginx might still hold the file open in memory and space won't be freed! Emptying it is much safer.
* **How:** Placing an empty redirect `>` directly into the file name clears its contents instantly.
* **Impact:** Immediately restores disk space to 50%, bringing the database back online and saving the company outage.

## 6. Expected Output
```text
$ df -h
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1        50G   50G     0 100% /
/dev/sdb1       100G   20G   80G  20% /data

$ cd /var; sudo du -sh *
200M    cache
48G     log
100M    lib

$ cd log; ls -lhSr
-rw-r--r-- 1 root root  12K Oct 26 12:00 messages
-rw-r--r-- 1 root root 48G Oct 26 12:45 nginx-error.log

$ > nginx-error.log
$ df -h /
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1        50G    2G   48G   4% /
```

## 7. Tips / Best Practices
* **Don't `rm` logs in use:** If you `rm` a log file that a background service is currently writing to, Linux won't free the space until you restart the service! Always truncate with `> filename`.
* **Combining commands line:** `du -sk * | sort -n` is an older, classic way to sort sizes from smallest to largest.
* **Log Rotation:** The permanently correct way to prevent this scenario is to set up a `logrotate` rule so files never grow forever.

## 8. Interview Questions
1. **Q:** What does `df -h` show compared to `du -sh`?
   **A:** `df` reports system-wide disk space usage based on filesystem mounts, while `du` scans and calculates the size of specific directories and files.
2. **Q:** Your disk is 100% full. You delete a 10GB log file using `rm`, but `df -h` still shows the disk space is at 100%. Why?
   **A:** A process is still holding the deleted file open in memory. The space won't truly free until you restart the parent process, or you should have truncated the file instead.
3. **Q:** What does the `-h` flag do in both `df` and `du`?
   **A:** It formats the output into human-readable sizes like KB, MB, or GB instead of raw block/byte numbers.

---
[⬅️ Previous: 05_process_management](05_process_management.md) | [Next ➡️: 07_file_compression_archiving](07_file_compression_archiving.md)
