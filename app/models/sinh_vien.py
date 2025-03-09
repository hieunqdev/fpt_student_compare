from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date

class SinhVien(SQLModel, table=True):
    __tablename__ = "sinh_vien_quyet_dinh"

    id: Optional[int] = Field(default=None, primary_key=True)
    so_qd: Optional[str] = Field(default=None)
    stt: Optional[str] = Field(default=None)
    mssv: str = Field(index=True, unique=True)
    ho_va_ten: str
    ngay_sinh: Optional[str] = None
    gioi_tinh: Optional[str] = None
    dan_toc: Optional[str] = None
    chuyen_nganh: Optional[str] = None
    nganh: Optional[str] = None
