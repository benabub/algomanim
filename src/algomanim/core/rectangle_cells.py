from abc import ABC

import manim as mn

from .linear_container import LinearContainerStructure


class RectangleCellsStructure(LinearContainerStructure, ABC):
    """
    ...
    """

    def __init__(self):
        super().__init__()
        self._cell_params_auto = True
        self._cell_height = 0.65625
        self._top_bottom_buff = 0.15
        self._top_buff = 0.09
        self._bottom_buff = 0.16
        self._deep_bottom_buff = 0.05

    def _get_cell_params(
        self,
        font_size: float,
        font: str,
        weight: str,
        test_sign: str = "0",
    ) -> dict:
        """Calculate comprehensive cell layout parameters.

        Args:
            font_size: Font size for text measurement.
            font: Font family name.
            weight: Font weight (NORMAL, BOLD, etc.).
            test_sign: Character used for measurement (default "0").

        Returns:
            Dictionary containing:
            - top_bottom_buff: Internal top/bottom padding
            - cell_height: Total cell height
            - top_buff: Top alignment buffer
            - bottom_buff: Standard bottom alignment buffer
            - deep_bottom_buff: Deep bottom alignment buffer
        """
        zero_mob = mn.Text(test_sign, font=font, font_size=font_size, weight=weight)

        zero_mob_height = zero_mob.height  # 0.35625

        top_bottom_buff = zero_mob_height / 2.375
        cell_height = top_bottom_buff * 2 + zero_mob_height
        top_buff = zero_mob_height / 3.958
        bottom_buff = zero_mob_height / 35.625 + top_bottom_buff
        deep_bottom_buff = zero_mob_height / 7.125

        return {
            "top_bottom_buff": top_bottom_buff,
            "cell_height": cell_height,
            "top_buff": top_buff,
            "bottom_buff": bottom_buff,
            "deep_bottom_buff": deep_bottom_buff,
        }

    def _get_cell_width(
        self,
        text_mob: mn.Mobject,
        inter_buff: float,
        cell_height: float,
    ) -> float:
        """Calculate cell width based on text content and constraints.

        Args:
            text_mob: Text mobject to measure.
            inter_buff: Internal padding within cells.
            cell_height: Pre-calculated cell height.

        Returns:
            Cell width, ensuring it's at least as tall as the cell height
            for consistent visual proportions.
        """
        text_mob_height = text_mob.width
        res = inter_buff * 2.5 + text_mob_height
        if cell_height >= res:
            return cell_height
        else:
            return res

    def _cell_params(
        self,
        cell_params_auto,
        font_size,
        font,
        weight,
        cell_height,
        top_bottom_buff,
        top_buff,
        bottom_buff,
        deep_bottom_buff,
    ):
        if cell_params_auto:
            cell_params = self._get_cell_params(font_size, font, weight)
            self._cell_height = cell_params["cell_height"]
            self._top_bottom_buff = cell_params["top_bottom_buff"]
            self._top_buff = cell_params["top_buff"]
            self._bottom_buff = cell_params["bottom_buff"]
            self._deep_bottom_buff = cell_params["deep_bottom_buff"]
        else:
            self._cell_height = cell_height
            self._top_bottom_buff = top_bottom_buff
            self._top_buff = top_buff
            self._bottom_buff = bottom_buff
            self._deep_bottom_buff = deep_bottom_buff
