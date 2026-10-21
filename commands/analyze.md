---
description: Dev đọc tài liệu, tổng hợp và liệt kê câu hỏi. CHƯA code.
argument-hint: <yêu cầu hoặc đường dẫn tài liệu>
---

Yêu cầu của người dùng (NGUYÊN VĂN):
"""
$ARGUMENTS
"""

1. Gọi agent `dev` ở giai đoạn PHÂN TÍCH với nguyên văn yêu cầu trên. Nhấn mạnh: chỉ phân tích, KHÔNG sửa file nào.
2. Hiển thị nguyên báo cáo `🧠 DEV — PHÂN TÍCH` cho người dùng.
3. Nếu trạng thái là ❓ CẦN HỎI: hỏi người dùng các câu hỏi đó và dừng lại chờ trả lời.
4. Nếu ✅ ĐỦ THÔNG TIN: hỏi người dùng có muốn chạy `/ship` để implement không.
