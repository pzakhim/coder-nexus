# Frappe UI Specific Rules

1. **Component Architecture (Vue 3 Composition API)**:
   - All Frappe UI components must use Vue 3 `<script setup lang="ts">`.
   - Prefer single-file components (`.vue`) organized by domain/responsibility (`components/`, `pages/`, `dialogs/`).
   - Keep state reactive using `ref` and `computed`; never mutate props directly.

2. **Styling & Design System (Tailwind CSS)**:
   - Use Tailwind CSS utility classes exclusively. Avoid raw CSS stylesheets or arbitrary `style="..."` attributes.
   - Reuse Frappe UI standard design tokens (colors, borders, shadows, spacing) to maintain consistency with the Frappe Desk environment.

3. **Data Fetching & State (Frappe Resource Pattern)**:
   - Use Frappe UI's `createResource`, `createListResource`, or `createDocumentResource` for server communication.
   - Always handle all three resource states in the UI:
     - `resource.loading`: Render skeleton loaders or loading indicators.
     - `resource.data`: Render the successful content view.
     - `resource.error`: Render actionable error messages or retry buttons.

4. **Component Reuse First (Frappe UI Catalog)**:
   - Always reuse official Frappe UI components (`Button`, `Dialog`, `FormControl`, `ListView`, `Dropdown`, `FeatherIcon`) before inventing custom elements.
   - Missing or custom components must be documented as an explicit design decision.
