import pdfplumber
import re
import io
import time
from app.models.poly_cong_nhan_sinh_vien import PolyCongNhanSinhVien
from app.models.poly_mien_giam_mon_hoc import PolyMienGiamMonHoc
import numpy as np

# Poly lấy danh sách Công nhận sinh viên
def poly_cong_nhan_sinh_vien_lay_danh_sach_sinh_vien_tu_pdf(file_bytes, filename, ten_quyet_dinh, db):
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
                                    "so_qd": ten_quyet_dinh,
                                    "mssv": ma_sinh_vien,
                                    "ho_va_ten": ho_ten,
                                    "ngay_sinh": ngay_sinh,
                                    "gioi_tinh": gioi_tinh,
                                    "dan_toc": dan_toc,
                                }
                                danh_sach_sinh_vien.append(sinh_vien)

                                # Nếu cần lưu vào database
                                db_sinh_vien = PolyCongNhanSinhVien(**sinh_vien)
                                db.merge(db_sinh_vien)

        db.commit()  # Lưu vào database

    return danh_sach_sinh_vien

def poly_mien_giam_mon_hoc_lay_danh_sach_sinh_vien_tu_pdf(file_bytes, filename, db):
    """
        Trích xuất danh sách sinh viên từ PDF Poly Công nhận sinh viên.
    """
    danh_sach_sinh_vien = []

    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()

            if tables:

                for table in tables:
                    table = np.array(table).T.tolist()  # Hoán đổi dòng/cột

                    # Chuyển danh sách các cột thành danh sách các dòng
                    for i in range(len(table[0])):  # Lặp qua từng hàng dựa trên độ dài cột đầu tiên
                        row_data = [col[i] if i < len(col) else None for col in table]  # Lấy từng giá trị từ mỗi cột
                        print(f"Row: {row_data}")
                        if len(row_data) >= 3:  # Kiểm tra có đủ dữ liệu
                            ten_file = filename
                            match = re.search(r'QD\s*(\d+)', filename)
                            so_qd = match.group(1) if match else None
                            ma_sinh_vien = row_data[1].strip() if row_data[1] else None
                            ho_ten = row_data[2].strip() if row_data[2] else None

                            if ma_sinh_vien and ho_ten:
                                sinh_vien = {
                                    "ten_file": ten_file,
                                    "so_qd": so_qd,
                                    "mssv": ma_sinh_vien,
                                    "ho_va_ten": ho_ten,
                                }
                                danh_sach_sinh_vien.append(sinh_vien)
                                print(danh_sach_sinh_vien)
                                # Nếu cần lưu vào database
                                try:
                                    db_sinh_vien = PolyMienGiamMonHoc(**sinh_vien)  # Tạo instance đúng
                                    db.merge(db_sinh_vien)  # Sử dụng add() thay vì merge()
                                    db.commit()
                                    print("Data saved successfully!")
                                except Exception as e:
                                    db.rollback()
                                    print(f"Error saving data: {e}")
    return danh_sach_sinh_vien
