import sys
sys.path.append("./dependencies")

import os

from dotenv import load_dotenv

from watcher import Watcher
from git_wrapper import GitWrapper

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
                    
                    if self.invoke_webhook(repo["webhook"]["url"], repo["webhook"]["auth"]):
                        self.watcher.update_commit_sha(repo["repo_url"], branch["branch_name"], latest_commit_sha)
                else:
                    print("Commit SHA's match. Nothing to do...")

    def invoke_webhook(self, webhook_url, webhook_auth):
        print("Calling webhook...")
        return True

if __name__ == "__main__":
    main = Main()

    #main.watcher.set("https://github.com/Munkfeister/git-repo-watcher", ["master"], "blah", "blah")

    main.process_repos()