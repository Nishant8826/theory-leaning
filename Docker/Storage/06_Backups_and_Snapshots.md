# 📌 Topic: Backups and Snapshots (Volume Management)

## 🧠 Concept Explanation (Basic → Expert)
**Basic**: Backing up a Docker volume is about making a copy of the data folder. You can do this by zipping the folder and saving it somewhere safe.
**Expert**: In production, "Zipping a folder" is not enough. You need **Atomic Snapshots**. If you zip a database while it is running, the resulting file might be corrupted because the database was writing to the middle of the file during the zip. Staff-level engineering involves **Application-Level Backups** (e.g., `pg_dump`), **Filesystem-Level Snapshots** (e.g., LVM/ZFS/EBS), and **Off-site Replication** (S3/Glacier). You must also verify your backups regularly—a backup that hasn't been tested for restoration is not a backup.

## 🏗️ Mental Model
- **The Snapshot**: A high-speed camera flash. It freezes the state of the disk at an exact millisecond. Even if things are moving, the picture is clear.
- **The Zip/Copy**: A slow scan. If things move during the scan, the result is blurry and unusable.

## ⚡ Actual Behavior
- **Volume persistence**: Deleting a container doesn't touch the volume data.
- **Restoration**: You can "Restore" a volume by creating a new empty volume and unzipping a backup archive into it before attaching it to a container.

## 🔬 Internal Mechanics (The Atomic Problem)
1. **Cold Backup**: Stop the container, copy the files, start the container. (100% safe, but involves downtime).
2. **Hot Backup (App-level)**: Use the database's own backup tool (e.g., `mysqldump`). It uses internal locks or MVCC to ensure a consistent view of the data without stopping the service.
3. **Snapshot (EBS/ZFS)**: The storage layer creates a "Copy-on-Write" pointer. It doesn't physically copy data yet, making the snapshot nearly instant.

## 🔁 Execution Flow (The "Sidecar" Backup Pattern)
1. **Target**: Container `my-db` is running.
2. **Action**: Run a temporary container that "borrows" the volumes of `my-db`.
3. `docker run --rm --volumes-from my-db -v $(pwd):/backup alpine tar czf /backup/db_snap.tar.gz /data`.
4. **Result**: The tarball is created on the host machine.
5. **Cleanup**: The temporary container is deleted automatically.

## 🧠 Resource Behavior
- **CPU/Disk**: Compressing a large volume (e.g., 100GB) can saturate the host's CPU and Disk I/O, potentially slowing down your production application. Always run backups during "Off-peak" hours.

## 📐 ASCII Diagrams (REQUIRED)

```text
       BACKUP STRATEGIES
       
[ STORAGE LEVEL ]       [ APP LEVEL ]
(EBS / ZFS)             (pg_dump / mongodump)
      |                       |
+-----v-----+           +-----v-----+
| Snapshot  |           | Logical   |
| (Instant) |           | (Slower)  |
+-----------+           +-----------+
      |                       |
[ Data Files ]         [ SQL / JSON ]
(Hardware-tied)         (Portable)
```

## 🔍 Code (Automated Backup Script)
```bash
#!/bin/bash
# Backup a named volume to S3
VOLUME_NAME="production_db_data"
BACKUP_NAME="db_backup_$(date +%Y%m%d_%H%M%S).tar.gz"

echo "Starting backup of $VOLUME_NAME..."

docker run --rm \
  -v $VOLUME_NAME:/source:ro \
  -v $(pwd):/dest \
  alpine tar -czf /dest/$BACKUP_NAME -C /source .

# Push to AWS S3 (Requires AWS CLI configured on host)
# aws s3 cp $BACKUP_NAME s3://my-company-backups/docker-volumes/

echo "Backup complete: $BACKUP_NAME"
```

## 💥 Production Failures
- **The "Inconsistent State"**: Backing up a MongoDB volume by copying the files while the database is running. The copy happens at 12:00:01. The DB writes a related record at 12:00:02. The backup has half of the transaction. When you restore, MongoDB fails to start due to "Data Corruption."
- **Disk Full during Backup**: The backup script creates a 50GB tarball in the same partition as the 50GB volume. The disk hits 100%, and the production app crashes.
  *Fix*: Always stream backups to a different disk or directly to the network (S3).

## 🧪 Real-time Q&A
**Q: How often should I backup?**
**A**: It depends on your **RPO (Recovery Point Objective)**. If your business can only afford to lose 1 hour of data, you must backup every hour. If you can lose 1 day, nightly is fine. In Staff-level environments, we use **Transaction Log Shipping** (like Postgres WAL-E) to achieve near-real-time backups.

## ⚠️ Edge Cases
- **Large Volumes**: For volumes > 500GB, `tar` is too slow. You should use block-level snapshots (AWS EBS Snapshots) or tools like `Restic` which perform incremental, deduplicated backups.

## 🏢 Best Practices
- **Test Restoration**: Once a month, try to start a container using your backup file.
- **Off-site Storage**: Never keep your backups on the same physical server as your data.
- **Immutable Backups**: Store backups in S3 with "Object Lock" to protect against ransomware.

## ⚖️ Trade-offs
| Method | Speed | Reliability | Portability |
| :--- | :--- | :--- | :--- |
| **Tar/Zip** | Slow | Medium | **High** |
| **App Dump** | Medium | **High** | **High** |
| **Snapshot** | **Fastest** | High | Low |

## 💼 Interview Q&A
**Q: How do you backup a Docker volume without stopping the container?**
**A**: I use the **Sidecar Container Pattern** combined with **Application-Specific tools**. For a database, I run a temporary container that shares the network and volumes of the DB container and executes a logical backup (like `pg_dump` for Postgres). This ensures a consistent, non-corrupted copy of the data without interrupting service. For non-database volumes, I use the `--volumes-from` flag to mount the data into a temporary `alpine` container and run `tar` to create an archive, ensuring the mount is `read-only` to minimize impact on the running application.

## 🧩 Practice Problems
1. Write a script that automatically backups all "Named Volumes" on your system to a backup folder.
2. Simulate a disaster: Delete a container and its volume, then restore it using your latest backup.

---
Prev: [05_IO_Performance.md](./05_IO_Performance.md) | Index: [00_Index.md](../00_Index.md) | Next: [01_Docker_Compose_Internals.md](../Compose/01_Docker_Compose_Internals.md)
---
