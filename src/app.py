import os

from flask import Flask, jsonify, request
from flask_restful import Api
from dotenv import load_dotenv

from api.git import Git
from api.health import Health

load_dotenv()

config = {
    "redis_host": os.getenv("REDIS_HOSTNAME", "localhost"),
    "redis_port": os.getenv("REDIS_PORT", 6379),
    "port": os.getenv("PORT", 8080)
}

app = Flask(__name__)
api = Api(app)

api.add_resource(Git, '/', resource_class_kwargs={'config': config})
api.add_resource(Health, '/status', resource_class_kwargs={'config': config})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=config["port"])