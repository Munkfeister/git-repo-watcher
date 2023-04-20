import sys
sys.path.append("./dependencies")

import os
import redis

from git import Repo
from dotenv import load_dotenv
from redis.commands.json.path import Path

from watcher import Watcher

load_dotenv()

config = {
    "redis_host": os.getenv("REDIS_HOSTNAME", 6379),
    "redis_port": os.getenv("REDIS_PORT", 6379)
}

class Main(object):
    
    def __init__(self) -> None:
        print("Git Repo Watcher Starting...")
        self.watcher = Watcher()

if __name__ == "__main__":
    main = Main()