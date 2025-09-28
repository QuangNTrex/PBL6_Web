# import csv
# import json

# classes = []
# with open("data.csv", "r", encoding="utf-8") as f:
#     classes = [line.strip() for line in f]
# products = []
# with open("products.json", "r", encoding="utf-8") as ff:
#     products = json.load(ff)

# for p in products:
#     if p["class"] in classes:
#         continue
#     else:
#         print(p["class"])


# import re
# import json

# def extract_name_size(line):
#     """
#     Tách tên sản phẩm (name) và kích thước (size) từ 1 dòng text
#     """
#     pattern = r'(\d+(?:[.,]\d+)?\s*×\s*\d+(?:[.,]\d+)?\s*×\s*\d+(?:[.,]\d+)?\s*cm)'
#     match = re.search(pattern, line)
#     if match:
#         size = match.group(1).strip()
#         name = line.replace(size, "").replace(":", "").strip()
#         return {"name": name, "size": size}
#     else:
#         return {"name": line.strip(), "size": None}

# def process_file(input_file, output_file):
#     results = []
#     with open(input_file, "r", encoding="utf-8") as f:
#         for line in f:
#             if line.strip():  # bỏ dòng trống
#                 results.append(extract_name_size(line))

#     # Ghi ra file JSON
#     with open(output_file, "w", encoding="utf-8") as f:
#         json.dump(results, f, ensure_ascii=False, indent=4)

# # chạy thử
# process_file("name.txt", "output.json")




import json
import unicodedata

def remove_accents(input_str: str) -> str:
    # Chuẩn hóa chuỗi Unicode thành dạng NFD (Normalization Form Decomposition)
    nfkd_form = unicodedata.normalize('NFD', input_str)
    # Lọc bỏ các ký tự thuộc loại "dấu" (Mn = Mark, Nonspacing)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])


def sync_size(products_file, size_file, output_file):
    # Load dữ liệu
    with open(products_file, "r", encoding="utf-8") as f:
        products = json.load(f)

    with open(size_file, "r", encoding="utf-8") as f:
        categories = json.load(f)

    # Tạo map từ tên -> size
    # size_map = {item["name"].lower(): item["size"] for item in sizes if item["size"]}

    # Đồng bộ
    for product in products:
        for category in categories:
            if (category["name"].lower() in product["name"].lower()) or (remove_accents(category["name"].lower().replace(" ", "")) in product["class"].lower()):
                product["category_name"] = category["name"]
                product["category_id"] = category["id"]
                break
        if not product.get("category_id"):
            for category in categories:
                if product.get("category_id"): break
                if not category.get("keyword"):
                    continue
                for k in category["keyword"]:
                    if (k.lower() in product["name"].lower()) or (remove_accents(k.lower().replace(" ", "")) in product["class"].lower()):
                        product["category_name"] = category["name"]
                        product["category_id"] = category["id"]
                        break
        if not product.get("category_id"):
            print("ko them duoc product: " + product["name"])
    # Ghi ra file mới
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(products, f, ensure_ascii=False, indent=4)

# chạy thử
sync_size("products.json", "category.json", "products_synced.json")




