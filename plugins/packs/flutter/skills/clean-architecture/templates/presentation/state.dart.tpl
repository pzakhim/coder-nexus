part of '{{snake_case_feature}}_cubit.dart';

/// State machine for {{PascalCaseFeature}}.
///
/// Rules:
/// - Uses sealed class extending project BaseBlocState or Equatable.
/// - Each state is a final class overriding props / equatableProps.
sealed class {{PascalCaseFeature}}State {
  const {{PascalCaseFeature}}State();
}

final class {{PascalCaseFeature}}Initial extends {{PascalCaseFeature}}State {
  @override
  List<Object?> get equatableProps => [];
}

final class {{PascalCaseFeature}}Loading extends {{PascalCaseFeature}}State {
  @override
  List<Object?> get equatableProps => [];
}

final class {{PascalCaseFeature}}Success extends {{PascalCaseFeature}}State {
  final List<{{PascalCaseFeature}}Entity> items;

  {{PascalCaseFeature}}Success({required this.items});

  @override
  List<Object?> get equatableProps => [items];
}

final class {{PascalCaseFeature}}Error extends {{PascalCaseFeature}}State {
  final String message;

  {{PascalCaseFeature}}Error({required this.message});

  @override
  List<Object?> get equatableProps => [message];
}
