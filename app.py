import argparse
import os
import shutil
from dotenv import load_dotenv
from git import Repo

def parse_args():
    load_dotenv()

    GITHUB_REPO = os.getenv("GITHUB_REPO", "")
    LOCAL_PATH = os.getenv("LOCAL_PATH", "")
    FILE_EXTENSIONS = os.getenv("FILE_EXTENSIONS", ".py,.md")
    CODEBASE_NAME = os.getenv("CODEBASE_NAME", "local")

    parser = argparse.ArgumentParser(description="Process some parameters.")
    parser.add_argument("--github-repo", type=str, default=GITHUB_REPO, help="GitHub repository URL")
    parser.add_argument("--local-path", type=str, default=LOCAL_PATH, help="Local path to clone the repository")  
    parser.add_argument("--file-extensions", type=str, default=FILE_EXTENSIONS, help="File extensions to embed, e.g. '.py,.md'")  
    parser.add_argument("--codebase-name", type=str, default="local", help="Name of the codebase")

    args = parser.parse_args()
    if args.github_repo != "" and args.local_path != "":
        raise ValueError("Cannot specify both github-repo and local-path.  Please specify only one.")

    return args

def clone_repo(repo_url, dest_folder, remove_dot_git=True):
    Repo.clone_from(repo_url, dest_folder)
    if remove_dot_git:
        shutil.rmtree(f"{dest_folder}/.git")

def get_repo_name(repo_url):
    return repo_url.split("/")[-1].replace(".git", "")

if __name__ == "__main__":
    args = parse_args()

    # set varaibles
    codebase_name = args.codebase_name
    file_extensions = args.file_extensions.split(',')
    source_dir = "data/source"
    if args.github_repo:
        clone_repo(args.github_repo, source_dir)
        # only set to repo name if the codebase name is not set
        if codebase_name == "local":
            codebase_name = get_repo_name(args.github_repo)
    if args.local_path:
        source_dir = args.local_path
    
    
