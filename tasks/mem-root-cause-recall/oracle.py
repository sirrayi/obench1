# OBENCH1-CANARY-3be81f02c6
import subprocess
import sys
from checks import WS

ph = int(sys.argv[sys.argv.index("--phase") + 1])
DETECT = '''

def feed_format(lines):
    """Return the format a feed declares in its `# format:` header (v1 if it declares none)."""
    for line in lines:
        if line.startswith("# format:"):
            return line.split(":", 1)[1].strip()
    return "v1"
'''


def sub(path, old, new):
    p = WS / path
    s = p.read_text()
    assert old in s, (path, old)
    p.write_text(s.replace(old, new, 1))


if ph == 1:
    sub("meridian/text.py", '''def clean_number(raw):
    """Turn a feed amount into a plain decimal string ("1.234,56" -> "1234.56")."""
    return raw.strip().replace(".", "").replace(",", ".")''', '''def clean_number(raw, version="v1"):
    """Turn a feed amount into a plain decimal string: v1 is "1.234,56", v2 is already "1234.56"."""
    if version == "v2":
        return raw.strip()
    return raw.strip().replace(".", "").replace(",", ".")''')
    (WS / "meridian/text.py").write_text((WS / "meridian/text.py").read_text() + DETECT)
    sub("meridian/ingest/eu.py", '''        lines = [x for x in f.read().splitlines() if x and not x.startswith("#")]
''', '''        raw = f.read().splitlines()
    version = text.feed_format(raw)
    lines = [x for x in raw if x and not x.startswith("#")]
''')
    sub("meridian/ingest/eu.py", "text.clean_number(amount)", "text.clean_number(amount, version)")
    (WS / "tests/test_ingest_eu.py").write_text('''import os
import tempfile
import unittest
from decimal import Decimal

from meridian.ingest import eu


class T(unittest.TestCase):
    def test_both_formats(self):
        with tempfile.TemporaryDirectory() as d:
            for version, amount in (("v1", "1.234,56"), ("v2", "1234.56")):
                p = os.path.join(d, version + ".csv")
                with open(p, "w") as f:
                    f.write("# format: %s\\ndate;account;amount\\n2026-10-01;AC-1;%s\\n" % (version, amount))
                self.assertEqual(eu.read_feed(p)[0]["amount"], Decimal("1234.56"))
''')
    msg = "ingest: honour the feed's declared number format in the EU reader"
else:
    sub("meridian/ingest/apac.py", '"""Reader for the APAC ledger export (pipe-separated)."""\nfrom decimal import Decimal\n',
        '"""Reader for the APAC ledger export (pipe-separated)."""\nfrom decimal import Decimal\n\nfrom meridian import text\n')
    sub("meridian/ingest/apac.py", '''def _strip_grouping(raw):
    # APAC exports group thousands with spaces and use a decimal comma: "1 234,56"
    return raw.strip().replace(" ", "").replace(".", "").replace(",", ".")''', '''def _strip_grouping(raw, version="v1"):
    # v1 groups thousands with spaces and uses a decimal comma ("1 234,56"); v2 is plain "1234.56"
    if version == "v2":
        return raw.strip()
    return raw.strip().replace(" ", "").replace(".", "").replace(",", ".")''')
    sub("meridian/ingest/apac.py", '''    out = []
    with open(path, encoding="utf-8") as f:
        for line in f:''', '''    out = []
    with open(path, encoding="utf-8") as f:
        raw = f.read().splitlines()
    version = text.feed_format(raw)
    if True:
        for line in raw:''')
    sub("meridian/ingest/apac.py", "_strip_grouping(amount)", "_strip_grouping(amount, version)")
    (WS / "tests/test_ingest_apac.py").write_text('''import os
import tempfile
import unittest
from decimal import Decimal

from meridian.ingest import apac


class T(unittest.TestCase):
    def test_both_formats(self):
        with tempfile.TemporaryDirectory() as d:
            for version, amount in (("v1", "1 234,56"), ("v2", "1234.56")):
                p = os.path.join(d, version + ".csv")
                with open(p, "w") as f:
                    f.write("# format: %s\\ndate|account|amount\\n2026-10-01|AC-1|%s\\n" % (version, amount))
                self.assertEqual(apac.load(p)[0]["amount"], Decimal("1234.56"))
''')
    msg = "ingest: honour the feed's declared number format in the APAC reader"
subprocess.run(["git", "add", "-A", "meridian", "tests"], cwd=WS, check=True)
subprocess.run(["git", "commit", "-q", "-m", msg], cwd=WS, check=True)
