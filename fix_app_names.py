import os

apps = [
    "authentication",
    "dashboard",
    "expenses",
    "budgets",
    "goals",
    "insights",
    "chatbot",
    "core"
]

base_dir = "apps"

for app in apps:
    apps_py = os.path.join(base_dir, app, "apps.py")
    if os.path.exists(apps_py):
        with open(apps_py, "r") as f:
            content = f.read()
        
        # Simple string replacement
        old_str = f"name = '{app}'"
        new_str = f"name = 'apps.{app}'"
        
        if old_str in content:
            new_content = content.replace(old_str, new_str)
            with open(apps_py, "w") as f:
                f.write(new_content)
            print(f"Updated {apps_py}")
        else:
            # Check for double quotes too just in case
            old_str_double = f'name = "{app}"'
            new_str_double = f'name = "apps.{app}"'
            if old_str_double in content:
                new_content = content.replace(old_str_double, new_str_double)
                with open(apps_py, "w") as f:
                    f.write(new_content)
                print(f"Updated {apps_py} (double quotes)")
            else:
                print(f"Skipped {apps_py} (already correct or different)")
