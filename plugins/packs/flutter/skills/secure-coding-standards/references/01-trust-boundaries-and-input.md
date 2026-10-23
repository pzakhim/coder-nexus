# 01 - Trust Boundaries and Input Validation

Client applications run in an untrusted environment. All external input—user typing, clipboard content, deep links, push notifications, and API responses—must be validated at the trust boundary.

## 1. Form Inputs & User Data

- **Input Validation via `AppFormField`:**
  - Always provide a `validator` when `isRequired: true` on `AppFormField`.
  - Validate email formats, phone numbers, numeric limits, and string lengths before invoking UseCases or emitting API payloads.
  - Sanitize text inputs by trimming leading and trailing whitespace.
- **Obscuring Sensitive Inputs:**
  - Password, PIN, and sensitive credential fields must use `fieldType: AppFormFieldType.password` and `obscureText: true`.
  - Provide an eye toggle callback (`onObscureToggle`) for user review without revealing plaintext by default.

## 2. Deep Links and Navigation Boundaries

Deep links received from external apps, web browsers, or push payloads can be forged:

```dart
// BAD: Directly navigating with untrusted raw path
void handleDeepLink(Uri uri) {
  Navigator.pushNamed(context, uri.path); // Unchecked parameter navigation
}

// GOOD: Validate route name and sanitize query parameters
void handleDeepLink(Uri uri) {
  final path = uri.path;
  if (!AppRoute.isValidRoute(path)) {
    AppLogger.I.w('Rejected invalid deep link route: $path');
    return;
  }
  final rawId = uri.queryParameters['id'];
  final id = parseInt(rawId);
  if (id <= 0) {
    AppLogger.I.w('Invalid id parameter in deep link: $rawId');
    return;
  }
  Navigator.pushNamed(context, path, arguments: id);
}
```

## 3. Parsing External API Payloads

- Never assume backend payloads conform to schema.
- Use `app_util` safe parsers (`parseString`, `parseInt`, `parseDouble`, `parseBool`, `parseList`) inside DTO `fromJson` methods to avoid runtime type casting crashes (`TypeError`).
