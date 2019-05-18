import requests
import time
import json
from pymongo import MongoClient

books_url = "https://www.bitstamp.net/api/v2/order_book/btcusd"


def create_entry(entry):
    return {"price": float(entry[0]), "amount": float(entry[1])}


def get_books():
    resp = requests.get(books_url)
    data = resp.json()
    data["bids"] = [create_entry(e) for e in data["bids"][:25]]
    data["asks"] = [create_entry(e) for e in data["asks"][:25]]
    data["_id"] = data.pop("timestamp")
    return data, resp.status_code


def main():
    print("collecting books")

    client = MongoClient()
    db = client["crypto"]
    books_db = db["books"]

    while True:
        start = time.time()
        try:
            books, code = get_books()
        except Exception as e:
            print(e)
        else:
            if code != 200:
                print(code)
            else:
                books_db.update_one(
                    {"_id": books["_id"]}, {"$setOnInsert": books}, upsert=True
                )
                time_delta = time.time() - start
                if time_delta < 5:
                    time.sleep(5 - time_delta)


if __name__ == "__main__":
    main()

