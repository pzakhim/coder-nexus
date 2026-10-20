import 'package:get_it/get_it.dart';

import 'data/data_sources/{{snake_case_feature}}_data_source.dart';
import 'data/mappers/{{snake_case_feature}}_mapper.dart';
import 'data/repo_impl/{{snake_case_feature}}_repo_impl.dart';
import 'domain/repo/{{snake_case_feature}}_repository.dart';
import 'domain/usecases/get_{{snake_case_feature}}_usecase.dart';
import 'presentation/bloc/{{snake_case_feature}}_cubit.dart';

/// Module DI configuration for {{PascalCaseFeature}}.
///
/// MANDATORY Registration Order:
/// 1. Mapper (no dependencies)
/// 2. DataSource (injects API / network client from core)
/// 3. Repository (registers abstract interface contract)
/// 4. UseCases (one per business action)
/// 5. Cubits (factory for screen lifecycle)
Future<void> di{{PascalCaseFeature}}Module(GetIt injector) async {
  // 1. Mapper
  injector.registerLazySingleton(() => {{PascalCaseFeature}}Mapper());

  // 2. DataSource
  injector.registerLazySingleton<{{PascalCaseFeature}}DataSource>(
    () => {{PascalCaseFeature}}DataSourceImpl(
      apiService: injector(),
    ),
  );

  // 3. Repository (Contract bound to RepoImpl)
  injector.registerLazySingleton<{{PascalCaseFeature}}Repository>(
    () => {{PascalCaseFeature}}RepoImpl(
      dataSource: injector(),
      mapper: injector(),
    ),
  );

  // 4. UseCases
  injector.registerLazySingleton(() => Get{{PascalCaseFeature}}UseCase(repo: injector()));

  // 5. Cubits
  injector.registerFactory(
    () => {{PascalCaseFeature}}Cubit(getItemsUseCase: injector()),
  );
}
