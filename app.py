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
    parser.add_argument("--codebase-name", type=str, default=CODEBASE_NAME, help="Name of the codebase")

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

class App:
    def __init__(self, args):
        self.codebase_name = args.codebase_name if args.codebase_name != "local" else None
        self.file_extensions = args.file_extensions.split(',')
        self.source_dir = args.local_path if args.local_path else "data/source"
        self.github_repo = args.github_repo

        if self.github_repo:
            clone_repo(self.github_repo, self.source_dir)
            self.codebase_name = self.codebase_name or get_repo_name(self.github_repo)

if __name__ == "__main__":
    args = parse_args()
    app = App(args)
