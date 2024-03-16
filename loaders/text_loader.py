import os
from langchain_community.document_loaders import TextLoader
from utils.git import clone_repo, get_repo_name

repo_url = os.environ.get("GIT_REPO")
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

print(f"Loaded {len(docs)} files from {root_dir}")
