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
