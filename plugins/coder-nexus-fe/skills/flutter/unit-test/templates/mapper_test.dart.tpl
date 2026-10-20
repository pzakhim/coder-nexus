import 'package:flutter_test/flutter_test.dart';

void main() {
  final tJson = <String, dynamic>{
    'id': '123',
    'title': 'Test Item',
    'is_active': true,
  };

  final tModel = {{FEATURE_NAME_PASCAL}}Model(
    id: '123',
    title: 'Test Item',
    isActive: true,
  );

  group('{{FEATURE_NAME_PASCAL}}Model Serialization & Mapping', () {
    test('fromJson should return valid model from JSON map', () {
      // Act
      final result = {{FEATURE_NAME_PASCAL}}Model.fromJson(tJson);

      // Assert
      expect(result.id, equals('123'));
      expect(result.title, equals('Test Item'));
      expect(result.isActive, isTrue);
    });

    test('toJson should convert model into expected JSON map', () {
      // Act
      final result = tModel.toJson();

      // Assert
      expect(result, equals(tJson));
    });

    test('toEntity should map model fields to pure domain entity fields', () {
      // Act
      final entity = tModel.toEntity();

      // Assert
      expect(entity.id, equals(tModel.id));
      expect(entity.title, equals(tModel.title));
      expect(entity.isActive, equals(tModel.isActive));
    });
  });
}
