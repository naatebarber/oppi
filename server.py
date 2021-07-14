from flask import Flask
from poller import poll

app = Flask(__name__)


@app.route("/poll-api")
def poll_api():
    data = poll()
    print(data)
