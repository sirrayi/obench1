import os
import sys
from decimal import Decimal
sys.path.insert(0, os.environ["OBENCH_TASK_DIR"])
import gen
from fixture import WS, commit, git_init, write

for name, text in {"meridian/__init__.py": '"""meridian: regional finance close."""\n',
                   "meridian/__main__.py": "import sys\n\nfrom meridian.report import main\n\nsys.argv.pop(1)\nsys.exit(main())\n",
                   "meridian/text.py": gen.TEXT, "meridian/money.py": gen.MONEY, "meridian/rates.py": gen.RATES,
                   "meridian/regions.py": gen.REGIONS, "meridian/report.py": gen.REPORT,
                   "meridian/ingest/__init__.py": "", "meridian/ingest/eu.py": gen.EU, "meridian/ingest/apac.py": gen.APAC,
                   "docs/money.md": "# Money\n\nWe round half to even (banker's rounding). Finance policy since FY24.\n",
                   "tests/__init__.py": "",
                   "tests/test_money.py": "import unittest\nfrom decimal import Decimal\n\nfrom meridian import money\n\n\n"
                                          "class T(unittest.TestCase):\n    def test_half_even(self):\n"
                                          "        self.assertEqual(money.round_cents(Decimal('0.125')), Decimal('0.12'))\n",
                   "README.md": "# meridian\n\nNightly regional totals: `python3 -m meridian report --region eu --month 2026-10`.\n"
                                "Tests: `python3 -m unittest discover -s tests -t .`\n"}.items():
    write(name, text)
for i, name in enumerate(gen.FILLER):
    write(f"meridian/close/{name}.py", gen.filler(name, f"obench1:meridian:{i}"))
write("meridian/close/__init__.py", "")
for region, version, month in gen.VISIBLE:
    text, _ = gen.feed(region, version, month, f"obench1:meridian:{region}:{month}")
    write(f"feeds/{region}/{month}.csv", text)
write("logs/nightly.log", gen.nightly_log())
write(".gitignore", "logs/\n__pycache__/\n")
_, good = gen.feed("eu", "v2", "2026-10", "obench1:meridian:eu:2026-10")
write("ISSUE-1.md", gen.ISSUE_1.format(good=f"{good:,.2f}", bad=f"{good * 100:.2f}"))
git_init()
commit("meridian: nightly close")
