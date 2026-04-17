# 💾 Storage & Disk Management: The Warehouse

In cloud environments (like AWS EC2), you will frequently need to attach new hard drives (EBS volumes) when your database grows. Linux doesn't automatically use new drives; you must prepare them!

## 📦 The 3 Steps of Disk Management
Whenever you add a new disk, you must:
1. **Find it:** Identify the new raw disk.
2. **Format it:** Put a filesystem on it (like building shelves in an empty warehouse).
3. **Mount it:** Attach the formatted disk to a folder so you can save files there.

## 🛠️ The Commands
*   **`lsblk` (List Block Devices):** Shows all attached hard drives. Your new AWS drive might show up as `/dev/nvme1n1` or `/dev/xvdf`.
*   **`mkfs.ext4 /dev/nvme1n1`:** Formats the drive using the `ext4` filesystem. *(Warning: This destroys any existing data on that drive!)*
*   **`mount /dev/nvme1n1 /mnt/data`:** Attaches the drive to the `/mnt/data` folder. Anything you drop into `/mnt/data` is now stored on the new drive!

## 🚀 Persistent Mounting (`/etc/fstab`)
If you reboot the server, mounts disappear! To make it permanent, you must configure the `/etc/fstab` (File System Table) file. 

*   **DevOps Tip:** Always be extremely careful editing `/etc/fstab`. A typo can prevent your server from booting!

## 🧠 Core Concepts Summary
*   **What:** The mechanics of integrating brand-new, raw physical or virtual disk blocks exclusively into logical filesystem availability.
*   **Why:** When AWS databases max out capacity organically, you must append new block storage dynamically without destroying current infrastructure.
*   **How:** By identifying the hardware (`lsblk`), laying down an ext4 structure (`mkfs`), and integrating it securely (`mount` and `fstab`).
*   **Impact:** Empowers total independence regarding cloud administration—securing infinite horizontal scaling capabilities for robust persistent application states.

---
Prev: [22_web_servers_nginx.md](22_web_servers_nginx.md) | Index: [00_index.md](00_index.md) | Next: [24_security_firewalls.md](24_security_firewalls.md)
---
