import pdfplumber
import re

def lay_danh_sach_sinh_vien_tu_pdf(file):
    """
    Trích xuất dữ liệu từ bảng trong PDF.
    """
    danh_sach_sinh_vien = []

    # with pdfplumber.open(file.file) as pdf:
    #     for page in pdf.pages:
    #         tables = page.extract_tables()  # Lấy tất cả bảng trên trang
    #         if tables:
    #             for table in tables:
    #                 for row in table:
    #                     if len(row) >= 2:  # Mã SV + Họ tên
    #                         ma_sinh_vien = row[1].strip() if row[0] else None
    #                         ho_ten = row[2].strip() if row[1] else None
    #
    #                         if ma_sinh_vien and ho_ten:
    #                             danh_sach_sinh_vien.append({
    #                                 "ma_sinh_vien": ma_sinh_vien,
    #                                 "ho_ten": ho_ten
    #                             })

    file_name = file.filename
    match = re.search(r'QD\s*(\d+)', file_name)
    so_qd = match.group(1) if match else None
    return so_qd
