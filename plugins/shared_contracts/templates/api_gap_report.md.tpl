# Frontend API Gap Report: {{FeatureTitle}}

> **Reporter**: Spec Writer (Technical BA - FE)  
> **Target Module**: {{TargetModule}}  
> **Date**: {{ReportDate}}  
> **Status**: DRAFT_BY_FE  
> **Linked Contract**: `{{ContractPath}}`

## 1. Bối cảnh & Lý do cần API (Context)
{{ContextDescription}}

## 2. Thông số Endpoint mong đợi (Expected Endpoint Specs)
- **Method**: `{{HttpMethod}}`
- **Path**: `{{EndpointPath}}`
- **Tần suất gọi (Expected Volume)**: {{VolumeEstimate}}

## 3. Dữ liệu Mock tạm thời của FE (Temporary FE Mocking)
FE sẽ sử dụng mock model sau trong thời gian chờ BE hoàn tất:
```json
{{MockJsonPayload}}
```

## 4. Hành động yêu cầu từ BE (Action Required from BE-Nexus)
1. Thẩm định schema trong file `{{ContractPath}}`.
2. Phản hồi và xác nhận khả năng đáp ứng trong Sprint.
