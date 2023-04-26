import os
import requests

from dotenv import load_dotenv
from urllib.parse import urlparse

from helpers.watcher import Watcher
from helpers.git_wrapper import GitWrapper

load_dotenv()

config = {
    "redis_host": os.getenv("REDIS_HOSTNAME", "localhost"),
    "redis_port": os.getenv("REDIS_PORT", 6379)
}

class Main(object):
    
    def __init__(self) -> None:
        print("Git Repo Watcher Starting...")
        self.watcher = Watcher(config)

    def process_repos(self):
        repos = self.watcher.get_all()

        print("Found %s repos to process." % len(repos))

        for repo in repos:
            self.process_repo(repo)            

    def process_repo(self, repo):
        for branch in repo["branches"]:
            with GitWrapper(repo["repo_url"], branch["branch_name"]) as git:
                latest_commit_sha = git.get_latest_commit_sha()

                if branch["last_commit_sha"] != latest_commit_sha:
                    print("Commit SHA doesn't match: %s vs %s" % (branch["last_commit_sha"], latest_commit_sha))
                    
                    if self.invoke_webhook(repo["webhook"]["url"], repo["webhook"]["auth"], branch, latest_commit_sha):
                        self.watcher.update_commit_sha(repo["repo_url"], branch["branch_name"], latest_commit_sha)
                else:
                    print("Commit SHA's match. Nothing to do...")

    def invoke_webhook(self, webhook_url, webhook_auth, branch, latest_commit_sha):
        ## I'm currently not sure what the payload will look like, so I've taken a best guess based on examples on the interweb.

        headers = {
            "Authorization": "Basic %s" % webhook_auth,
            "Content-Type": "application/json"
        }

        data = {
            "push": {
                "changes": [
                    {
                        "new": {
                            "name": branch,
                            "target": {
                                "type": "commit",
                                "hash": latest_commit_sha
                            }
                        }
                    }
                ]
            },
            "repository": {
                "type": "repository",
                "full_name": urlparse(webhook_url).path
            }
        }

        result = requests.post(webhook_url, data=data, headers=headers)
        return True

if __name__ == "__main__":
    main = Main()
    main.process_repos()