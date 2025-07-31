# HydroCalc/pad/rectangular.py

from dataclasses import dataclass
from typing import Optional, Tuple
from abc import ABC, abstractmethod
from unit import ureg, qty


@dataclass(frozen=True)
class DimensionGroup:
    pad: qty
    slot: qty
    edge: qty

    @property
    def values(self) -> Tuple[qty, qty, qty]:
        return self.pad, self.slot, self.edge


class RectangularPad(Pad):
    def __init__(
        self,
        pad_length: Optional[qty] = None,
        slot_length: Optional[qty] = None,
        edge_length: Optional[qty] = None,
        pad_width: Optional[qty] = None,
        slot_width: Optional[qty] = None,
        edge_width: Optional[qty] = None,
    ):
        self._set_length_group(pad_length, slot_length, edge_length)
        self._set_width_group(pad_width, slot_width, edge_width)

    def _set_length_group(
        self,
        pad_length: Optional[qty] = None,
        slot_length: Optional[qty] = None,
        edge_length: Optional[qty] = None,
    ) -> None:
        self.length_group = self._derive_group(
            "LengthGroup", pad_length, slot_length, edge_length
        )

    def _set_width_group(
        self,
        pad_width: Optional[qty] = None,
        slot_width: Optional[qty] = None,
        edge_width: Optional[qty] = None,
    ) -> None:
        self.width_group = self._derive_group(
            "WidthGroup", pad_width, slot_width, edge_width
        )

    def update_length_group(
        self,
        *,
        pad_length: Optional[qty] = None,
        slot_length: Optional[qty] = None,
        edge_length: Optional[qty] = None,
    ) -> None:
        self._set_length_group(pad_length, slot_length, edge_length)

    def update_width_group(
        self,
        *,
        pad_width: Optional[qty] = None,
        slot_width: Optional[qty] = None,
        edge_width: Optional[qty] = None,
    ) -> None:
        self._set_width_group(pad_width, slot_width, edge_width)

    @staticmethod
    def _derive_group(
        name: str,
        pad: Optional[qty],
        slot: Optional[qty],
        edge: Optional[qty],
    ) -> DimensionGroup:
        known = [pad is not None, slot is not None, edge is not None]
        known_count = known.count(True)

        if known_count < 2:
            raise ValueError(
                f"At least two of {name} (pad, slot, edge) must be provided"
            )

        if known_count == 3:
            expected_pad = slot + 2 * edge
            if not RectangularPad._is_close(pad, expected_pad):
                raise ValueError(
                    f"Over-constrained {name}: pad={pad}, expected {expected_pad} (slot + 2 * edge)"
                )
            return DimensionGroup(pad, slot, edge)

        if pad is None:
            pad = slot + 2 * edge
        elif slot is None:
            slot = pad - 2 * edge
        elif edge is None:
            edge = (pad - slot) / 2

        return DimensionGroup(pad, slot, edge)

    @staticmethod
    def _is_close(a: qty, b: qty, rel_tol: float = 1e-6) -> bool:
        return abs(
            a.to_base_units().magnitude - b.to_base_units().magnitude
        ) <= rel_tol * max(abs(a.magnitude), abs(b.magnitude))

    # --- Properties (Read Only) ---
    @property
    def pad_length(self) -> qty:
        return self.length_group.pad

    @property
    def slot_length(self) -> qty:
        return self.length_group.slot

    @property
    def edge_length(self) -> qty:
        return self.length_group.edge

    @property
    def pad_width(self) -> qty:
        return self.width_group.pad

    @property
    def slot_width(self) -> qty:
        return self.width_group.slot

    @property
    def edge_width(self) -> qty:
        return self.width_group.edge

    @property
    def flow_rate_coefficient(self) -> qty:
        # Placeholder
        return ureg.Quantity(1, "m^3/s")

    @property
    def effective_area(self) -> qty:
        return ureg.Quantity(
            self.pad_length.magnitude * self.pad_width.magnitude, "m^2"
        )
