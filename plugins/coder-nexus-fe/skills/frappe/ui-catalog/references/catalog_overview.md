# Frappe UI Component Reference

| Component | Category | Common Props | Example Usage |
| :--- | :--- | :--- | :--- |
| `Button` | Action | `variant` ('solid', 'subtle', 'outline', 'ghost'), `theme` ('gray', 'blue', 'green', 'red'), `size` ('sm', 'md', 'lg'), `loading` | `<Button variant="solid" theme="blue" :loading="saving">Save</Button>` |
| `Dialog` | Overlay | `v-model`, `title`, `size` ('sm', 'md', 'lg', 'xl') | `<Dialog v-model="isOpen" title="Confirm Delete">...</Dialog>` |
| `FormControl` | Form | `label`, `type` ('text', 'select', 'date'), `description`, `required`, `errorMessage` | `<FormControl v-model="name" label="Full Name" required />` |
| `ListView` | Display | `columns`, `rows`, `options` | `<ListView :columns="columns" :rows="data" />` |
| `Badge` | Display | `theme`, `size`, `label` | `<Badge theme="green" label="Active" />` |
| `FeatherIcon` | Icon | `name`, `class` | `<FeatherIcon name="search" class="w-4 h-4" />` |
