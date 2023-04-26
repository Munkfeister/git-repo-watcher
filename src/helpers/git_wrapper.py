import sys
sys.path.append("./dependencies")

import git
import os
import tempfile

class GitWrapper(object):
    
    def __init__(self, repo_url, branch):
        self.tf = tempfile.TemporaryDirectory()

        print("Initialising git repo: %s (%s)" % (repo_url, branch))
        self.repo = git.Repo.clone_from(repo_url, self.tf.name, branch=branch)
    
    def __enter__(self):
        return self

    def __del__(self):
        self.repo.__del__

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def get_latest_commit_sha(self):
        sha = self.repo.head.object.hexsha
        print(sha)

        return sha
        