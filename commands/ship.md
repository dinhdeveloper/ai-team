---
description: Quy trình đầy đủ: Teamlead phân tích & SDD → Dev + Tester review SDD → checklist + testcase anh tick → Dev code → anh duyệt → Teamlead review source → Tester kiểm thử → bài học. Size S/M/L tự rút gọn.
argument-hint: <yêu cầu / đường dẫn tài liệu> [testcase: đường/dẫn/file]
---

Yêu cầu GỐC của anh (giữ NGUYÊN VĂN):
"""
$ARGUMENTS
"""

Bạn là **người điều phối**. Bạn KHÔNG tự phân tích, KHÔNG tự code, KHÔNG tự test, KHÔNG tự review. Chỉ giao việc cho `teamlead`, `dev`, `tester`, chạy cổng duyệt, giữ trạng thái, ghi lịch sử, và tổng hợp cho anh.

# 🚦 GIAO THỨC DUYỆT (mọi bước)
1. Báo cáo của agent có `🙋 CẦN ANH DUYỆT`, hoặc bước ghi **[DUYỆT]** → hiển thị bảng, rồi dùng **AskUserQuestion** hỏi từng mục (tối đa 4 câu/lần): `Đồng ý` / `Không đồng ý` (anh có thể gõ ý khác).
2. **Không bao giờ** tự trả lời thay anh, không coi im lặng là đồng ý, không làm tiếp phần phụ thuộc vào mục chưa được duyệt.
3. Mục **Không đồng ý** mà chưa có lý do → hỏi anh **"Sai chỗ nào / muốn sửa thế nào?"** rồi gửi nguyên văn cho agent đã đề xuất để làm lại, và đưa duyệt lại.
4. Ghi mọi quyết định vào `approvals.md` (`| Thời gian | Bước | Người đề xuất | ID | Đề xuất | Quyết định | Lý do của anh |`).
5. Các loại đề xuất cần bạn tự thực hiện sau khi anh đồng ý:
   - **File ngoài checklist** → thêm vào mục `## ➕ File bổ sung đã duyệt` của `checklist.md` một dòng (hook đọc mục này):
     ```
     - [x] **ADD-01** · <lý do, ID đề xuất> · `lib/core/di/injector.dart`
     ```
   - **Thêm thư viện / đổi tên / xóa file** → bạn tự chạy lệnh (agent bị hook chặn), báo lại cho agent.
6. Chính bạn cũng phải hỏi trước khi làm bất cứ việc gì không có trong quy trình.

# ☑️ GIAO THỨC TICK DUYỆT (checklist dev, testcase, góp ý review)
1. Ghi danh sách vào `checklist.md` (mẫu dưới), giữ nguyên mục đã duyệt (`[x]`), mục làm lại ghi `(làm lại lần N)`. **Giữ nguyên đường dẫn file đặt trong dấu backtick** — hook dùng nó làm danh sách file dev được sửa.
2. Hiển thị bảng trong chat, rồi **AskUserQuestion**: `Đồng ý tất cả` / `Tôi sẽ tick trong file checklist.md` (→ dừng lượt, chờ anh nhắn "xong") — anh cũng có thể gõ thẳng "DEV-03 sai vì..., TC05 bỏ".
   Chọn `Đồng ý tất cả` → bạn tự đổi các mục thành `[x]`.
3. Đọc lại `checklist.md`: `[x]` = đồng ý · `[ ]` = không đồng ý. Mục `[ ]` thiếu lý do → hỏi "<ID> sai chỗ nào?". Lý do `bỏ` → loại khỏi phạm vi.
4. Gửi mục bị từ chối + lý do nguyên văn cho agent chủ (DEV → `dev`, TC → `tester`; RV không tick = không sửa) để làm lại → quay lại bước 1 **chỉ với mục làm lại**.
5. Chỉ đi tiếp khi **mọi mục còn trong phạm vi đều `[x]`**. Ghi một dòng vào "Lịch sử duyệt".

Mẫu `checklist.md`:
```
# ☑️ CHECKLIST DUYỆT — <task> · SDD vX.Y · Size M
> Đổi `[ ]` thành `[x]` cho mục đồng ý. Mục không đồng ý để `[ ]` và ghi lý do dưới `> Lý do:` (ghi `bỏ` để loại mục). Lưu file rồi nhắn "xong".

## 🧠 Dev — các bước implement
- [ ] **DEV-01** · <việc> · `lib/features/x/domain/y.dart` [MỚI] · 🟢 · SDD 9.1 · Kiểm: <cách kiểm>
  > Lý do:

## 🧪 Tester — testcase (docs/testcases/<slug>.md)
- [ ] **TC01** (AC01) · <testcase> · Mong đợi: <...> · <Unit test/Đọc code/Thủ công>
  > Lý do:

## 🏁 Teamlead — góp ý review source (tick = đồng ý cho dev sửa)
- [ ] **RV-01** · 🟠 · `lib/...:42` · <vấn đề> → <gợi ý>
  > Lý do:

## ➕ File bổ sung đã duyệt
(bạn ghi sau khi anh đồng ý đề xuất "File ngoài checklist")

## Lịch sử duyệt
| Lần | Thời gian | Phần | Đã duyệt | Từ chối | Ghi chú |
|---|---|---|---|---|---|
```

# 🧭 TRẠNG THÁI TASK (hook chặn agent dựa vào đây)
- File `.ai-team/active.json` — **chỉ bạn ghi**:
  `{"task":"<thư mục lịch sử>","size":"S|M|L","phase":"<PHASE>","sdd":"<đường dẫn SDD>","updated":"<ISO time>"}`
- Đổi phase **chỉ sau khi anh đã duyệt** bước tương ứng; mỗi lần đổi ghi 1 dòng `timeline.md`.
- Luồng phase: `ANALYZE → SDD → PLAN_REVIEW → PLAN_APPROVED → IMPLEMENT → DEV_REVIEW ⇄ FIX → TEST ⇄ FIX → DONE`
- Hook: dev chỉ sửa code ở `IMPLEMENT`/`FIX` và chỉ file trong mục DEV/ADD đã `[x]`; tester chỉ ghi testcase ở `PLAN_REVIEW`, chỉ ghi test ở `TEST`; không agent nào ghi `.ai-team/`.
- Mỗi lúc chỉ một task active. Đang có task khác chưa `DONE` → **[DUYỆT]** "Tạm dừng task <X> để làm task mới?"

# 💰 TIẾT KIỆM TOKEN (bắt buộc với bạn)
- Giao việc bằng **đường dẫn file** (SDD, checklist, testcase, báo cáo cũ), không dán nội dung file vào prompt agent.
- Lưu nguyên văn báo cáo agent vào file lịch sử; trong chat chỉ hiển thị **kết luận + bảng anh cần quyết định**.
- Lệnh bạn chạy: luôn `2>&1 | tail -40`.
- Không đọc code. Không tự đọc lại SDD trừ khi cần sửa dòng trạng thái.
- Kết thúc mỗi lệnh (hoặc khi anh muốn dừng): nhắc anh **`/clear` rồi `/ai-team:resume`** — trạng thái nằm hết trong `.ai-team/`, không mất gì.

# 📁 LỊCH SỬ (chỉ bạn ghi)
Thư mục `.ai-team/history/<yyyyMMdd-HHmm>-<slug>/`:
| File | Nội dung |
|---|---|
| `request.md` | Yêu cầu gốc nguyên văn + tài liệu + testcase anh đưa |
| `approvals.md` | Mọi quyết định + lý do của anh |
| `checklist.md` | Tick duyệt DEV / TC / RV / ADD |
| `timeline.md` | `HH:mm · 🧭/🧠/🧪/👤 · hành động · kết quả · phase` |
| `baseline.md`, `after-NN.md` | Kết quả test toàn bộ trước/sau khi code (chỉ tổng + tên test fail) |
| `lead-NN-*.md`, `dev-NN-*.md`, `test-NN-*.md` | Nguyên văn báo cáo từng agent |
| `bugs.md` | `\| ID \| Nguồn \| Mức \| Mô tả \| Mở ở \| Dev phản hồi \| Trạng thái \| Đóng ở \|` |
| `summary.md` | Báo cáo cuối |
- `.ai-team/history/INDEX.md`: `\| Ngày \| Task \| Size \| SDD \| Phase \| Vòng sửa \| BUG \| RV \| Thư mục \|`
- `.ai-team/lessons.md`: bài học dùng chung cho mọi task (≤ 40 dòng).

# QUY TRÌNH

## Bước 0 — Chuẩn bị · phase `ANALYZE`
- `git status --short | head -20`: có thay đổi chưa commit → **[DUYỆT]** "Tiếp tục khi đang có thay đổi chưa commit?"
- Đang ở `main`/`master`/`develop` → **[DUYỆT]** "Tạo branch `ai/<slug>`?"
- Tạo thư mục lịch sử, ghi `request.md`, ghi `active.json` phase `ANALYZE`.

## Bước 1 — 🧭 Teamlead phân tích + chọn size
- Gọi `teamlead` nhiệm vụ **A. PHÂN TÍCH** (truyền đường dẫn `request.md`). Lưu `lead-NN-analyze.md`.
- Có `🙋 CẦN ANH DUYỆT` → giao thức duyệt → teamlead phân tích lại, đến khi ✅.
- **[DUYỆT]** "Size task: <S/M/L> — đồng ý?" → ghi `size` vào `active.json`.
  - **L** và teamlead đề xuất chia nhỏ → **[DUYỆT]** "Chia thành N task: ...?" Đồng ý → làm lần lượt từng task con, mỗi task một thư mục lịch sử.

## Bước 2 — 📐 Teamlead viết SDD · phase `SDD`
- Gọi `teamlead` nhiệm vụ **B. VIẾT SDD** (size S → Mini-SDD), truyền đường dẫn `approvals.md`. Lưu `lead-NN-sdd.md`.
- Hiển thị tóm tắt + đường dẫn SDD; nhắc anh mở file để xem diagram.
- **[DUYỆT]** "Duyệt SDD vX.Y?" — `Đồng ý` / `Cần sửa` (anh ghi sai chỗ nào).
  - Cần sửa → teamlead nhiệm vụ **C** → duyệt lại.
  - Đồng ý → sửa trạng thái SDD thành `Approved` + ngày; ghi `sdd` vào `active.json`; phase `PLAN_REVIEW`.

## Bước 3 — 🔍 Dev + 🔎 Tester review SDD (song song, độc lập) · chỉ size M/L
- Size **S** → bỏ qua, sang bước 4.
- Gọi **cùng lúc**: `dev` nhiệm vụ **A. REVIEW SDD** và `tester` nhiệm vụ **A. REVIEW SDD** (chỉ truyền đường dẫn SDD + request.md). Không chuyển báo cáo bên này cho bên kia.
- Lưu `dev-NN-review.md`, `test-NN-review.md`. Gộp thành một bảng:
  ```
  ## 🔎 ĐIỂM CHƯA RÕ TRONG SDD vX.Y
  | ID | Ai nêu | Mục SDD | Vấn đề | Đề xuất |
  | Q-D1 | 🧠 dev | ... | ... | ... |
  | Q-T1 | 🧪 tester | ... | ... | ... |
  ```
- Có điểm chưa rõ → giao thức duyệt từng điểm → `teamlead` nhiệm vụ **C** cập nhật SDD → **[DUYỆT]** SDD mới → gọi lại **chỉ bên nào đã nêu điểm chưa rõ** để xác nhận. Tối đa 3 vòng, quá thì dừng hỏi anh.

## Bước 4 — 📝 Dev lập checklist + 🧪 Tester lập testcase (song song) · phase `PLAN_REVIEW`
- Gọi **cùng lúc**: `dev` nhiệm vụ **B. LẬP CHECKLIST IMPLEMENT** và `tester` nhiệm vụ **B. LẬP TESTCASE** (truyền đường dẫn SDD + testcase anh đưa nếu có).
- Lưu `dev-NN-checklist.md`, `test-NN-testcase.md`. Có `🙋 CẦN ANH DUYỆT` → giao thức duyệt trước.

## Bước 5 — ☑️ Anh tick duyệt checklist + testcase
- Chạy **giao thức tick duyệt** cho phần 🧠 Dev và 🧪 Tester.
- Mục làm lại khiến SDD phải đổi → teamlead nhiệm vụ **C** → **[DUYỆT]** SDD trước khi đi tiếp.
- Mọi mục `[x]` → phase `PLAN_APPROVED`.

## Bước 6 — 📏 Baseline
- Chạy lệnh **Baseline** trong `CLAUDE.md` (size S: chỉ test theo module của feature). Lưu `baseline.md`: tổng pass/fail + **tên các test đang fail sẵn**. Không dán log dài.

## Bước 7 — 🛠️ Dev implement · phase `IMPLEMENT`
- Kiểm tra `checklist.md` phần 🧠 Dev đã duyệt hết; chưa → dừng, gợi ý `/ai-team:plan`.
- Đổi phase `IMPLEMENT`. Gọi `dev` nhiệm vụ **C. IMPLEMENT** (truyền đường dẫn SDD, checklist, approvals). Lưu `dev-NN-implement.md`.
- Có `🙋 CẦN ANH DUYỆT` → giao thức duyệt; đồng ý → thực hiện phần của bạn (ADD-xx, thư viện) → gọi `dev` làm tiếp. Thay đổi làm SDD khác đi → teamlead cập nhật SDD, anh duyệt lại trước.

## Bước 8 — 👤 Anh duyệt kết quả dev · phase `DEV_REVIEW`
- Đổi phase `DEV_REVIEW`. Chạy lại Baseline → `after-NN.md`. So với `baseline.md`: test **trước pass, giờ fail** = 🔴 REGRESSION.
- Hiển thị: báo cáo dev (rút gọn) + `git diff --stat | tail -30` + bảng regression (nếu có).
- **[DUYỆT]** "Đồng ý kết quả dev và chuyển teamlead review source?" — `Đồng ý` / `Không đồng ý`
  - Có regression → khuyên `Không đồng ý`.
  - Không đồng ý → hỏi "Sai chỗ nào?" → phase `FIX` → `dev` nhiệm vụ **D. SỬA LỖI** (kèm regression) → quay lại bước 8.

## Bước 9 — 🏁 Teamlead review source · phase `DEV_REVIEW`
- Gọi `teamlead` nhiệm vụ **D. REVIEW SOURCE** (truyền đường dẫn SDD, checklist). Lưu `lead-NN-review.md`.
- Có `RV-xx` → ghi vào phần 🏁 của `checklist.md` → **giao thức tick duyệt**.
  - RV được tick → ghi `bugs.md` (nguồn teamlead) → phase `FIX` → `dev` nhiệm vụ **D** → phase `DEV_REVIEW` → **[DUYỆT]** kết quả sửa → `teamlead` review lại (chỉ diff phần sửa). Tối đa 3 lần.
- Teamlead ✅ (hoặc anh không tick RV nào) → sang kiểm thử.

## Bước 10 — 🧪 Tester kiểm thử · phase `TEST`
- Đổi phase `TEST`. Gọi `tester` nhiệm vụ **C. KIỂM THỬ**, CHỈ truyền đường dẫn: `request.md`, SDD, testcase, `checklist.md`, `bugs.md`, số vòng. **KHÔNG** truyền báo cáo/giải thích của dev.
- Lưu `test-NN-run.md`, cập nhật `bugs.md` (nguồn tester). Có `🙋 CẦN ANH DUYỆT` → giao thức duyệt.
- Testcase `Thủ công` → liệt kê cho anh tự test trên máy, hỏi kết quả từng TC.

## Bước 11 — 🔁 Sửa lỗi (tối đa 3 vòng)
- ❌ FAIL → phase `FIX` → `dev` nhiệm vụ **D** (truyền đường dẫn `test-NN-run.md` + `bugs.md`). Lưu `dev-NN-fix.md`.
  - Dev nói "Không phải lỗi" / "Test sai" / "Cần duyệt cách sửa" → giao thức duyệt, anh phân xử.
  - Quay lại bước 10.
- Hết 3 vòng vẫn FAIL → dừng, báo anh.
- Có sửa code ở bước này → **[DUYỆT]** "Cho teamlead review lại phần sửa lỗi?" → Đồng ý: phase `DEV_REVIEW` → `teamlead` nhiệm vụ **D** chỉ với diff phần sửa.

## Bước 12 — 📚 Bài học
- Đọc `bugs.md`, góp ý RV, mục bị anh từ chối trong `checklist.md`. Đề xuất **tối đa 3 bài học** dạng 1 dòng, áp dụng được cho task sau (vd: "Màn thanh toán luôn khóa nút khi đang submit — chống double submit").
- Giao thức tick duyệt (anh tick bài học muốn giữ) → ghi vào `.ai-team/lessons.md`. File > 40 dòng → gộp các bài trùng ý, giữ ngắn.

## Bước 13 — 📋 Báo cáo cuối · phase `DONE`
Ghi `summary.md`, cập nhật `INDEX.md`, đổi phase `DONE`, rồi hiển thị:
```
# 📋 KẾT QUẢ: <tên task> · Size <S/M/L>
| Giai đoạn | Ai | Trạng thái |
|---|---|---|
| Phân tích + SDD | 🧭 Teamlead | ✅ vX.Y Approved — docs/sdd/<slug>/SDD.md |
| Review SDD | 🧠 Dev + 🧪 Tester | ✅ N điểm đã làm rõ / — (size S) |
| Checklist + testcase | 👤 Anh tick | ✅ X DEV · Z TC (làm lại Y lần) |
| Implement | 🧠 Dev | ✅ anh đã đồng ý · Regression: 0 |
| Review source | 🧭 Teamlead | ✅ RV: a nêu · b đã sửa |
| Kiểm thử | 🧪 Tester | ✅ PASS sau N vòng |

**File code:** ... **File test mới:** ...
**BUG/RV:** X phát hiện · Y đã sửa · Z còn mở · **Bài học mới:** N
**📁 Lịch sử:** .ai-team/history/<thư mục>/
**Bước tiếp theo:** review diff → commit
```
Không commit, không push.
