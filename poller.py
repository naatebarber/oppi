import requests
import os
import json

API_KEY = os.environ.get("RAPIKEY")
API_URL = os.environ.get("RAPIURL")


def poll(log=False):
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": "alpha-vantage.p.rapidapi.com",
    }

    query = {
        "function": "CRYPTO_INTRADAY",
        "symbol": "DOGE",
        "market": "USD",
        "interval": "5min",
        "output_size": "full",
    }

    r = requests.get(API_URL, params=query, headers=headers)
    r = r.json()

    if log:
        curpath = os.path.dirname(os.path.realpath(__file__))
        rlogpath = os.path.join(curpath, "requests.log")
        f = open(rlogpath, "a")
        f.write(json.dumps(r) + "\n")
        f.close()

    r = list(list(r.values())[1].values())
    for i in range(len(r)):
        r[i] = list(r[i].values())
        for j in range(len(r[i])):
            r[i][j] = float(r[i][j])

    return r
