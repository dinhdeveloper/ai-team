---
description: Dev review source (diff hiện tại, file hoặc thư mục) theo rule project và gợi ý cách làm đúng. Không sửa file.
argument-hint: [đường dẫn file/thư mục | để trống = git diff hiện tại]
---

Phạm vi review: $ARGUMENTS
(Để trống = review `git diff` hiện tại so với HEAD.)

1. Đang có task active chưa `DONE` → báo anh: review trong task thì dùng `/ai-team:resume`; lệnh này chỉ review, **không sửa**.
2. Gọi `dev` nhiệm vụ **E. REVIEW SOURCE** với phạm vi trên. Nhấn mạnh: KHÔNG sửa file nào. Lệnh luôn `| tail`.
3. Hiển thị kết quả `🔍 DEV — REVIEW SOURCE`.
4. Không có task active → **AskUserQuestion** hỏi anh muốn dev sửa những mục nào (multiSelect nếu ≤ 4 mục, nhiều hơn thì cho anh gõ số). Anh chọn → gọi `dev` sửa đúng các mục đó → hỏi có chạy `/ai-team:test` không. Không tự sửa.
