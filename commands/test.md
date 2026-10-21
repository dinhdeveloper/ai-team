---
description: Chỉ chạy Tester kiểm tra thay đổi hiện tại theo nghiệp vụ hoặc file testcase
argument-hint: <mô tả nghiệp vụ> [testcase: đường/dẫn/file]
---

Yêu cầu nghiệp vụ / testcase của người dùng (NGUYÊN VĂN):
"""
$ARGUMENTS
"""

1. Chạy `git status` và ghi lại.
2. Gọi agent `tester` chỉ với nội dung trên. Không thêm giải thích nào về code.
3. Chạy lại `git status`. Nếu có file thay đổi so với bước 1 → cảnh báo người dùng.
4. Hiển thị nguyên báo cáo `🧪 TESTER — BÁO CÁO`.
5. Nếu ❌ FAIL: hỏi người dùng có muốn gửi lỗi cho `dev` sửa không. Không tự gửi.
