from sqlmodel import SQLModel, Field
from typing import Optional

class PolyMienGiamMonHoc(SQLModel, table=True):
    __tablename__ = "poly_mien_giam_mon_hoc"

    id: Optional[int] = Field(default=None, primary_key=True)
    ten_file : Optional[str] = Field(default=None)
    so_qd: Optional[str] = Field(default=None)
    mssv: str = Field(index=True, unique=True)
    ho_va_ten: str
