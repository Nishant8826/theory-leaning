# Volumes & Data Persistence

## Why This Exists
By default, data inside a Docker container is **ephemeral**. This means if you run a MongoDB container, insert some data, and then delete the container (`docker rm`), your data is gone forever.

In production, you cannot afford to lose user data or database records. You need a way to persist data outside the lifecycle of a container. Volumes solve this problem by mapping a directory inside the container to a directory on the host machine.

## Real World Analogy
Think of a Docker container like a **Rental Car**.
- You can drive it, put things in the glovebox, and adjust the seats.
- But when you return the car (destroy the container), anything you left in the glovebox is gone.

If you want to keep your stuff, you put it in a **Suitcase** (Volume) that you take with you when you return the car.

## Core Concepts
- **Volumes**: Managed by Docker. Best way to persist data. Stored in a part of the host filesystem owned by Docker.
- **Bind Mounts**: Maps a specific path on the host to a path in the container. Great for development (live reloading).
- **Tmpfs Mounts**: Stored in the host's memory only. Never written to disk. Good for sensitive data or performance.

## Architecture / Flow

```text
[Container App]
      |
      | 1. Writes to /data/db
      v
[Isolated Path in Container]
      |
      | 2. Mapped by Docker
      v
[Host Machine Folder]
(3. Data persists here even if container is deleted)
```


## Practical Commands
```bash
# Create a volume
docker volume create my-data

# List volumes
docker volume ls

# Inspect a volume (see where it is on host)
docker volume inspect my-data

# Run a container with a named volume
docker run -d --name my-db -v my-data:/data/db mongo:latest

# Run a container with a bind mount (for dev)
docker run -d --name my-app -v $(pwd)/src:/app/src node:22-alpine

# Remove a volume (only works if not used by any container)
docker volume rm my-data
```

## Hands-On Exercise
Let's verify that data persists after a container is deleted.

1. Create a named volume:
   ```bash
   docker volume create test-vol
   ```
2. Run a container and write a file to the volume:
   ```bash
   docker run --rm -v test-vol:/app alpine sh -c "echo 'Hello Persistence' > /app/hello.txt"
   ```
   *Note: `--rm` deletes the container immediately after it finishes.*
3. Run a *new* container and read the file:
   ```bash
   docker run --rm -v test-vol:/app alpine cat /app/hello.txt
   ```
   You should see `Hello Persistence` even though the first container is gone!

## Mini Project
**Task**: Run a MySQL database and ensure data persists across container restarts.

1. Run MySQL with a volume:
   ```bash
   docker run -d --name mysql-db -e MYSQL_ROOT_PASSWORD=secret -v mysql-data:/var/lib/mysql -p 3306:3306 mysql:latest
   ```
2. Connect and create a database (or use GUI tool like TablePlus).
3. Stop and remove the container:
   ```bash
   docker stop mysql-db
   docker rm mysql-db
   ```
4. Re-run the container with the SAME volume:
   ```bash
   docker run -d --name mysql-db -e MYSQL_ROOT_PASSWORD=secret -v mysql-data:/var/lib/mysql -p 3306:3306 mysql:latest
   ```
5. Verify that your database still exists.

## Real Production Usage
- **Databases**: Always use Volumes for DBs like PostgreSQL, MongoDB, MySQL.
- **Backups**: You can easily back up a volume by copying the files from the host path or using tools like Velero (in K8s).
- **Cloud**: In AWS, Docker volumes can be mapped to AWS EBS (Elastic Block Store) or EFS (Elastic File System) for highly available storage.

## Common Mistakes
- **Forgetting to name volumes**: Running `docker run -v /data/db mongo` creates an anonymous volume. If you delete the container, the volume is hard to track down and clean up.
- **Bind mounting entire project for production**: Bind mounts depend on the host's directory structure. Never use bind mounts in production; use named volumes or bake the code into the image.

## Debugging Guide
- **Permission Denied errors**: Often happen when using Bind Mounts because the user inside the container doesn't have permissions to read/write the host directory.
  - Fix by checking ownership or using named volumes.

## Best Practices
- **Use Volumes, not Bind Mounts for production**: Volumes are completely managed by Docker and are more secure and portable.
- **Clean up unused volumes**: Run `docker volume prune` to delete all unused volumes and save disk space.

## Interview Questions
1. **What is the difference between a Bind Mount and a Volume?**
   *Answer*: Bind mounts map a specific host path to a container path and depend on host structure. Volumes are managed by Docker, stored in a Docker-managed directory, and are independent of host structure.
2. **What happens to data in a container without a volume when the container is deleted?**
   *Answer*: It is lost permanently.

## Summary
Data persistence is critical for production. Volumes allow you to separate the lifecycle of your data from the lifecycle of your containers. Use Bind Mounts for development (live reload) and Volumes for production data.

---
Prev: [03_dockerfile.md](./03_dockerfile.md) | Index: [Index](../00_index.md) | Next: [05_networks.md](./05_networks.md)
