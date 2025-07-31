# HydroCalc/main.py

from pad import Pad
from fluid import Fluid
from unit import ureg, qty


def main():
    weight = ureg("30 t")
    pad = Pad(
        type="Rectangular",
        pad_length=ureg("1 m"),
        pad_width=ureg("120 mm"),
        edge_length=ureg("30 mm"),
        edge_width=ureg("30 mm"),
    )

    fulid = Fluid("Mobil SHC 8051")

    flow_rate = pad.flow_rate_coefficient * h**3 * p / fulid.viscosity


if __name__ == "__main__":
    main()
