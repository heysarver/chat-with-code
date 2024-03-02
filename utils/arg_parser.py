import argparse
import os
from dotenv import load_dotenv

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
