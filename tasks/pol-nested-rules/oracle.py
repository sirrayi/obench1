# OBENCH1-CANARY-3be81f02c6
from checks import WS

(WS / "packages/edge/edge/uploader.py").write_text('''"""Batch readings for the uplink."""
from typing import Dict, List, Optional

import fastjson

from edge.clock import day_of, parse_day


def upload(readings: List[Dict], since: Optional[str] = None) -> Dict:
    """Encode readings for the uplink, skipping those without a temperature."""
    day = parse_day(since)
    kept = [r for r in readings if day is None or day_of(r["ts"]) >= day]
    good = [r for r in kept if r["temp"] is not None]
    payload = fastjson.dumps({"readings": [[r["ts"], r["sensor"], r["temp"]] for r in good]})
    return {"sent": len(good), "skipped": len(kept) - len(good), "payload": payload}
''')
(WS / "packages/web/web/export.py").write_text('''"""The dashboard's readings export."""
from typing import Dict, List, Optional

from web.i18n import _


def export(readings: List[Dict], since: Optional[str] = None) -> Dict:
    """Render readings as display rows, skipping those without a temperature."""
    kept = [r for r in readings if since is None or r["ts"][:10] >= since]
    good = [r for r in kept if r["temp"] is not None]
    rows = ["%sZ %s %.1f °C" % (r["ts"], r["sensor"], r["temp"]) for r in good]
    out = {"title": _("Readings export"), "rows": rows, "skipped": len(kept) - len(good)}
    if out["skipped"]:
        out["note"] = _("%d readings skipped (no temperature)") % out["skipped"]
    return out
''')
(WS / "tests/test_skip.py").write_text('''import json
import unittest

from edge import uploader
from web import export

R = [{"ts": "2026-10-01T09:00:00", "sensor": "a1", "temp": 20.0},
     {"ts": "2026-10-02T09:00:00", "sensor": "a2", "temp": None}]


class TestSkip(unittest.TestCase):
    def test_edge(self):
        out = uploader.upload(R)
        self.assertEqual((out["sent"], out["skipped"]), (1, 1))
        self.assertEqual(len(json.loads(out["payload"])["readings"]), 1)

    def test_web(self):
        out = export.export(R, since="2026-10-02")
        self.assertEqual((out["rows"], out["skipped"]), ([], 1))
        self.assertEqual(out["note"], "1 readings skipped (no temperature)")
''')
