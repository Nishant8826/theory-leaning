# 🏋️ Practice Linux Commands

Now it's time to get your hands dirty. Follow these steps to practice the workflow of a DevOps engineer.

## 🎯 The Mission: Prepare a Log Directory
Imagine you are setting up a folder to store logs for a new web application.

### Step 1: Create the Folder
```bash
mkdir -p my_app/logs
```
*Tip: `-p` creates the parent folder if it doesn't exist.*

### Step 2: Navigate and Verify
```bash
cd my_app/logs
pwd
```

### Step 3: Create Mock Log Files
```bash
touch error.log access.log
ls
```

### Step 4: Write some "Errors" to the file
```bash
echo "ERROR: Database connection failed at 12:00" >> error.log
echo "ERROR: Password incorrect at 12:05" >> error.log
```

### Step 5: Search for specific errors
```bash
grep "12:05" error.log
```

## 🛠️ Handy Shortcuts (Must Know!)
- **TAB**: Press TAB to auto-complete filenames. (Saves hours of typing).
- **UP ARROW**: See the last command you typed.
- **CTRL + C**: Stop a command that is stuck.
- **CTRL + L**: Clear the screen.

## ⚠️ Common Mistakes
- **Deleting the wrong thing**: `rm -rf /` will delete your entire system. Never run it!
- **Wrong Case**: `cd Document` won't work if the folder is named `Documents`.
- **Spaces**: Avoid spaces in filenames (User `my_file.txt` instead of `my file.txt`).

## ✍️ Final Task
1. Run `df -h` to see how much space is left on your machine.
2. Run `whoami` to see your current Linux username.

---
Prev: [11_linux_unix_commands_in_devops.md](11_linux_unix_commands_in_devops.md) | Next: NA
