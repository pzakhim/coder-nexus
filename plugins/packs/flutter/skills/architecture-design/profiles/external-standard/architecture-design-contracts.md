# External Standard Architecture Design Contracts

> Topic: Ponytail minimalist Clean Architecture and standard Flutter SDK design rules (external-standard profile)

## 1. Activation & Ponytail Minimalism (`external-standard`)

This profile applies when the Flutter Client has neither `imespro` packages nor a pre-existing `lib/core/` / `lib/shared/` foundation framework (e.g., greenfield apps or vanilla Flutter repositories).

Follow the **Ponytail Minimalism & YAGNI** standard:
1. **Smallest Clear Architecture:** Include only the folders and layers under `lib/modules/<feature>/` required by the approved behavior. Never scaffold speculative `lib/core/` wrappers, custom `BaseScreen` classes, or unused pass-through layers "just in case".
2. **Standard Flutter & Dart 3 First:**
   - **Screens & Widgets:** Standard `StatelessWidget` / `StatefulWidget`, Material 3 / Cupertino components (`FilledButton`, `TextFormField`, `CircularProgressIndicator`, `AlertDialog`), and feature-private widgets under `lib/modules/<feature>/presentation/widgets/`.
   - **State & Results:** Use the state package already in `pubspec.yaml` (`flutter_bloc`, `riverpod`, `provider`, or `ValueNotifier`/`ChangeNotifier`) and Dart 3 `sealed class` states/results.
   - **Data & Parsing:** Standard `fromJson`/`toJson` (or `json_serializable` if already installed) with safe numeric casts (`(json['key'] as num?)?.toDouble()`).
3. **Rule of Two for Shared Code:** Build new widgets and utilities inside `lib/modules/<feature>/` first; promote to `lib/commons/` only when two or more distinct features require the exact same component.
