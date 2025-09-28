import csv
import json

reader = []
products = []
with open("data.csv", mode="r", encoding="utf-8") as file:
    reader = list(csv.reader(file))
with open("products.json", "r", encoding="utf-8") as f:
    products = json.load(f)

for p in products:
    for r in reader:
        if p["class"] == r[0]:
            p["name"] = r[1]
            p["price"] = int(r[2])
            p["size"] = r[3]

with open("products_synced.json", "w", encoding="utf-8") as out:
    json.dump(products, out, ensure_ascii=False, indent=4)


        
