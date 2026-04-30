from dataclasses import dataclass
from abc import abstractmethod
from typing import TYPE_CHECKING

import manim as mn

from .linear_container import LinearContainerStructure

if TYPE_CHECKING:
    from algomanim.datastructures.string import String
    from algomanim.datastructures.array import Array


@dataclass(frozen=True)
class CellConfig:
    cell_height: float = 0.65625
    top_bottom_buff: float = 0.15
    top_buff: float = 0.09
    bottom_buff: float = 0.16
    deep_bottom_buff: float = 0.05
    top_bottom_buff_div: float = 2.375
    top_buff_div: float = 3.958
    bottom_buff_div: float = 35.625
    deep_bottom_buff_div: float = 7.125
    inter_buff_factor: float = 2.5


class RectangleCellsStructure(LinearContainerStructure):
    """Base class for rectangle cell structures with automatic cell parameter calculation.

    Warning:
        This is base class only, cannot be instantiated directly.

    Args:
        cell_params_auto (bool): Whether to auto-calculate cell parameters.
        cell_height (float): Manual cell height when auto-calculation disabled.
        top_bottom_buff (float): Internal top/bottom padding within cells.
        top_buff (float): Top alignment buffer for specific characters.
        bottom_buff (float): Bottom alignment buffer for most characters.
        deep_bottom_buff (float): Deep bottom alignment for descending characters.
        **kwargs: Additional keyword arguments passed to parent class.
    """

    CELL_CONFIG = CellConfig()

    def __init__(
        self,
        # ---- data ----
        data_len: int,
        # ---- frame ----
        frame_from: "Array | String |  None " = None,
        # ---- cell params ----
        cell_params_auto=True,
        cell_height=CELL_CONFIG.cell_height,
        top_bottom_buff=CELL_CONFIG.top_bottom_buff,
        top_buff=CELL_CONFIG.top_buff,
        bottom_buff=CELL_CONFIG.bottom_buff,
        deep_bottom_buff=CELL_CONFIG.deep_bottom_buff,
        **kwargs,
    ):
        if type(self) is RectangleCellsStructure:
            raise NotImplementedError(
                "RectangleCellsStructure is base class only, cannot be instantiated directly."
            )
        super().__init__(**kwargs)
        self._data_len = data_len
        self._frame_from = frame_from
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

        top_bottom_buff = zero_mob_height / self.CELL_CONFIG.top_bottom_buff_div
        cell_height = top_bottom_buff * 2 + zero_mob_height
        top_buff = zero_mob_height / self.CELL_CONFIG.top_buff_div
        bottom_buff = (
            zero_mob_height / self.CELL_CONFIG.bottom_buff_div + top_bottom_buff
        )
        deep_bottom_buff = zero_mob_height / self.CELL_CONFIG.deep_bottom_buff_div

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
        lock_width: bool,
    ) -> float:
        """Calculate cell width based on text content and constraints.

        Args:
            text_mob (mn.Mobject): Text mobject to measure.
            inter_buff (float): Internal padding within cells.
            cell_height (float): Pre-calculated cell height.

        Returns:
            float: Cell width ensuring consistent visual proportions.
        """
        if not lock_width:
            text_mob_height = text_mob.width
            res = inter_buff * self.CELL_CONFIG.inter_buff_factor + text_mob_height
            if cell_height >= res:
                return cell_height
            else:
                return res
        else:
            return cell_height

    @abstractmethod
    def _create_containers_mob(self) -> mn.VGroup:
        """Create container mobjects for cells. Must be implemented by child classes."""
        raise NotImplementedError

    def _import_frame(self) -> None:
        """Import container frames from another Array instance.

        Copies containers from frame_from, validates length, and applies
        current container and fill colors to all cells.
        """
        if self._frame_from:
            import_frame = self._frame_from._containers_mob.copy()

            if len(import_frame) != self._data_len:
                raise ValueError("Lenght of base Array for frame import is not equal")

            if import_frame[0].color != self._container_color:
                for cell in import_frame:
                    cell.color = self._container_color  # type: ignore

            if import_frame[0].fill_color != self._fill_color:
                for cell in import_frame:
                    cell.fill_color = self._fill_color  # type: ignore

            self._containers_mob = import_frame

    def _set_containers_mob(self) -> None:
        """Create or import container mobjects for data cells.

        If frame_from is provided, imports containers from another Array or String instance.
        Otherwise creates new containers. Adds to scene and applies positioning.
        """
        if self._frame_from:
            self._import_frame()
        else:
            self._containers_mob = self._create_containers_mob()

        self.add(self._containers_mob)
        self._position()
