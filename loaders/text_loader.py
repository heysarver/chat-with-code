import os
import shutil
from langchain_community.document_loaders import TextLoader
from utils.git import clone_repo, get_repo_name

def is_local_path(url: str):
    return not (url.startswith("http") or url.startswith("git"))

def load_text_files(src: str, delete_src_when_done: bool = False):
    
    if is_local_path(src):
        print(f"Loading files from {src}")
        root_dir = src
    else:
        repo_url = src
        repo_name = get_repo_name(repo_url)
        root_dir = f"./{repo_name}"
        print(f"Cloning {repo_url}")
        clone_repo(repo_url, repo_name)

    docs = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for file in filenames:
            try:
                loader = TextLoader(os.path.join(dirpath, file), encoding='utf-8')
                docs.extend(loader.load_and_split())
            except Exception as e:
                pass
    
    if delete_src_when_done and os.path.exists(root_dir):
        print(f"Removing {root_dir}")
        shutil.rmtree(root_dir)

    print(f"Loaded {len(docs)} files from {root_dir}")
    return docs
