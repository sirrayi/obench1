# OBENCH1-CANARY-3be81f02c6
import json
import sys
from checks import WS, Grader, run

g = Grader()
PROBE = r'''
import json, math, sys
sys.path.insert(0, sys.argv[1])
from units import convert
def near(a, b): return math.isclose(a, b, rel_tol=1e-9, abs_tol=1e-9)
def ok(v, s, d, want):
    try: return near(convert(v, s, d), want)
    except Exception: return False
def err(v, s, d):
    try: convert(v, s, d)
    except ValueError: return True
    except Exception: return False
    return False
r = {
 "length": all([ok(1, "mi", "km", 1.609344), ok(12, "in", "ft", 1.0), ok(250, "cm", "in", 250 * 0.01 / 0.0254), ok(3, "ft", "m", 0.9144), ok(5, "km", "mi", 5000 / 1609.344), ok(1, "m", "m", 1)]),
 "mass": all([ok(1, "lb", "oz", 16), ok(1, "kg", "lb", 1 / 0.45359237), ok(500, "g", "kg", 0.5), ok(8, "oz", "g", 8 * 0.45359237 / 16 * 1000)]),
 "temperature": all([ok(-40, "C", "F", -40), ok(0, "K", "C", -273.15), ok(98.6, "F", "C", 37), ok(300, "K", "F", 300 * 9 / 5 - 459.67), ok(20, "C", "K", 293.15)]),
 "errors": all([err(1, "kg", "m"), err(1, "KM", "m"), err(1, "furlong", "m"), err(1, "C", "kg"), err(-1, "K", "C"), err(-500, "F", "C")]),
}
print(json.dumps(r))
'''
code, out = run([sys.executable, "-I", "-c", PROBE, str(WS)], timeout=60)
try:
    r = json.loads(out.strip().splitlines()[-1])
except (ValueError, IndexError):
    r = {}
g.check("length conversions", r.get("length") is True, 1)
g.check("mass conversions", r.get("mass") is True, 1)
g.check("temperature (affine, not just a factor)", r.get("temperature") is True, 1.5)
g.check("cross-dimension, unknown, wrong-case and below-absolute-zero raise ValueError", r.get("errors") is True, 1)
cli = True
for args, want in ((["10", "km", "mi"], "6.21371"), (["212", "F", "C"], "100"), (["1", "oz", "g"], "28.3495")):
    c, o = run([sys.executable, "-m", "units", *args], timeout=30)
    cli = cli and c == 0 and o.strip() == want
c, o = run([sys.executable, "-m", "units", "1", "kg", "m"], timeout=30)
cli = cli and c == 2
g.check("the CLI: %.6g on stdout, errors exit 2", cli, 1, o[-120:], cat="instructions")
c, o = run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-t", "."], timeout=60)
g.check("the existing tests pass", c == 0 and bool(r.get("length")), 0.5, o[-120:])
g.done()
