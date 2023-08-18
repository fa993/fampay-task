from flask import Flask, Response, json, request
from pymongo import MongoClient
import pymongo
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timezone, timedelta

import poptask
import os

load_dotenv()

client = MongoClient(host=os.environ["DB_URI"])

db = client.ytsc
vids = db[poptask.src_term+"vids"]

sched = BackgroundScheduler(daemon=True)
# sched.add_job(poptask.exec_sche, 'interval', seconds=10)
sched.start()

app = Flask(__name__)


@app.route("/querydata")
def qdata():
    ts = (datetime.now(timezone.utc) -
          timedelta(hours=10))
    print(ts)
    out = []
    if request.args.get("last") == None:
        pass
    else:
        out = list(vids.find({"publishedAt": {"$gte": ts}}, {"_id": 0}).sort(
            'publishedAt', pymongo.DESCENDING).limit(request.args.get("length", default=10)))
    return Response(
        response=json.dumps(out),
        mimetype='application/json'
    )


@app.route("/")
def hello_world():
    ts = (datetime.now(timezone.utc) -
          timedelta(hours=10))
    print(ts)
    out = []
    if request.args.get("last") == None:
        pass
    else:
        out = list(vids.find({"publishedAt": {"$gte": ts}}, {"_id": 0}).sort(
            'publishedAt', pymongo.DESCENDING).limit(request.args.get("length", default=10)))
    return Response(
        response=json.dumps(out),
        mimetype='application/json'
    )


@app.route("/changesearch", methods=['POST'])
def changesearchterm():
    if len(str(request.data)) >= 2:
        poptask.src_term = request.data
        return Response(status=200)
    else:
        return Response(status=400)
