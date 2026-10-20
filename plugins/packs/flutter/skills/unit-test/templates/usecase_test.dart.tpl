import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';

// Mock dependencies
class Mock{{FEATURE_NAME_PASCAL}}Repository extends Mock implements {{FEATURE_NAME_PASCAL}}Repository {}

void main() {
  late {{FEATURE_NAME_PASCAL}}UseCase useCase;
  late Mock{{FEATURE_NAME_PASCAL}}Repository mockRepository;

  setUp(() {
    mockRepository = Mock{{FEATURE_NAME_PASCAL}}Repository();
    useCase = {{FEATURE_NAME_PASCAL}}UseCase(mockRepository);
  });

  final tParams = {{FEATURE_NAME_PASCAL}}Params(/* test parameters */);
  final tEntity = {{FEATURE_NAME_PASCAL}}Entity(/* expected entity values */);

  group('{{FEATURE_NAME_PASCAL}}UseCase', () {
    test('should return data from repository when call is successful', () async {
      // Arrange
      when(() => mockRepository.execute(any()))
          .thenAnswer((_) async => Right(tEntity));

      // Act
      final result = await useCase.call(tParams);

      // Assert
      expect(result, equals(Right(tEntity)));
      verify(() => mockRepository.execute(tParams)).called(1);
      verifyNoMoreInteractions(mockRepository);
    });

    test('should return Failure when repository call fails', () async {
      // Arrange
      const tFailure = ServerFailure(message: 'Server error');
      when(() => mockRepository.execute(any()))
          .thenAnswer((_) async => const Left(tFailure));

      // Act
      final result = await useCase.call(tParams);

      // Assert
      expect(result, equals(const Left(tFailure)));
      verify(() => mockRepository.execute(tParams)).called(1);
      verifyNoMoreInteractions(mockRepository);
    });
  });
}
