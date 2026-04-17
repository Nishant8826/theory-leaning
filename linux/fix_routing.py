import os
import re

directory = r"d:\learning\theory\linux"

ordered_files = [
    "01_linux_overview.md",
    "02_linux_architecture_shell.md",
    "03_filesystem_hierarchy.md",
    "04_basic_commands.md",
    "06_user_management.md",
    "07_file_permissions.md",
    "16_linux_boot_process.md",
    "08_process_management.md",
    "17_logs_debugging.md",
    "19_linux_day_to_day_tasks.md",
    "11_package_management.md",
    "10_service_management.md",
    "18_http_status_codes.md",
    "09_system_monitoring.md",
    "13_ssh_key_management.md",
    "12_networking.md",
    "14_vi_editor.md",
    "15_shell_scripting_basics.md",
    "05_advanced_commands.md",
    "20_linux_cheatsheet.md",
    "21_linux_tips_2026.md"
]

for i, filename in enumerate(ordered_files):
    path = os.path.join(directory, filename)
    if not os.path.exists(path):
        continue
    
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    prev_file = f"[{ordered_files[i-1]}]({ordered_files[i-1]})" if i > 0 else "None"
    next_file = f"[{ordered_files[i+1]}]({ordered_files[i+1]})" if i < len(ordered_files) - 1 else "None"

    pattern = re.compile(r'Prev: .* \| Index: .* \| Next: .*')
    
    # Adding markdown syntax for correct clickable routing
    new_nav_line = f"Prev: {prev_file} | Index: [00_index.md](00_index.md) | Next: {next_file}"
    
    if pattern.search(content):
        content = pattern.sub(new_nav_line, content, count=1)
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

# Index needs fix too
index_path = os.path.join(directory, "00_index.md")
if os.path.exists(index_path):
    with open(index_path, "r", encoding="utf-8") as f:
        content = f.read()
    pattern = re.compile(r'Prev: .* \| Index: .* \| Next: .*')
    new_nav_line = f"Prev: None | Index: [00_index.md](00_index.md) | Next: [01_linux_overview.md](01_linux_overview.md)"
    if pattern.search(content):
        content = pattern.sub(new_nav_line, content, count=1)
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(content)

print("Routing paths updated into clickable markdown standard.")
