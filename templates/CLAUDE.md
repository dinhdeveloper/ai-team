# <Tên project>

> Copy file này vào thư mục gốc của mỗi project và điền thông tin. Cả dev và tester đều đọc file này.

## Tổng quan
- Mô tả: <app làm gì, cho ai>
- Nền tảng: Flutter <version> / Android Kotlin / Zalo Mini App
- Kiến trúc: Clean Architecture — presentation / domain / data
- State management: <Bloc / Riverpod / GetX / ...>
- DI: <get_it / injectable / Hilt / ...>

## Cấu trúc thư mục
```
lib/
  core/        # ...
  features/    # mỗi feature: data/, domain/, presentation/
test/
```

## Lệnh
| Việc | Lệnh |
|------|------|
| Lấy package | `flutter pub get` |
| Analyze | `flutter analyze` |
| Unit test | `flutter test` |
| Build kiểm tra | `flutter build apk --flavor dev -t lib/main_dev.dart --debug` |

## Flavor / môi trường
DEV / UAT / STG / PROD — config ở: <đường dẫn>. Không hardcode URL/key.

## Quy ước code
- Naming: ...
- Không dùng `print`, dùng logger: ...
- Không log dữ liệu nhạy cảm (số tiền, số tài khoản, CCCD, token)
- Thư viện được phép thêm: phải hỏi trước

## Tài liệu tham khảo
- Nghiệp vụ: `docs/...`
- API spec: `docs/api/...`
- Testcase: `docs/testcases/...`
