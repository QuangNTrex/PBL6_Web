# from sqlalchemy import create_engine, MetaData, Table, select
# import json
# import datetime

# # Kết nối SQL Server
# DATABASE_URL = "mssql+pyodbc://@DESKTOP-1PDGM0O/PBL6_WEB?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
# engine = create_engine(DATABASE_URL)

# metadata = MetaData()
# metadata.reflect(engine)

# # Lấy bảng category
# category_table = metadata.tables.get("Categories")

# if category_table is None:
#     raise ValueError("Không tìm thấy bảng 'category' trong database")

# with engine.connect() as conn:
#     result = conn.execute(select(category_table))
#     rows = []
#     for row in result:
#         row_dict = dict(row._mapping)
#         # Convert datetime -> string
#         for key, value in row_dict.items():
#             if isinstance(value, (datetime.date, datetime.datetime)):
#                 row_dict[key] = value.isoformat()
#         rows.append(row_dict)

# # Xuất ra JSON
# with open("category.json", "w", encoding="utf-8") as f:
#     json.dump(rows, f, ensure_ascii=False, indent=4)

# print("✅ Đã export bảng category ra file category.json")


import json
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import json
from datetime import datetime
from sqlalchemy import create_engine, MetaData
 

# DATABASE_URL = "mssql+pyodbc://sa:123456789@localhost/PBL6?driver=ODBC+Driver+17+for+SQL+Server"
DATABASE_URL = "mssql+pyodbc://@DESKTOP-1PDGM0O/PBL6_WEB?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"

# Tạo engine kết nối
engine = create_engine(DATABASE_URL)



# 1. Kết nối đến SQL
# SQLite
# engine = create_engine("sqlite:///mydb.db", echo=True)

# MySQL
# engine = create_engine("mysql+pymysql://username:password@localhost:3306/mydb?charset=utf8mb4")

# PostgreSQL
# engine = create_engine("postgresql://username:password@localhost:5432/mydb")

metadata = MetaData()
metadata.reflect(bind=engine)

# 3. Lấy bảng Products
product_table = metadata.tables.get("Products")

if product_table is None:
    raise Exception("❌ Không tìm thấy bảng 'Products' trong DB. Kiểm tra lại tên bảng.")

# 4. Đọc dữ liệu từ file JSON (list sản phẩm)
with open("products_synced.json", "r", encoding="utf-8") as f:
    products_data = json.load(f)  # đây là list

# 5. Insert nhiều sản phẩm
with engine.connect() as conn:
    insert_list = []
    for product in products_data:
        insert_list.append({
            "code": product.get("class"),
            "name": product.get("name"),
            "price": float(product.get("price", 0)),
            "quantity": 50,
            "description": product.get("description"),
            "unit": "cái",
            "image_path": product.get("image_path"),
            "category_id": int(product.get("category_id")),
            
            "user_id": 1,  # ⚡ thay bằng user_id hợp lệ
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        })

    conn.execute(product_table.insert(), insert_list)
    conn.commit()
    print(f"✅ Insert {len(insert_list)} sản phẩm thành công!")
