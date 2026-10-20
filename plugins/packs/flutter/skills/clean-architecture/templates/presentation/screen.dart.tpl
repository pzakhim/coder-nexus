// Resolve every placeholder against the active Client package and router.
// A commented or missing BaseScreen contract is BLOCKED.
import 'package:flutter/material.dart';
import '{{verified_base_screen_import}}';
{{verified_metadata_imports_if_required}}

{{verified_route_annotation_if_required}}
class {{PascalCaseFeature}}Screen extends BaseScreen {
  const {{PascalCaseFeature}}Screen({super.key});

  {{verified_create_state_override}}
  {{verified_screen_metadata_override}}
}

class _{{PascalCaseFeature}}ScreenState extends BaseScreenState<{{PascalCaseFeature}}Screen> {
  // Supply the layout override required by the resolved BaseScreenState.
  // Keep BlocBuilder for rendering and BlocListener for side effects when
  // this screen has a Cubit. Follow the real router and DI conventions.
  {{verified_layout_override_and_screen_body}}
}
