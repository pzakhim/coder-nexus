# Hướng dẫn cài đặt & bắt đầu với Coder Nexus cho dự án Flutter (Từ A–Z)

Tài liệu này hướng dẫn từng bước dành cho người mới để cài đặt **Coder Nexus** cho dự án **Flutter**: từ thao tác bấm `Ctrl+Shift+P` (`Cmd+Shift+P`) trong **Antigravity**, đồng bộ **Flutter Pack**, thiết lập **Huly** (`setup huly`), thiết lập **Flutter** (`setup flutter`) cho đến những dòng lệnh đầu tiên.

---

## 1. Tổng quan trước khi bắt đầu

**Coder Nexus** gồm 2 phần cần được cài đặt:
1. **Extension trên Antigravity**: Giúp đồng bộ (Sync) bộ Agent Roles, Skills, Rules của **Flutter Pack** vào dự án và cung cấp menu lệnh nhanh (`Ctrl+Shift+P` / `Cmd+Shift+P`).
2. **`coder-nexus` CLI**: Công cụ dòng lệnh đóng vai trò MCP Server cho Agent, đồng thời cung cấp các lệnh `setup huly`, `setup flutter`, tải thiết kế Figma và kiểm tra môi trường.

---

## 2. Bước 1: Cài đặt Extension Coder Nexus

1. Mở **Antigravity**, nhấn `Ctrl+Shift+X` (Windows/Linux) hoặc `Cmd+Shift+X` (macOS) để mở mục **Extensions**.
2. Gõ tìm kiếm **`Coder Nexus`** (Publisher: `IMP-AIFactory`) và nhấn **Install**.
   - *Nếu cài từ file `.vsix`*: Nhấn vào biểu tượng `...` ở góc trên bên phải bảng Extensions → chọn **Install from VSIX...** và chọn file `.vsix`.

---

## 3. Bước 2: Cài đặt `coder-nexus` CLI (qua `Ctrl+Shift+P`)

1. Mở **Command Palette**: nhấn `Ctrl+Shift+P` (Windows/Linux) hoặc `Cmd+Shift+P` (macOS).
2. Gõ `Coder Nexus` và chọn lệnh:
   ```text
   Coder Nexus: Install / Update CLI
   ```
   *(Hoặc bấm vào chữ **Coder Nexus** dưới thanh Status Bar ở góc dưới màn hình → chọn **Install / Update CLI**).*
3. Hệ thống sẽ tự động cài `uv` (nếu máy chưa có) và cài đặt gói `coder-nexus` + `skill-factory` khớp với phiên bản Extension.
4. **Kiểm tra CLI sau khi cài xong**:
   - Nhấn `Ctrl+Shift+P` / `Cmd+Shift+P` → chọn **`Coder Nexus: Doctor / Check Environment & CLI`**.
   - Hoặc mở Terminal (`Ctrl+\``) và chạy:
     ```sh
     coder-nexus doctor
     ```

---

## 4. Bước 3: Đồng bộ gói Flutter vào dự án (Flutter Sync)

Mở thư mục dự án Flutter của bạn trên Antigravity, sau đó thực hiện đồng bộ bộ Agent/Skill của Flutter:

1. Nhấn `Ctrl+Shift+P` (hoặc `Cmd+Shift+P`).
2. Gõ `Coder Nexus` và chọn lệnh dành riêng cho Flutter:
   ```text
   Coder Nexus: Install Flutter Pack in Workspace
   ```
   *(Lưu ý: Bạn cũng có thể chọn `Coder Nexus: Install Frontend (Flutter) Pack in Workspace` hoặc `Coder Nexus: Sync Stack to Workspace (Auto-Detect)` rồi chọn `flutter` — kết quả đều cài đặt gói Flutter vào dự án).*

> **Lưu ý quan trọng:** Hãy chạy lại lệnh **Install Flutter Pack in Workspace** này **sau khi** bạn vừa cài đặt hoặc cập nhật CLI ở Bước 2 để file `.agents/plugins/coder-nexus/mcp_config.json` cập nhật đúng đường dẫn tuyệt đối tới `coder-nexus`.

Sau khi Sync gói Flutter xong, dự án của bạn sẽ có:
- `.agents/agents/`: 7 vai trò Agent đã gắn quy tắc Flutter (`Spec Writer`, `Planning`, `Code Writer`, `Code Reviewer`, `Test Runner`, `Docs Writer`, `Bug Fixer`).
- `.agents/plugins/coder-nexus/rules/clean_architecture_rules.md`: Quy tắc Clean Architecture luôn bật (`trigger: always_on`) cho Flutter.
- `.agents/plugins/coder-nexus/skills/`: Các kỹ năng dùng chung + bộ kỹ năng `flutter-*` (`flutter-clean-architecture`, `flutter-clean-code`, `flutter-ui-kit-mapping`, `flutter-unit-testing`...).
- `.agents/plugins/coder-nexus/mcp_config.json`: Cấu hình để Antigravity tự khởi chạy MCP Server.
- `.agents/stack.json`: Ghi nhận dự án đang dùng stack `flutter`.

---

## 5. Bước 4: Thiết lập Huly (`setup huly`) & Figma

Bước này giúp Agent tự động đọc nội dung task, Acceptance Criteria từ Huly và tải thiết kế Figma về máy.

### 5.1. Chạy lệnh `coder-nexus setup huly`
Mở Terminal tại thư mục gốc của dự án Flutter và chạy:

```sh
coder-nexus setup huly
```

Quá trình cài đặt sẽ diễn ra qua **2 bước tương tác**:

1. **`— Step 1/2: Huly URL —` (Nhập & kiểm tra Domain Huly)**:
   - CLI sẽ hỏi bạn địa chỉ Huly Server (mặc định gợi ý `https://huly.app` hoặc URL đang có trong `.env`):
     ```text
     Huly URL [https://huly.app]: https://huly.ten-cong-ty.com
     ```
   - Bạn nhập domain Huly của công ty/dự án vào (hoặc truyền thẳng qua cờ `coder-nexus setup huly --url https://huly.ten-cong-ty.com`).
   - CLI sẽ tự động chuẩn hoá URL (`https://...`), ping kiểm tra `<url>/config.json` để xác nhận đúng máy chủ Huly (`✅ Huly server detected (config.json OK)`) rồi lưu `HULY_WORKSPACE_URL` vào `.env`.
   - *(Nếu bạn đổi sang một domain Huly khác với domain cũ trong `.env`, CLI sẽ tự động xoá `HULY_SESSION_TOKEN` và `HULY_WORKSPACE_ID` cũ để đăng nhập lại từ đầu).*

2. **`— Step 2/2: Huly account —` (Đăng nhập tài khoản)**:
   - Nhập `Email / username` và `Password`.
   - CLI đăng nhập vào Huly, tự động lấy `HULY_SESSION_TOKEN` và `HULY_WORKSPACE_ID`, lưu vào file `.env`, đồng thời đọc thử danh sách task đang mở của bạn để xác minh kết nối.

> **Cảnh báo bảo mật:** Luôn đảm bảo file `.env` đã có trong `.gitignore` (nếu thiếu, CLI sẽ hiện cảnh báo `⚠️ .env is not in .gitignore`). Tuyệt đối không commit `.env` lên Git.

### 5.2. Các lệnh kiểm tra và lấy Task từ Huly
```sh
# 1. Xem trạng thái cấu hình Huly hiện tại trong file .env
coder-nexus setup huly --check

# 2. Đặt lại cấu hình và đăng nhập lại từ đầu (khi đổi tài khoản / hết hạn phiên)
coder-nexus setup huly --reset

# 3. Xem danh sách các task đang mở của bạn
coder-nexus my-tasks

# 4. Xem chi tiết một task kèm Acceptance Criteria (ví dụ IMES-1235)
coder-nexus task-detail IMES-1235

# 5. Xem chi tiết task VÀ tải luôn file đính kèm + thiết kế Figma về .superpowers/sources/<ID>/
coder-nexus task-detail IMES-1235 --download
```

### 5.3. Cấu hình Figma (Tuỳ chọn)
Để tải thiết kế Figma (`tokens.json`, `<node>.spec.json` và ảnh chụp từng màn hình `.png`), hãy mở file `.env` của dự án và điền Personal Access Token của Figma vào khoá `FIGMA_TOKEN`:

```env
FIGMA_TOKEN=figd_xxxxxxxxxxxxxxxxxxxx
```

*(Mẹo: Bạn có thể chạy lệnh `coder-nexus init` trước để CLI tự tạo khung file `.env` gồm đầy đủ các khoá `HULY_*` và `FIGMA_TOKEN`).*

---

## 6. Bước 5: Thiết lập môi trường Flutter (`setup flutter`)

Lệnh `setup flutter` giúp thiết lập **Architecture Profile**, kiểm tra kết nối tới các gói nền tảng (như `app_core`, `app_util`, `app_ui_kit`) và cài đặt các công cụ kiểm tra code cho Flutter.

### 6.1. Chọn Architecture Profile phù hợp
| Lựa chọn | Tên Profile | Khi nào sử dụng? |
|---|---|---|
| Phím **`1`** (Mặc định) | **`imespro`** | Dự án nội bộ công ty sử dụng 3 gói đặt cạnh thư mục dự án (`../app-core`, `../app-util`, `../app-ui-kit`). |
| Phím **`2`** | **`external-structured`** | Dự án khách hàng/bên ngoài đã có sẵn tầng nền tảng riêng (`lib/core/`, `lib/shared/`, `lib/common/`). |
| Phím **`3`** | **`external-standard`** | Dự án Flutter tiêu chuẩn độc lập, chưa có bộ thư viện dùng chung. |

### 6.2. Chạy lệnh `coder-nexus setup flutter`
Tại Terminal của thư mục dự án Flutter, chạy:

```sh
coder-nexus setup flutter
```
*(Hoặc truyền thẳng profile, ví dụ: `coder-nexus setup flutter --profile imespro` hoặc `coder-nexus setup flutter --profile external-standard`).*

Khi chạy, CLI sẽ thực hiện tuần tự **6 bước**:
1. **`[1/6] Architecture profile`**: Hỏi bạn chọn profile (`1: imespro`, `2: external-structured`, `3: external-standard`).
2. **`[2/6] Flutter project`**: Kiểm tra `pubspec.yaml` (nếu thư mục trống chưa có project, CLI sẽ hỏi bạn có muốn khởi tạo project Flutter chuẩn với các thư mục `lib/app`, `lib/config`, `lib/commons`, `lib/di`, `lib/router`, `lib/constants`, `lib/modules` hay không).
3. **`[3/6] Dependencies & foundations`**:
   - Với profile **`imespro`**: Kiểm tra 3 thư mục anh em nằm cạnh dự án (`../app-core`, `../app-util`, `../app-ui-kit`), hỗ trợ clone nếu thiếu (khi đã cấu hình `$CODER_NEXUS_CORE_GIT`), và tự động cập nhật `pubspec.yaml` (path dependencies + overrides) rồi chạy `flutter pub get`.
   - Với **`external-structured`** / **`external-standard`**: Kiểm tra cấu trúc thư mục và chạy `flutter pub get`.
4. **`[4/6] Developer tools`**: Kiểm tra và hỏi bạn xác nhận trước khi cài các gói hỗ trợ kiểm tra code (`flutter_lints`, `mocktail`, `bloc_test`, cấu hình `analysis_options.yaml`, `ripgrep`, `mockoon-cli`...).
5. **`[5/6] Record setup state`**: Ghi trạng thái kiến trúc và profile vào `.superpowers/setup.json` (tách biệt với `.agents/coder-nexus.setup.json` — nơi lưu kết quả cài đặt developer tools từ Bước `[4/6]` / `coder-nexus setup tools`), đồng thời tự động chép bộ tài liệu quy chuẩn của profile vừa chọn vào các skill Flutter trong `.agents/plugins/coder-nexus/skills/`.
6. **`[6/6] Verification check (--check)`**: Kiểm tra tổng thể lần cuối và in ra `STATUS: READY`.

### 6.3. Kiểm tra nhanh trạng thái Flutter bất kỳ lúc nào
```sh
coder-nexus setup flutter --check
```
Khi màn hình hiện `STATUS: READY`, dự án Flutter của bạn đã sẵn sàng 100%!

---

## 7. Bước 6: Những câu lệnh giao việc đầu tiên trong khung Chat

Mở khung chat của **Antigravity** và bắt đầu giao việc cho Agent theo 4 luồng:

### 1. Phát triển tính năng mới (`dev-team`)
Đi qua 3 cổng phê duyệt (**Gate 1**: Requirements & màn hình `S-NN`/luồng `W-NN` → **Gate 2**: Technical Design & UI Kit Mapping → **Gate 3**: Implementation Plan) trước khi viết code:
```text
Triển khai task IMES-1235 theo quy trình dev-team
```
hoặc:
```text
Dùng dev-team xây dựng màn hình danh sách đơn hàng từ link Figma: https://www.figma.com/design/...
```

### 2. Sửa lỗi kiểm soát 4 bước (`bug-squad`)
Tái hiện lỗi trước → tìm nguyên nhân gốc (Root Cause) & phạm vi ảnh hưởng → xác nhận mức độ (`S1–S4`, `L1/L2/L3`) → sửa code và chạy kiểm thử:
```text
Dùng bug-squad sửa lỗi: màn hình danh sách đơn hàng bị crash khi danh sách rỗng
```

### 3. Điều tra / Trace luồng không làm bẩn code (`debug-investigation`)
Chỉ đọc code hoặc gắn log tạm `[DBG-<slug>]` để tìm nguyên nhân, xuất báo cáo `diagnosis.md` và tự động xoá sạch log tạm:
```text
Debug giúp tôi: tại sao khi chuyển từ màn hình A sang màn hình B API lại bị gọi 2 lần?
```

### 4. Kiểm thử theo kịch bản (`feature-testing`)
Đóng vai `Test Runner` chạy thử kịch bản trên ứng dụng thực tế và xuất báo cáo `PASS`/`FAIL`:
```text
Test luồng đăng nhập sau đó mở màn hình chi tiết đơn hàng kiểm tra dữ liệu hiển thị
```

---

## 8. Bảng tra cứu lệnh nhanh (Cheat Sheet cho Flutter)

| Mục đích | Thao tác / Câu lệnh |
|---|---|
| Cài đặt / Cập nhật CLI | `Ctrl/Cmd + Shift + P` → `Coder Nexus: Install / Update CLI` |
| **Đồng bộ gói Flutter vào dự án** | `Ctrl/Cmd + Shift + P` → `Coder Nexus: Install Flutter Pack in Workspace` |
| Kiểm tra sức khoẻ toàn diện | `coder-nexus doctor` |
| Tạo khung file `.env` mẫu | `coder-nexus init` |
| Thiết lập đăng nhập Huly | `coder-nexus setup huly` |
| Đổi URL / Đăng nhập lại Huly | `coder-nexus setup huly --reset` |
| Kiểm tra cấu hình Huly | `coder-nexus setup huly --check` |
| Xem danh sách task của tôi | `coder-nexus my-tasks` |
| Tải chi tiết task & Figma | `coder-nexus task-detail <TASK_ID> --download` |
| Thiết lập dự án Flutter (`imespro`) | `coder-nexus setup flutter --profile imespro` |
| Kiểm tra môi trường Flutter | `coder-nexus setup flutter --check` |
| Chỉ cài / kiểm tra dev tools Flutter | `coder-nexus setup tools --pack flutter` |
