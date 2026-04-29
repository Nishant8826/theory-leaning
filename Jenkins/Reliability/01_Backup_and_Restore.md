# 🛡️ Backup and Restore

## 📌 Topic Name
State Preservation: Backing up JENKINS_HOME

## 🧠 Concept Explanation (Basic → Expert)
*   **Basic**: Saving a copy of Jenkins so if the server burns down, you can restore it.
*   **Expert**: Jenkins state is notoriously difficult to back up because it relies on a massive, highly-concurrent XML filesystem (`$JENKINS_HOME`) rather than a relational database. A Staff engineer knows that copying the directory while Jenkins is running results in corrupted, torn reads. True state preservation requires **Atomic Snapshots** (e.g., EBS/ZFS snapshots), **Thin Backups** (backing up configuration but discarding heavy workspace/artifact data), and isolating the encryption keys (`secrets/master.key`) to ensure backups are both consistent and secure.

## 🏗️ Mental Model
Think of backing up Jenkins like **Photocopying a Busy Accountant's Desk**.
- **The Desk**: Covered in thousands of sticky notes (XML files).
- **The Accountant (Jenkins)**: Frantically writing and moving sticky notes 100 times a second.
- **The Bad Backup (rsync)**: You try to copy the sticky notes one by one. By the time you finish, the accountant has changed half of them. Your copy is out of sync and useless.
- **The Good Backup (Snapshot)**: You freeze time for 1 millisecond, take a high-resolution photo of the entire desk at once, and unfreeze time.

## ⚡ Actual Behavior
- **Torn Reads**: If a backup script (`tar` or `rsync`) reads `config.xml` exactly while Jenkins is halfway through writing to it, the backup will contain a malformed XML file. Restoring from this backup will crash Jenkins on boot.
- **Storage Bloat**: `$JENKINS_HOME` contains `workspaces/` (gigabytes of source code) and `builds/` (gigabytes of logs/artifacts). Backing these up daily is incredibly expensive and slow.

## 🔬 Internal Mechanics (Jenkins core + OS + networking)
1.  **Thin Backup**: A strategy to only back up the state required to rebuild the server: `*.xml` files (Job configs), `secrets/` (Encryption keys), and `users/`. It intentionally excludes `workspace/`, `builds/`, and `plugins/` (which can be re-downloaded).
2.  **Filesystem Snapshots**: Modern infrastructure uses block-level snapshots (AWS EBS Snapshots or ZFS). The OS flushes filesystem buffers (`fsfreeze`), takes an instantaneous block-level pointer copy of the disk, and unfreezes. This guarantees atomic consistency without stopping Jenkins.
3.  **Quiet Down**: A Jenkins API endpoint (`/quietDown`) that stops new builds from starting. This is useful for taking consistent backups, but disrupts CI/CD flow.

## 🔁 Execution Flow (EBS Snapshot Backup)
1.  **Trigger**: Cron job runs at 2:00 AM.
2.  **Freeze (Optional but safe)**: Script calls `fsfreeze -f /var/jenkins_home`.
3.  **Snapshot**: Script calls AWS API `CreateSnapshot` for the EBS volume. (Takes 1 second).
4.  **Unfreeze**: Script calls `fsfreeze -u /var/jenkins_home`.
5.  **Background Copy**: AWS copies the blocks to S3 in the background. Jenkins continues running unharmed.

## 🧠 Resource Behavior (CPU, memory, IO, threads)
- **Disk Thrashing**: Running `tar -czf` on a 500GB Jenkins home directory will max out disk Read IOPS, slowing down every running build on the Controller.
- **Inode Scanning**: Finding all the `.xml` files in a directory with 10 million files takes significant time and RAM.

## 📐 ASCII Diagrams (MANDATORY)
```text
[ JENKINS CONTROLLER ]
        |
  /var/jenkins_home/
        |-- config.xml (KEEP)
        |-- secrets/   (KEEP)
        |-- jobs/
        |     |-- my-job/config.xml (KEEP)
        |     |-- my-job/builds/    (IGNORE - Too heavy)
        |-- workspace/              (IGNORE - Can be re-cloned)
```

## 🔍 Code (Jenkinsfile / Groovy / CLI / YAML)
```bash
# Example: A crude but effective "Thin Backup" script using rsync
# Run this via a Cron job on the Jenkins Controller OS
BACKUP_DIR="/mnt/nfs/jenkins_backup/$(date +%F)"
JENKINS_HOME="/var/jenkins_home"

mkdir -p "$BACKUP_DIR"

# Rsync only specific configuration files, excluding heavy state
rsync -avz --prune-empty-dirs \
    --include="*/" \
    --include="*.xml" \
    --include="secrets/**" \
    --include="users/**" \
    --exclude="*" \
    "$JENKINS_HOME/" "$BACKUP_DIR/"

# Compress the thin backup
tar -czf "${BACKUP_DIR}.tar.gz" -C "/mnt/nfs/jenkins_backup" "$(date +%F)"
```

## 💥 Production Failures
1.  **The Missing Master Key**: An admin uses a plugin to back up job configurations, but the plugin ignores the `secrets/` directory. The server dies. They restore the configurations to a new server. Every single job fails because none of the credentials (AWS keys, Git passwords) can be decrypted without the `master.key`.
2.  **The Workspace Tarball**: A script runs `tar -czf backup.tar.gz $JENKINS_HOME`. The home directory is 2TB because of uncleaned workspaces. The tar process fills the remaining disk space, causing a `No space left on device` crash.
3.  **Plugin Version Mismatch**: An admin restores the `config.xml` files but downloads the latest plugins. The XML schema changed in the newer plugins. Jenkins boots, fails to parse the old XML, and drops all the job configurations.

## 🧪 Real-time Q&A
*   **Q**: Should I backup Jenkins builds and logs?
*   **A**: Usually no. They consume massive storage. Push pipeline telemetry to an external SIEM (Splunk/ELK) and push artifacts to S3/Artifactory. Let Jenkins be stateless compute.
*   **Q**: Does Jenkins Configuration as Code (JCasC) replace backups?
*   **A**: Mostly. JCasC backs up the *system* configuration to Git. Multibranch pipelines back up the *job* configuration to Git. You still need to back up the `secrets/master.key` and potentially the build history if compliance requires it.

## ⚠️ Edge Cases
*   **Symlinks**: Jenkins workspaces often contain symlinks (especially `node_modules`). A naive backup script might try to follow the symlinks and infinitely loop or backup the entire OS disk.

## 🏢 Best Practices
1.  **Block-Level Storage**: Always use cloud-native volume snapshots (AWS EBS, GCP Persistent Disk) rather than file-level copies (`tar`/`rsync`) for primary backups.
2.  **Separate State**: Mount `/var/jenkins_home/workspace` on a separate, high-speed, ephemeral disk that is *excluded* from backups entirely.
3.  **Test Restores**: A backup is only a backup if you have successfully restored it to an empty server in the last 30 days.

## ⚖️ Trade-offs
*   **Full vs Thin Backups**:
    *   *Full*: Guarantees perfect restoration, including build history. Expensive, slow, high risk of I/O impact.
    *   *Thin*: Fast, cheap, safe. Loses all build history and requires plugins to be manually re-downloaded upon restore.

## 💼 Interview Q&A
*   **Q**: You are tasked with migrating a Jenkins server to a new AWS region. The `$JENKINS_HOME` directory is 1TB. You need to do this with minimal downtime. How do you proceed?
*   **A**: Copying 1TB over the network via `rsync` will take hours and result in inconsistent XML files if Jenkins is running. I would minimize downtime by separating the data. First, I would implement **Configuration as Code (JCasC)** and **Multibranch Pipelines** so the configuration is stored in Git. This makes the 1TB mostly disposable workspaces and historical logs. If I *must* migrate the full 1TB, I would use an AWS EBS Snapshot. I would put Jenkins in `/quietDown` mode (minutes of downtime, not hours), take an EBS snapshot, copy the snapshot to the new region, create a volume, and attach it to the new EC2 instance.

## 🧩 Practice Problems
1.  Navigate to `$JENKINS_HOME` on a test instance. Identify the location of the `secrets/master.key` and `secrets/hudson.util.Secret`.
2.  Write an `rsync` command that copies `$JENKINS_HOME` but explicitly excludes the `workspace/` and `jobs/*/builds/` directories.
