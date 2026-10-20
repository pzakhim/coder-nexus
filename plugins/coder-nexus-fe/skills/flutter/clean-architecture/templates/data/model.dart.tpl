/// DTO Model for {{PascalCaseFeature}}.
///
/// Rules:
/// - Safe parsing with strict validation on mandatory fields.
/// - Mandatory fields validate and fail-fast; NO silent fake fallbacks (0, empty string, fake timestamp).
/// - Optional fields should be nullable without fake defaults.
class {{PascalCaseFeature}}Model {
  final String id;
  final String title;
  final String status;
  final DateTime createdAt;

  {{PascalCaseFeature}}Model({
    required this.id,
    required this.title,
    required this.status,
    required this.createdAt,
  });

  factory {{PascalCaseFeature}}Model.fromJson(Map<String, dynamic> json) {
    final id = json['id'] as String?;
    if (id == null || id.isEmpty) {
      throw const FormatException('{{PascalCaseFeature}}Model missing required field: id');
    }

    final title = json['title'] as String?;
    if (title == null || title.isEmpty) {
      throw const FormatException('{{PascalCaseFeature}}Model missing required field: title');
    }

    final status = json['status'] as String?;
    if (status == null || status.isEmpty) {
      throw const FormatException('{{PascalCaseFeature}}Model missing required field: status');
    }

    final rawCreatedAt = json['createdAt'] as String?;
    if (rawCreatedAt == null) {
      throw const FormatException('{{PascalCaseFeature}}Model missing required field: createdAt');
    }
    final createdAt = DateTime.tryParse(rawCreatedAt);
    if (createdAt == null) {
      throw const FormatException('{{PascalCaseFeature}}Model invalid date format: createdAt');
    }

    return {{PascalCaseFeature}}Model(
      id: id,
      title: title,
      status: status,
      createdAt: createdAt,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'title': title,
      'status': status,
      'createdAt': createdAt.toIso8601String(),
    };
  }
}
