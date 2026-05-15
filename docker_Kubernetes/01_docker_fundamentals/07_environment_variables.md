# Environment Variables

## Why This Exists
In software development, you should never hardcode configuration values (like database URLs, API keys, or feature flags) into your source code. This is especially true for Docker images. If you bake configuration into an image, you have to build a new image for every environment (Dev, Staging, Prod).

Environment variables allow you to keep your Docker images **configuration-agnostic**. You build the image once and configure it at runtime by passing different environment variables.

## Real World Analogy
Think of a Docker image like a **Universal Remote Control**.
- The remote has buttons (code) that do specific things (send signals).
- But the remote doesn't know what TV it's controlling until you program it (pass environment variables).
- You can use the same remote for a Sony TV (Dev) or a Samsung TV (Prod) just by changing the settings.

## Core Concepts
- **Runtime Variables**: Passed when running the container using the `-e` flag.
- **Build-time Variables (ARG)**: Passed during the build process using `--build-arg`. They are not available in the running container.
- **Env Files**: Storing variables in a file (e.g., `.env`) and passing the file to Docker.

## Architecture / Flow

```text
[Define Variables]
(Terminal, .env file, or CI/CD)
        |
        | 1. docker run -e KEY=VALUE
        v
[Docker Daemon]
        |
        | 2. Injects into
        v
[Running Container]
        |
        | 3. App code reads process.env.KEY
```


## Practical Commands
```bash
# Pass a single environment variable
docker run -d -e DB_HOST=mongo -e DB_PORT=27017 my-app:latest

# Pass variables from a file
docker run -d --env-file .env my-app:latest

# Check environment variables in a running container
docker exec -it <container_name> env
```

## Hands-On Exercise
1. Run a container and pass an environment variable:
   ```bash
   docker run --rm -e MY_NAME=John alpine env
   ```
2. You should see `MY_NAME=John` in the output list of environment variables.
3. Run a Node.js container and access the variable:
   ```bash
   docker run --rm -e MESSAGE="Hello from Docker" node:22-alpine node -e "console.log(process.env.MESSAGE)"
   ```
   You should see `Hello from Docker` printed.

## Mini Project
**Task**: Run a Node.js app that connects to a database, passing the database credentials via environment variables.

1. Create a `.env` file:
   ```env
   DB_HOST=database.example.com
   DB_USER=admin
   DB_PASS=secret123
   ```
2. Run your app container using this file:
   ```bash
   docker run -d --name my-app --env-file .env my-node-app
   ```
3. Your application code (Node.js) can access these values using `process.env.DB_HOST`, etc.

## Real Production Usage
- **Secrets Management**: In production (like Kubernetes or AWS ECS), you don't use `.env` files on the server. You use secrets managers (like AWS Secrets Manager or Kubernetes Secrets) which inject the variables securely into the container at runtime.
- **Feature Flags**: You can enable or disable features in production without redeploying code, just by changing an environment variable and restarting the container.

## Common Mistakes
- **Baking secrets into images**: Never use `ENV` in a Dockerfile to set sensitive data like passwords. Anyone who can pull the image can see the secrets using `docker inspect`.
- **Committing `.env` files to Git**: Always add `.env` to your `.gitignore`.

## Debugging Guide
- **Variables not loading**:
  - Run `docker exec -it <container_name> env` to see if the variables actually made it into the container.
  - Check for typos in the variable names (they are case-sensitive).

## Best Practices
- **Use `.env` files for local dev**: It keeps your command line clean.
- **Fail fast**: In your application code, check if required environment variables are present at startup. If not, log an error and exit.

## Interview Questions
1. **What is the difference between `ENV` and `ARG` in a Dockerfile?**
   *Answer*: `ARG` defines variables available only *during the build process*. `ENV` defines variables available both during the build and *inside the running container*.
2. **How do you pass secrets to a Docker container securely?**
   *Answer*: By passing them at runtime using environment variables (preferably from a secrets manager) rather than hardcoding them in the Dockerfile.

## Summary
Environment variables make your Docker images reusable across different environments. Always separate configuration from code, and never commit secrets to your source code or bake them into images.

---
Prev: [06_ports.md](./06_ports.md) | Index: [Index](../00_index.md) | Next: [08_docker_compose.md](./08_docker_compose.md)
