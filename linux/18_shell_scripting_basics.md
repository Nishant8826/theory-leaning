# 📜 Shell Scripting Basics: The Magic Spellbook

If commands are like individual words, a **Script** is a story. It's a way to tell the computer to do 10 things in a row by typing only 1 word.

## 🧙 What is Scripting?
Imagine you make coffee every morning.
*   **Command:** Boil water.
*   **Command:** Add coffee.
*   **Command:** Add milk.
*   **Script:** "Morning Coffee Routine" (Does all of the above automatically).

---

## 🚀 Anatomy of a Script (`script.sh`)
```bash
#!/bin/bash
# That first line is called a "Shebang" - it tells Linux to use Bash to run this.

NAME="DevOps Ninja"
echo "Hello, $NAME!"
echo "Today is $(date)"
echo "Listing my files..."
ls -l
```

## 🛠️ How to run it:
1.  **Create:** `vi myscript.sh`
2.  **Write content.**
3.  **Permissions:** `chmod +x myscript.sh` (Give it the "power" to run).
4.  **Run:** `./myscript.sh`

---

## 💡 Why Scripting matters in DevOps
DevOps is all about "Automation." Instead of manually creating a database every time, we write a script that does it perfectly every time. This prevents human errors and saves hours of manual work!

---

## ✍️ Hands-on Task
1. Create a file called `backup.sh`.
2. Put this content inside:
   ```bash
   #!/bin/bash
   echo "Starting backup of documents..."
   cp -r ~/Documents ~/Documents_Backup
   echo "Backup complete!"
   ```
3. Run `chmod +x backup.sh` and then `./backup.sh`.

## 🧠 Core Concepts Summary
*   **What:** Writing files with sequential chains of shell logic `.sh` (loops, variables) to automate repetitive terminal chores.
*   **Why:** Performing identical 10-step server deployments manually creates inevitable human error and exhausts time.
*   **How:** You wrap standard commands in bash logic structures and invoke them natively (`./deploy.sh`) or via temporal triggers like `cron`.
*   **Impact:** The literal backbone of DevOps automation—allowing scripts to handle routine backups, disk cleaning, and scaling configurations dynamically.

---
Prev: [17_vi_editor.md](17_vi_editor.md) | Index: [00_index.md](00_index.md) | Next: [19_advanced_commands.md](19_advanced_commands.md)
---
