from flask import Flask, Response, json, request, render_template
from pymongo import MongoClient
from datetime import datetime, timezone, timedelta
import pymongo
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
from dateutil.parser import *
import poptask
import os

load_dotenv()

client = MongoClient(host=os.environ["DB_URI"])

db = client.get_default_database(default="ytsc")
vids = db[poptask.src_term+"vids"]

sched = BackgroundScheduler(daemon=True)
sched.add_job(poptask.exec_sche, "interval", minutes=10)
sched.add_job(poptask.exec_sche_urg, 'interval', seconds=10)
sched.start()

app = Flask(__name__)


@app.route("/")
def dashboard():
    poptask.act_lock.acquire()
    poptask.act = 6
    poptask.act_lock.release()
    ts = datetime.utcnow()
    ts = (ts - timedelta(minutes=1))
    out = list(vids.find({"publishedAt": {"$lt": ts}}, {"_id": 0}).sort(
        'publishedAt', pymongo.DESCENDING).limit(10))
    return render_template("index.html", out=out)


@app.route("/querydata")
def qdata():
    poptask.act_lock.acquire()
    poptask.act = 6
    poptask.act_lock.release()
    length = request.args.get("length", default=10)
    out = []
    if request.args.get("last") != None:
        ts = parse(request.args.get("last"))
        ts = ts.replace(tzinfo=timezone.utc)
        out = list(vids.find({"publishedAt": {"$lt": ts}}, {"_id": 0}).sort(
            'publishedAt', pymongo.DESCENDING).limit(length))
        pass
    elif request.args.get("first") != None:
        ts = parse(request.args.get("first"))
        ts = ts.replace(tzinfo=timezone.utc)
        out = list(vids.find({"publishedAt": {"$gt": ts}}, {"_id": 0}).sort(
            'publishedAt', pymongo.DESCENDING).limit(length))
        pass
    else:
        out = list(vids.find({}, {"_id": 0}).sort(
            'publishedAt', pymongo.DESCENDING).limit(length))
    return Response(
        response=json.dumps(out),
        mimetype='application/json'
    )


@app.route("/changesearch", methods=['POST'])
def changesearchterm():
    global vids
    dts = str(request.data)[2:-1]
    if len(dts) >= 2:
        poptask.src_term = dts
        vids = db[poptask.src_term+"vids"]
        poptask.create_collection()
        poptask.act_lock.acquire()
        poptask.act = 6
        poptask.act_lock.release()
        return Response(status=200)
    else:
        return Response(status=400)
