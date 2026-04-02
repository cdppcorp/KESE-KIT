🌐 [한국어](../README.md) | [English](../README.md#english) | [Français](README.fr.md) | [日本語](README.ja.md) | [中文](README.zh.md) | [Русский](README.ru.md) | [Español](README.es.md) | [Deutsch](README.de.md) | [Português](README.pt.md) | [Italiano](README.it.md) | [العربية](README.ar.md) | [हिन्दी](README.hi.md) | [Türkçe](README.tr.md) | [Tiếng Việt](README.vi.md) | [ภาษาไทย](README.th.md) | [Bahasa Indonesia](README.id.md) | [Polski](README.pl.md) | [Nederlands](README.nl.md) | [Svenska](README.sv.md) | [Українська](README.uk.md)

---

# KESE - KISA Enhanced Security Evaluation Kit

Plugin kỹ năng Claude Code dành cho phân tích-đánh giá lỗ hổng Hạ tầng Thông tin Trọng yếu (CII) và đánh giá bảo mật AI.

---

## Tổng quan

KESE (KISA Enhanced Security Evaluation Kit) là một plugin Claude Code cung cấp khả năng đánh giá lỗ hổng bảo mật toàn diện dựa trên hướng dẫn của KISA (Cơ quan An ninh và Internet Hàn Quốc). Hỗ trợ cả đánh giá Hạ tầng Thông tin Trọng yếu (CII) và đánh giá Bảo mật AI.

## Tính năng

| Kỹ năng | Mô tả |
|---------|-------|
| `/kesekit:start` | Chạy đánh giá lỗ hổng bảo mật toàn diện (CII 560+ hạng mục hoặc Bảo mật AI) |
| `/kesekit:check` | Danh sách kiểm tra tuân thủ bảo mật trước triển khai |
| `/kesekit:fix` | Tự động tạo script tăng cường bảo mật và bản vá lỗ hổng |
| `/kesekit:guide` | Tạo prompt lập trình an toàn cho các công cụ AI |

## Hướng dẫn được hỗ trợ

### 1. CII (Hạ tầng Thông tin Trọng yếu) — 560+ hạng mục

**Đánh giá Kỹ thuật**
| Hệ thống | Mã | Hạng mục |
|----------|-----|:--------:|
| Máy chủ Unix/Linux | U-01~U-67 | 67 |
| Máy chủ Windows | W-01~W-64 | 64 |
| Dịch vụ Web | WEB-01~WEB-26 | 26 |
| Thiết bị Bảo mật | S-01~S-23 | 23 |
| Thiết bị Mạng | N-01~N-38 | 38 |
| Hệ thống Điều khiển | C-01~C-51 | 46 |
| PC | PC-01~PC-18 | 18 |
| DBMS | D-01~D-26 | 26 |
| Di động | M-01~M-04 | 4 |
| Web Application | 21 mã | 21 |
| Ảo hóa | HV-01~HV-25 | 25 |
| Đám mây | CA-01~CA-19 | 19 |

**Đánh giá Quản lý**: A-1~A-127 (127 hạng mục, 14 lĩnh vực)
**Đánh giá Vật lý**: P-1~P-18 (18 hạng mục)

### 2. Hướng dẫn Bảo mật AI — 54+ hạng mục

| Đối tượng | Hạng mục | Vòng đời |
|-----------|:--------:|----------|
| Nhà phát triển AI | 54 | 6 giai đoạn (Lập kế hoạch→Dữ liệu→Mô hình→Triển khai→Giám sát→Loại bỏ) |
| Nhà cung cấp dịch vụ | ~43 | 6 giai đoạn (Lập kế hoạch→Phát triển→Vận hành→Bảo trì→Phản hồi→Loại bỏ) |
| Người dùng | 7 | Các phương pháp bảo mật tốt nhất |

## Cài đặt

```bash
claude plugins install kesekit
```

## Cách sử dụng

```bash
# Bắt đầu đánh giá bảo mật toàn diện
/kesekit:start

# Chạy danh sách kiểm tra trước triển khai
/kesekit:check

# Tạo script tăng cường bảo mật
/kesekit:fix

# Nhận prompt lập trình an toàn
/kesekit:guide
```

---

## Cấu trúc Dự án

```
KESE-KIT/
├── .claude-plugin/
│   └── marketplace.json              ← Siêu dữ liệu plugin
├── skills/                            ← Kỹ năng tiếng Anh (bộ định tuyến)
│   ├── start/
│   │   ├── SKILL.md                  ← Bộ định tuyến (~80 dòng)
│   │   └── references/               ← Kiến thức theo hướng dẫn
│   │       ├── cii/                  ← CII 14 tài liệu tham khảo
│   │       └── ai-security/          ← Bảo mật AI 4 tài liệu tham khảo
│   ├── check/
│   ├── fix/
│   └── guide/
├── skills-ko/                         ← Kỹ năng tiếng Hàn (cùng cấu trúc)
├── authorkit/                         ← Tài liệu gốc và sản phẩm công việc
│   ├── converted/
│   │   ├── ref-001/                  ← Hướng dẫn quản lý/vật lý (full.md)
│   │   ├── ref-002/                  ← Hướng dẫn kỹ thuật (full.md)
│   │   └── ref-003/                  ← Hướng dẫn bảo mật AI (full.md)
│   └── ...
├── 문서/                              ← PDF gốc
└── README.md
```

---

## Lịch sử Thay đổi

### v2.0.0 (2026-03-30)

**Tái cấu trúc — Áp dụng mẫu Progressive Disclosure**

| Thay đổi | Trước (v1.0) | Sau (v2.0) |
|----------|-------------|------------|
| SKILL.md | Toàn bộ kiến thức nội tuyến (270~465 dòng) | Chỉ bộ định tuyến (~50~80 dòng) |
| Hướng dẫn | Chỉ hỗ trợ CII | Hỗ trợ CII + Bảo mật AI |
| Lưu trữ kiến thức | Mã cứng trong SKILL.md | Tách riêng vào `references/` (18 tệp) |
| Mã hạng mục | Chỉ bao gồm một số hạng mục | Toàn bộ hạng mục dựa trên hướng dẫn 2026 |
| Khả năng mở rộng | Thêm hướng dẫn mới tăng số kỹ năng | Cố định 4 kỹ năng, chỉ thêm references |

**Thêm hướng dẫn mới: Hướng dẫn Bảo mật AI**
- Nguồn: Bộ Khoa học và ICT · KISA 「Hướng dẫn Bảo mật Trí tuệ Nhân tạo (AI)」
- Nhà phát triển AI: 54 hạng mục xác minh (vòng đời 6 giai đoạn)
- Yêu cầu bảo mật cho nhà cung cấp dịch vụ AI
- 7 quy tắc bảo mật cho người dùng AI

**Cập nhật Hướng dẫn CII**
- Trích xuất lại toàn bộ hạng mục dựa trên hướng dẫn chi tiết 2026
- Phản ánh hệ thống mã hạng mục (WEB, HV, CA và các mã mới khác)

### v1.0.0 (2026-03-29)

- Phiên bản đầu tiên
- 4 kỹ năng phân tích-đánh giá lỗ hổng CII (Hàn/Anh)
- Kỹ thuật (424) + Quản lý (127) + Vật lý (9) hạng mục

---

## Cơ sở Pháp lý

- **Luật Bảo vệ Hạ tầng Thông tin và Truyền thông** (Act on Protection of Information and Communications Infrastructure)
- **Luật Chính phủ Điện tử** (e-Government Act)
- **Luật Bảo vệ Thông tin Cá nhân** (Personal Information Protection Act)
- **Luật Cơ bản về Trí tuệ Nhân tạo** (AI Basic Act, có hiệu lực từ 2026.1.22)

---

## Tài liệu Liên quan

- [Hướng dẫn Chi tiết Phân tích-Đánh giá Lỗ hổng Kỹ thuật KISA](https://www.kisa.or.kr)
- [Hướng dẫn Bảo mật Trí tuệ Nhân tạo (AI)](https://www.kisa.or.kr)
- [OWASP Top 10](https://owasp.org/Top10/)
- [OWASP Top 10 for LLM](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [CWE/SANS Top 25](https://cwe.mitre.org/top25/)

---

## Built With

| Plugin | Mô tả |
|--------|-------|
| [authorkit-ko](https://github.com/cdppcorp/authorkit) | Kỹ năng hỗ trợ viết sách - phân tích PDF, trích xuất cấu trúc, biên tập/viết lại |
| [win-hooks](https://github.com/anthropics/claude-code-plugins) | Tương thích hook plugin Claude Code trên môi trường Windows |

---

## License

MIT License

## Author

CDPP Corp (https://github.com/cdppcorp)
