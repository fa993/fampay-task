from flask import Flask, Response, json, request, render_template
from pymongo import MongoClient
import pymongo
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
from dateutil.parser import *
import poptask
import os

load_dotenv()

client = MongoClient(host=os.environ["DB_URI"])

db = client.get_default_database()
vids = db[poptask.src_term+"vids"]

sched = BackgroundScheduler(daemon=True)
# sched.add_job(poptask.exec_sche, "interval", minutes=10)
# sched.add_job(poptask.exec_sche_urg, 'interval', seconds=10)
sched.start()

app = Flask(__name__)


@app.route("/")
def dashboard():
    # poptask.act = 6
    out = list(vids.find({}, {"_id": 0}).sort(
        'publishedAt', pymongo.DESCENDING).limit(10))
    return render_template("index.html", out=out)


@app.route("/querydata")
def qdata():
    poptask.act = 6
    length = request.args.get("length", default=10)
    out = []
    if request.args.get("last") != None:
        out = list(vids.find({"publishedAt": {"$lt": parse(request.args.get("last"))}}, {"_id": 0}).sort(
            'publishedAt', pymongo.DESCENDING).limit(length))
        pass
    elif request.args.get("first") != None:
        out = list(vids.find({"publishedAt": {"$gt": parse(request.args.get("first"))}}, {"_id": 0}).sort(
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
    if len(str(request.data)) >= 2:
        poptask.src_term = request.data
        poptask.create_collection()
        poptask.act = 6
        return Response(status=200)
    else:
        return Response(status=400)
