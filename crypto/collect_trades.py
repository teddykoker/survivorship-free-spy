import requests
import time
import json
from pymongo import MongoClient

trades_url = "https://www.bitstamp.net/api/v2/transactions/btcusd"


def create_trade(trade):
    return {
        "_id": int(trade["tid"]),
        "timestamp": int(trade["date"]),
        "price": float(trade["price"]),
        "amount": float(trade["amount"]),
    }


def get_trades():
    resp = requests.get(trades_url)
    data = resp.json()
    data = [create_trade(t) for t in data]
    return data, resp.status_code


def main():
    print("collecting trades")

    client = MongoClient()
    db = client["crypto"]
    trades_db = db["trades"]

    while True:
        start = time.time()
        try:
            trades, code = get_trades()
        except Exception as e:
            print(e)
        else:
            if code != 200:
                print(code)
            else:
                for trade in trades:
                    trades_db.update_one(
                        {"_id": trade["_id"]}, {"$setOnInsert": trade}, upsert=True
                    )
                time.sleep(60 * 58)  # sleep for 58 min so we dont miss any data


if __name__ == "__main__":
    main()
