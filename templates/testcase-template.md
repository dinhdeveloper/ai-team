# Testcase: <Tên tính năng>

**Yêu cầu nghiệp vụ:** <mô tả ngắn hoặc link tài liệu>
**Điều kiện chung:** <user đã login, tài khoản có số dư ≥ X, môi trường UAT...>

| ID | Tên testcase | Tiền điều kiện | Bước thực hiện | Kết quả mong đợi | Mức độ |
|----|--------------|----------------|----------------|------------------|--------|
| TC01 | Thanh toán thành công | Số dư đủ | 1. Nhập 100.000đ 2. Xác nhận | Hiển thị màn thành công, số dư giảm 100.000đ | Cao |
| TC02 | Số tiền = 0 | | 1. Nhập 0 | Nút Xác nhận bị disable | Cao |
| TC03 | Mất mạng khi xác nhận | | 1. Tắt mạng 2. Xác nhận | Báo lỗi mạng, không trừ tiền, cho thử lại | Cao |
| TC04 | Bấm Xác nhận 2 lần liên tiếp | | 1. Double tap | Chỉ tạo 1 giao dịch | Cao |
