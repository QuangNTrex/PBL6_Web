import csv
import json

# Đọc dữ liệu từ file JSON
with open("products_synced.json", "r", encoding="utf-8") as f:
    products = json.load(f)

# Sort theo class
products_sorted = sorted(products, key=lambda x: x["class"])

# Ghi file CSV với utf-8-sig để Excel đọc được tiếng Việt
with open("products-sync.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["class", "name", "price", "size"])  # header
    for p in products_sorted:
        writer.writerow([p["class"], p["name"], p["price"], p["size"]])

print("✅ Dữ liệu đã lưu vào products.csv với UTF-8 BOM (Excel đọc tiếng Việt OK).")