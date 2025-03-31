import uvicorn
from fastapi import FastAPI
from app.routes.upload import router as upload_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Cấu hình CORS
app = FastAPI(
    title="FPTStudentCompare",
    description="API giúp so sánh danh sách sinh viên giữa Google Sheets và PDF",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cho phép tất cả các nguồn
    allow_credentials=True,
    allow_methods=["*"],  # Cho phép tất cả các phương thức (GET, POST, v.v.)
    allow_headers=["*"],  # Cho phép tất cả các header
)

# Đăng ký các router từ routes
app.include_router(upload_router, prefix="/api", tags=["Upload"])

# Điểm bắt đầu chạy server bằng uvicorn
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
