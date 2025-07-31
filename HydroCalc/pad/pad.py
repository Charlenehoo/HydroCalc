# HydroCalc/pad/pad.py

from dataclasses import dataclass
from typing import Optional, Tuple
from abc import ABC, abstractmethod
from unit import ureg, qty


class Pad(ABC):

    @abstractmethod
    @property
    def flow_rate_coefficient(self) -> qty:
        pass

    @abstractmethod
    @property
    def effective_area(self) -> qty:
        pass
