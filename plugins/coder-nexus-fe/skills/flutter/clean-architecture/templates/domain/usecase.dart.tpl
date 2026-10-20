// UseCase handling single business action: retrieving items.
//
// Rules:
// - One UseCase per specific business operation.
// - Injects abstract repository contract.
// - Adapt base UseCase class or interface to match Client workspace conventions.

import 'package:equatable/equatable.dart';

import '../entities/{{snake_case_feature}}_entity.dart';
import '../repo/{{snake_case_feature}}_repository.dart';

/// Parameters for Get{{PascalCaseFeature}}UseCase.
class Get{{PascalCaseFeature}}Params extends Equatable {
  final String? filter;

  const Get{{PascalCaseFeature}}Params({this.filter});

  @override
  List<Object?> get props => [filter];
}

class Get{{PascalCaseFeature}}UseCase {
  final {{PascalCaseFeature}}Repository repo;

  Get{{PascalCaseFeature}}UseCase({required this.repo});

  Future<DataState<List<{{PascalCaseFeature}}Entity>>> call(Get{{PascalCaseFeature}}Params params) {
    return repo.getItems(filter: params.filter);
  }
}
