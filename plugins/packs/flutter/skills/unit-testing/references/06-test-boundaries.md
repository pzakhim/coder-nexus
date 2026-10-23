# 06 - Test Boundaries and Limitations

Maintain clarity on what unit tests prove and what requires other verification layers.

## 1. What Unit Tests Prove

- UseCase business logic branching correctly based on mocked inputs.
- Cubit state transitions emitting expected state sequence in response to events.
- Data mapper conversions between JSON maps, DTOs, and Domain Entities.
- Error handling logic when repository returns `DataFailure`.

## 2. What Unit Tests Do NOT Prove

- **Real API Communication:** Unit tests mock `ApiService` and cannot verify whether backend schemas have changed in production (requires integration testing).
- **Pixel-Perfect Rendering:** Unit tests do not verify widget rendering, colors, or touch target sizes (requires `{{slot:visual-quality}}` or golden tests).
- **Physical Device Sensors / Hardware:** Platform features like camera, GPS, or push tokens must be verified on emulator/device.
