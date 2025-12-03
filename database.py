

import json
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import json
from datetime import datetime
from sqlalchemy import create_engine, MetaData
 

# DATABASE_URL = "mssql+pyodbc://sa:123456789@localhost/PBL6?driver=ODBC+Driver+17+for+SQL+Server"
# DATABASE_URL = "mssql+pyodbc://@DESKTOP-1PDGM0O/PBL6_WEB?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
DATABASE_URL = "mssql+pyodbc://sa:123456aA%40%24@localhost:1433/PBL6_WEB?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes"
# Tạo engine kết nối
engine = create_engine(DATABASE_URL)

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
