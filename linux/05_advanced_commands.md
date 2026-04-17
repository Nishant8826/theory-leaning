# ⚡ Advanced Linux Commands (The Power Tools)

Once you know the basics, it's time to learn the commands that save DevOps engineers hours of work.

## 🔍 Finding & Searching (The Detectives)
*   **`grep`:** Search for specific text inside a file.
    *   *Example:* `grep "error" server.log` (Finds every line containing "error").
*   **`find`:** Search for files or folders by name or date.
    *   *Example:* `find /home -name "*.jpg"` (Finds all JPG images).

## 🛠️ Editing & Processing (The Surgeons)
*   **`awk`:** A powerful tool for handling text columns (like a mini Excel in the terminal).
    *   *Example:* `ls -l | awk '{print $9}'` (Only shows the 9th column - the filenames).
*   **`sed`:** Find and replace text automatically.
    *   *Example:* `sed -i 's/blue/red/g' config.txt` (Changes all "blue" to "red" inside the file).

## 📦 Archiving & Permissions
*   **`tar`:** Bundle multiple files into one "archive" package.
    *   *Example:* `tar -cvf backup.tar my_folder`
*   **`chmod` & `chown`:** Change who can read/write a file (covered more in Topic 07).

## 🌐 Networking & Others
*   **`curl`:** Download files or test websites.
    *   *Example:* `curl https://google.com`
*   **`sudo`:** "Do this as the admin." (The "Please" command for the computer).

---

## 💡 Real-World Scenario
Your server is running slow because a log file is too big. You use `grep` to find common errors, `tar` to compress old logs, and `rm` to delete the useless ones.

---

## ✍️ Hands-on Task
1. Create a file called `data.txt` with the text "Linux is awesome".
2. Use `grep "Linux" data.txt` to find the line.
3. Try to use `find . -name "*.txt"` to see all text files in your current folder.

---
Prev: [15_shell_scripting_basics.md](15_shell_scripting_basics.md) | Index: [00_index.md](00_index.md) | Next: [20_linux_cheatsheet.md](20_linux_cheatsheet.md)
---
