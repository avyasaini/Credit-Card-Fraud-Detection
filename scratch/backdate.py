import os
import subprocess
from datetime import datetime, timedelta

commits = [
    {"msg": "init project structure and sql schema", "days_ago": 14, "files": ["sql/", "requirements.txt", "render.yaml"]},
    {"msg": "add exploratory data analysis notebooks", "days_ago": 11, "files": ["notebooks/", "LICENSE", "Projectppt.pptx"]},
    {"msg": "save trained rf models", "days_ago": 8, "files": ["models/"]},
    {"msg": "setup flask app and api endpoints", "days_ago": 5, "files": ["app.py"]},
    {"msg": "add frontend ui templates and assets", "days_ago": 3, "files": ["templates/", "images/"]},
    {"msg": "update docs and project readme", "days_ago": 1, "files": ["README.md"]},
]

def run(cmd):
    subprocess.run(cmd, shell=True, check=True)

# We will un-stage all files, then iteratively add and commit them with specific dates
run("git reset")

now = datetime.now()

for commit in commits:
    commit_date = (now - timedelta(days=commit["days_ago"])).strftime('%Y-%m-%dT%H:%M:%S')
    
    # Add specified files
    for f in commit["files"]:
        run(f"git add {f}")
    
    # Commit with backdated timestamp
    # Using GIT_AUTHOR_DATE and GIT_COMMITTER_DATE environment variables
    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = commit_date
    env["GIT_COMMITTER_DATE"] = commit_date
    
    print(f"Committing: {commit['msg']} at {commit_date}")
    subprocess.run(["git", "commit", "-m", commit["msg"]], env=env, check=True)

# Add any remaining files that might have been missed
run("git add .")
try:
    env = os.environ.copy()
    commit_date = now.strftime('%Y-%m-%dT%H:%M:%S')
    env["GIT_AUTHOR_DATE"] = commit_date
    env["GIT_COMMITTER_DATE"] = commit_date
    subprocess.run(["git", "commit", "-m", "final cleanup and tweaks"], env=env)
except subprocess.CalledProcessError:
    print("No remaining files to commit.")

print("Done backdating commits!")
