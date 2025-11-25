from abc import ABC

import manim as mn

from .linear_container import LinearContainerStructure


class RectangleCellsStructure(LinearContainerStructure, ABC):
    """Base class for rectangle cell structures with automatic cell parameter calculation.

    Args:
        cell_params_auto (bool): Whether to auto-calculate cell parameters.
        cell_height (float): Manual cell height when auto-calculation disabled.
        top_bottom_buff (float): Internal top/bottom padding within cells.
        top_buff (float): Top alignment buffer for specific characters.
        bottom_buff (float): Bottom alignment buffer for most characters.
        deep_bottom_buff (float): Deep bottom alignment for descending characters.
        **kwargs: Additional keyword arguments passed to parent class.
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
            font_size (float): Font size for text measurement.
            font (str): Font family name.
            weight (str): Font weight (NORMAL, BOLD, etc.).
            test_sign (str): Character used for measurement.

        Returns:
            dict: Dictionary containing cell layout parameters.
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
            text_mob (mn.Mobject): Text mobject to measure.
            inter_buff (float): Internal padding within cells.
            cell_height (float): Pre-calculated cell height.

        Returns:
            float: Cell width ensuring consistent visual proportions.
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
        """Set cell parameters either automatically or manually.

        Args:
            cell_params_auto (bool): Whether to auto-calculate parameters.
            font_size (float): Font size for auto-calculation.
            font (str): Font family for auto-calculation.
            weight (str): Font weight for auto-calculation.
            cell_height (float): Manual cell height.
            top_bottom_buff (float): Manual top/bottom buffer.
            top_buff (float): Manual top buffer.
            bottom_buff (float): Manual bottom buffer.
            deep_bottom_buff (float): Manual deep bottom buffer.
        """

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
