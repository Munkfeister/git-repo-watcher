from flask import request
from flask_restful import Resource

from helpers.watcher import Watcher

class Git(Resource):
    
    def __init__(self, **kwargs) -> None:
        print("Git Repo Watcher Starting...")
        self.watcher = Watcher(kwargs["config"])

    def post(self):
        data = request.get_json()

        print(data)

        success, reason = self.watcher.set(data["address"], data["branches"], data["webhookUrl"], data["webhookAuth"])
        
        if success:
            return {"result": 1}
        else:
            return {"result": 0, "reason": reason}
                                   
                                
                         
        #"https://github.com/Munkfeister/git-repo-watcher", ["master"], "blah", "blah")

