// Repository implementation for {{PascalCaseFeature}}.
// Note: Adapt DataState / Result wrappers, error handling, and helper extensions
// to match the Client workspace conventions.

import '../../domain/entities/{{snake_case_feature}}_entity.dart';
import '../../domain/repo/{{snake_case_feature}}_repository.dart';
import '../data_sources/{{snake_case_feature}}_data_source.dart';
import '../mappers/{{snake_case_feature}}_mapper.dart';
import '../models/{{snake_case_feature}}_model.dart';

class {{PascalCaseFeature}}RepoImpl implements {{PascalCaseFeature}}Repository {
  final {{PascalCaseFeature}}DataSource dataSource;
  final {{PascalCaseFeature}}Mapper mapper;

  {{PascalCaseFeature}}RepoImpl({
    required this.dataSource,
    required this.mapper,
  });

  @override
  Future<DataState<List<{{PascalCaseFeature}}Entity>>> getItems({String? filter}) async {
    try {
      final response = await dataSource.getItems(filter: filter);
      final dynamic rawList = response.data;
      if (rawList is! List) {
        return DataFailure(
          ErrorEntity(
            message: 'Invalid response format: expected List but received ${rawList.runtimeType}',
          ),
        );
      }
      final models = rawList
          .map((item) => {{PascalCaseFeature}}Model.fromJson(Map<String, dynamic>.from(item as Map)))
          .toList();
      return DataSuccess(mapper.toEntities(models));
    } catch (e) {
      return DataFailure(ErrorEntity(message: e.toString()));
    }
  }

  @override
  Future<DataState<{{PascalCaseFeature}}Entity>> getItemById(String id) async {
    try {
      final response = await dataSource.getItemById(id);
      final dynamic rawData = response.data;
      if (rawData is! Map) {
        return DataFailure(
          ErrorEntity(
            message: 'Invalid response format: expected Map but received ${rawData.runtimeType}',
          ),
        );
      }
      final model = {{PascalCaseFeature}}Model.fromJson(
        Map<String, dynamic>.from(rawData),
      );
      return DataSuccess(mapper.toEntity(model));
    } catch (e) {
      return DataFailure(ErrorEntity(message: e.toString()));
    }
  }
}
