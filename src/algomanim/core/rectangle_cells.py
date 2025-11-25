from abc import ABC

import manim as mn

from .linear_container import LinearContainerStructure


class RectangleCellsStructure(LinearContainerStructure, ABC):
    """
    ...
    """

    DEFAULT_CELL_HEIGHT = 0.65625
    DEFAULT_TOP_BOTTOM_BUFF = 0.15
    DEFAULT_TOP_BUFF = 0.09
    DEFAULT_BOTTOM_BUFF = 0.16
    DEFAULT_DEEP_BOTTOM_BUFF = 0.05

    TOP_BOTTOM_BUFF_DIV = 2.375
    TOP_BUFF_DIV = 3.958
    BOTTOM_BUFF_DIV = 35.625
    DEEP_BOTTOM_BUFF_DIV = 7.125

    INTER_BUFF_FACTOR = 2.5

    def __init__(
        self,
        cell_params_auto=True,
        cell_height=DEFAULT_CELL_HEIGHT,
        top_bottom_buff=DEFAULT_TOP_BOTTOM_BUFF,
        top_buff=DEFAULT_TOP_BUFF,
        bottom_buff=DEFAULT_BOTTOM_BUFF,
        deep_bottom_buff=DEFAULT_DEEP_BOTTOM_BUFF,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self._cell_params_auto = cell_params_auto
        self._cell_height = cell_height
        self._top_bottom_buff = top_bottom_buff
        self._top_buff = top_buff
        self._bottom_buff = bottom_buff
        self._deep_bottom_buff = deep_bottom_buff

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

        zero_mob_height = zero_mob.height

        top_bottom_buff = zero_mob_height / self.TOP_BOTTOM_BUFF_DIV
        cell_height = top_bottom_buff * 2 + zero_mob_height
        top_buff = zero_mob_height / self.TOP_BUFF_DIV
        bottom_buff = zero_mob_height / self.BOTTOM_BUFF_DIV + top_bottom_buff
        deep_bottom_buff = zero_mob_height / self.DEEP_BOTTOM_BUFF_DIV

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
        res = inter_buff * self.INTER_BUFF_FACTOR + text_mob_height
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
