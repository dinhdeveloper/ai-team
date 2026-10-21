# <Tên project>

> File này được nạp vào **mọi** agent ở **mọi** lượt → giữ ≤ 150 dòng, chỉ ghi rule và chỉ đường. Chi tiết để ở `docs/` và trỏ tới.
> Rule ở đây ưu tiên hơn thói quen của agent.

## Tổng quan
- App: <làm gì, cho ai> · Nền tảng: Flutter <version> / Kotlin / Zalo Mini App
- Kiến trúc: Clean Architecture (presentation / domain / data) · State: <Bloc/Riverpod/...> · DI: <get_it/Hilt/...> · Router: <go_router/...>

## Cấu trúc
```
lib/core/       # dùng chung
lib/features/   # mỗi feature: data/ domain/ presentation/
test/           # mirror theo lib/
docs/sdd/       # SDD (teamlead)
docs/testcases/ # testcase (tester)
```

## Lệnh
| Việc | Lệnh |
|------|------|
| Lấy package | `flutter pub get` |
| Analyze theo module | `flutter analyze lib/features/<feature> 2>&1 \| tail -60` |
| Analyze toàn bộ | `flutter analyze 2>&1 \| tail -60` |
| Test theo module | `flutter test test/features/<feature> 2>&1 \| tail -80` |
| **Baseline** (toàn bộ test, chỉ in lỗi + tổng) | `flutter test --reporter failures-only 2>&1 \| tail -60` |
| Sinh code | `dart run build_runner build --delete-conflicting-outputs 2>&1 \| tail -20` |
| Build kiểm tra | `flutter build apk --flavor dev -t lib/main_dev.dart --debug 2>&1 \| tail -20` |

## Flavor
DEV / UAT / STG / PROD — config: <đường dẫn>. Không hardcode URL/key.

## Quy ước code
- Naming: ... · Logger: ... (không `print`)
- Không log số tiền, số tài khoản, CCCD, token, OTP
- Thêm thư viện: anh duyệt trước

## Dùng chung (ưu tiên tái sử dụng)
| Thành phần | Vị trí |
|---|---|
| Base screen / widget | `lib/core/...` |
| Failure / error handling | `lib/core/error/...` |
| Network client | `lib/core/network/...` |
| Format tiền, ngày | `lib/core/utils/...` |
| Theme | `lib/core/theme/...` |

## Feature mẫu
- `lib/features/<feature-chuẩn-nhất>/` + test mẫu `test/features/<feature-chuẩn-nhất>/`

## 🔒 Luồng được bảo vệ (mọi thay đổi phải anh duyệt)
- Thanh toán & callback/deeplink ví (MoMo, ZaloPay, VNPay...)
- Đăng nhập, OTP, sinh trắc học, token
- <thêm>

## Quy ước test
- `flutter_test` + `mocktail` (ghi đúng cái đang dùng) · tên test `'TCxx (ACxx) - hành vi'`

## Definition of Done
- Analyze sạch · test module pass · không regression so với baseline · teamlead review ✅ · tester PASS

## Tài liệu (agent chỉ đọc khi cần)
- Nghiệp vụ: `docs/...` · API: `docs/api/...` · Design: <link Figma>
- Mẫu SDD: `templates/sdd-template.md` của plugin ai-team (hoặc mẫu riêng: <đường dẫn>)
