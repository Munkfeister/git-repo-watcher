import sys
sys.path.append("./dependencies")

import os
import redis

from redis.commands.json.path import Path

class Watcher(object):
    
    def __init__(self):
        print("Connecting to Redis...")
        self.connection = redis.Redis(host=config["redis_host"], port=config["redis_port"])
    
    def __enter__(self):
        return self

    def delete(self, repo_url):
        self.connection.delete(f"repo_url:{repo_url}")
        self.connection.bgsave()

        return True

    def set(self, repo_url, branches, webhook_url, webhook_auth):
        repo = {
            "branches": [branches.split(",")],
            "webhook": {
                "url": webhook_url,
                "auth": webhook_auth
            }
        }

        self.connection.json().set(f"repo_url:{repo_url}", Path.root_path(), repo)
        self.connection.bgsave()

        return True

    def get(self, repo_url):
        result = self.connection.json().get(f"repo_url:{repo_url}")

        if result is not None:
            result["repo_url"] = repo_url

        print(result)

        return result

    def get_all(self):
        result = []

        for key in self.connection.scan_iter("repo_url:*"):
            repo = self.connection.json().get(key.decode("utf-8"))
            repo["repo_url"] = key.decode("utf-8").split(":")[1]

            result.append(repo)

        print(result)

        return result