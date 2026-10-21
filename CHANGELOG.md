# Changelog

## v1.4.1 — 2026-10-21
- Thêm scripts/release.sh, CHANGELOG.md, hướng dẫn phát hành

## v1.4.0 — 2026-10-21
- Hook chặn theo giai đoạn (`.ai-team/active.json`) và allowlist file từ `checklist.md`
- Baseline regression trước/sau khi code
- Gói ngữ cảnh trong SDD (mục 5), size S/M/L, Mini-SDD
- Lệnh `/ai-team:resume`, bài học `.ai-team/lessons.md`
- Báo cáo gọn ≤ 60 dòng, test theo module, `maxTurns` cho từng agent
- `HUONG-DAN.md`: hướng dẫn cài đặt và sử dụng chi tiết

## v1.3.0 — 2026-10-21
- Dev + tester cùng review SDD, nêu điểm chưa rõ
- Dev lập checklist, tester lập testcase; anh tick duyệt từng mục, mục bị từ chối làm lại theo lý do
- Teamlead review source sau khi anh đồng ý kết quả dev
- Lệnh `/ai-team:plan`

## v1.2.0 — 2026-10-21
- Thêm agent teamlead: phân tích, viết SDD + diagram Mermaid, nghiệm thu
- Cổng duyệt: mọi điểm chưa rõ đều hỏi anh Đồng ý / Không đồng ý
- Lệnh `/ai-team:sdd`, `/ai-team:dev`

## v1.1.0 — 2026-10-21
- Dev khảo sát base, không bịa, phân loại 🟢/🟡/🔴, xin duyệt khi đổi luồng cũ
- Tester được viết unit test (chỉ trong thư mục test)
- Hook bảo vệ, lịch sử `.ai-team/history/`, lệnh `/ai-team:review`, `/ai-team:history`

## v1.0.0 — 2026-10-21
- Bản đầu: agent dev + tester, lệnh `/ai-team:analyze`, `/ai-team:ship`, `/ai-team:test`
