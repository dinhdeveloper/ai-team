# Testcase: <Tên tính năng>

**SDD:** `docs/sdd/<slug>/SDD.md` (vX.Y)
**Yêu cầu nghiệp vụ:** <mô tả ngắn hoặc link tài liệu>
**Điều kiện chung:** <user đã login, tài khoản có số dư ≥ X, môi trường UAT...>

| ID | AC | Tên testcase | Tiền điều kiện | Bước thực hiện | Kết quả mong đợi | Cách kiểm | Mức |
|----|----|--------------|----------------|----------------|------------------|-----------|-----|
| TC01 | AC01 | Thanh toán thành công | Số dư đủ | 1. Nhập 100.000đ 2. Xác nhận | Hiển thị màn thành công, số dư giảm 100.000đ | Unit test | Cao |
| TC02 | AC02 | Số tiền = 0 | | 1. Nhập 0 | Nút Xác nhận bị disable | Unit test | Cao |
| TC03 | AC03 | Mất mạng khi xác nhận | | 1. Tắt mạng 2. Xác nhận | Báo lỗi mạng, không trừ tiền, cho thử lại | Unit test | Cao |
| TC04 | AC03 | Bấm Xác nhận 2 lần liên tiếp | | 1. Double tap | Chỉ tạo 1 giao dịch | Unit test | Cao |
| TC05 | AC01 | Hiển thị đúng design | | 1. Mở màn hình | Đúng layout theo Figma | Thủ công | Trung bình |

> Cách kiểm: `Unit test` (tester viết test tự động) · `Đọc code` (tester soát logic) · `Thủ công` (anh tự test trên máy)
