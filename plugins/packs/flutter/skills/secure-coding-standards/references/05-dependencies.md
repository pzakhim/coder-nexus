# 05 - Dependency Management & Plugin Vetting

Mobile Flutter apps depend on Dart packages and native Android/iOS plugins. Native plugins execute with full application privileges.

## 1. Vetting Third-Party Packages

Before adding any new package to `pubspec.yaml`:
1. **Publisher Verification:** Check pub.dev verified publisher status and package popularity.
2. **Maintenance Status:** Verify that the package has recent updates (within the last 6 months) and supports current Flutter / Dart versions.
3. **Native Permissions:** Inspect Android `AndroidManifest.xml` and iOS `Info.plist` declared by the plugin. Reject packages that request excessive permissions (e.g. background location, camera) beyond their feature requirement.

## 2. Dependency Audit Commands

```bash
# Check for outdated packages and breaking upgrades
flutter pub outdated

# Verify dependency graph consistency
flutter pub get
```
