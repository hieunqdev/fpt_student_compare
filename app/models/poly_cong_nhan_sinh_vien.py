from sqlmodel import SQLModel, Field
from typing import Optional

class PolyCongNhanSinhVien(SQLModel, table=True):
    __tablename__ = "poly_cong_nhan_sinh_vien"

    id: Optional[int] = Field(default=None, primary_key=True)
    ten_file : Optional[str] = Field(default=None)
    so_qd: Optional[str] = Field(default=None)
    mssv: str = Field(index=True, unique=True)
    ho_va_ten: str
    ngay_sinh: Optional[str] = None
    gioi_tinh: Optional[str] = None
    dan_toc: Optional[str] = None
