# 📚 Interview Preparation Knowledge Base

> A structured collection of high-quality interview questions across various domains, designed for senior engineering roles.

---

## 📋 Topics

| # | Topic | Documentation | Status |
| :--- | :--- | :--- | :--- |
| 01 | **JavaScript** | [View Prep Material](./01_Javascript.md) | ✅ Completed |
| 02 | **Node.js** | [View Prep Material](./02_Nodejs.md) | ✅ Completed |

---

## 🛠️ Knowledge Base Generator

Use the prompt below to generate new topic files. This ensures consistency in structure, quality, and navigation across the entire repository.

### 📝 The Prompt

<details>
<summary>Click to expand and copy the prompt</summary>

```text
You are a senior interviewer, domain expert, and hiring manager.

Your task is to generate interview questions and maintain a structured knowledge base.

--------------------------------------------------

INPUT:
- File Number: [FILE_NUMBER]   (e.g., 01, 02, 03)
- Topic Name: [TOPIC_NAME]

--------------------------------------------------

OUTPUT REQUIREMENTS:

### PART 1 — MAIN FILE

1. Create a Markdown (.md) file.

2. File structure:
   - Folder: Interview-prep
   - File name:
     [FILE_NUMBER]_[TOPIC_NAME].md

3. Start with:

# 🚀 Interview Preparation - [TOPIC_NAME]

> **Domain:** Web Development / Frontend & Backend  
> **Level:** Beginner to Expert  
> **Target Role:** Software Engineer / Senior Engineer / Lead

---

4. Generate ~100 high-quality interview questions.

5. Cover all levels:
   - Beginner
   - Intermediate
   - Advanced
   - Expert

6. Structure:

## 🟢 Beginner Level

### ❓ Q1. **Question**

<details>
<summary><b>👀 Show Answer</b></summary>

Answer...

> 💡 **Interviewer Focus:** Key points...

</details>

<hr/>

### ❓ Q2. **Question**
*(No answer provided. Discuss [topic].)*

<hr/>

## 🟡 Intermediate Level
...

## 🔴 Advanced Level
...

## 🟣 Expert Level
...

7. Question types:
   - Conceptual
   - Scenario-based
   - Debugging
   - System design
   - Deep "why/how"

8. For at least 25–30 key questions:
   - Provide strong answers
   - Include key interviewer points (`> 💡 **Interviewer Focus:**`)

9. IMPORTANT UI:
   - Use `<details>` and `<summary><b>👀 Show Answer</b></summary>`
   - Use `<hr/>` after every question
   - Make questions bold
   - Answers hidden by default

10. Keep content:
   - Non-repetitive
   - Practical
   - Interview-focused

--------------------------------------------------

### NAVIGATION SECTION (MANDATORY)

At the END of the file, add:

---

### 🧭 Navigation

| ⬅️ Previous | 🏠 Index | ➡️ Next |
| :--- | :---: | ---: |
| [⬅️ <Previous Topic>](./<PREV_FILE>.md) | [Home](./00_Index.md) | [➡️ <Next Topic>](./<NEXT_FILE>.md) |

Rules:
- If previous file is unknown, write: `🚫 *None*` in the Previous column.
- If next file is unknown, write: `🚫 *None*` in the Next column.
- Replace placeholders correctly using numbering

Example:

### 🧭 Navigation

| ⬅️ Previous | 🏠 Index | ➡️ Next |
| :--- | :---: | ---: |
| [⬅️ Docker](./01_Docker.md) | [Home](./00_Index.md) | [➡️ Kubernetes](./03_Kubernetes.md) |

--------------------------------------------------

### PART 2 — UPDATE INDEX FILE

File: Interview-prep/00_Index.md

1. Maintain:

# Interview Preparation Index

---

## Topics

- [01 - Docker](./01_Docker.md)
- [02 - Kubernetes](./02_Kubernetes.md)

2. Rules:
- Keep sorted by number
- No duplicates
- Clean format

--------------------------------------------------

FINAL OUTPUT RULE:

Return TWO sections:

1. File: Interview-prep/[FILE_NUMBER]_[TOPIC_NAME].md
2. File: Interview-prep/00_Index.md

No extra explanation.
Everything must be copy-paste ready.
```

</details>

---
*Maintained by Senior Interviewer AI*