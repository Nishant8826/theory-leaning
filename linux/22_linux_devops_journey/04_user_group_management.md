# 1. Scenario: Onboarding a New Engineer

## 2. Real-world Context
Your company has just hired a new Junior Developer named Alice. She needs access to the main development server to start contributing. However, she should only have access to specific developer resources and should firmly be placed within the `developers` group so that she can collaborate on shared company codebases securely.

## 3. Objective
Create a new user, assign them a password, create a specific user group, and attach the user to that group.

## 4. Step-by-step Solution

**Step 1: Create the new 'developers' group**
```bash
sudo groupadd developers
```
* **What:** Creates a new group named `developers` entirely from scratch.
* **Why:** Using groups is the most efficient way to manage bulk permissions. Instead of setting permissions for 50 individual users, you give permissions to the group once.
* **How:** `sudo groupadd [group_name]`.
* **Impact:** Sets up role-based access control (RBAC), a foundational Linux security standard in enterprise systems.

**Step 2: Create the user 'alice'**
```bash
sudo useradd -m -s /bin/bash alice
```
* **What:** Creates the user account `alice` with a home directory and sets her default shell to Bash.
* **Why:** She needs her own isolated space (`/home/alice`) to store her personal files and configs without interfering with root or other users.
* **How:** `useradd` creates the user. `-m` creates the home directory. `-s /bin/bash` defines the default terminal shell she will get when she logs in.
* **Impact:** Provides a secure, auditable individual login. Sharing accounts ("admin") is a huge security risk.

**Step 3: Set a password for alice**
```bash
sudo passwd alice
```
* **What:** Assigns a security password to `alice`.
* **Why:** An account is completely inaccessible remotely until it has authentication credentials set up.
* **How:** Executing `passwd [user]` prompts the system to securely request the new password twice.
* **Impact:** Alice can now log into the server securely using SSH or console.

**Step 4: Add alice to the 'developers' group**
```bash
sudo usermod -aG developers alice
```
* **What:** Appends Alice to the `developers` group without removing her from any existing standard groups.
* **Why:** So she can access files that the development team shares.
* **How:** `usermod` modifies a user. `-a` means "append", `-G` stands for "supplementary groups."
* **Impact:** Alice inherits all the access rights assigned to the developers team immediately.

**Step 5: Verify user creation and groups**
```bash
id alice
```
* **What:** Displays user ID, primary group ID, and supplementary groups for the user.
* **Why:** Always double-check your changes. If the `-a` flag was missed in the previous step, you would have wiped out her other group memberships!
* **How:** `id [username]`.
* **Impact:** Confirms the ticket is successfully completed before you email Alice her credentials.

## 6. Expected Output
```text
$ sudo groupadd developers
$ sudo useradd -m -s /bin/bash alice
$ sudo passwd alice
New password:
Retype new password:
passwd: password updated successfully
$ sudo usermod -aG developers alice
$ id alice
uid=1001(alice) gid=1001(alice) groups=1001(alice),1002(developers)
```

## 7. Tips / Best Practices
* **Dangers of `usermod -G`:** If you forget the `-a` (append) flag and just write `usermod -G developers alice`, it will REMOVE alice from the `sudo` group or any other groups she was in! ALWAYS use `-aG`.
* **Locking accounts:** If Alice leaves the company, use `sudo passwd -l alice` to lock her account without deleting her files.
* **Check `/etc/passwd`:** All user accounts are registered in the `/etc/passwd` file.

## 8. Interview Questions
1. **Q:** What file stores user account information in Linux?
   **A:** The `/etc/passwd` file stores basic user information, while `/etc/shadow` securely stores the encrypted passwords.
2. **Q:** Why must you include `-a` when using `usermod -G`?
   **A:** The `-a` (append) flag ensures the user is added to the new group without being removed from their current secondary groups.
3. **Q:** How can you delete a user and their home directory simultaneously?
   **A:** Using the command `userdel -r username`.
