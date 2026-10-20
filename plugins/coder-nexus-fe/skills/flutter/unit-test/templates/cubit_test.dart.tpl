import 'package:bloc_test/bloc_test.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';

class Mock{{FEATURE_NAME_PASCAL}}UseCase extends Mock implements {{FEATURE_NAME_PASCAL}}UseCase {}

void main() {
  late {{FEATURE_NAME_PASCAL}}Cubit cubit;
  late Mock{{FEATURE_NAME_PASCAL}}UseCase mockUseCase;

  setUp(() {
    mockUseCase = Mock{{FEATURE_NAME_PASCAL}}UseCase();
    cubit = {{FEATURE_NAME_PASCAL}}Cubit(useCase: mockUseCase);
  });

  tearDown(() {
    cubit.close();
  });

  final tEntity = {{FEATURE_NAME_PASCAL}}Entity(/* expected test entity */);

  test('initial state should be {{FEATURE_NAME_PASCAL}}InitialState', () {
    expect(cubit.state, equals(const {{FEATURE_NAME_PASCAL}}InitialState()));
  });

  group('{{FEATURE_NAME_PASCAL}}Cubit Execution Flow', () {
    blocTest<{{FEATURE_NAME_PASCAL}}Cubit, {{FEATURE_NAME_PASCAL}}State>(
      'emits [LoadingState, SuccessState] when usecase succeeds',
      build: () {
        when(() => mockUseCase.call(any()))
            .thenAnswer((_) async => Right(tEntity));
        return cubit;
      },
      act: (cubit) => cubit.loadData(),
      expect: () => [
        isA<{{FEATURE_NAME_PASCAL}}LoadingState>(),
        isA<{{FEATURE_NAME_PASCAL}}SuccessState>(),
      ],
      verify: (_) {
        verify(() => mockUseCase.call(any())).called(1);
      },
    );

    blocTest<{{FEATURE_NAME_PASCAL}}Cubit, {{FEATURE_NAME_PASCAL}}State>(
      'emits [LoadingState, ErrorState] when usecase fails',
      build: () {
        when(() => mockUseCase.call(any()))
            .thenAnswer((_) async => const Left(ServerFailure(message: 'Error')));
        return cubit;
      },
      act: (cubit) => cubit.loadData(),
      expect: () => [
        isA<{{FEATURE_NAME_PASCAL}}LoadingState>(),
        isA<{{FEATURE_NAME_PASCAL}}ErrorState>(),
      ],
      verify: (_) {
        verify(() => mockUseCase.call(any())).called(1);
      },
    );
  });
}
