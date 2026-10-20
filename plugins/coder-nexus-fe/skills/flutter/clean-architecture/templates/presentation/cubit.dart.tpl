// Cubit managing {{PascalCaseFeature}} state.
//
// Rules:
// - Injects UseCase(s) from Domain layer.
// - Emits states deriving from feature state or Client base bloc state.

import 'package:flutter_bloc/flutter_bloc.dart';

import '../../domain/entities/{{snake_case_feature}}_entity.dart';
import '../../domain/usecases/get_{{snake_case_feature}}_usecase.dart';

part '{{snake_case_feature}}_state.dart';

class {{PascalCaseFeature}}Cubit extends Cubit<{{PascalCaseFeature}}State> {
  final Get{{PascalCaseFeature}}UseCase getItemsUseCase;

  {{PascalCaseFeature}}Cubit({required this.getItemsUseCase}) : super({{PascalCaseFeature}}Initial());

  Future<void> fetchItems({String? filter}) async {
    emit({{PascalCaseFeature}}Loading());

    final result = await getItemsUseCase(Get{{PascalCaseFeature}}Params(filter: filter));

    if (result.isSuccess && result.data != null) {
      emit({{PascalCaseFeature}}Success(items: result.data!));
    } else {
      final error = result.error;
      emit({{PascalCaseFeature}}Error(message: error?.message ?? 'Failed to fetch items'));
    }
  }
}
