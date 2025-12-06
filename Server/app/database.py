from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# ==============================
# Cấu hình kết nối SQL Server
# ==============================
# DATABASE_URL = "mssql+pyodbc://sa:123456789@localhost/PBL6?driver=ODBC+Driver+17+for+SQL+Server"
DATABASE_URL = "mssql+pyodbc://@DESKTOP-1PDGM0O/PBL6_WEB?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
# DATABASE_URL = "mssql+pyodbc://sa:123456aA%40%24@localhost:1433/PBL6_WEB?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes"
# Tạo engine kết nối
engine = create_engine(DATABASE_URL)

# SessionLocal: mỗi request sẽ tạo 1 session riêng
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base: cho models kế thừa
Base = declarative_base()

# Dependency để dùng trong FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()