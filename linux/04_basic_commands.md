# ⌨️ Basic Linux Commands (The Everyday Tools)

To talk to Linux, you need to learn its language. Here are the most common commands you'll use every single day.

## 1. Navigating and Viewing
*   **`pwd` (Print Working Directory):** "Where am I?"
    *   *Example:* `pwd` might show `/home/user/documents`.
*   **`ls` (List Files):** "Show me what's in here."
    *   *Example:* `ls -l` shows details like size and date.
*   **`cd` (Change Directory):** "Move to another room."
    *   *Example:* `cd /var/log` takes you to the logs folder.

## 2. Managing Files & Folders
*   **`mkdir` (Make Directory):** "Create a new folder."
    *   *Example:* `mkdir my_project`
*   **`touch` (Create File):** "Create an empty file."
    *   *Example:* `touch index.html`
*   **`cp` (Copy):** "Clone this file."
    *   *Example:* `cp file.txt backup.txt`
*   **`mv` (Move/Rename):** "Move this or change its name."
    *   *Example:* `mv old.txt new.txt`
*   **`rm` (Remove):** "Delete it." (Be careful!)
    *   *Example:* `rm file.txt` (Use `rm -r` for folders).

## 3. Reading and Cleaning
*   **`cat` (Concatenate):** "Show me what's inside the file."
    *   *Example:* `cat README.md`
*   **`clear`:** "Clean my messy screen."

---

## 🚀 DevOps Use Case
Imagine you need to deploy a website. You would:
1. `mkdir website` (Create a folder)
2. `cd website` (Enter it)
3. `touch index.html` (Create the file)
4. `ls` (Verify it's there)

---

## ✍️ Hands-on Task
1. Open your terminal.
2. Create a folder called `linux_practice`.
3. Inside it, create a file called `hello.txt`.
4. Copy `hello.txt` to `copy_of_hello.txt`.
5. List the files to see both.
6. Delete the original `hello.txt`.


### 💡 Dev Tip
*   `cp -r build/ /var/www/html/` to upload your React/Next.js production builds.

---
Prev: [03_filesystem_hierarchy.md](03_filesystem_hierarchy.md) | Index: [00_index.md](00_index.md) | Next: [06_user_management.md](06_user_management.md)
---
