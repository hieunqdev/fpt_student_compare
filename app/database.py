from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Load biến môi trường từ .env
load_dotenv()

# Lấy DATABASE_URL từ file .env
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:1@localhost/db_fpt_student_compare")

# Tạo engine kết nối PostgreSQL
engine = create_engine(DATABASE_URL)

# Tạo session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Kiểm tra kết nối
def test_connection():
    try:
        with engine.connect() as connection:
            print("✅ Kết nối đến PostgreSQL thành công!")
    except Exception as e:
        print(f"❌ Lỗi kết nối: {e}")

if __name__ == "__main__":
    test_connection()
