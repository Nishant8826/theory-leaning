# 📦 Package Management: Installing Apps the Linux Way

In Windows, you download an `.exe` file and click "Next, Next, Next." In Linux, we use "Package Managers" (like an App Store for the terminal).

## 🛒 The Two Main Shops
Depending on your version of Linux, you'll use one of these:
1.  **APT (Advanced Package Tool):** Used in **Ubuntu** and **Debian**.
2.  **YUM / DNF:** Used in **CentOS** and **RedHat**.

---

## 🛠️ Package Management (Commands - Example using APT)
*   **`sudo apt update`:** Update the list of available software (Refreshing the shop's catalog).
*   **`sudo apt install git`:** Download and install Git.
*   **`sudo apt remove git`:** Uninstall software.
*   **`sudo apt upgrade`:** Update all installed apps to their newest versions.

## 🚀 Real-World DevOps Use Case
When you set up a new server for a website, you don't go to a browser to download things. You write a script that says:
`sudo apt update && sudo apt install nginx docker.io git -y`. 
This installs everything you need in seconds without a single click!

---

## ✍️ Hands-on Task
1. Search Google for "What package manager do I use for CentOS?".
2. Try to install the `sl` (Steam Locomotive) package: `sudo apt install sl`.
3. If it installs, type `sl` and watch what happens! (It's a fun prank command).

---
Previous: [10_service_management.md](10_service_management.md)  
Next: [12_networking.md](12_networking.md)
---
