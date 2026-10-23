# FE-BE API Handshake Protocol

Quy ước chuẩn kết nối và chuyển giao giữa các **Frontend pack** (Client UI) và **Backend pack** (API Service). Hai bên nằm ở hai workspace riêng (mỗi workspace cài đúng một pack); mỗi bên chỉ sửa các đường dẫn mà pack của workspace đó sở hữu trong `.agents/stack.json`.

---

## 1. Nguyên tắc cốt lõi (Core Principles)

### Installed location and evidence policy

The canonical source is `plugins/shared_contracts/api_handshake_protocol.md`. Both installers copy it into each selected plugin as `shared_contracts/api_handshake_protocol.md`. All FE and BE roles read that plugin-root path. Project API contracts remain separate, revisioned artifacts under the work item's approved `contracts/` location; transporting them between workspaces is explicit and never implies authority to edit the other repository.

- A proposed FE contract remains `DRAFT_BY_FE` until BE reviews it. User approval of a Mockoon environment does not imply `APPROVED_BY_BE` or `LIVE_DEPLOYED`.
- Every external BE API dependency is classified as either **`BE_API_READY`** (live/documented BE API verified against user specification) or **`MOCKOON_MOCKED`** (no BE API available yet; served locally via `mockoon-cli` using `mocks/<feature>_mockoon.json`).
- All external API contracts, Huly task context (fetched once), and agreed Pass/Default vs. Fail rules are consolidated into **`PHASE-00` (`phases/phase-00-prepare.md`)** and `design.md` so downstream agents (`code_writer`, `code_reviewer`, `test_runner`) read from a single source without re-querying Huly or hunting for specs.
- When `MOCKOON_MOCKED` is approved, `planning` agrees with the user on which inputs trigger **Pass/Default (`200/201`)**, **Empty (`[]`)**, and **Fail (`400/401/403/500`)** in `design.md`, and `PHASE-00` is marked `[EXECUTE]` to prepare `mocks/<feature>_mockoon.json` and verify `mockoon-cli` before `PHASE-01` starts. `lib/` must always implement the real `RemoteDataSource` calling `ApiService` over HTTP — never create fake `Mock<Feature>DataSource` classes or production fallbacks in `lib/`.
- Unknown fields/behavior stay open questions. Required contract evidence missing or conflicting with Client policy means `BLOCKED`; agents cannot fabricate a successful source.
- QA (`test_runner`) focuses strictly on **UI / Widget / Visual verification** (4 visual states: `Loading`, `Content`, `Empty`, `Error`) and records **UI/contract checks (via `MOCKOON_MOCKED` or `BE_API_READY`)** and **live integration checks** with data provenance, contract revision, and code revision.
- Switching from `MOCKOON_MOCKED` to live BE services updates the environment Base URL (`.env` / `AppConfig`) and verifies live auth, schemas, errors, and behavior without rewriting `lib/` Data or Presentation classes.

Unit-test doubles (`mocktail` / `bloc_test`) remain owned by `code_writer` and audited by `code_reviewer` for isolated logic checks using the agreed Pass/Default and Fail payloads in `design.md`.

1. **Contract-First as Single Source of Truth (SSOT)**: Mọi tương tác dữ liệu giữa Client và Server phải được đặc tả bằng Schema trước khi code.
2. **Technical BA Boundary**: 
   - FE Technical BA không tự tiện yêu cầu BE viết API phi thực tế.
   - BE Technical BA không tự ý đổi kiểu dữ liệu (data types) mà không thông báo cho FE.
3. **No Unblocked Assumptions**: Khi FE cần một API chưa tồn tại, FE không được giả định API đó tự động có mặt. FE phải kích hoạt luồng `MOCKOON_MOCKED` (ở `PHASE-00`) hoặc Handshake chính thức.

---

## 2. Quy trình Handshake 5 bước (5-Step Lifecycle)

```
[ FE-NEXUS ]                                                          [ BE-NEXUS ]
(Client Repo)                                                          (Server Repo)
      │                                                                      ▲
      ▼ (Bước 1: Phát hiện Gap)                                              │
1. Spec Writer (FE) phân tích feature,                                       │
   chốt BE_API_READY hoặc MOCKOON_MOCKED                                     │
      │                                                                      │
      ▼ (Bước 2: Xuất Contract / Chuẩn bị PHASE-00)                          │
2. Tạo: `mocks/<feature>_mockoon.json` (nếu MOCKOON_MOCKED)                  │
   hoặc `contracts/drafts/<feature>_api.json` ───────────────────────────────┤
                                                                             │
                                                                             ▼ (Bước 3: Thẩm định Kỹ thuật)
                                                                       3. Spec Writer & Planning (BE):
                                                                          • Review schema & feasibility
                                                                          • Đối soát với DB & Auth
                                                                          • Duyệt: `APPROVED_BY_BE`
                                                                             │
                                                                             ▼ (Bước 4: Thực thi & Kiểm thử)
                                                                       4. BE Coder & Tester:
                                                                          • Code endpoint & Unit Test
                                                                          • Xuất Mock URL / Swagger
                                                                             │
      ▲ (Bước 5: Tích hợp Hoàn tất)                                          │
5. FE Coder & Tester: ◄──────────────────────────────────────────────────────┘
   • Trỏ Base URL sang endpoint thật
   • UI & End-to-End Verification
   • Đóng Handshake Ticket
```

---

## 3. Cấu trúc Schema Hợp đồng (Contract Schema)

Tất cả file Handshake Contract lưu tại `contracts/` hoặc `mocks/<feature>_mockoon.json` theo định dạng JSON / OpenAPI:
- **`endpoint`**: Đường dẫn tương đối (vd: `/api/v1/<feature>/export`).
- **`method`**: `GET`, `POST`, `PUT`, `PATCH`, `DELETE`.
- **`headers`**: Yêu cầu xác thực (`Authorization: Bearer <token>`), Content-Type.
- **`request`**: Query parameters và Request Body JSON Schema.
- **`responses`**: Các mã HTTP phản hồi (`200`, `201`, `400`, `401`, `404`, `500`) kèm response payload schema.

---

## 4. Trạng thái Vòng đời Handshake (Handshake Lifecycle Statuses)

| Trạng thái | Ý nghĩa | Chủ sở hữu hiện tại |
| :--- | :--- | :--- |
| `DRAFT_BY_FE` | FE vừa tạo bản nháp yêu cầu API mới | FE Technical BA |
| `IN_BE_REVIEW` | BE đang thẩm định tính khả thi và DB schema | BE Technical BA & Tech Lead |
| `APPROVED_BY_BE` | BE đã chốt schema và đưa vào kế hoạch sprint | BE Planning |
| `READY_FOR_MOCK` | BE đã cung cấp Mock Server hoặc Swagger schema | FE Coder có thể bắt đầu code UI |
| `LIVE_DEPLOYED` | Endpoint đã deploy môi trường Staging/Dev | FE Coder cắm live API |
| `VERIFIED_CLOSED` | Cả 2 bên kiểm thử tích hợp thành công | Done |
