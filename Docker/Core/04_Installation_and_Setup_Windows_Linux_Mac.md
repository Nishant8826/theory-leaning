# 📌 Topic: Installation and Setup (Windows, Linux, Mac)

🟢 **Simple Explanation (Beginner)**
-----------------------------------
Docker runs natively on **Linux**.
When you run Docker on **Windows** or **Mac**, it's actually running a very tiny, invisible Linux Virtual Machine in the background.

- **On Windows**: We use **WSL2** (Windows Subsystem for Linux). It's like having a Linux heart inside a Windows body.
- **On Mac**: Apple has a special hypervisor framework that Docker uses to run a Linux kernel.
- **On Linux**: Docker runs directly on the "bare metal" kernel, which is why it's fastest and most efficient there.

🟡 **Practical Usage**
-----------------------------------
### 1. Windows (The Modern Way)
1. Install **WSL2** (`wsl --install` in PowerShell).
2. Download and install **Docker Desktop**.
3. In Settings, ensure "Use the WSL 2 based engine" is checked.
4. Open your favorite terminal (VS Code, CMD, PowerShell) and type `docker version`.

### 2. Linux (Ubuntu/Debian)
```bash
# Update and install dependencies
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg

# Add Docker's official GPG key
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Set up the repository
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker Engine
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

🔵 **Intermediate Understanding**
-----------------------------------
### Docker Desktop vs. Docker Engine
- **Docker Engine**: The CLI + Daemon. This is what you install on Linux servers.
- **Docker Desktop**: A GUI application that includes the Engine, a Kubernetes cluster, a Vulnerability Scanner, and specialized networking to bridge your laptop and the Linux VM.

### The "Sudo" Issue on Linux
By default, the Docker daemon binds to a Unix socket owned by `root`. 
To run docker without `sudo`, you must add your user to the `docker` group:
```bash
sudo usermod -aG docker $USER
# Log out and log back in for changes to take effect
```

🔴 **Internals (Advanced)**
-----------------------------------
### WSL2 Architecture (Windows)
When you run `docker ps` on Windows:
1. The Windows `docker` client talks to the `/var/run/docker.sock` inside the WSL2 utility VM.
2. WSL2 uses a **Dynamic Memory Allocation** system. It requests RAM from Windows when needed and gives it back when the container stops.

### Linux Kernel Dependencies
Docker requires specific kernel features enabled:
- `CONFIG_NAMESPACES`
- `CONFIG_CGROUPS`
- `CONFIG_OVERLAY_FS`
You can verify these using the `check-config.sh` script provided by Docker.

⚫ **Staff-Level Insights**
-----------------------------------
### The "WSL2 RAM Eater" Problem
WSL2 is known to consume huge amounts of RAM and not release it properly.
**Staff Solution**: Create a `.wslconfig` file in your Windows user profile (`%UserProfile%`) to limit it:
```ini
[wsl2]
memory=4GB # Limit memory to 4GB
processors=2 # Limit to 2 cores
```

### Licensing and Cost
**Important**: Docker Desktop is NOT free for large companies (more than 250 employees or $10M revenue). For Staff Engineers, you might need to look at alternatives like **Colima** (Mac) or **Rancher Desktop** to avoid licensing costs.

🏗️ **Mental Model**
Installing Docker is like installing a **Translator**. It allows your OS to speak "Container" to the hardware.

⚡ **Actual Behavior**
On Windows/Mac, your "localhost" is mapped to the Linux VM's IP address automatically so `localhost:8080` just works.

🧠 **Resource Behavior**
- **Disk Space**: Docker images are stored in `/var/lib/docker`. On Windows, this is a virtual disk (`ext4.vhdx`) that grows but **never shrinks** automatically even if you delete images. You have to manually "compact" the VHDX.

💥 **Production Failures**
- **Firewall Interference**: Corporate VPNs or firewalls often block the Docker network bridge, causing `docker pull` to hang forever.
- **Clock Skew**: If your laptop goes to sleep, the Linux VM's clock can get out of sync. This causes HTTPS certificates to fail (invalid time).

🏢 **Best Practices**
- Use **Docker Desktop** for ease of use in dev.
- Use **Native Linux** for production.
- Always use the **WSL2 Backend** on Windows, not Hyper-V.

🧪 **Debugging**
```powershell
# Check if WSL2 is running
wsl -l -v

# Check Docker logs on Windows (GUI)
# Go to Docker Desktop -> Troubleshoot (bug icon) -> View Logs
```

💼 **Interview Q&A**
- **Q**: Why do we need WSL2 for Docker on Windows?
- **A**: Because containers require a Linux Kernel (for Namespaces and Cgroups). Windows Kernel is different. WSL2 provides a real Linux Kernel.

---
Prev: [03_Docker_Architecture_Overview.md](03_Docker_Architecture_Overview.md) | Index: [00_Index.md](../00_Index.md) | Next: [05_The_Anatomy_of_an_Image.md](../Images/05_The_Anatomy_of_an_Image.md)
---
