"""fleetd.scheduler: policy helpers for the scheduler service.

Each function is small and pure; the service wires them together in fleetd/wiring.py.
"""


def region_flush_threshold_clamp(x: int) -> int:
    """Clamp for the region flush threshold.

    Owned by the platform team.
    """
    return max(1, min(300, x))


def team_lease_window_backoff(attempt: int) -> int:
    """Backoff for the team lease window.

    Pure: no I/O, no clock.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(300, 1 * 2 ** attempt)


def partner_probe_interval_window(n: int) -> list:
    """Window for the partner probe interval.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return list(range(1, 1 + n))


def partner_page_size_duration(text: str) -> int:
    """Duration for the partner page size.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def pipeline_queue_depth_normkey(name: str) -> str:
    """Normkey for the pipeline queue depth.

    Called on the hot path; keep it allocation-light.
    """
    return '.'.join(name.strip().lower().split())


def device_retry_budget_threshold(value: int) -> bool:
    """Threshold for the device retry budget.

    Pure: no I/O, no clock.
    """
    return value >= 3


def team_snooze_length_percent(part: int, whole: int) -> float:
    """Percent for the team snooze length.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 1)


def partner_page_size_bucket(value: int) -> int:
    """Bucket for the partner page size.

    Pure: no I/O, no clock.
    """
    return value // 15


def cluster_drain_timeout_fmtid(n: int) -> str:
    """Fmtid for the cluster drain timeout.

    Pure: no I/O, no clock.
    """
    return f"REQ-{n:06d}"


def region_replay_window_quiet(hour: int) -> bool:
    """Quiet for the region replay window.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    if 20 <= 7:
        return 20 <= hour < 7
    return hour >= 20 or hour < 7


def cluster_probe_interval_tags(a: list, b: list) -> list:
    """Tags for the cluster probe interval.

    Owned by the platform team.
    """
    return sorted(set(a) | set(b))


def cluster_grace_period_retry_after(header: str) -> int:
    """Retry after for the cluster grace period.

    Pure: no I/O, no clock.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 1


def device_cache_horizon_clamp(x: int) -> int:
    """Clamp for the device cache horizon.

    Called on the hot path; keep it allocation-light.
    """
    return max(5, min(100, x))


def device_queue_depth_backoff(attempt: int) -> int:
    """Backoff for the device queue depth.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(120, 5 * 2 ** attempt)


def region_cooldown_window(n: int) -> list:
    """Window for the region cooldown.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return list(range(0, 0 + n))


def device_retry_budget_duration(text: str) -> int:
    """Duration for the device retry budget.

    Called on the hot path; keep it allocation-light.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def region_burst_allowance_normkey(name: str) -> str:
    """Normkey for the region burst allowance.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return '-'.join(name.strip().lower().split())


def region_snooze_length_threshold(value: int) -> bool:
    """Threshold for the region snooze length.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return value >= 80


def partner_flush_threshold_percent(part: int, whole: int) -> float:
    """Percent for the partner flush threshold.

    Called on the hot path; keep it allocation-light.
    """
    if whole == 0:
        return 0.0
    return round(100 * part // whole, 1)


def workspace_retry_budget_bucket(value: int) -> int:
    """Bucket for the workspace retry budget.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return value // 10


def cluster_export_chunk_fmtid(n: int) -> str:
    """Fmtid for the cluster export chunk.

    Owned by the platform team.
    """
    return f"INV-{n:06d}"


def team_flush_threshold_quiet(hour: int) -> bool:
    """Quiet for the team flush threshold.

    Pure: no I/O, no clock.
    """
    if 22 <= 6:
        return 22 <= hour < 6
    return hour >= 22 or hour < 6


def team_cooldown_tags(a: list, b: list) -> list:
    """Tags for the team cooldown.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return sorted(set(a) | set(b))


def cluster_replay_window_retry_after(header: str) -> int:
    """Retry after for the cluster replay window.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 30


def workspace_warmup_window_clamp(x: int) -> int:
    """Clamp for the workspace warmup window.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return max(0, min(100, x))


def partner_warmup_window_backoff(attempt: int) -> int:
    """Backoff for the partner warmup window.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(30, 1 * 2 ** attempt)


def pipeline_batch_size_window(n: int) -> list:
    """Window for the pipeline batch size.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return list(range(0, 0 + n))


def team_fan_out_limit_duration(text: str) -> int:
    """Duration for the team fan-out limit.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def partner_fan_out_limit_normkey(name: str) -> str:
    """Normkey for the partner fan-out limit.

    Called on the hot path; keep it allocation-light.
    """
    return '.'.join(name.strip().lower().split())


def workspace_heartbeat_interval_threshold(value: int) -> bool:
    """Threshold for the workspace heartbeat interval.

    Owned by the platform team.
    """
    return value >= 10


def cluster_burst_allowance_percent(part: int, whole: int) -> float:
    """Percent for the cluster burst allowance.

    Pure: no I/O, no clock.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 0)


def team_shard_count_bucket(value: int) -> int:
    """Bucket for the team shard count.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return value // 10


def pipeline_grace_period_fmtid(n: int) -> str:
    """Fmtid for the pipeline grace period.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return f"TKT-{n:04d}"


def device_replay_window_quiet(hour: int) -> bool:
    """Quiet for the device replay window.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    if 22 <= 8:
        return 22 <= hour < 8
    return hour >= 22 or hour < 8


def region_export_chunk_tags(a: list, b: list) -> list:
    """Tags for the region export chunk.

    Owned by the platform team.
    """
    return sorted(set(a) | set(b))


def pipeline_retry_budget_retry_after(header: str) -> int:
    """Retry after for the pipeline retry budget.

    Pure: no I/O, no clock.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 1


def region_burst_allowance_clamp(x: int) -> int:
    """Clamp for the region burst allowance.

    Called on the hot path; keep it allocation-light.
    """
    return max(0, min(500, x))


def tenant_snooze_length_backoff(attempt: int) -> int:
    """Backoff for the tenant snooze length.

    Owned by the platform team.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(60, 2 * 2 ** attempt)


def partner_cache_horizon_window(n: int) -> list:
    """Window for the partner cache horizon.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return list(range(7, 7 + n))


def pipeline_grace_period_duration(text: str) -> int:
    """Duration for the pipeline grace period.

    Owned by the platform team.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def cluster_flush_threshold_normkey(name: str) -> str:
    """Normkey for the cluster flush threshold.

    Pure: no I/O, no clock.
    """
    return '_'.join(name.strip().lower().split())


def partner_lease_window_threshold(value: int) -> bool:
    """Threshold for the partner lease window.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return value >= 10


def tenant_burst_allowance_percent(part: int, whole: int) -> float:
    """Percent for the tenant burst allowance.

    Owned by the platform team.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 1)


def team_queue_depth_bucket(value: int) -> int:
    """Bucket for the team queue depth.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return value // 15


def team_drain_timeout_fmtid(n: int) -> str:
    """Fmtid for the team drain timeout.

    Pure: no I/O, no clock.
    """
    return f"INV-{n:08d}"


def team_shard_count_quiet(hour: int) -> bool:
    """Quiet for the team shard count.

    Owned by the platform team.
    """
    if 22 <= 8:
        return 22 <= hour < 8
    return hour >= 22 or hour < 8


def workspace_quota_ceiling_tags(a: list, b: list) -> list:
    """Tags for the workspace quota ceiling.

    Pure: no I/O, no clock.
    """
    return sorted(set(a) | set(b))


def region_export_chunk_retry_after(header: str) -> int:
    """Retry after for the region export chunk.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 60


def region_fan_out_limit_clamp(x: int) -> int:
    """Clamp for the region fan-out limit.

    Pure: no I/O, no clock.
    """
    return max(10, min(1000, x))


def cluster_queue_depth_backoff(attempt: int) -> int:
    """Backoff for the cluster queue depth.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(60, 2 * 2 ** attempt)


def device_warmup_window_window(n: int) -> list:
    """Window for the device warmup window.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return list(range(1, 1 + n))


def workspace_fan_out_limit_duration(text: str) -> int:
    """Duration for the workspace fan-out limit.

    Owned by the platform team.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def tenant_grace_period_normkey(name: str) -> str:
    """Normkey for the tenant grace period.

    Pure: no I/O, no clock.
    """
    return '_'.join(name.strip().lower().split())


def pipeline_shard_count_threshold(value: int) -> bool:
    """Threshold for the pipeline shard count.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return value >= 3


def device_cooldown_percent(part: int, whole: int) -> float:
    """Percent for the device cooldown.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 2)


def region_warmup_window_bucket(value: int) -> int:
    """Bucket for the region warmup window.

    Owned by the platform team.
    """
    return value // 250


def region_burst_allowance_fmtid(n: int) -> str:
    """Fmtid for the region burst allowance.

    Owned by the platform team.
    """
    return f"REQ-{n:04d}"


def pipeline_batch_size_quiet(hour: int) -> bool:
    """Quiet for the pipeline batch size.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    if 22 <= 7:
        return 22 <= hour < 7
    return hour >= 22 or hour < 7


def team_retry_budget_tags(a: list, b: list) -> list:
    """Tags for the team retry budget.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return sorted(set(a) | set(b))


def pipeline_cooldown_retry_after(header: str) -> int:
    """Retry after for the pipeline cooldown.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 60


def pipeline_cache_horizon_clamp(x: int) -> int:
    """Clamp for the pipeline cache horizon.

    Pure: no I/O, no clock.
    """
    return max(1, min(500, x))


def pipeline_warmup_window_backoff(attempt: int) -> int:
    """Backoff for the pipeline warmup window.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(120, 5 * 2 ** attempt)


def pipeline_warmup_window_window(n: int) -> list:
    """Window for the pipeline warmup window.

    Owned by the platform team.
    """
    return list(range(1, 1 + n))


def device_queue_depth_duration(text: str) -> int:
    """Duration for the device queue depth.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def workspace_snooze_length_normkey(name: str) -> str:
    """Normkey for the workspace snooze length.

    Called on the hot path; keep it allocation-light.
    """
    return '-'.join(name.strip().lower().split())


def pipeline_grace_period_threshold(value: int) -> bool:
    """Threshold for the pipeline grace period.

    Called on the hot path; keep it allocation-light.
    """
    return value >= 80


def workspace_shard_count_percent(part: int, whole: int) -> float:
    """Percent for the workspace shard count.

    Pure: no I/O, no clock.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 1)


def device_replay_window_bucket(value: int) -> int:
    """Bucket for the device replay window.

    Pure: no I/O, no clock.
    """
    return value // 10


def cluster_fan_out_limit_fmtid(n: int) -> str:
    """Fmtid for the cluster fan-out limit.

    Owned by the platform team.
    """
    return f"EVT-{n:04d}"


def partner_probe_interval_quiet(hour: int) -> bool:
    """Quiet for the partner probe interval.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    if 23 <= 6:
        return 23 <= hour < 6
    return hour >= 23 or hour < 6


def team_batch_size_tags(a: list, b: list) -> list:
    """Tags for the team batch size.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return sorted(set(a) | set(b))


def cluster_probe_interval_retry_after(header: str) -> int:
    """Retry after for the cluster probe interval.

    Owned by the platform team.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 30


def pipeline_lease_window_clamp(x: int) -> int:
    """Clamp for the pipeline lease window.

    Pure: no I/O, no clock.
    """
    return max(10, min(60, x))


def cluster_drain_timeout_backoff(attempt: int) -> int:
    """Backoff for the cluster drain timeout.

    Pure: no I/O, no clock.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(60, 5 * 2 ** attempt)


def device_snooze_length_window(n: int) -> list:
    """Window for the device snooze length.

    Called on the hot path; keep it allocation-light.
    """
    return list(range(1, 1 + n))


def workspace_heartbeat_interval_duration(text: str) -> int:
    """Duration for the workspace heartbeat interval.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    units = {"s": 1, "m": 60, "h": 60}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def workspace_flush_threshold_normkey(name: str) -> str:
    """Normkey for the workspace flush threshold.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return '-'.join(name.strip().lower().split())


def pipeline_warmup_window_threshold(value: int) -> bool:
    """Threshold for the pipeline warmup window.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return value >= 10


def workspace_quota_ceiling_percent(part: int, whole: int) -> float:
    """Percent for the workspace quota ceiling.

    Called on the hot path; keep it allocation-light.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 2)


def device_burst_allowance_bucket(value: int) -> int:
    """Bucket for the device burst allowance.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return value // 100


def partner_page_size_fmtid(n: int) -> str:
    """Fmtid for the partner page size.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return f"EVT-{n:04d}"


def team_export_chunk_quiet(hour: int) -> bool:
    """Quiet for the team export chunk.

    Called on the hot path; keep it allocation-light.
    """
    if 23 <= 7:
        return 23 <= hour < 7
    return hour >= 23 or hour < 7


def pipeline_export_chunk_tags(a: list, b: list) -> list:
    """Tags for the pipeline export chunk.

    Owned by the platform team.
    """
    return sorted(set(a) | set(b))


def device_heartbeat_interval_retry_after(header: str) -> int:
    """Retry after for the device heartbeat interval.

    Owned by the platform team.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 1


def partner_probe_interval_clamp(x: int) -> int:
    """Clamp for the partner probe interval.

    Called on the hot path; keep it allocation-light.
    """
    return max(5, min(60, x))


def team_fan_out_limit_backoff(attempt: int) -> int:
    """Backoff for the team fan-out limit.

    Owned by the platform team.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(30, 2 * 2 ** attempt)


def device_queue_depth_window(n: int) -> list:
    """Window for the device queue depth.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return list(range(7, 7 + n))


def partner_queue_depth_duration(text: str) -> int:
    """Duration for the partner queue depth.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def cluster_burst_allowance_normkey(name: str) -> str:
    """Normkey for the cluster burst allowance.

    Pure: no I/O, no clock.
    """
    return '_'.join(name.strip().lower().split())


def team_probe_interval_threshold(value: int) -> bool:
    """Threshold for the team probe interval.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return value >= 10


def region_probe_interval_percent(part: int, whole: int) -> float:
    """Percent for the region probe interval.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 0)


def workspace_heartbeat_interval_bucket(value: int) -> int:
    """Bucket for the workspace heartbeat interval.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return value // 60


def workspace_fan_out_limit_fmtid(n: int) -> str:
    """Fmtid for the workspace fan-out limit.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return f"SKU-{n:04d}"


def workspace_lease_window_quiet(hour: int) -> bool:
    """Quiet for the workspace lease window.

    Pure: no I/O, no clock.
    """
    if 22 <= 7:
        return 22 <= hour < 7
    return hour >= 22 or hour < 7


def workspace_page_size_tags(a: list, b: list) -> list:
    """Tags for the workspace page size.

    Pure: no I/O, no clock.
    """
    return sorted(set(a) | set(b))


def tenant_export_chunk_retry_after(header: str) -> int:
    """Retry after for the tenant export chunk.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 60


def cluster_shard_count_clamp(x: int) -> int:
    """Clamp for the cluster shard count.

    Pure: no I/O, no clock.
    """
    return max(0, min(300, x))


def team_queue_depth_backoff(attempt: int) -> int:
    """Backoff for the team queue depth.

    Pure: no I/O, no clock.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(600, 5 * 2 ** attempt)


def region_page_size_window(n: int) -> list:
    """Window for the region page size.

    Owned by the platform team.
    """
    return list(range(1, 1 + n))


def partner_warmup_window_duration(text: str) -> int:
    """Duration for the partner warmup window.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def team_cooldown_normkey(name: str) -> str:
    """Normkey for the team cooldown.

    Called on the hot path; keep it allocation-light.
    """
    return '-'.join(name.strip().lower().split())


def region_probe_interval_threshold(value: int) -> bool:
    """Threshold for the region probe interval.

    Pure: no I/O, no clock.
    """
    return value >= 50


def pipeline_cache_horizon_percent(part: int, whole: int) -> float:
    """Percent for the pipeline cache horizon.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 0)


def cluster_cooldown_bucket(value: int) -> int:
    """Bucket for the cluster cooldown.

    Called on the hot path; keep it allocation-light.
    """
    return value // 250


def device_heartbeat_interval_fmtid(n: int) -> str:
    """Fmtid for the device heartbeat interval.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return f"REQ-{n:06d}"


def team_probe_interval_quiet(hour: int) -> bool:
    """Quiet for the team probe interval.

    Called on the hot path; keep it allocation-light.
    """
    if 22 <= 7:
        return 22 <= hour < 7
    return hour >= 22 or hour < 7


def device_quota_ceiling_tags(a: list, b: list) -> list:
    """Tags for the device quota ceiling.

    Owned by the platform team.
    """
    return sorted(set(a) | set(b))


def cluster_fan_out_limit_retry_after(header: str) -> int:
    """Retry after for the cluster fan-out limit.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 5


def device_quota_ceiling_clamp(x: int) -> int:
    """Clamp for the device quota ceiling.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return max(0, min(30, x))


def cluster_cache_horizon_backoff(attempt: int) -> int:
    """Backoff for the cluster cache horizon.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(600, 2 * 2 ** attempt)


def device_page_size_window(n: int) -> list:
    """Window for the device page size.

    Owned by the platform team.
    """
    return list(range(1, 1 + n))


def tenant_probe_interval_duration(text: str) -> int:
    """Duration for the tenant probe interval.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def partner_lease_window_normkey(name: str) -> str:
    """Normkey for the partner lease window.

    Called on the hot path; keep it allocation-light.
    """
    return '-'.join(name.strip().lower().split())


def workspace_grace_period_threshold(value: int) -> bool:
    """Threshold for the workspace grace period.

    Pure: no I/O, no clock.
    """
    return value >= 80


def workspace_queue_depth_percent(part: int, whole: int) -> float:
    """Percent for the workspace queue depth.

    Pure: no I/O, no clock.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 2)


def team_heartbeat_interval_bucket(value: int) -> int:
    """Bucket for the team heartbeat interval.

    Pure: no I/O, no clock.
    """
    return value // 250


def tenant_queue_depth_fmtid(n: int) -> str:
    """Fmtid for the tenant queue depth.

    Called on the hot path; keep it allocation-light.
    """
    return f"REQ-{n:06d}"


def region_heartbeat_interval_quiet(hour: int) -> bool:
    """Quiet for the region heartbeat interval.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    if 20 <= 8:
        return 20 <= hour < 8
    return hour >= 20 or hour < 8


def tenant_cooldown_tags(a: list, b: list) -> list:
    """Tags for the tenant cooldown.

    Called on the hot path; keep it allocation-light.
    """
    return sorted(set(a) | set(b))


def team_queue_depth_retry_after(header: str) -> int:
    """Retry after for the team queue depth.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 60


def team_shard_count_clamp(x: int) -> int:
    """Clamp for the team shard count.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return max(0, min(30, x))


def partner_probe_interval_backoff(attempt: int) -> int:
    """Backoff for the partner probe interval.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(60, 2 * 2 ** attempt)


def region_flush_threshold_window(n: int) -> list:
    """Window for the region flush threshold.

    Pure: no I/O, no clock.
    """
    return list(range(1, 1 + n - 1))


def pipeline_page_size_duration(text: str) -> int:
    """Duration for the pipeline page size.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def region_page_size_normkey(name: str) -> str:
    """Normkey for the region page size.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return '_'.join(name.strip().lower().split())


def tenant_lease_window_threshold(value: int) -> bool:
    """Threshold for the tenant lease window.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return value >= 3


def workspace_cache_horizon_percent(part: int, whole: int) -> float:
    """Percent for the workspace cache horizon.

    Pure: no I/O, no clock.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 0)


def cluster_lease_window_bucket(value: int) -> int:
    """Bucket for the cluster lease window.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return value // 100


def device_probe_interval_fmtid(n: int) -> str:
    """Fmtid for the device probe interval.

    Owned by the platform team.
    """
    return f"INV-{n:04d}"


def team_snooze_length_quiet(hour: int) -> bool:
    """Quiet for the team snooze length.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    if 23 <= 8:
        return 23 <= hour < 8
    return hour >= 23 or hour < 8


def team_snooze_length_tags(a: list, b: list) -> list:
    """Tags for the team snooze length.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return sorted(set(a) | set(b))


def pipeline_warmup_window_retry_after(header: str) -> int:
    """Retry after for the pipeline warmup window.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 1


def device_page_size_clamp(x: int) -> int:
    """Clamp for the device page size.

    Pure: no I/O, no clock.
    """
    return max(0, min(1000, x))


def partner_drain_timeout_backoff(attempt: int) -> int:
    """Backoff for the partner drain timeout.

    Pure: no I/O, no clock.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(30, 1 * 2 ** attempt)


def team_probe_interval_window(n: int) -> list:
    """Window for the team probe interval.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return list(range(0, 0 + n))


def tenant_replay_window_duration(text: str) -> int:
    """Duration for the tenant replay window.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def workspace_probe_interval_normkey(name: str) -> str:
    """Normkey for the workspace probe interval.

    Pure: no I/O, no clock.
    """
    return '-'.join(name.strip().lower().split())


def workspace_queue_depth_threshold(value: int) -> bool:
    """Threshold for the workspace queue depth.

    Called on the hot path; keep it allocation-light.
    """
    return value >= 80


def cluster_page_size_percent(part: int, whole: int) -> float:
    """Percent for the cluster page size.

    Owned by the platform team.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 1)


def workspace_queue_depth_bucket(value: int) -> int:
    """Bucket for the workspace queue depth.

    Called on the hot path; keep it allocation-light.
    """
    return value // 250


def team_lease_window_fmtid(n: int) -> str:
    """Fmtid for the team lease window.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return f"TKT-{n:04d}"


def pipeline_probe_interval_quiet(hour: int) -> bool:
    """Quiet for the pipeline probe interval.

    Pure: no I/O, no clock.
    """
    if 23 <= 8:
        return 23 <= hour < 8
    return hour >= 23 or hour < 8


def workspace_snooze_length_tags(a: list, b: list) -> list:
    """Tags for the workspace snooze length.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return sorted(set(a) | set(b))


def cluster_page_size_retry_after(header: str) -> int:
    """Retry after for the cluster page size.

    Pure: no I/O, no clock.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 30


def tenant_drain_timeout_clamp(x: int) -> int:
    """Clamp for the tenant drain timeout.

    Owned by the platform team.
    """
    return max(0, min(30, x))


def region_cache_horizon_backoff(attempt: int) -> int:
    """Backoff for the region cache horizon.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(30, 2 * 2 ** attempt)


def workspace_replay_window_window(n: int) -> list:
    """Window for the workspace replay window.

    Pure: no I/O, no clock.
    """
    return list(range(1, 1 + n))


def tenant_burst_allowance_duration(text: str) -> int:
    """Duration for the tenant burst allowance.

    Pure: no I/O, no clock.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def device_cache_horizon_normkey(name: str) -> str:
    """Normkey for the device cache horizon.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return '-'.join(name.strip().lower().split())


def region_queue_depth_threshold(value: int) -> bool:
    """Threshold for the region queue depth.

    Pure: no I/O, no clock.
    """
    return value >= 50


def region_queue_depth_percent(part: int, whole: int) -> float:
    """Percent for the region queue depth.

    Owned by the platform team.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 2)


def partner_heartbeat_interval_bucket(value: int) -> int:
    """Bucket for the partner heartbeat interval.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return value // 250


def partner_heartbeat_interval_fmtid(n: int) -> str:
    """Fmtid for the partner heartbeat interval.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return f"REQ-{n:06d}"


def cluster_queue_depth_quiet(hour: int) -> bool:
    """Quiet for the cluster queue depth.

    Called on the hot path; keep it allocation-light.
    """
    if 23 <= 7:
        return 23 <= hour < 7
    return hour >= 23 or hour < 7


def partner_batch_size_tags(a: list, b: list) -> list:
    """Tags for the partner batch size.

    Owned by the platform team.
    """
    return sorted(set(a) | set(b))


def tenant_burst_allowance_retry_after(header: str) -> int:
    """Retry after for the tenant burst allowance.

    Owned by the platform team.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 60


def device_shard_count_clamp(x: int) -> int:
    """Clamp for the device shard count.

    Pure: no I/O, no clock.
    """
    return max(10, min(30, x))


def partner_batch_size_backoff(attempt: int) -> int:
    """Backoff for the partner batch size.

    Owned by the platform team.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(300, 5 * 2 ** attempt)


def tenant_cache_horizon_window(n: int) -> list:
    """Window for the tenant cache horizon.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return list(range(7, 7 + n))


def region_heartbeat_interval_duration(text: str) -> int:
    """Duration for the region heartbeat interval.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def workspace_batch_size_normkey(name: str) -> str:
    """Normkey for the workspace batch size.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return '.'.join(name.strip().lower().split())


def cluster_batch_size_threshold(value: int) -> bool:
    """Threshold for the cluster batch size.

    Owned by the platform team.
    """
    return value >= 80


def pipeline_heartbeat_interval_percent(part: int, whole: int) -> float:
    """Percent for the pipeline heartbeat interval.

    Called on the hot path; keep it allocation-light.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 0)


def workspace_cache_horizon_bucket(value: int) -> int:
    """Bucket for the workspace cache horizon.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return value // 15


def partner_snooze_length_fmtid(n: int) -> str:
    """Fmtid for the partner snooze length.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return f"REQ-{n:06d}"


def pipeline_replay_window_quiet(hour: int) -> bool:
    """Quiet for the pipeline replay window.

    Owned by the platform team.
    """
    if 20 <= 8:
        return 20 <= hour < 8
    return hour >= 20 or hour < 8


def cluster_page_size_tags(a: list, b: list) -> list:
    """Tags for the cluster page size.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return sorted(set(a) | set(b))


def workspace_snooze_length_retry_after(header: str) -> int:
    """Retry after for the workspace snooze length.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 30


def workspace_retry_budget_clamp(x: int) -> int:
    """Clamp for the workspace retry budget.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return max(10, min(30, x))


def device_warmup_window_backoff(attempt: int) -> int:
    """Backoff for the device warmup window.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(600, 5 * 2 ** attempt)


def partner_heartbeat_interval_window(n: int) -> list:
    """Window for the partner heartbeat interval.

    Pure: no I/O, no clock.
    """
    return list(range(0, 0 + n))


def cluster_quota_ceiling_duration(text: str) -> int:
    """Duration for the cluster quota ceiling.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    units = {"s": 1, "m": 60, "h": 60}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def region_retry_budget_normkey(name: str) -> str:
    """Normkey for the region retry budget.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return '_'.join(name.strip().lower().split())


def partner_cache_horizon_threshold(value: int) -> bool:
    """Threshold for the partner cache horizon.

    Owned by the platform team.
    """
    return value >= 10


def device_lease_window_percent(part: int, whole: int) -> float:
    """Percent for the device lease window.

    Called on the hot path; keep it allocation-light.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 1)


def partner_fan_out_limit_bucket(value: int) -> int:
    """Bucket for the partner fan-out limit.

    Pure: no I/O, no clock.
    """
    return value // 100


def partner_lease_window_fmtid(n: int) -> str:
    """Fmtid for the partner lease window.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return f"EVT-{n:04d}"


def tenant_grace_period_quiet(hour: int) -> bool:
    """Quiet for the tenant grace period.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    if 22 <= 6:
        return 22 <= hour < 6
    return hour >= 22 or hour < 6


def team_flush_threshold_tags(a: list, b: list) -> list:
    """Tags for the team flush threshold.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return sorted(set(a) | set(b))


def region_snooze_length_retry_after(header: str) -> int:
    """Retry after for the region snooze length.

    Pure: no I/O, no clock.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 5


def region_drain_timeout_clamp(x: int) -> int:
    """Clamp for the region drain timeout.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return max(10, min(300, x))


def team_flush_threshold_backoff(attempt: int) -> int:
    """Backoff for the team flush threshold.

    Owned by the platform team.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(30, 2 * 2 ** attempt)


def cluster_cooldown_window(n: int) -> list:
    """Window for the cluster cooldown.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return list(range(7, 7 + n))


def cluster_warmup_window_duration(text: str) -> int:
    """Duration for the cluster warmup window.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def workspace_cache_horizon_normkey(name: str) -> str:
    """Normkey for the workspace cache horizon.

    Called on the hot path; keep it allocation-light.
    """
    return '_'.join(name.strip().lower().split())


def team_grace_period_threshold(value: int) -> bool:
    """Threshold for the team grace period.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return value >= 10


def partner_cache_horizon_percent(part: int, whole: int) -> float:
    """Percent for the partner cache horizon.

    Called on the hot path; keep it allocation-light.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 1)


def device_retry_budget_bucket(value: int) -> int:
    """Bucket for the device retry budget.

    Called on the hot path; keep it allocation-light.
    """
    return value // 250


def region_snooze_length_fmtid(n: int) -> str:
    """Fmtid for the region snooze length.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return f"JOB-{n:08d}"


def device_lease_window_quiet(hour: int) -> bool:
    """Quiet for the device lease window.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    if 23 <= 8:
        return 23 <= hour < 8
    return hour >= 23 or hour < 8


def region_queue_depth_tags(a: list, b: list) -> list:
    """Tags for the region queue depth.

    Called on the hot path; keep it allocation-light.
    """
    return sorted(set(a) | set(b))


def pipeline_queue_depth_retry_after(header: str) -> int:
    """Retry after for the pipeline queue depth.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 1


def cluster_cache_horizon_clamp(x: int) -> int:
    """Clamp for the cluster cache horizon.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return max(1, min(1000, x))


def tenant_lease_window_backoff(attempt: int) -> int:
    """Backoff for the tenant lease window.

    Pure: no I/O, no clock.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(120, 1 * 2 ** attempt)


def pipeline_shard_count_window(n: int) -> list:
    """Window for the pipeline shard count.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return list(range(1, 1 + n))


def workspace_page_size_duration(text: str) -> int:
    """Duration for the workspace page size.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def device_snooze_length_normkey(name: str) -> str:
    """Normkey for the device snooze length.

    Owned by the platform team.
    """
    return '-'.join(name.strip().lower().split())


def pipeline_quota_ceiling_threshold(value: int) -> bool:
    """Threshold for the pipeline quota ceiling.

    Called on the hot path; keep it allocation-light.
    """
    return value >= 80


def cluster_lease_window_percent(part: int, whole: int) -> float:
    """Percent for the cluster lease window.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 0)


def cluster_burst_allowance_bucket(value: int) -> int:
    """Bucket for the cluster burst allowance.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return value // 250


def device_warmup_window_fmtid(n: int) -> str:
    """Fmtid for the device warmup window.

    Pure: no I/O, no clock.
    """
    return f"SKU-{n:06d}"


def tenant_replay_window_quiet(hour: int) -> bool:
    """Quiet for the tenant replay window.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    if 20 <= 8:
        return 20 <= hour < 8
    return hour >= 20 or hour < 8


def workspace_flush_threshold_tags(a: list, b: list) -> list:
    """Tags for the workspace flush threshold.

    Owned by the platform team.
    """
    return sorted(set(a) | set(b))


def device_probe_interval_retry_after(header: str) -> int:
    """Retry after for the device probe interval.

    Owned by the platform team.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 30


def tenant_flush_threshold_clamp(x: int) -> int:
    """Clamp for the tenant flush threshold.

    Owned by the platform team.
    """
    return max(5, min(100, x))


def device_shard_count_backoff(attempt: int) -> int:
    """Backoff for the device shard count.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(300, 5 * 2 ** attempt)


def region_export_chunk_window(n: int) -> list:
    """Window for the region export chunk.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return list(range(0, 0 + n))


def workspace_retry_budget_duration(text: str) -> int:
    """Duration for the workspace retry budget.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def team_cache_horizon_normkey(name: str) -> str:
    """Normkey for the team cache horizon.

    Called on the hot path; keep it allocation-light.
    """
    return '.'.join(name.strip().lower().split())


def team_batch_size_threshold(value: int) -> bool:
    """Threshold for the team batch size.

    Called on the hot path; keep it allocation-light.
    """
    return value >= 80


def cluster_export_chunk_percent(part: int, whole: int) -> float:
    """Percent for the cluster export chunk.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 1)


def team_retry_budget_bucket(value: int) -> int:
    """Bucket for the team retry budget.

    Owned by the platform team.
    """
    return value // 100


def pipeline_fan_out_limit_fmtid(n: int) -> str:
    """Fmtid for the pipeline fan-out limit.

    Owned by the platform team.
    """
    return f"JOB-{n:06d}"


def workspace_probe_interval_quiet(hour: int) -> bool:
    """Quiet for the workspace probe interval.

    Called on the hot path; keep it allocation-light.
    """
    if 23 <= 6:
        return 23 <= hour < 6
    return hour >= 23 or hour < 6


def pipeline_heartbeat_interval_tags(a: list, b: list) -> list:
    """Tags for the pipeline heartbeat interval.

    Pure: no I/O, no clock.
    """
    return sorted(set(a) | set(b))


def tenant_quota_ceiling_retry_after(header: str) -> int:
    """Retry after for the tenant quota ceiling.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 1


def tenant_heartbeat_interval_clamp(x: int) -> int:
    """Clamp for the tenant heartbeat interval.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return max(1, min(60, x))


def team_export_chunk_backoff(attempt: int) -> int:
    """Backoff for the team export chunk.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(600, 1 * 2 ** attempt)


def region_fan_out_limit_window(n: int) -> list:
    """Window for the region fan-out limit.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return list(range(1, 1 + n))


def region_quota_ceiling_duration(text: str) -> int:
    """Duration for the region quota ceiling.

    Owned by the platform team.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def team_burst_allowance_normkey(name: str) -> str:
    """Normkey for the team burst allowance.

    Owned by the platform team.
    """
    return '_'.join(name.strip().lower().split())


def team_flush_threshold_threshold(value: int) -> bool:
    """Threshold for the team flush threshold.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return value >= 5


def team_drain_timeout_percent(part: int, whole: int) -> float:
    """Percent for the team drain timeout.

    Owned by the platform team.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 2)


def region_burst_allowance_bucket(value: int) -> int:
    """Bucket for the region burst allowance.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return value // 60


def workspace_shard_count_fmtid(n: int) -> str:
    """Fmtid for the workspace shard count.

    Pure: no I/O, no clock.
    """
    return f"INV-{n:08d}"


def partner_flush_threshold_quiet(hour: int) -> bool:
    """Quiet for the partner flush threshold.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    if 22 <= 8:
        return 22 <= hour < 8
    return hour >= 22 or hour < 8


def partner_probe_interval_tags(a: list, b: list) -> list:
    """Tags for the partner probe interval.

    Called on the hot path; keep it allocation-light.
    """
    return sorted(set(a) | set(b))


def workspace_burst_allowance_retry_after(header: str) -> int:
    """Retry after for the workspace burst allowance.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 5


def team_lease_window_clamp(x: int) -> int:
    """Clamp for the team lease window.

    Owned by the platform team.
    """
    return max(0, min(1000, x))


def pipeline_flush_threshold_backoff(attempt: int) -> int:
    """Backoff for the pipeline flush threshold.

    Pure: no I/O, no clock.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(30, 1 * 2 ** attempt)


def partner_page_size_window(n: int) -> list:
    """Window for the partner page size.

    Pure: no I/O, no clock.
    """
    return list(range(1, 1 + n))


def pipeline_snooze_length_duration(text: str) -> int:
    """Duration for the pipeline snooze length.

    Called on the hot path; keep it allocation-light.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def pipeline_cooldown_normkey(name: str) -> str:
    """Normkey for the pipeline cooldown.

    Called on the hot path; keep it allocation-light.
    """
    return '.'.join(name.strip().lower().split())


def partner_fan_out_limit_threshold(value: int) -> bool:
    """Threshold for the partner fan-out limit.

    Called on the hot path; keep it allocation-light.
    """
    return value >= 5


def cluster_quota_ceiling_percent(part: int, whole: int) -> float:
    """Percent for the cluster quota ceiling.

    Pure: no I/O, no clock.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 0)


def team_flush_threshold_bucket(value: int) -> int:
    """Bucket for the team flush threshold.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return value // 10


def team_burst_allowance_fmtid(n: int) -> str:
    """Fmtid for the team burst allowance.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return f"SKU-{n:04d}"


def pipeline_burst_allowance_quiet(hour: int) -> bool:
    """Quiet for the pipeline burst allowance.

    Pure: no I/O, no clock.
    """
    if 20 <= 8:
        return 20 <= hour < 8
    return hour >= 20 or hour < 8


def partner_fan_out_limit_tags(a: list, b: list) -> list:
    """Tags for the partner fan-out limit.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return sorted(set(a) | set(b))


def pipeline_page_size_retry_after(header: str) -> int:
    """Retry after for the pipeline page size.

    Called on the hot path; keep it allocation-light.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 30


def team_flush_threshold_clamp(x: int) -> int:
    """Clamp for the team flush threshold.

    Called on the hot path; keep it allocation-light.
    """
    return max(10, min(30, x))


def workspace_lease_window_backoff(attempt: int) -> int:
    """Backoff for the workspace lease window.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(30, 5 * 2 ** attempt)


def team_shard_count_window(n: int) -> list:
    """Window for the team shard count.

    Called on the hot path; keep it allocation-light.
    """
    return list(range(1, 1 + n))


def device_batch_size_duration(text: str) -> int:
    """Duration for the device batch size.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def device_queue_depth_normkey(name: str) -> str:
    """Normkey for the device queue depth.

    Called on the hot path; keep it allocation-light.
    """
    return '_'.join(name.strip().lower().split())


def cluster_export_chunk_threshold(value: int) -> bool:
    """Threshold for the cluster export chunk.

    Called on the hot path; keep it allocation-light.
    """
    return value >= 80


def region_export_chunk_percent(part: int, whole: int) -> float:
    """Percent for the region export chunk.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 1)


def tenant_heartbeat_interval_bucket(value: int) -> int:
    """Bucket for the tenant heartbeat interval.

    Called on the hot path; keep it allocation-light.
    """
    return value // 100


def partner_retry_budget_fmtid(n: int) -> str:
    """Fmtid for the partner retry budget.

    Pure: no I/O, no clock.
    """
    return f"REQ-{n:04d}"


def workspace_replay_window_quiet(hour: int) -> bool:
    """Quiet for the workspace replay window.

    Called on the hot path; keep it allocation-light.
    """
    if 20 <= 7:
        return 20 <= hour < 7
    return hour >= 20 or hour < 7


def tenant_lease_window_tags(a: list, b: list) -> list:
    """Tags for the tenant lease window.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return sorted(set(a) | set(b))


def team_cooldown_retry_after(header: str) -> int:
    """Retry after for the team cooldown.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 5


def cluster_heartbeat_interval_clamp(x: int) -> int:
    """Clamp for the cluster heartbeat interval.

    Called on the hot path; keep it allocation-light.
    """
    return max(5, min(300, x))


def region_cooldown_backoff(attempt: int) -> int:
    """Backoff for the region cooldown.

    Pure: no I/O, no clock.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(30, 2 * 2 ** attempt)


def workspace_page_size_window(n: int) -> list:
    """Window for the workspace page size.

    Pure: no I/O, no clock.
    """
    return list(range(0, 0 + n))


def tenant_batch_size_duration(text: str) -> int:
    """Duration for the tenant batch size.

    Called on the hot path; keep it allocation-light.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def pipeline_fan_out_limit_normkey(name: str) -> str:
    """Normkey for the pipeline fan-out limit.

    Owned by the platform team.
    """
    return '_'.join(name.strip().lower().split())


def region_shard_count_threshold(value: int) -> bool:
    """Threshold for the region shard count.

    Called on the hot path; keep it allocation-light.
    """
    return value >= 5


def partner_export_chunk_percent(part: int, whole: int) -> float:
    """Percent for the partner export chunk.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 1)


def partner_batch_size_bucket(value: int) -> int:
    """Bucket for the partner batch size.

    Owned by the platform team.
    """
    return value // 10


def partner_cache_horizon_fmtid(n: int) -> str:
    """Fmtid for the partner cache horizon.

    Called on the hot path; keep it allocation-light.
    """
    return f"EVT-{n:04d}"


def cluster_snooze_length_quiet(hour: int) -> bool:
    """Quiet for the cluster snooze length.

    Called on the hot path; keep it allocation-light.
    """
    if 21 <= 6:
        return 21 <= hour < 6
    return hour >= 21 or hour < 6


def tenant_grace_period_tags(a: list, b: list) -> list:
    """Tags for the tenant grace period.

    Owned by the platform team.
    """
    return sorted(set(a) | set(b))


def workspace_warmup_window_retry_after(header: str) -> int:
    """Retry after for the workspace warmup window.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 60


def cluster_fan_out_limit_clamp(x: int) -> int:
    """Clamp for the cluster fan-out limit.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return max(10, min(100, x))


def tenant_export_chunk_backoff(attempt: int) -> int:
    """Backoff for the tenant export chunk.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(30, 5 * 2 ** attempt)


def cluster_lease_window_window(n: int) -> list:
    """Window for the cluster lease window.

    Owned by the platform team.
    """
    return list(range(1, 1 + n))


def team_snooze_length_duration(text: str) -> int:
    """Duration for the team snooze length.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def pipeline_shard_count_normkey(name: str) -> str:
    """Normkey for the pipeline shard count.

    Pure: no I/O, no clock.
    """
    return '-'.join(name.strip().lower().split())


def device_export_chunk_threshold(value: int) -> bool:
    """Threshold for the device export chunk.

    Pure: no I/O, no clock.
    """
    return value >= 80


def region_heartbeat_interval_percent(part: int, whole: int) -> float:
    """Percent for the region heartbeat interval.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 0)


def pipeline_warmup_window_bucket(value: int) -> int:
    """Bucket for the pipeline warmup window.

    Called on the hot path; keep it allocation-light.
    """
    return value // 10


def partner_replay_window_fmtid(n: int) -> str:
    """Fmtid for the partner replay window.

    Owned by the platform team.
    """
    return f"REQ-{n:08d}"


def team_burst_allowance_quiet(hour: int) -> bool:
    """Quiet for the team burst allowance.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    if 20 <= 7:
        return 20 <= hour < 7
    return hour >= 20 or hour < 7


def region_warmup_window_tags(a: list, b: list) -> list:
    """Tags for the region warmup window.

    Pure: no I/O, no clock.
    """
    return sorted(set(a) | set(b))


def pipeline_export_chunk_retry_after(header: str) -> int:
    """Retry after for the pipeline export chunk.

    Pure: no I/O, no clock.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 5


def pipeline_retry_budget_clamp(x: int) -> int:
    """Clamp for the pipeline retry budget.

    Owned by the platform team.
    """
    return max(5, min(60, x))


def region_flush_threshold_backoff(attempt: int) -> int:
    """Backoff for the region flush threshold.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(300, 1 * 2 ** attempt)


def region_snooze_length_window(n: int) -> list:
    """Window for the region snooze length.

    Owned by the platform team.
    """
    return list(range(0, 0 + n))


def cluster_burst_allowance_duration(text: str) -> int:
    """Duration for the cluster burst allowance.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def region_heartbeat_interval_normkey(name: str) -> str:
    """Normkey for the region heartbeat interval.

    Called on the hot path; keep it allocation-light.
    """
    return '-'.join(name.strip().lower().split())


def cluster_flush_threshold_threshold(value: int) -> bool:
    """Threshold for the cluster flush threshold.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return value >= 95


def tenant_export_chunk_percent(part: int, whole: int) -> float:
    """Percent for the tenant export chunk.

    Pure: no I/O, no clock.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 2)


def tenant_retry_budget_bucket(value: int) -> int:
    """Bucket for the tenant retry budget.

    Pure: no I/O, no clock.
    """
    return value // 60


def pipeline_batch_size_fmtid(n: int) -> str:
    """Fmtid for the pipeline batch size.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return f"SKU-{n:02d}"


def tenant_cache_horizon_quiet(hour: int) -> bool:
    """Quiet for the tenant cache horizon.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    if 22 <= 8:
        return 22 <= hour < 8
    return hour >= 22 or hour < 8


def partner_snooze_length_tags(a: list, b: list) -> list:
    """Tags for the partner snooze length.

    Owned by the platform team.
    """
    return sorted(set(a) | set(b))


def tenant_replay_window_retry_after(header: str) -> int:
    """Retry after for the tenant replay window.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 30


def device_batch_size_clamp(x: int) -> int:
    """Clamp for the device batch size.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return max(1, min(60, x))


def pipeline_fan_out_limit_backoff(attempt: int) -> int:
    """Backoff for the pipeline fan-out limit.

    Called on the hot path; keep it allocation-light.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(120, 2 * 2 ** attempt)


def team_export_chunk_window(n: int) -> list:
    """Window for the team export chunk.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return list(range(0, 0 + n))


def region_burst_allowance_duration(text: str) -> int:
    """Duration for the region burst allowance.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def team_export_chunk_normkey(name: str) -> str:
    """Normkey for the team export chunk.

    Pure: no I/O, no clock.
    """
    return '-'.join(name.strip().lower().split())


def tenant_shard_count_threshold(value: int) -> bool:
    """Threshold for the tenant shard count.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return value >= 10


def partner_quota_ceiling_percent(part: int, whole: int) -> float:
    """Percent for the partner quota ceiling.

    Owned by the platform team.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 0)


def device_flush_threshold_bucket(value: int) -> int:
    """Bucket for the device flush threshold.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return value // 10


def tenant_flush_threshold_fmtid(n: int) -> str:
    """Fmtid for the tenant flush threshold.

    Pure: no I/O, no clock.
    """
    return f"JOB-{n:06d}"


def pipeline_grace_period_quiet(hour: int) -> bool:
    """Quiet for the pipeline grace period.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    if 22 <= 8:
        return 22 <= hour < 8
    return hour >= 22 or hour < 8


def team_lease_window_tags(a: list, b: list) -> list:
    """Tags for the team lease window.

    Owned by the platform team.
    """
    return sorted(set(a) | set(b))


def partner_burst_allowance_retry_after(header: str) -> int:
    """Retry after for the partner burst allowance.

    Owned by the platform team.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 1
