# ⚙️ Service Management: Controlling Your Apps

In Linux, a "Service" (also called a Daemon) is a program that runs silently in the background. Examples: Web servers (Nginx), Databases (PostgreSQL), or Docker.

## 🛠️ The Master Tool: `systemctl`
Most modern Linux systems use `systemctl` to control these background workers.

| Command | What it does | Real-Life Analogy |
| :--- | :--- | :--- |
| `systemctl start nginx` | **Turn on** | Turning on the lights in a room. |
| `systemctl stop nginx` | **Turn off** | Turning off the lights. |
| `systemctl restart nginx` | **Reboot** | Unplugging and plugging back in. |
| `systemctl status nginx` | **Check Health** | Asking "Is the light still on?" |
| `systemctl enable nginx` | **Auto-start** | Setting the lights to turn on automatically at 6 PM. |

---

## 💡 Real-World DevOps Use Case
You just updated your website's configuration. For the changes to take effect, you must restart the web server:
1. `sudo systemctl restart nginx`
2. You check the status to make sure it didn't crash: `sudo systemctl status nginx`.

---

## ✍️ Hands-on Task
*(Note: This works only if you are on a real Linux server or WSL)*
1. Check the status of the cron service (which handles scheduled tasks): `systemctl status cron`.
2. See if it's "Active (running)". 
3. Exit by pressing `q`.

---
Previous: [09_system_monitoring.md](09_system_monitoring.md) Next: [11_package_management.md](11_package_management.md)
---
