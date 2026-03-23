# 🌐 Networking in Linux: Connecting the World

Linux is the fuel for the "Networked Universe." Understanding how computers talk to each other is a core skill for any DevOps engineer.

## 📡 The Networking Tools (Commands)
1.  **`ping`:** Check if another computer is "awake" and reachable.
    *   *Example:* `ping google.com`
2.  **`curl`:** Talk to a website and get its content (like a browser without the pretty buttons).
    *   *Example:* `curl https://wikipedia.org`
3.  **`netstat` / `ss`:** Show which "Ports" are open on your server (like seeing which doors are open in a building).
    *   *Example:* `ss -tulpn` (Shows all listening connections).
4.  **`ifconfig` / `ip addr`:** Check your own IP address (Your server's home address).
5.  **`nslookup` / `dig`:** Check what the IP address of a domain name is (DNS).

---

## 💡 Real-World DevOps Usage
*   **Troubleshooting:** Is the server down? No, the `ping` works. Maybe the "door" (port 80 for websites) is closed? Use `netstat` to check.
*   **API Testing:** You created a new API and want to test it. Use `curl` to send a "request" and see if it responds with "200 OK."

---

## ✍️ Hands-on Task
1. Open your terminal and type `ping google.com`. Press `Ctrl+C` to stop it.
2. Type `curl http://wttr.in/`. (This is a cool weather service in the terminal!)
3. Check your IP address by typing `ip addr` or `ifconfig`. Look for the "inet" number.

---
Previous: [11_package_management.md](11_package_management.md)  
Next: [13_ssh_key_management.md](13_ssh_key_management.md)
---
