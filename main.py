from utils.arg_parser import parse_args
from app.app import App
from utils.embedder import embed_files

if __name__ == "__main__":
    args = parse_args()
    app = App(args)
    
    embed_files(app.file_list(), None, None)
    
