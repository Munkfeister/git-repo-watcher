import sys
sys.path.append("./dependencies")

import os
import redis

from redis.commands.json.path import Path

class Watcher(object):
    
    def __init__(self, config):
        print("Connecting to Redis...")
        self.connection = redis.Redis(host=config["redis_host"], port=config["redis_port"])
    
    def __enter__(self):
        return self

    def delete(self, repo_url):
        self.connection.delete(f"repo_url:{self.safe_repo_url(repo_url)}")
        self.connection.bgsave()

        return True

    def safe_repo_url(self, repo_url):
        return repo_url.replace(":", "!colon!")

    def rev_safe_repo_url(self, repo_url):
        return repo_url.replace("!colon!", ":")

    def set(self, repo_url, branches, webhook_url, webhook_auth):
        try:
            branch_json = []

            for branch in branches:
                branch_json.append({
                    "branch_name": branch,
                    "last_commit_sha": ""
                })

            repo = {
                "branches": branch_json,
                "webhook": {
                    "url": webhook_url,
                    "auth": webhook_auth
                }
            }

            self.connection.json().set(f"repo_url:{self.safe_repo_url(repo_url)}", Path.root_path(), repo)
            self.connection.bgsave()
        except Exception as ex:
            reason = ex
            return False, ex

        return True, None

    def update_commit_sha(self, repo_url, branch_name, commit_sha):
        self.connection.json().set(f"repo_url:{self.safe_repo_url(repo_url)}", ".branches[?(@branch_name == '%s')].last_commit_sha" % branch_name, commit_sha)

    def get(self, repo_url):
        result = self.connection.json().get(f"repo_url:{self.safe_repo_url(repo_url)}")

        if result is not None:
            result["repo_url"] = repo_url

        print(result)

        return result

    def get_all(self):
        result = []

        for key in self.connection.scan_iter("repo_url:*"):
            repo = self.connection.json().get(key.decode("utf-8"))
            repo["repo_url"] = self.rev_safe_repo_url(key.decode("utf-8").split(":")[1])

            result.append(repo)

        print(result)

        return result