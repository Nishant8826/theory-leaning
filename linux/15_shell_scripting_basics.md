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

---
Prev: [14_vi_editor.md](14_vi_editor.md) | Index: [00_index.md](00_index.md) | Next: [05_advanced_commands.md](05_advanced_commands.md)
---
