# [0.1.4] - 2025-08-27

## Added
- `Array` class
- `TopText` class
- `CodeBlock` class
- `TitleTop` class

---

# [0.1.5] - 2025-09-07

## Added
- `CodeBlock`: line background highlighting

---

# [0.1.6] - 2025-09-11

## Fixed
- Typing for all vectors
- Tests

## Added
- `mob_center` param for all classes

---

# [0.2.0] - 2025-10-05

## Added
- `TitleText` class
- `TitleLogo` class

## Changed
- All font defaults -> "" (Manim standard)
- Most colors defaults -> "WHITE"

## Refactored
- `TopText` -> `RelativeText`

---

# [0.2.1] - 2025-10-12

## Added
- `String` class
- `RelativeText` class (the old one was renamed)
- `square_scale()` function

## Changed
- `RelativeText`: add `align_edge` param
- `CodeBlock`: add `pre_code_lines` param

## Refactored
- `RelativeText` -> `RelativeTextValue`
- `{i,j,k}_color` -> `color_{1,2,3}`
- `{ij,ik,jk}_color` -> `color_{12,13,23}`
- `pointers_{1,2,3}()` -> `pointers()`
- `highlight_blocks_{1,2,3}()` -> `highlight_blocks()`
- `pointer_special()` -> `pointer_on_value()`

## Removed
- `tests/` directory

---

# [0.2.2] - 2025-10-22

## Added
- `utils.py` module

## Changed
- {`Array`, `String`}: unified scaling via `font_size`, removed `square_size` param
- {`Array`, `String`}: support dynamic length changes in `update_value()`

## Refactored
- `Array`: `update_numbers()` -> `update_value()`
- `String`: `update_numbers()` -> `update_value()`

## Removed
- `square_scale()` function

---

# [0.2.3] - 2025-11-03

## Added
- `algomanim/examples/` directory with rendering scripts and usage documentation
- `algomanim/utils.py`: `create_pointers()`, `get_cell_params()`, `get_cell_width()`
- `algomanim/svg/` directory for vector assets
- `algomanim/datastructures.py` with LeetCode data structure definitions

## Changed
- `Array`: dynamic cell width calculation for multi-character values
- {`Array`, `String`}: `_update_internal_state()` now preserves highlight colors
- {`Array`, `String`}: added support for empty arrays/strings
- {`Array`, `String`}: automatic cell parameter calculation for precise text alignment
- {`Array`, `String`}: character-specific vertical alignment in cells

## Refactored
- {`Array`, `String`}: `highlight_blocks()` → `highlight_cells()`
- {`Array`, `String`}: `highlight_blocks_with_value()` → `highlight_cells_with_value()`

## Fixed
- `String`: {`update_value()`, `_update_internal_state()`}: left_aligned issues
