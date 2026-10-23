# 02 - Size and Structure (Flutter / Dart)

Maintain small, focused, composable units across presentation, domain, and data layers.

## 1. Size Thresholds

| Scope | Threshold | Remedy when exceeded |
|---|---|---|
| Method / Function | $\le 30$ lines | Extract sub-methods or separate utility helper. |
| Widget `build()` method | $\le 40$ lines | Extract sub-widgets (see [02b-splitting](02b-splitting.md)). |
| Class | $\le 200$ lines | Decompose responsibilities; split presentation from state management. |
| File | $\le 250$ lines | Split into multiple files or move sub-widgets to private files. |
| Parameters per function | $\le 4$ parameters | Use named parameters; group parameters into value objects / request models. |
| Widget tree nesting depth | $\le 4$ levels | Extract intermediate widgets to flatten build tree. |

## 2. BaseScreen Lifecycle & Structure

Route screens in iMESPro must inherit from `BaseScreen` and `BaseScreenState`:

```dart
class OrderListScreen extends BaseScreen {
  const OrderListScreen({super.key});

  @override
  ScreenModel getScreen() => const ScreenModel(
        id: 101,
        name: 'order_list_screen',
        route: '/orders',
      );

  @override
  State<OrderListScreen> createState() => _OrderListScreenState();
}

class _OrderListScreenState extends BaseScreenState<OrderListScreen> {
  @override
  Widget buildMobilePortrait() {
    return Scaffold(
      appBar: const AppDefaultAppbar(title: 'Orders'),
      body: BlocBuilder<OrderListCubit, OrderListState>(
        builder: (context, state) => _OrderListView(state: state),
      ),
    );
  }
}
```

### Critical Gotchas
- **NEVER override `build()` in `BaseScreenState`**: Overriding `build()` completely skips `TrackingBaseState` (Matomo & Firebase tracking) and `ResponsiveLayoutBuilder`. Always override `buildMobilePortrait()`.
- **Pure `build()` methods**: A `build()` method must be completely deterministic and free of side effects. Never trigger navigation, network requests, or `cubit.fetch()` inside `build()`. Trigger them in `initState()`, `BlocListener`, or user event callbacks.
- **Resource Management**: Any class that creates a `TextEditingController`, `AnimationController`, `FocusNode`, or `StreamSubscription` must dispose them in `dispose()`:
  ```dart
  @override
  void dispose() {
    _searchController.dispose();
    _subscription?.cancel();
    super.dispose();
  }
  ```
