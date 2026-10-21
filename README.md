# ai-team — Dev + Tester cho Claude Code

## Cài đặt (1 lần)
1. Tạo repo GitHub `dinh-ai-team` (private cũng được), push toàn bộ thư mục này lên.
2. Trong Claude Code, ở bất kỳ project nào:
   ```
   /plugin marketplace add <github-user>/dinh-ai-team
   /plugin install ai-team@dinh-tools
   ```
3. Kiểm tra: gõ `/agents` → thấy `dev` và `tester`.

Thử nhanh không cần GitHub: `/plugin marketplace add /đường/dẫn/tới/ai-team`

## Mỗi project mới
1. Copy `templates/CLAUDE.md` vào gốc project, điền lệnh build/test, kiến trúc.
2. Thêm `.ai-team/` vào `.gitignore` (nơi lưu báo cáo).
3. Để testcase ở `docs/testcases/` theo mẫu `templates/testcase-template.md`.

## Lệnh
| Lệnh | Làm gì |
|------|--------|
| `/analyze <yêu cầu>` | Dev đọc tài liệu, tổng hợp, liệt kê câu hỏi. Chưa code. |
| `/ship <yêu cầu> testcase: docs/testcases/x.md` | Toàn bộ: phân tích → hỏi → code → test → sửa (tối đa 3 vòng) → báo cáo |
| `/test <nghiệp vụ> testcase: ...` | Chỉ tester kiểm tra thay đổi hiện tại |

Nếu trùng tên lệnh với plugin khác, gọi đầy đủ: `/ai-team:ship`.

## Cập nhật
Sửa agent → tăng `version` trong `.claude-plugin/plugin.json` → push → trong Claude Code: `/plugin marketplace update dinh-tools`.
