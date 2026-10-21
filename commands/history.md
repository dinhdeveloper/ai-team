---
description: Xem lịch sử làm việc, quyết định của anh, lỗi còn mở và bài học
argument-hint: [để trống = danh sách task | tên task | bugs | approvals | lessons]
---

Tham số: $ARGUMENTS

Chỉ đọc, không sửa file nào. Chưa có `.ai-team/` → báo chưa có lịch sử. Đọc gọn (head/tail), không đọc toàn bộ báo cáo agent.

- **Để trống:** `INDEX.md` — 10 task gần nhất (size, phase, vòng sửa, BUG, RV) + task đang active.
- **Tên task:** `timeline.md`, `approvals.md`, phần đếm của `checklist.md`, `bugs.md`, `summary.md`:
  ```
  # 📁 <task> · Size · Phase
  ### ⏱️ Dòng thời gian   (🧭 teamlead · 🧠 dev · 🧪 tester · 👤 anh)
  ### 🙋 Quyết định của anh
  ### ☑️ Checklist
  ### 🐞 BUG & RV
  ### 📋 Kết quả
  ```
- **bugs:** BUG/RV chưa ✅ Verified ở mọi task.
- **approvals:** 20 quyết định gần nhất.
- **lessons:** nội dung `.ai-team/lessons.md`.
