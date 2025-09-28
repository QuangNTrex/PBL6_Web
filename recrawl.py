import re
import json

with open("products_synced.json", "r", encoding="utf-8") as f:
    products = json.load(f)

def check():
    log = ""
    for p in products:
        if p["name"] == "" or p["name"] == "Name":
            log += "+ sai name\n"
        if p["price"] == 45000:
            log += "+ sai price\n"
        if not p["description"]:
            log += "+ sai desc\n"
        if not p.get("size"):
            log += "+ sai size\n"
        if not p.get("image_path"):
            log += "+ sai image\n"
        if not p.get("category_id"):
            log += "+ sai categ\n"
        if log:
            print(p.get("class"))
            print(log)
        log = ""

check()