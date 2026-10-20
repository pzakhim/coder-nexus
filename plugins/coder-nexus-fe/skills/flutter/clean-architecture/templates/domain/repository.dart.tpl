/// Abstract contract for {{PascalCaseFeature}} repository.
///
/// Rules:
/// - Defined in Domain Layer.
/// - Returns Future<DataState<T>> or Result<T> according to Client workspace conventions.
/// - Does not depend on Data layer or implementation details.

import '../entities/{{snake_case_feature}}_entity.dart';

abstract class {{PascalCaseFeature}}Repository {
  Future<DataState<List<{{PascalCaseFeature}}Entity>>> getItems({String? filter});
  Future<DataState<{{PascalCaseFeature}}Entity>> getItemById(String id);
}
