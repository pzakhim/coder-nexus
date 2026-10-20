// Template: Remote DataSource for {{PascalCaseFeature}}.
// Note: Adapt package imports, base classes, and HTTP client to match your project conventions.

abstract class {{PascalCaseFeature}}DataSource {
  Future<dynamic> getItems({String? filter});
  Future<dynamic> getItemById(String id);
}

class {{PascalCaseFeature}}DataSourceImpl implements {{PascalCaseFeature}}DataSource {
  final dynamic apiService;

  {{PascalCaseFeature}}DataSourceImpl({
    required this.apiService,
  });

  @override
  Future<dynamic> getItems({String? filter}) async {
    return apiService.get(
      '/api/{{camelCaseFeature}}',
      queryParameters: {
        if (filter != null) 'filter': filter,
      },
    );
  }

  @override
  Future<dynamic> getItemById(String id) async {
    return apiService.get('/api/{{camelCaseFeature}}/$id');
  }
}
