import os
import shutil
from git import Repo

def clone_repo(repo_url, dest_folder, remove_dot_git=True):
    if os.path.exists(dest_folder) and os.listdir(dest_folder):
        print(f"Destination path '{dest_folder}' already exists and is not an empty directory.  Skipping git clone.")
        return
    Repo.clone_from(repo_url, dest_folder)
    if remove_dot_git:
        shutil.rmtree(f"{dest_folder}/.git")

def get_repo_name(repo_url):
    return repo_url.split("/")[-1].replace(".git", "")
