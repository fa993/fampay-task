from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta
from dateutil.parser import *
import requests
import os
import json
import logging

load_dotenv()

src_term = os.environ["YT_QUERY"]

client = MongoClient(host=os.environ["DB_URI"])
db = client.ytsc

try:
    db.create_collection(src_term+"vids",
                         {
                             "timeseries": {
                                 "timeField": "publishedAt",
                                 "granularity": "seconds"
                             },
                             "expireAfterSeconds": 86400
                         }
                         )
    logging.debug("Created collection successfully")
except Exception:
    # do nothing
    pass

vids = db[src_term+"vids"]


def exec_sche():
    ts = (datetime.now(timezone.utc) -
          timedelta(hours=1)).astimezone().isoformat()

    payload = {"part": "snippet", "maxResults": 25,
               "q": src_term, "key": os.environ["API_KEY"],
               "type": "video", "order": "date",
               "publishedAfter": ts}

    r = requests.get(
        "https://youtube.googleapis.com/youtube/v3/search", params=payload)

    rt = json.loads(r.text)

    rtp = map(lambda x: {"_id": x["id"]["videoId"], "title": x["snippet"]["title"], "description": x["snippet"]["description"],
                         "publishedAt": parse(x["snippet"]["publishedAt"]), "thumbnail": x["snippet"]["thumbnails"]["default"]["url"]}, rt["items"])
    try:
        vids.insert_many(rtp, ordered=False)
    except Exception as e:
        print(e)
        # do nothing
        pass
    logging.info("Scheduled Insert Finished")


# exec_sche()
