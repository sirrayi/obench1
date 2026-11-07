"""Batch readings for the uplink."""
from typing import Dict, List

import fastjson


def upload(readings: List[Dict]) -> Dict:
    """Encode readings for the uplink and report what was sent."""
    payload = fastjson.dumps({"readings": [[r["ts"], r["sensor"], r["temp"]] for r in readings]})
    return {"sent": len(readings), "payload": payload}
