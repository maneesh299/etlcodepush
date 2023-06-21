from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from google.cloud import storage
import pandas as pd
import json
import socket
import configparser

app = Flask(__name__)
config = configparser.ConfigParser()
config.read('config.ini')

mongo_uri = config.get('Config', 'DBURI')

app.config['MONGO_URI'] = mongo_uri
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
mongo = PyMongo(app)
db = mongo.db


@app.route("/")
def index():
    bucket_name = config.get('Config', 'GCP_PROJECT')
    file_name = config.get('Config', 'FILE_NAME')
    csv_data = pd.DataFrame(pd.read_csv('gs://' + bucket_name + '/' + file_name, encoding='utf-8', encoding_errors='ignore'))
    csv_data = csv_data.to_dict(orient="records")
    db.task.insert_many(csv_data)
    
    return jsonify(
        message="Welcome to file read from config! I am converting csv to document structure in json!"
    )


@app.route("/tasks")
def get_all_tasks():
    tasks = db.task.find()
    data = []
    for task in tasks:
        item = {
            "Name": str(task["Name"]),
            "Identity": task["Identity"]
        }
        data.append(item)
    return jsonify(
        data=data
    )





if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
