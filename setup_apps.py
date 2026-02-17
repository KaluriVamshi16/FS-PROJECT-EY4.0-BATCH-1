import os
import subprocess
import shutil

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
if not os.path.exists(base_dir):
    os.makedirs(base_dir)
    # Create __init__.py for apps package
    with open(os.path.join(base_dir, "__init__.py"), "w") as f:
        pass

for app in apps:
    app_dir = os.path.join(base_dir, app)
    if not os.path.exists(app_dir):
        os.makedirs(app_dir)
    
    print(f"Creating app: {app} in {app_dir}")
    try:
        subprocess.run(["python", "manage.py", "startapp", app, app_dir], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error creating app {app}: {e}")
