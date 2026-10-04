## Setup ban đầu

Check các tùy chọn sau:

- [x] Cho phép gõ tự do
- [x] Cho phép gõ tắt
- [x] Cho phép gõ tắt cả khi tắt Tiếng Việt
- [x] Bật kiểm tra chính tả
- [x] Khởi động cùng Windows

Còn lại là tắt hết

## Shortcut dictionary (Windows + macOS)

Chỉ sửa **một file duy nhất**: `shortcuts.txt`

```text
dtl:Đức Thánh Linh
ko:không
# dòng bắt đầu bằng # là comment
```

Mỗi lần push lên `master`, GitHub Actions tự generate:

| File | Dùng cho | Format |
| --- | --- | --- |
| `unikey-shortcut.txt` | Windows / UniKey | `shortcut:replacement` (UTF-8 BOM, CRLF) |
| `evkey-shortcut.txt` | macOS / EVKey | `shortcut\|\|replacement` |

Không sửa trực tiếp 2 file trên — chúng sẽ bị ghi đè. Sau khi push, chạy `git pull` để lấy commit do bot tạo.

Build thử ở local:

```bash
python3 scripts/build.py
```

Build sẽ fail nếu có dòng thiếu `:`, thiếu nội dung, hoặc shortcut bị trùng.
