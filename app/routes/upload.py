from fastapi import APIRouter, HTTPException, UploadFile, File, Depends, BackgroundTasks
from app.utils.google_sheets import lay_danh_sach_sinh_vien_tu_sheets
from app.utils.pdf_reader import lay_danh_sach_sinh_vien_tu_pdf
from pydantic import BaseModel
import time
from app.database import SessionLocal
from sqlmodel import Session
from app.models.sinh_vien import SinhVien


router = APIRouter()

class GoogleSheetRequest(BaseModel):
    sheet_url: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def normalize_text(text):
    """Chuẩn hóa văn bản: loại bỏ khoảng trắng hai đầu, xuống dòng và viết thường"""
    return text.strip().replace("\n", " ").lower() if text else ""

def compare_students(ds_sinh_vien_sheets, ds_sinh_vien_pdf):
    """
    Hàm so sánh danh sách sinh viên giữa Google Sheets và database (PDF).
    Trả về danh sách sinh viên có thông tin khác nhau.
    """
    ds_sinh_vien_pdf_dict = {sv.mssv: sv for sv in ds_sinh_vien_pdf}
    cap_nhat_ket_qua = []

    for sv_sheets in ds_sinh_vien_sheets:
        mssv = sv_sheets["mssv"]
        sv_pdf = ds_sinh_vien_pdf_dict.get(mssv)

        if sv_pdf:
            khac_biet = []

            if normalize_text(sv_sheets["ho_va_ten"]) != normalize_text(sv_pdf.ho_va_ten):
                khac_biet.append(f"Họ và tên: {normalize_text(sv_sheets['ho_va_ten'])} → {normalize_text(sv_pdf.ho_va_ten)}")

            if normalize_text(sv_sheets["ngay_sinh"]) != normalize_text(sv_pdf.ngay_sinh):
                khac_biet.append(f"Ngày sinh: {normalize_text(sv_sheets['ngay_sinh'])} → {normalize_text(sv_pdf.ngay_sinh)}")

            if normalize_text(sv_sheets["gioi_tinh"]) != normalize_text(sv_pdf.gioi_tinh):
                khac_biet.append(f"Giới tính: {normalize_text(sv_sheets['gioi_tinh'])} → {normalize_text(sv_pdf.gioi_tinh)}")

            if normalize_text(sv_sheets["nganh"]) != normalize_text(sv_pdf.nganh):
                khac_biet.append(f"Ngành: {normalize_text(sv_sheets['nganh'])} → {normalize_text(sv_pdf.nganh)}")

            if khac_biet:
                cap_nhat_ket_qua.append({"mssv": mssv, "ghi_chu": ", ".join(khac_biet)})

    return cap_nhat_ket_qua

@router.post("/upload/sheets")
async def upload_google_sheets(request: GoogleSheetRequest, db: Session = Depends(get_db)):
    """
    API để nhập danh sách sinh viên từ Google Sheets, so sánh với danh sách từ PDF trong database.
    """
    try:
        start_time = time.time()

        # 1. Lấy danh sách sinh viên từ Google Sheets
        ds_sinh_vien_sheets = lay_danh_sach_sinh_vien_tu_sheets(request.sheet_url)

        # 2. Lấy danh sách sinh viên từ database (PDF đã upload trước đó)
        ds_sinh_vien_pdf = db.query(SinhVien).all()

        # 3. So sánh danh sách sinh viên
        cap_nhat_ket_qua = compare_students(ds_sinh_vien_sheets, ds_sinh_vien_pdf)

        end_time = time.time()
        print(f"Thời gian thực thi: {end_time - start_time:.4f} giây")

        return {
            "status": "success",
            "message": "Nhập danh sách từ Google Sheets thành công!",
            "so_luong_sinh_vien": len(ds_sinh_vien_sheets),
            "khac_biet": cap_nhat_ket_qua
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/upload/pdf")
async def upload_pdf(files: list[UploadFile] = File(...), background_tasks: BackgroundTasks = BackgroundTasks(),
                     db: Session = Depends(get_db)):
    """
    API tải lên file PDF chứa danh sách sinh viên và lưu vào PostgreSQL.
    """
    print("hello world")
    file_data_list = [(await file.read(), file.filename) for file in files]  # Đọc file ngay tại đây

    def process_and_save_pdfs():
        danh_sach_tat_ca_sinh_vien = []
        for file_bytes, filename in file_data_list:
            danh_sach_sinh_vien = lay_danh_sach_sinh_vien_tu_pdf(file_bytes, filename, db)
            danh_sach_tat_ca_sinh_vien.extend(danh_sach_sinh_vien)

        db.bulk_save_objects(danh_sach_tat_ca_sinh_vien)
        db.commit()

    # Chạy xử lý dữ liệu trong nền
    background_tasks.add_task(process_and_save_pdfs)

    return {
        "status": "processing",
        "message": "Dữ liệu đang được xử lý và lưu vào database.",
    }


