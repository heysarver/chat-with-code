import os
from utils.git_utils import clone_repo, get_repo_name

class App:
    def __init__(self, args):
        self.codebase_name = args.codebase_name if args.codebase_name != "local" else None
        self.file_extensions = args.file_extensions.split(',')
        self.source_dir = args.local_path if args.local_path else "data/source"
        self.github_repo = args.github_repo

        if self.github_repo:
            clone_repo(self.github_repo, self.source_dir)
            self.codebase_name = self.codebase_name or get_repo_name(self.github_repo)

    def file_list(self):
        files = []
        for dirpath, dirnames, filenames in os.walk(self.source_dir):
            for filename in filenames:
                if filename.endswith(tuple(self.file_extensions)):
                    files.append(os.path.join(dirpath, filename))
        return files
