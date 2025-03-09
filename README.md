# Quản lý và Xác minh Quyết định Sinh viên

## Mô tả
Dự án này giúp tự động kiểm tra và xác minh các quyết định liên quan đến sinh viên bằng cách đối chiếu dữ liệu từ danh sách sinh viên và danh sách quyết định.

## Yêu cầu đầu vào
- **Danh sách sinh viên**: Google Sheets hoặc Excel, chứa thông tin sinh viên.
- **Danh sách quyết định**: Chứa các quyết định như công nhận sinh viên, kỷ luật, chuyển cơ sở, nghỉ học, v.v.

## Mục tiêu
- Đọc dữ liệu từ danh sách sinh viên và danh sách quyết định.
- Xác định sinh viên nào đã có quyết định công nhận.
- Kiểm tra thông tin chi tiết trong quyết định để phát hiện sai sót.
- Xác định sinh viên có thay đổi trạng thái (ví dụ: chuyển cơ sở, nghỉ học).
- Lưu kết quả vào file Google Sheets hoặc Excel.

## Các bước triển khai

### 1. Đọc dữ liệu từ Google Sheets hoặc Excel
- **Google Sheets**: Sử dụng thư viện `gspread` để đọc dữ liệu. (1000 sv: 1s)
- **Excel**: Sử dụng thư viện `pandas` để xử lý file `.xlsx`. (20000 sv: 2p lần đầu, 0s các lần sau)

### 2. Xử lý dữ liệu
- Dùng **mã sinh viên** để tra cứu thông tin trong danh sách quyết định.
- Đánh dấu sinh viên nào đã có **quyết định công nhận**.
- Kiểm tra thông tin chi tiết (tên, ngành, dân tộc, ...) để phát hiện **sai lệch**.
- Xác định sinh viên có **thay đổi trạng thái** (chuyển cơ sở, nghỉ học, ...).

### 3. Cập nhật kết quả
- Ghi lại kết quả vào **Google Sheets** hoặc **Excel**.
- Nếu sinh viên **chưa có quyết định**, tiếp tục kiểm tra trong các kỳ tiếp theo.


