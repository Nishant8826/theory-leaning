# 📌 Topic: Env Config and Secrets (Security)

## 🧠 Concept Explanation (Basic → Expert)
**Basic**: You use environment variables to change how your app works without changing the code (e.g., `DB_URL`). Secrets are sensitive variables like passwords that shouldn't be seen in the logs.
**Expert**: Configuration and Secret management is the implementation of **Separation of Concerns**. Staff-level engineering requires a "Secretless" approach where the container image is generic and environment-agnostic. Secrets should never be baked into the image or passed as standard environment variables (which are visible in `docker inspect`). Instead, they should be mounted as **Files in Memory (tmpfs)** or fetched from an **External Vault** (AWS Secrets Manager/HashiCorp Vault) at runtime.

## 🏗️ Mental Model
- **Config**: A recipe that says "Add Salt." (Public knowledge).
- **Secrets**: The combination to the safe where the salt is kept. (Private knowledge). You don't write the combination on the recipe card; you give the cook a temporary key to the safe.

## ⚡ Actual Behavior
- **Environment Variables**: Visible to anyone with access to the host or the Docker API. They can also leak into logs during crashes.
- **Docker Secrets**: (Swarm Mode) Secrets are encrypted at rest and only mounted into the container's memory (`/run/secrets/`). They never touch the disk.
- **Compose Secrets**: (Local) Compose simulates this by mounting a file from your host into the container.

## 🔬 Internal Mechanics (The tmpfs Mount)
1. When a Secret is used, Docker creates a temporary filesystem in RAM (**tmpfs**).
2. It writes the secret value to a file (e.g., `/run/secrets/db_password`).
3. The file is only visible to the container's namespace.
4. When the container stops, the RAM is wiped. The secret never left a trace on the host's physical disk.

## 🔁 Execution Flow
1. `docker compose up`.
2. Compose reads `db_password.txt`.
3. Compose creates a mount point in the container at `/run/secrets/db_password`.
4. App starts and reads the password from the file.
5. `docker inspect` shows the mount point, but NOT the password value.

## 🧠 Resource Behavior
- **Memory**: Secrets consume a tiny amount of RAM (usually <4KB).
- **Security**: Reduces the risk of "Log Leaking" where an app accidentally prints its entire environment to a log file.

## 📐 ASCII Diagrams (REQUIRED)

```text
       SECURE SECRET INJECTION
       
[ HOST DISK ]          [ CONTAINER RAM ]
(password.txt) --(Mount)--> [ /run/secrets/pw ]
      |                          |
      +----( Hidden from )-------+
      |      docker inspect      |
      v                          v
[ ENV VARS ]           [ APP PROCESS ]
(VISIBLE!)             (Reads from file)
```

## 🔍 Code (Safe Secret Handling)
```yaml
services:
  app:
    image: my-app:latest
    environment:
      # Pass the PATH to the secret, not the secret itself
      - DB_PASSWORD_FILE=/run/secrets/db_pw
    secrets:
      - db_pw

  db:
    image: postgres:15
    environment:
      - POSTGRES_PASSWORD_FILE=/run/secrets/db_pw
    secrets:
      - db_pw

secrets:
  db_pw:
    file: ./db_password.txt # In prod, this would be a Swarm/K8s secret
```

## 💥 Production Failures
- **The "Git Leak"**: A developer accidentally commits a `.env` file containing the production database password to GitHub. Within 5 minutes, a bot finds it and wipes the database.
  *Fix*: Always add `.env` to `.gitignore`.
- **The "Inspect Leak"**: An attacker gains "read-only" access to your Docker Engine API. They run `docker inspect` on your containers and find all your API keys and passwords listed in the `Env` section.

## 🧪 Real-time Q&A
**Q: Is `env_file` more secure than `environment`?**
**A**: No. Both result in variables being stored in the container's environment, making them visible to `docker inspect`. The only difference is that `env_file` keeps your YAML cleaner. Use **Secrets** (files) for actual sensitive data.

## ⚠️ Edge Cases
- **Application Support**: Some older applications only know how to read from environment variables and can't read from files. 
  *Workaround*: Use a small entrypoint script (`entrypoint.sh`) that reads the file and exports it as an environment variable just before starting the app.

## 🏢 Best Practices
- **Use `.env.example`**: Commit a template to Git, but never the actual values.
- **One Secret per File**: Don't put 10 passwords in one file.
- **Fail Fast**: If a required secret is missing, the container should exit immediately with a clear error message.

## ⚖️ Trade-offs
| Method | Ease of Use | Security |
| :--- | :--- | :--- |
| **Hardcoded** | **Highest** | Zero |
| **Env Vars** | High | Low |
| **Docker Secrets**| Medium | **High** |
| **External Vault**| Low | **Highest** |

## 💼 Interview Q&A
**Q: Why is it recommended to use Docker Secrets instead of environment variables for sensitive data?**
**A**: Environment variables are inherently insecure because they are visible in `docker inspect` and `docker history`, and they often leak into application logs or crash reports. Docker Secrets, on the other hand, are mounted as files in a temporary in-memory filesystem (`tmpfs`). This ensures that the secret never touches the host's physical disk and is not visible via standard Docker inspection tools. Additionally, it allows for better audit trails and access control in orchestrated environments like Swarm or Kubernetes.

## 🧩 Practice Problems
1. Create a Compose file that uses a secret to set a database password. Verify that the password is NOT visible in `docker inspect`.
2. Write a Node.js snippet that tries to read a secret from a file, with a fallback to an environment variable for local development.

---
Prev: [03_Local_Dev_Environment.md](./03_Local_Dev_Environment.md) | Index: [00_Index.md](../00_Index.md) | Next: [05_Scaling_with_Compose.md](./05_Scaling_with_Compose.md)
---
