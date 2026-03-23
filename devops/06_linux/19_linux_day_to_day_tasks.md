# ☕ Linux Day-to-Day Tasks: A Day in the Life

What does a DevOps engineer actually do on a server? It's not always about coding "magic." Most of the time, it's about keeping things clean and stable.

## 🌅 Morning: Health Checks
1.  **Check Resources:** Is the RAM okay? (`free -m`)
2.  **Check Disk Space:** Is the log folder full? (`df -h`)
3.  **Check Status:** Are the critical apps running? (`systemctl status nginx`)

## 🌞 Afternoon: Maintenance & Deployments
1.  **Updating Apps:** Getting the newest features. (`sudo apt update && sudo apt upgrade`)
2.  **Changing Configs:** Adjusting settings to handle more users. (`vi /etc/nginx/nginx.conf`)
3.  **Deploying Code:** Downloading the newest site version from GitHub. (`git pull`)

## 🌙 Evening: Cleanup
1.  **Removing Temp Files:** Cleaning up the trash. (`rm -rf /tmp/*`)
2.  **Checking Backups:** Making sure the data is safe. (`ls -l /backups`)
3.  **Reviewing Logs:** Looking for any "Strange" Login attempts. (`last`)

---

## 💡 Industry Tip
Most senior DevOps engineers don't do these things manually. They write "Cron Jobs" (Scheduled tasks) that do the cleanup and health checks automatically while they sleep!

---

## ✍️ Hands-on Task
1. Type `last` in your terminal to see a list of every time you logged into your computer recently.
2. Type `history` to see a list of every command you typed today. It's like a time machine for your work!

---
Previous: [18_http_status_codes.md](18_http_status_codes.md)  
Next: [20_linux_cheatsheet.md](20_linux_cheatsheet.md)
---
