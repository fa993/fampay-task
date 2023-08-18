from flask import Flask, Response, json
from pymongo import MongoClient
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler

import poptask
import os

load_dotenv()

client = MongoClient(host=os.environ["DB_URI"])

db = client.ytsc
vids = db[poptask.src_term+"vids"]

# sched = BackgroundScheduler(daemon=True)
# sched.add_job(poptask.exec_sche, 'interval', seconds=10)
# sched.start()

app = Flask(__name__)


@app.route("/")
def hello_world():
    out = list(vids.find({}, {"_id": 0}))
    return Response(
        response=json.dumps(out),
        mimetype='application/json'
    )
