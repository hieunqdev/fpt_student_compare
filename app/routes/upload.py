from fastapi import APIRouter, HTTPException, UploadFile, File
from app.utils.google_sheets import lay_danh_sach_sinh_vien_tu_sheets
from typing import List
from app.utils.pdf_reader import lay_danh_sach_sinh_vien_tu_pdf
from pydantic import BaseModel


router = APIRouter()

router = APIRouter()

class GoogleSheetRequest(BaseModel):
    sheet_url: str

@router.post("/upload/sheets")
async def upload_google_sheets(request: GoogleSheetRequest):
    """
    API để nhập danh sách sinh viên từ Google Sheets bằng requests.
    """
    try:
        danh_sach_sinh_vien = lay_danh_sach_sinh_vien_tu_sheets(request.sheet_url)
        return {
            "status": "success",
            "message": "Nhập danh sách từ Google Sheets thành công!",
            "sinh_vien": danh_sach_sinh_vien
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/upload/pdf")
async def upload_pdf(files: List[UploadFile] = File(...)):
    """
    API tải lên file PDF chứa danh sách sinh viên.
    """
    danh_sach_tat_ca_sinh_vien = []

    try:
        for file in files:
            so_qd = lay_danh_sach_sinh_vien_tu_pdf(file)
            # sinh_vien = lay_danh_sach_sinh_vien_tu_pdf(file)
            # danh_sach_tat_ca_sinh_vien.extend(sinh_vien)

        return {
            "status": "success",
            "message": "Nhập danh sách từ PDF thành công!",
            "so_qd": so_qd,
            # "sinh_vien": danh_sach_tat_ca_sinh_vien
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Lỗi: {str(e)}")
