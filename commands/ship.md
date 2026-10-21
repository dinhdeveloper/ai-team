---
description: Quy trình đầy đủ - Dev phân tích → hỏi nếu thiếu → implement → Tester kiểm tra → lặp sửa lỗi
argument-hint: <yêu cầu> [testcase: đường/dẫn/file]
---

Yêu cầu GỐC của người dùng (giữ NGUYÊN VĂN, dùng lại cho tester):
"""
$ARGUMENTS
"""

Bạn là người điều phối. Bạn KHÔNG tự viết code, KHÔNG tự test. Chỉ giao việc cho agent `dev` và `tester`, rồi tổng hợp.

## Bước 0 — Chuẩn bị
- Chạy `git status`. Nếu đang có thay đổi chưa commit, báo người dùng và hỏi có tiếp tục không.
- Ghi lại tên branch hiện tại. Nếu đang ở `main`/`master`/`develop`, đề xuất tạo branch `ai/<tên-ngắn>` và hỏi người dùng.

## Bước 1 — Phân tích
- Gọi `dev` ở giai đoạn PHÂN TÍCH với yêu cầu gốc.
- Nếu kết quả là ❓ CẦN HỎI → hiển thị câu hỏi cho người dùng và **DỪNG**. Khi người dùng trả lời, gửi câu trả lời cho `dev` và phân tích lại.
- Chỉ sang bước 2 khi `dev` báo ✅ ĐỦ THÔNG TIN. Hiển thị kế hoạch và hỏi người dùng xác nhận trước khi code.

## Bước 2 — Implement
- Gọi `dev` implement theo kế hoạch đã chốt (kèm câu trả lời của người dùng nếu có).

## Bước 3 — Test (độc lập)
- Gọi `tester` và chỉ truyền:
  1. Yêu cầu GỐC nguyên văn ở trên (+ câu trả lời làm rõ của người dùng, nếu có)
  2. Đường dẫn file testcase nếu người dùng cung cấp
- **KHÔNG** truyền báo cáo, kế hoạch hay giải thích của dev cho tester.
- Sau khi tester xong, chạy `git status` và so với trước bước 3. Nếu tester đã làm thay đổi bất kỳ file nào → cảnh báo người dùng ngay.

## Bước 4 — Vòng sửa lỗi (tối đa 3 vòng)
- ❌ FAIL → gửi nguyên phần `🐞 Lỗi gửi Dev` cho `dev` sửa → quay lại Bước 3.
- ⚠️ CẦN LÀM RÕ → hỏi người dùng, dừng chờ trả lời.
- Hết 3 vòng vẫn FAIL → dừng và báo người dùng, không lặp tiếp.

## Bước 5 — Báo cáo cuối
Lưu báo cáo vào `.ai-team/reports/<yyyy-MM-dd-HHmm>-<tên-ngắn>.md`, rồi hiển thị:

```
# 📋 KẾT QUẢ: <tên task>
| Hạng mục | Trạng thái |
|----------|-----------|
| Phân tích | ✅ |
| Implement | ✅ |
| Test | ✅ PASS sau N vòng / ❌ FAIL |
| Analyze | ✅ |

**File thay đổi:** ...
**Lỗi đã sửa:** BUG-01 ..., BUG-02 ...
**Còn tồn đọng:** ...
**Bước tiếp theo đề xuất:** review diff → commit
```
Không commit, không push.
