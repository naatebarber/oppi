from apscheduler.schedulers.blocking import BlockingScheduler
from poller import poll
from datastore import Datastore
import json

def poll_and_persist():
    """
    Pulls new data from market API, stores in Sqlite3 database, trains model.
    """

    db = Datastore().setup()
    data = poll()

    data_blob = json.dumps(data)
    db.persist(data_blob)
    records = db.fetch_all()
    print(len(records))

    db.close()

    # train model and save joblib



def test():
    print("hello")


scheduler = BlockingScheduler()
scheduler.add_job(poll_and_persist, "interval", hours=1)
scheduler.start()
