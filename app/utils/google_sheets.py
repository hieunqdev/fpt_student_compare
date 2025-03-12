# import requests
# import pandas as pd
# from io import StringIO
#
# def lay_danh_sach_sinh_vien_tu_sheets(sheet_url: str):
#     """
#     Truy xuất danh sách sinh viên từ Google Sheets bằng Pandas.
#     Google Sheets cần được chia sẻ công khai (Anyone with the link can view).
#     """
#     try:
#         # Chuyển đổi URL thành dạng CSV
#         sheet_id = sheet_url.split("/d/")[1].split("/")[0]
#         csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
#
#         # Dùng session để tối ưu request
#         session = requests.Session()
#         response = session.get(csv_url, timeout=10)
#         response.raise_for_status()
#
#         # Đọc CSV trực tiếp vào Pandas
#         df = pd.read_csv(StringIO(response.content.decode("utf-8")), dtype=str)
#
#         # Xóa các dòng có dữ liệu trống hoặc không hợp lệ
#         df = df.dropna(subset=['MSSV'])
#
#         # Định dạng dữ liệu nhanh bằng `.apply()`
#         df = df.iloc[:, 0:8].apply(lambda x: x.str.strip().str.replace("\n", " "))
#
#         # Đổi tên cột theo yêu cầu
#         df.columns = ["stt", "mssv", "ho_va_ten", "ngay_sinh", "gioi_tinh", "dan_toc", "chuyen_nganh", "nganh"]
#
#         # Xử lý NaN, Inf, -Inf trước khi convert JSON
#         df = df.fillna("").replace([float('inf'), -float('inf')], 0)
#
#         return df.to_dict(orient="records")
#
#     except Exception as e:
#         raise Exception(f"Lỗi khi lấy dữ liệu từ Google Sheets: {str(e)}")
