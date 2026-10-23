# 02 - Layer Isolation & Hypothesizing

Isolate defects by evaluating each layer in the Clean Architecture stack sequentially.

## 1. Top-Down Layer Inspection

1. **Presentation / UI Layer:**
   - Did the widget receive the expected state from the Cubit?
   - Is `buildWhen` in `BlocBuilder` filtering out the state?
   - Is `BaseScreenState.buildMobilePortrait()` being called?
2. **State Management (Cubit):**
   - Did the Cubit trigger the UseCase?
   - Did the Cubit emit the Failure state when an error occurred?
   - Was state mutated in place instead of emitting a new instance?
3. **Domain Layer (UseCase):**
   - Were the parameters passed to `UseCasePower` valid?
   - Did business validation fail unexpectedly?
4. **Data Layer (Repository & Data Source):**
   - Did `ApiService` receive an unexpected HTTP status code?
   - Did `.tryCatch` return a `DataFailure`?
   - Did the model `fromJson` fail to parse fields?

## 2. Testing the Hypothesis

- Formulate a single concise hypothesis: "The Cubit fails to emit an error state when the API returns HTTP 404 because `.tryCatch` failure is not checked before reading `data`."
- Test the hypothesis by verifying the failing test case matches this exact failure point.
