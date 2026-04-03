# 1. Scenario: Filtering Application Error Logs

## 2. Real-world Context
Developers are complaining that the login system is randomly failing. You pull the raw application log file containing 100,000 lines. Attempting to scroll through the file manually is impossible. You need to leverage text processing tools to actively filter for "ERROR" words, extract the specific user IDs causing the failure, and replace some messy formatting output on the fly.

## 3. Objective
Search, parse, format, and manipulate raw text files using core Linux command-line utilities.

## 4. Step-by-step Solution

### Prerequisite: Setting up the Practice Environment
*To practice searching and filtering text, let's generate a mock application log file:*

```bash
cat <<EOF > app.log
2026-10-27 10:00:01 INFO System booted up normal
2026-10-27 10:00:05 ERROR USER_ID:9042 Login Failed
2026-10-27 10:01:10 INFO User uploaded file
2026-10-27 10:05:32 ERROR USER_ID:8422 Missing Token
2026-10-27 10:10:00 INFO System running healthy
EOF
```
* **What:** Uses a heredoc to create a file named `app.log` containing five lines of simulated server log data.
* **Why:** We need a structured text file containing both "INFO" and "ERROR" lines to successfully demonstrate `grep`, `awk`, and `sed`.
* **How:** `cat <<EOF > app.log` writes the block of text into the file in your current directory.
* **Impact:** Provides the exact dataset required so that your text parsing outputs match the examples perfectly.

**Step 1: Check the head and tail of the file to understand the structure**
```bash
head -n 5 app.log
```
* **What:** Prints only the top 5 lines of the log file. (Similarly, `tail` prints the bottom).
* **Why:** You need to see the column structure (e.g. timestamp, log level, message) before writing complex text parsers.
* **How:** `head -n [number] [file]`.
* **Impact:** Prevents wasting time hunting blindly. Fast diagnosis.

**Step 2: Isolate the "ERROR" lines**
```bash
grep "ERROR" app.log
```
* **What:** Scans the whole file and outputs exclusively the lines harboring the word "ERROR".
* **Why:** This filters out 99,000 useless "INFO" lines, shrinking the problem strictly to the failures.
* **How:** `grep [pattern] [file]`.
* **Impact:** The single most important command in a DevOps diagnostic toolkit. It turns a mountain of noise into targeted answers.

**Step 3: Extract a specific column with awk**
```bash
grep "ERROR" app.log | awk '{print $4}'
```
* **What:** Sends the filtered ERROR lines to `awk`, which extracts only the 4th column of text (separated by spaces).
* **Why:** If the 4th column contains the `UserID`, we only care about the UserIDs having problems, not the messy error trace.
* **How:** The pipe `|` sends output from the first command into `awk`. `$4` tells `awk` to print only the 4th space-separated word on the line.
* **Impact:** Isolates pure, actionable datasets from unstructured logs.

**Step 4: Use sed to replace and clean the text**
```bash
grep "ERROR" app.log | awk '{print $4}' | sed 's/USER_ID://g'
```
* **What:** Takes the output from step 3 (which looks like `USER_ID:5099`) and removes the `USER_ID:` part.
* **Why:** A developer just asked for a clean list of numbers to check against the database.
* **How:** `sed` is a stream editor. `'s/USER_ID://g'` means **s**ubstitute "USER_ID:" with nothing (empty), **g**lobally.
* **Impact:** Automates tedious data cleansing, looking like sheer magic to standard computer users.

## 6. Expected Output
```text
$ head -n 3 app.log
2026-10-27 10:00:01 INFO System booted up normal
2026-10-27 10:00:05 ERROR USER_ID:9042 Login Failed
2026-10-27 10:01:10 INFO User uploaded file

$ grep "ERROR" app.log
2026-10-27 10:00:05 ERROR USER_ID:9042 Login Failed
2026-10-27 10:05:32 ERROR USER_ID:8422 Missing Token

$ grep "ERROR" app.log | awk '{print $4}'
USER_ID:9042
USER_ID:8422

$ grep "ERROR" app.log | awk '{print $4}' | sed 's/USER_ID://g'
9042
8422
```

## 7. Tips / Best Practices
* **Power of the Pipe `|`:** The vertical bar connects the output of one command to the input of another. This allows chaining commands to build limitless mini-scripts on the fly.
* **Case insensitivity:** Use `grep -i "error"` to match "error", "ERROR", and "Error".
* **Sort and Unique:** Add `| sort | uniq -c` to the very end of that long command chain to count how many times each user failed!

## 8. Interview Questions
1. **Q:** What does `awk '{print $2}'` mean?
   **A:** Awk splits a string by spaces and prints the second word on every line passed into it.
2. **Q:** What is the pipe `|` used for in Linux?
   **A:** It takes the standard output (`stdout`) of the command to its left and uses it as the standard input (`stdin`) for the command on its right.
3. **Q:** What command would you use to replace all instances of "apple" with "orange" in a text stream?
   **A:** `sed 's/apple/orange/g'`

---
[⬅️ Previous: 07_file_compression_archiving](07_file_compression_archiving.md) | [Next ➡️: 09_searching_files_logs](09_searching_files_logs.md)
