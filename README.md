## Setup ban đầu

Check các tùy chọn sau:

- [x] Cho phép gõ tự do
- [x] Cho phép gõ tắt
- [x] Cho phép gõ tắt cả khi tắt Tiếng Việt
- [x] Bật kiểm tra chính tả
- [x] Khởi động cùng Windows

Còn lại là tắt hết

## Build EVKey shortcut file

The source of truth is:

`unikey-shortcut.txt`

Generate EVKey Mac format with:

```bash
python3 scripts/build-evkey.py
```

This generates:
`evkey-shortcut.txt`

Format conversion:

UniKey:
`shortcut:replacement`

EVKey:
`shortcut||replacement`
