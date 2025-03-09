from database import engine
from models.sinh_vien import SQLModel

def create_tables():
    print("⏳ Đang tạo bảng trong cơ sở dữ liệu...")
    SQLModel.metadata.create_all(engine)
    print("✅ Đã tạo xong bảng!")

if __name__ == "__main__":
    create_tables()
