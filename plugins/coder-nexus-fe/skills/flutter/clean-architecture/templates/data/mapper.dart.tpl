import '../../domain/entities/{{snake_case_feature}}_entity.dart';
import '../models/{{snake_case_feature}}_model.dart';

/// Mapper converting between {{PascalCaseFeature}}Model (DTO) and {{PascalCaseFeature}}Entity.
class {{PascalCaseFeature}}Mapper {
  {{PascalCaseFeature}}Entity toEntity({{PascalCaseFeature}}Model model) {
    return {{PascalCaseFeature}}Entity(
      id: model.id,
      title: model.title,
      status: model.status,
      createdAt: model.createdAt,
    );
  }

  List<{{PascalCaseFeature}}Entity> toEntities(List<{{PascalCaseFeature}}Model> models) {
    return models.map(toEntity).toList();
  }

  {{PascalCaseFeature}}Model toModel({{PascalCaseFeature}}Entity entity) {
    return {{PascalCaseFeature}}Model(
      id: entity.id,
      title: entity.title,
      status: entity.status,
      createdAt: entity.createdAt,
    );
  }
}
