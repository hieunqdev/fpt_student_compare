import pdfplumber
import re
import io
import time
from app.models.poly_cong_nhan_sinh_vien import PolyCongNhanSinhVien

# Poly lấy danh sách Công nhận sinh viên
def poly_cong_nhan_sinh_vien_lay_danh_sach_sinh_vien_tu_pdf(file_bytes, filename, db):
    """
        Trích xuất danh sách sinh viên từ PDF Poly Công nhận sinh viên.
    """
    danh_sach_sinh_vien = []

    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            if tables:
                for table in tables:
                    for row in table:
                        if len(row) >= 2:
                            ten_file = filename
                            match = re.search(r'QD\s*(\d+)', filename)
                            so_qd = match.group(1) if match else None
                            ma_sinh_vien = row[1].strip() if row[1] else None
                            ho_ten = row[2].strip() if row[2] else None
                            ngay_sinh = row[3].strip() if row[3] else None
                            gioi_tinh = row[4].strip() if row[4] else None
                            dan_toc = row[5].strip() if row[5] else None

                            if ma_sinh_vien and ho_ten:
                                sinh_vien = {
                                    "ten_file": ten_file,
                                    "so_qd": so_qd,
                                    "mssv": ma_sinh_vien,
                                    "ho_va_ten": ho_ten,
                                    "ngay_sinh": ngay_sinh,
                                    "gioi_tinh": gioi_tinh,
                                    "dan_toc": dan_toc,
                                }
                                danh_sach_sinh_vien.append(sinh_vien)

                                # Nếu cần lưu vào database
                                db_sinh_vien = PolyCongNhanSinhVien(**sinh_vien)
                                db.add(db_sinh_vien)

        db.commit()  # Lưu vào database

    return danh_sach_sinh_vien


def lay_danh_sach_sinh_vien_tu_pdf(file_bytes, filename, db):
    """
    Trích xuất danh sách sinh viên từ PDF từ bytes file.
    """
    danh_sach_sinh_vien = []

    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            if tables:
                for table in tables:
                    for row in table:
                        if len(row) >= 2:
                            match = re.search(r'QD\s*(\d+)', filename)
                            so_qd = match.group(1) if match else None
                            stt = row[0].strip() if row[1] else None
                            ma_sinh_vien = row[1].strip() if row[1] else None
                            ho_ten = row[2].strip() if row[2] else None
                            ngay_sinh = row[3].strip() if row[3] else None
                            gioi_tinh = row[4].strip() if row[4] else None
                            dan_toc = row[5].strip() if row[5] else None
                            chuyen_nganh = row[6].strip() if row[5] else None
                            nganh = row[7].strip() if row[6] else None

                            if ma_sinh_vien and ho_ten:
                                sinh_vien = {
                                    "so_qd": so_qd,
                                    "stt": stt,
                                    "mssv": ma_sinh_vien,
                                    "ho_va_ten": ho_ten,
                                    "ngay_sinh": ngay_sinh,
                                    "gioi_tinh": gioi_tinh,
                                    "dan_toc": dan_toc,
                                    "chuyen_nganh": chuyen_nganh,
                                    "nganh": nganh,
                                }
                                danh_sach_sinh_vien.append(sinh_vien)

                                # Nếu cần lưu vào database
                                from app.models.sinh_vien import SinhVien
                                db_sinh_vien = SinhVien(**sinh_vien)
                                db.add(db_sinh_vien)

        db.commit()  # Lưu vào database

    return danh_sach_sinh_vien