"""chaos-provider-storm: an ordinary small job (a units converter and its
CLI) done while the provider misbehaves in every way the gateway knows:
background faults plus three storms of 429, 5xx, errors inside 200s, stalls,
cut and trickled streams, garbage. The work has to come out right anyway,
without thrashing."""

TASK = ("Finish the `units` package: implement `units.convert(value, src, dst)` for every unit in README.md, and the "
        "`python3 -m units <value> <src> <dst>` command it describes. The existing tests must pass.")
README = """# units

`convert(value, src, dst) -> float`. Units, by dimension:

| dimension | units |
|---|---|
| length | `m`, `km`, `cm`, `mi` (1609.344 m), `ft` (0.3048 m), `in` (0.0254 m) |
| mass | `kg`, `g`, `lb` (0.45359237 kg), `oz` (1/16 lb) |
| temperature | `C`, `F`, `K` |

Unit names are case-sensitive. Converting across dimensions, or an unknown unit, raises `ValueError`.
Temperatures below absolute zero raise `ValueError` too.

CLI: `python3 -m units 10 km mi` prints the result with `%.6g` and nothing else, e.g. `6.21371`. Errors go to stderr with exit status 2.
"""
FILES = {
    "README.md": README,
    "units/__init__.py": '"""Unit conversion, see README.md."""\n\n\ndef convert(value, src, dst):\n    raise NotImplementedError\n',
    "tests/__init__.py": "",
    "tests/test_units.py": '''import unittest

from units import convert


class TestUnits(unittest.TestCase):
    def test_km_to_m(self):
        self.assertAlmostEqual(convert(1.5, "km", "m"), 1500)

    def test_boiling(self):
        self.assertAlmostEqual(convert(100, "C", "F"), 212)
''',
}
REFERENCE = '''"""Unit conversion, see README.md."""
LINEAR = {
    "m": ("length", 1.0), "km": ("length", 1000.0), "cm": ("length", 0.01), "mi": ("length", 1609.344),
    "ft": ("length", 0.3048), "in": ("length", 0.0254),
    "kg": ("mass", 1.0), "g": ("mass", 0.001), "lb": ("mass", 0.45359237), "oz": ("mass", 0.45359237 / 16),
}
TEMP = {"C": (1.0, 273.15), "F": (5 / 9, 273.15 - 32 * 5 / 9), "K": (1.0, 0.0)}


def convert(value, src, dst):
    if src in TEMP and dst in TEMP:
        a, b = TEMP[src]
        k = value * a + b
        if k < 0:
            raise ValueError("below absolute zero")
        a, b = TEMP[dst]
        return (k - b) / a
    if src in LINEAR and dst in LINEAR and LINEAR[src][0] == LINEAR[dst][0]:
        return value * LINEAR[src][1] / LINEAR[dst][1]
    raise ValueError(f"can't convert {src} to {dst}")
'''
MAIN = '''import sys

from units import convert


def main(argv):
    try:
        value, src, dst = float(argv[0]), argv[1], argv[2]
        print("%.6g" % convert(value, src, dst))
    except (ValueError, IndexError) as e:
        print(f"units: {e}", file=sys.stderr)
        return 2
    return 0


sys.exit(main(sys.argv[1:]))
'''
