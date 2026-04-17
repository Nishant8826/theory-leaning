# 🔑 SSH Key Management: The Secure Keycard

How do you enter a high-security lab? You either use a password (old way) or a **Keycard** (secure way). SSH keys are your keycards for the internet.

## 🛡️ What is SSH? (Secure SHell)
SSH is a way to log into a remote computer (like a server in Amazon AWS) and run commands as if you were sitting right in front of it.

## 🗝️ Public vs Private Key (The Two Parts)
1.  **Private Key (`id_rsa`):** This stays on your laptop. NEVER SHARE THIS! It's the "Key" in your pocket.
2.  **Public Key (`id_rsa.pub`):** This goes onto the server. It's the "Lock" on the door.

---

## 🛠️ Step-by-Step (Commands)
1.  **Generate a Key:** `ssh-keygen -t rsa -b 4096`. (Press Enter for everything).
2.  **See your Key:** `cat ~/.ssh/id_rsa.pub`. 
3.  **Use your Key:** You must copy the text from the public key and add it to your cloud providers.
    *   **On GitHub:**
        1. Go to **Settings** -> **SSH and GPG keys**.
        2. Click **New SSH Key**.
        3. Paste the contents of `id_rsa.pub` into the "Key" box and save.
    *   **On AWS EC2 (Management Console):**
        1. Go to **EC2 Dashboard** -> **Key Pairs**.
        2. Click **Actions** -> **Import key pair**.
        3. Give it a name, paste the `id_rsa.pub` text into the box, and click Import.
    *   **On an existing Linux Server:**
        *   Paste the public key as a new line at the bottom of the `~/.ssh/authorized_keys` file for the user you want to log in as.
4.  **Connect:** `ssh username@server_address` (No password needed - the key handles it!).

## 🚀 Real-World DevOps Use Case: Onboarding a Remote Worker

**Scenario:** Mary is a remote developer. As the Server Administrator, you need to give her access to your AWS EC2 instance without giving her your own private key, and without using insecure passwords.

**Step 1: Mary's Task (On her laptop at home)**
1. Mary runs `ssh-keygen` on her own local laptop to generate her personal keypair.
2. She views her public "Lock": `cat ~/.ssh/id_rsa.pub`.
3. She copies that text and sends it to you (the Admin) over Slack or email. *(She keeps the private key completely secret!)*

**Step 2: Admin's Task (On the Cloud Server)**
1. You log into the server using your admin account.
2. Create her user account: `sudo useradd -m mary`
3. Switch to her user to set up her files: `sudo su - mary`
4. Create the hidden SSH folder: `mkdir -p ~/.ssh`
5. Open the keys file: `nano ~/.ssh/authorized_keys`
6. **Paste the public key** text Mary sent you into this file and save it (`Ctrl+O`, `Enter`, `Ctrl+X`).
7. Secure the permissions (otherwise SSH will reject the connection):
   `chmod 700 ~/.ssh`
   `chmod 600 ~/.ssh/authorized_keys`

**Step 3: Mary Connects!**
Mary can now open her terminal at home and type `ssh mary@your_server_ip`. Her laptop will automatically use her private key to unlock the public "lock" you just placed on the server. She logs in instantly!

---

## ✍️ Hands-on Task
1. Look into your `.ssh` folder by typing `ls -a ~/.ssh`.
2. See if you already have any keys (Look for files starting with `id_`).
3. If not, try creating one using `ssh-keygen`.


### 💡 Dev Tip
*   Use `scp` to quickly sync `.env` files or application builds to your AWS EC2 instances securely for uploading build to EC2.

## 🧠 Core Concepts Summary
*   **What:** Creating cryptographic public/private key pairs to securely authenticate into remote machines without typing passwords.
*   **Why:** Human-made passwords are brute-forceable and inherently insecure; 2048-bit RSA keys are mathematically impenetrable.
*   **How:** Using `ssh-keygen` locally, pushing the lock part (`id_rsa.pub`) into the server's `~/.ssh/authorized_keys`, and letting cryptography verify your identity.
*   **Impact:** Radically hardens server entrance boundaries and enables zero-touch automated CI/CD pipeline deployments.

---
Prev: [14_system_monitoring.md](14_system_monitoring.md) | Index: [00_index.md](00_index.md) | Next: [16_networking.md](16_networking.md)
---
