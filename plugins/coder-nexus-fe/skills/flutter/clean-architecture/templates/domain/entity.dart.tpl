import 'package:equatable/equatable.dart';

/// Pure Dart entity representing {{feature_entity_name}}.
///
/// Rules:
/// - Immutable fields (final).
/// - No Flutter UI imports.
/// - Value equality via Equatable.
class {{PascalCaseFeature}}Entity extends Equatable {
  final String id;
  final String title;
  final String status;
  final DateTime createdAt;

  const {{PascalCaseFeature}}Entity({
    required this.id,
    required this.title,
    required this.status,
    required this.createdAt,
  });

  @override
  List<Object?> get props => [id, title, status, createdAt];
}
