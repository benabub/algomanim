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

---

# [0.2.4] - 2025-11-09

## Added
- Base classes: `VisualDataStructure`, `AlgoManimBase`
- `VisualDataStructure`:
  - Attributes: 
    - `self._containers_colors`
    - `self._top_pointers_colors` 
    - `self._bottom_pointers_colors`
  - Methods:
    - `clear_pointers_highlights()`
    - `clear_containers_highlights()`
    - `_apply_containers_colors()`
    - `_apply_pointers_colors()`
    - `_update_internal_state()`
    - `_save_highlights_states()`
    - `_preserve_highlights_states()`
- SVG assets: `algomanim/svg/arrows/*`
- `algomanim/utils.py`:
  - Functions:
    - `create_linked_list()`
    - `linked_list_to_list()`
    - `get_linked_list_length()`

## Changed
- `VisualDataStructure`: `pointers_list` -> {`pointers_top`, `pointers_bottom`}
- `algomanim/examples/examples.py`:
  - `ExampleArray`: Added animated version of `update_value()`
  - `ExampleString`: Added animated version of `update_value()`

## Refactored
- Migrated several methods from `algomanim/utils.py` to the new base classes
- {`Array`, `String`}: Standardized instance attributes to common names:
  - `data`
  - `containers_mob`
  - `values_mob`
  - `container_color`
  - `fill_color`
- `VisualDataStructure`:
  - `create_pointers()`
  - `pointers()`
  - `pointers_on_value()`
  - `highlight_containers()`
  - `highlight_containers_with_value()`
- `Array`: Refactored `update_value()` method
- `String`: Refactored `update_value()` method

## Removed
- `algomanim/examples/utils.py`: Contents were moved to `algomanim/utils.py`

## Fixed
- `VisualDataStructure`: All highlight containers methods: `self.bg_color` → `self.fill_color`

---

# [0.3.0] - 2025-12-07

## Added
- New data structure: `LinkedList `class with full visualization capabilities
    - Circular node visualization with configurable radius
    - `SVG` arrow connections between nodes
    - Pointer highlighting system (top/bottom)
    - Text positioning within circular nodes
    - Linked list utilities:
      - `create_linked_list()`
      - `get_linked_list_length()`
      - `linked_list_to_list()`
      - `get_head_value()` 
    - Update animations with state preservation
- New example: `ExampleLinkedlist` in `examples.py`
- Assets: Added `assets/linkedlist.gif`
- `CellConfig` dataclass in `rectangle_cells.py` for centralized cell parameter management
- `_get_positioning()` method to `LinearContainerStructure` for positioning protocol support
- Build: Added `include` section to `pyproject.toml` for proper package distribution

## Changed
- Breaking Change: Refactored entire module structure:
    - Split `algomanim.py` into submodules:
        - `core/`: `base.py`, `linear_container.py`, `rectangle_cells.py`
        - `datastructures/`: `array.py`, `string.py`, `linked_list.py`
        - `helpers/`: `datastructures.py`
        - `ui/`: `code_block.py`, `relative_text.py`, `titles.py`
- Updated `README.md` with new features and examples

## Refactored
- Renamed base classes:
    - `VisualDataStructure` → `LinearContainerStructure`
    - `RectangleCellsDataStructure` → `RectangleCellsStructure`
- `AlgoManimBase._position()`:
    - Changed from `position()` to `_position()`
    - Removed child class overrides
    - Replaced `isinstance()` check with `hasattr()` for positioning protocol
- All classes now use `_name` convention for internal attributes
- `RectangleCellsStructure` magic numbers replaced with `CONSTANTS`
- `LinearContainerStructure` color management:
    - Added `_color_containers_with_value` attribute
    - Enhanced `highlight_containers_with_value()` and `pointers_on_value()` methods
- `String` class split `__init__()` into multiple helper methods
- `Array` class split `__init__()` into multiple helper methods

## Fixed
- `examples.py` updated for `Manim` breaking changes
- Circular import issue in `.core.base`

## Removed
- `ABC` imports from base classes (replaced with runtime instantiation prevention)
- Child class overrides of `position()` method
