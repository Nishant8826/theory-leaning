import os
import re

directory = r"d:\learning\theory\linux"

ordered_files = [
    # Module 1
    "01_linux_overview.md",
    "02_linux_architecture_shell.md",
    "03_filesystem_hierarchy.md",
    "04_basic_commands.md",
    "06_user_management.md",
    "07_file_permissions.md",
    "16_linux_boot_process.md",
    # Module 2
    "08_process_management.md",
    "17_logs_debugging.md",
    "19_linux_day_to_day_tasks.md",
    # Module 3
    "11_package_management.md",
    # Module 4
    "10_service_management.md",
    "18_http_status_codes.md",
    # Module 6
    "09_system_monitoring.md",
    "13_ssh_key_management.md",
    # Module 7
    "12_networking.md",
    # Module 8
    "14_vi_editor.md",
    "15_shell_scripting_basics.md",
    # Module 9
    "05_advanced_commands.md",
    "20_linux_cheatsheet.md",
    "21_linux_tips_2026.md"
]

dev_tips = {
    "04_basic_commands.md": "\n### 💡 Dev Tip\n*   `cp -r build/ /var/www/html/` to upload your React/Next.js production builds.\n",
    "07_file_permissions.md": "\n### 💡 Dev Tip\n*   `chmod +x` is often the key to fixing deployment issues when executing Node.js processes or shell scripts on AWS EC2.\n",
    "08_process_management.md": "\n### 💡 Dev Tip\n*   `ps aux | grep node` (or `top`) helps verify if your Express or Next app is still checking Node server processes in the background.\n",
    "09_system_monitoring.md": "\n### 💡 Dev Tip\n*   `df -h` is critical to prevent filled up disk space from logs, which can silently crash Node.js PM2 apps or databases operations.\n",
    "11_package_management.md": "\n### 💡 Dev Tip\n*   You often need system packages to build Node modules like `node-gyp` or to serve a React app correctly.\n",
    "12_networking.md": "\n### 💡 Dev Tip\n*   `netstat -tulpn` or `lsof -i :3000` helps debug \"port already in use\" issues with Next.js or React dev servers or for port debugging.\n",
    "13_ssh_key_management.md": "\n### 💡 Dev Tip\n*   Use `scp` to quickly sync `.env` files or application builds to your AWS EC2 instances securely for uploading build to EC2.\n",
    "17_logs_debugging.md": "\n### 💡 Dev Tip\n*   Use `tail -f` to stream real-time logs for backend Node apps or database queries when tracking down a live AWS workflow error.\n"
}

for i, filename in enumerate(ordered_files):
    path = os.path.join(directory, filename)
    if not os.path.exists(path):
        continue
    
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    prev_file = ordered_files[i-1] if i > 0 else "None"
    next_file = ordered_files[i+1] if i < len(ordered_files) - 1 else "None"

    new_nav_line = f"Prev: {prev_file} | Index: 00_index.md | Next: {next_file}"
    new_nav = f"---\n{new_nav_line}\n---"
    
    # Let's replace the existing bottom navigation. We look for the last "---" section
    import re
    # We will search for ---\n(starts with Prev or Next)*\n---
    # To be safe, we just find the last couple of lines.
    
    # Using regex to find the typical footer:   
    # e.g., 
    # ---
    # Previous: [01_linux_overview.md](01_linux_overview.md) Next: [03_filesystem_hierarchy.md](03_filesystem_hierarchy.md)
    # ---
    pattern = re.compile(r'---\n+(?:.*)(?:Previous|Next).*?\n+---', re.IGNORECASE)
    
    if pattern.search(content):
        # Only replace the last occurrence if multiple exist, but usually there's only one at the bottom.
        # Let's just do a direct sub.
        # Ensure we only replace if it's towards the end by doing rsplit or sub
        content = pattern.sub(new_nav, content, count=1)
    else:
        # Check if there's any ---\n(Next:|Previous:).*
        alt_pattern = re.compile(r'---\s*\n\s*(?:Next|Previous):[^\n]*\n\s*---', re.IGNORECASE)
        if alt_pattern.search(content):
            content = alt_pattern.sub(new_nav, content, count=1)
        else:
            # Just append
            content = content.strip() + f"\n\n{new_nav}\n"
    
    if filename in dev_tips and "💡 Dev Tip" not in content:
        content = content.replace(f"\n{new_nav}", f"\n{dev_tips[filename]}\n{new_nav}")

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

print("Updated links and dev tips!")
