import sys
sys.path.append("./dependencies")

import os

from git import Repo
from dotenv import load_dotenv

load_dotenv()

config = {
    
}

class Main(object):
    
    def __init__(self) -> None:
        print("Git Repo Watcher Starting...")
        
if __name__ == "__main__":
    main = Main()