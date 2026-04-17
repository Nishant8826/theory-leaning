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
*   **`tar`:** Bundle multiple files into one single "archive" package (similar to a `.zip` file).
    *   *Example:* `tar -cvf backup.tar my_folder`
    *   *What the flags mean (`-cvf`):*
        *   **`-c` (Create):** Tells the system you want to *create* a new archive file.
        *   **`-v` (Verbose):** "Talkative mode." The terminal will print out the name of every single file as it packs it, so you can see exactly what is happening.
        *   **`-f` (File):** Tells the command that the very next word (`backup.tar`) is the name of the new file. *(Always put `-f` last!)*
        *   ***Bonus Note:*** `tar` only groups files together. To make them strictly *smaller*, add `-z` (`-czvf`) to "zip" it into a `.tar.gz` file!
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

## 🧠 Core Concepts Summary
*   **What:** Evolving beyond basic interactions to leverage pipeline operators (`|`), structured find utilities (`find`), and streaming parsers (`awk`, `sed`).
*   **Why:** Extracting 3 unique IDs from 1,000,000 lines of chaotic logs manually is impossible; you require text-manipulation powerhouses.
*   **How:** Splicing commands perfectly together: locating a file, passing its content through a regex filter, and writing out statistics instantly.
*   **Impact:** Demonstrates supreme environment mastery, allowing engineering leads to conjure data insights instantaneously without complex code.

---
Prev: [18_shell_scripting_basics.md](18_shell_scripting_basics.md) | Index: [00_index.md](00_index.md) | Next: [20_linux_cheatsheet.md](20_linux_cheatsheet.md)
---
