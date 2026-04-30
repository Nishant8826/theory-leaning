# 📌 Topic: Compose Profiles and Environment Variables

🟢 **Simple Explanation (Beginner)**
-----------------------------------
Imagine you have a **Swiss Army Knife**. 
- You don't always need the scissors, the saw, and the corkscrew open at the same time. You only open what you need for the task.

**Compose Profiles** allow you to group your services. You can have a "Dev" profile that includes a debugger, and a "Prod" profile that doesn't. 

**Environment Variables** are like **Post-it Notes** on the wall. Instead of changing the "blueprint" (the YAML code) every time you move to a new server, you just change the Post-it note (e.g., `DB_PASSWORD=secret`).

🟡 **Practical Usage**
-----------------------------------
### 1. Using a `.env` file
Docker Compose automatically looks for a file named `.env` in the same folder.
```bash
# .env file
DB_USER=admin
DB_PASS=supersecret
```
In your YAML:
```yaml
services:
  db:
    image: postgres
    environment:
      - POSTGRES_USER=${DB_USER}
      - POSTGRES_PASSWORD=${DB_PASS}
```

### 2. Using Profiles
```yaml
services:
  web:
    image: my-app
  
  phpmyadmin:
    image: phpmyadmin
    profiles: ["debug"] # This service won't start by default!
```
**To start with profiles:**
```bash
docker compose --profile debug up
```

🔵 **Intermediate Understanding**
-----------------------------------
### Variable Substitution
You can set default values in your YAML:
`${DB_PORT:-5432}`
- If `DB_PORT` is set in the environment, use it.
- Otherwise, use `5432`.

### Precedence (The "Who Wins?" Rule)
If you define the same variable in multiple places, here is the order of who wins:
1. **CLI Environment** (`export DB_PASS=...`) **<- WINNER**
2. **The `.env` file**
3. **The Dockerfile `ENV` instruction**
4. **Default values in the YAML**

🔴 **Internals (Advanced)**
-----------------------------------
### How Compose loads `.env`
Compose reads the `.env` file *before* it parses the YAML. This means you can even use variables to change the image name or the project name:
`image: myapp:${APP_VERSION}`

### Passing the Host's Environment
If you define a variable in the YAML but don't give it a value, Compose will "steal" it from your actual computer's shell:
```yaml
environment:
  - API_KEY # No value here! Compose will look for $API_KEY on your laptop.
```

⚫ **Staff-Level Insights**
-----------------------------------
### The Security Trap
**Staff Warning**: Never commit your `.env` file to Git. 
**Solution**: Commit a `.env.example` file with empty values, and use a "Secrets Manager" (like HashiCorp Vault or AWS Secrets Manager) to populate the real `.env` during the CI/CD build process.

### Environment-Specific Overrides
Instead of one massive YAML file with 50 profiles, use **Override Files**.
- `docker-compose.yml` (Base config)
- `docker-compose.override.yml` (Local dev changes - loaded automatically)
- `docker-compose.prod.yml` (Production changes)

**Command:**
`docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d`

🏗️ **Mental Model**
- **Profiles**: **Logical Switches** for groups of services.
- **Env Vars**: **Settings** for those services.

⚡ **Actual Behavior**
Compose "interpolates" (replaces) all `${VAR}` strings in the YAML with their actual values before sending the final configuration to the Docker API.

🧠 **Resource Behavior**
- **Memory**: Using hundreds of environment variables has negligible impact on memory, but it makes debugging harder.

💥 **Production Failures**
- **The "Undefined Variable" Failure**: You used `${DB_PASS}` but forgot to put it in the `.env` file. Compose might replace it with an empty string, and your database will fail to start because the password is empty.
- **Variable Type Confusion**: You set `PORT=8080` in `.env`, but the YAML interprets it as a number instead of a string, causing a parsing error.

🏢 **Best Practices**
- Use profiles for "optional" tools like Admin panels, Swagger UI, or Debuggers.
- Use a `.env` file for local development to avoid huge CLI commands.
- Use the `${VAR:-default}` syntax to prevent crashes if a variable is missing.

🧪 **Debugging**
```bash
# See the final YAML with all variables replaced
docker compose config

# Check variables inside a running container
docker exec <id> env
```

💼 **Interview Q&A**
- **Q**: How do you keep a service from starting by default in Compose?
- **A**: Use the `profiles` key in the service definition.
- **Q**: What happens if I have a variable in my shell and the same one in my `.env` file?
- **A**: The one in your shell wins.

---
Prev: [23_Managing_Multi_Container_Applications.md](23_Managing_Multi_Container_Applications.md) | Index: [00_Index.md](../00_Index.md) | Next: [../Internals/25_Linux_Namespaces_The_Isolation_Engine.md](../Internals/25_Linux_Namespaces_The_Isolation_Engine.md)
---
