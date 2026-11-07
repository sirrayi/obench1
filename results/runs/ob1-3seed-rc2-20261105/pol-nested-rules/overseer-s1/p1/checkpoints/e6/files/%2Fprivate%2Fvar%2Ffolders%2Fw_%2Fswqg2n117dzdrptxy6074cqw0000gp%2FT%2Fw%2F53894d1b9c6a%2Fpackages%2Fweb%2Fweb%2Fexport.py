"""The dashboard's readings export."""
from typing import Dict, List

from web.i18n import _


def export(readings: List[Dict]) -> Dict:
    """Render readings as display rows."""
    rows = ["%sZ %s %.1f °C" % (r["ts"], r["sensor"], r["temp"]) for r in readings]
    return {"title": _("Readings export"), "rows": rows}
