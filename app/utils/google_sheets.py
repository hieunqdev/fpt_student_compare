import gspread
import requests
import csv
from io import StringIO


def lay_danh_sach_sinh_vien_tu_sheets(sheet_url: str):
    """
    Truy xuất danh sách sinh viên từ Google Sheets bằng requests.
    Google Sheets cần được chia sẻ công khai (Anyone with the link can view).
    """
    try:
        # Chuyển đổi URL thành dạng CSV
        sheet_id = sheet_url.split("/d/")[1].split("/")[0]
        csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

        # Gửi request đến Google Sheets
        response = requests.get(csv_url)
        response.raise_for_status()  # Kiểm tra lỗi HTTP

        # Đọc dữ liệu CSV từ nội dung phản hồi
        csv_data = StringIO(response.content.decode("utf-8"))
        reader = csv.reader(csv_data)

        # Bỏ dòng tiêu đề và xử lý danh sách sinh viên
        danh_sach_sinh_vien = []
        next(reader)  # Bỏ dòng tiêu đề

        for row in reader:
            if len(row) >= 2:  # Đảm bảo có ít nhất 2 cột
                danh_sach_sinh_vien.append({
                    "MSSV": row[1].strip().replace("\n", " "),
                    "Họ và tên": row[2].strip().replace("\n", " "),
                    "Ngày sinh": row[3].strip().replace("\n", " "),
                    "Giới tính": row[4].strip().replace("\n", " "),
                    "Dân tộc": row[5].strip().replace("\n", " "),
                    "Chuyên ngành": row[6].strip().replace("\n", " "),
                    "Ngành": row[7].strip().replace("\n", " "),
                })

        return danh_sach_sinh_vien

    except Exception as e:
        raise Exception(f"Lỗi khi lấy dữ liệu từ Google Sheets: {str(e)}")
