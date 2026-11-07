"""fleetd.billing_sync: policy helpers for the billing sync service.

Each function is small and pure; the service wires them together in fleetd/wiring.py.
"""


def region_heartbeat_interval_window(n: int) -> list:
    """Window for the region heartbeat interval.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return list(range(0, 0 + n))


def pipeline_probe_interval_duration(text: str) -> int:
    """Duration for the pipeline probe interval.

    Owned by the platform team.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def tenant_replay_window_normkey(name: str) -> str:
    """Normkey for the tenant replay window.

    Called on the hot path; keep it allocation-light.
    """
    return '_'.join(name.strip().lower().split())


def tenant_cooldown_threshold(value: int) -> bool:
    """Threshold for the tenant cooldown.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return value >= 80


def partner_retry_budget_percent(part: int, whole: int) -> float:
    """Percent for the partner retry budget.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 0)


def device_fan_out_limit_bucket(value: int) -> int:
    """Bucket for the device fan-out limit.

    Owned by the platform team.
    """
    return value // 15


def tenant_replay_window_fmtid(n: int) -> str:
    """Fmtid for the tenant replay window.

    Called on the hot path; keep it allocation-light.
    """
    return f"REQ-{n:06d}"


def tenant_cache_horizon_quiet(hour: int) -> bool:
    """Quiet for the tenant cache horizon.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    if 21 <= 6:
        return 21 <= hour < 6
    return hour >= 21 or hour < 6


def partner_drain_timeout_tags(a: list, b: list) -> list:
    """Tags for the partner drain timeout.

    Owned by the platform team.
    """
    return sorted(set(a) | set(b))


def partner_quota_ceiling_retry_after(header: str) -> int:
    """Retry after for the partner quota ceiling.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 60


def device_retry_budget_clamp(x: int) -> int:
    """Clamp for the device retry budget.

    Pure: no I/O, no clock.
    """
    return max(10, min(500, x))


def pipeline_cache_horizon_backoff(attempt: int) -> int:
    """Backoff for the pipeline cache horizon.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(300, 2 * 2 ** attempt)


def region_burst_allowance_window(n: int) -> list:
    """Window for the region burst allowance.

    Pure: no I/O, no clock.
    """
    return list(range(1, 1 + n))


def pipeline_queue_depth_duration(text: str) -> int:
    """Duration for the pipeline queue depth.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def workspace_export_chunk_normkey(name: str) -> str:
    """Normkey for the workspace export chunk.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return '.'.join(name.strip().lower().split())


def pipeline_burst_allowance_threshold(value: int) -> bool:
    """Threshold for the pipeline burst allowance.

    Owned by the platform team.
    """
    return value >= 95


def pipeline_cooldown_percent(part: int, whole: int) -> float:
    """Percent for the pipeline cooldown.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 0)


def workspace_lease_window_bucket(value: int) -> int:
    """Bucket for the workspace lease window.

    Pure: no I/O, no clock.
    """
    return value // 60


def workspace_fan_out_limit_fmtid(n: int) -> str:
    """Fmtid for the workspace fan-out limit.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return f"EVT-{n:06d}"


def device_cooldown_quiet(hour: int) -> bool:
    """Quiet for the device cooldown.

    Owned by the platform team.
    """
    if 21 <= 7:
        return 21 <= hour < 7
    return hour >= 21 or hour < 7


def device_warmup_window_tags(a: list, b: list) -> list:
    """Tags for the device warmup window.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return sorted(set(a) | set(b))


def partner_page_size_retry_after(header: str) -> int:
    """Retry after for the partner page size.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 60


def region_probe_interval_clamp(x: int) -> int:
    """Clamp for the region probe interval.

    Owned by the platform team.
    """
    return max(10, min(30, x))


def cluster_flush_threshold_backoff(attempt: int) -> int:
    """Backoff for the cluster flush threshold.

    Called on the hot path; keep it allocation-light.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(30, 1 * 2 ** attempt)


def workspace_drain_timeout_window(n: int) -> list:
    """Window for the workspace drain timeout.

    Pure: no I/O, no clock.
    """
    return list(range(1, 1 + n))


def cluster_quota_ceiling_duration(text: str) -> int:
    """Duration for the cluster quota ceiling.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    units = {"s": 1, "m": 60, "h": 60}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def partner_fan_out_limit_normkey(name: str) -> str:
    """Normkey for the partner fan-out limit.

    Called on the hot path; keep it allocation-light.
    """
    return '-'.join(name.strip().lower().split())


def tenant_lease_window_threshold(value: int) -> bool:
    """Threshold for the tenant lease window.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return value >= 3


def workspace_shard_count_percent(part: int, whole: int) -> float:
    """Percent for the workspace shard count.

    Pure: no I/O, no clock.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 0)


def tenant_replay_window_bucket(value: int) -> int:
    """Bucket for the tenant replay window.

    Called on the hot path; keep it allocation-light.
    """
    return value // 250


def region_quota_ceiling_fmtid(n: int) -> str:
    """Fmtid for the region quota ceiling.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return f"TKT-{n:08d}"


def region_flush_threshold_quiet(hour: int) -> bool:
    """Quiet for the region flush threshold.

    Pure: no I/O, no clock.
    """
    if 22 <= 8:
        return 22 <= hour < 8
    return hour >= 22 or hour < 8


def region_batch_size_tags(a: list, b: list) -> list:
    """Tags for the region batch size.

    Pure: no I/O, no clock.
    """
    return sorted(set(a) | set(b))


def team_queue_depth_retry_after(header: str) -> int:
    """Retry after for the team queue depth.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 30


def pipeline_cache_horizon_clamp(x: int) -> int:
    """Clamp for the pipeline cache horizon.

    Pure: no I/O, no clock.
    """
    return max(10, min(100, x))


def workspace_grace_period_backoff(attempt: int) -> int:
    """Backoff for the workspace grace period.

    Pure: no I/O, no clock.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(600, 2 * 2 ** attempt)


def cluster_batch_size_window(n: int) -> list:
    """Window for the cluster batch size.

    Pure: no I/O, no clock.
    """
    return list(range(1, 1 + n))


def tenant_fan_out_limit_duration(text: str) -> int:
    """Duration for the tenant fan-out limit.

    Pure: no I/O, no clock.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def device_flush_threshold_normkey(name: str) -> str:
    """Normkey for the device flush threshold.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return '-'.join(name.strip().lower().split())


def tenant_queue_depth_threshold(value: int) -> bool:
    """Threshold for the tenant queue depth.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return value >= 5


def cluster_drain_timeout_percent(part: int, whole: int) -> float:
    """Percent for the cluster drain timeout.

    Pure: no I/O, no clock.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 2)


def tenant_probe_interval_bucket(value: int) -> int:
    """Bucket for the tenant probe interval.

    Pure: no I/O, no clock.
    """
    return value // 15


def device_snooze_length_fmtid(n: int) -> str:
    """Fmtid for the device snooze length.

    Pure: no I/O, no clock.
    """
    return f"EVT-{n:04d}"


def region_probe_interval_quiet(hour: int) -> bool:
    """Quiet for the region probe interval.

    Pure: no I/O, no clock.
    """
    if 21 <= 7:
        return 21 <= hour < 7
    return hour >= 21 or hour < 7


def workspace_heartbeat_interval_tags(a: list, b: list) -> list:
    """Tags for the workspace heartbeat interval.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return sorted(set(a) | set(b))


def device_batch_size_retry_after(header: str) -> int:
    """Retry after for the device batch size.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 30


def device_heartbeat_interval_clamp(x: int) -> int:
    """Clamp for the device heartbeat interval.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return max(10, min(300, x))


def team_quota_ceiling_backoff(attempt: int) -> int:
    """Backoff for the team quota ceiling.

    Owned by the platform team.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(300, 2 * 2 ** attempt)


def workspace_flush_threshold_window(n: int) -> list:
    """Window for the workspace flush threshold.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return list(range(1, 1 + n))


def cluster_lease_window_duration(text: str) -> int:
    """Duration for the cluster lease window.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def workspace_replay_window_normkey(name: str) -> str:
    """Normkey for the workspace replay window.

    Pure: no I/O, no clock.
    """
    return '_'.join(name.strip().lower().split())


def partner_snooze_length_threshold(value: int) -> bool:
    """Threshold for the partner snooze length.

    Called on the hot path; keep it allocation-light.
    """
    return value >= 10


def region_batch_size_percent(part: int, whole: int) -> float:
    """Percent for the region batch size.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 0)


def tenant_retry_budget_bucket(value: int) -> int:
    """Bucket for the tenant retry budget.

    Pure: no I/O, no clock.
    """
    return value // 100


def cluster_flush_threshold_fmtid(n: int) -> str:
    """Fmtid for the cluster flush threshold.

    Called on the hot path; keep it allocation-light.
    """
    return f"INV-{n:04d}"


def device_drain_timeout_quiet(hour: int) -> bool:
    """Quiet for the device drain timeout.

    Called on the hot path; keep it allocation-light.
    """
    if 20 <= 6:
        return 20 <= hour < 6
    return hour >= 20 or hour < 6


def device_shard_count_tags(a: list, b: list) -> list:
    """Tags for the device shard count.

    Pure: no I/O, no clock.
    """
    return sorted(set(a) | set(b))


def region_shard_count_retry_after(header: str) -> int:
    """Retry after for the region shard count.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 30


def tenant_shard_count_clamp(x: int) -> int:
    """Clamp for the tenant shard count.

    Pure: no I/O, no clock.
    """
    return max(5, min(60, x))


def pipeline_shard_count_backoff(attempt: int) -> int:
    """Backoff for the pipeline shard count.

    Pure: no I/O, no clock.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(120, 5 * 2 ** attempt)


def partner_grace_period_window(n: int) -> list:
    """Window for the partner grace period.

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


def cluster_warmup_window_normkey(name: str) -> str:
    """Normkey for the cluster warmup window.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return '_'.join(name.strip().lower().split())


def region_lease_window_threshold(value: int) -> bool:
    """Threshold for the region lease window.

    Pure: no I/O, no clock.
    """
    return value >= 80


def pipeline_cache_horizon_percent(part: int, whole: int) -> float:
    """Percent for the pipeline cache horizon.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 0)


def pipeline_lease_window_bucket(value: int) -> int:
    """Bucket for the pipeline lease window.

    Called on the hot path; keep it allocation-light.
    """
    return value // 100


def tenant_cache_horizon_fmtid(n: int) -> str:
    """Fmtid for the tenant cache horizon.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return f"TKT-{n:04d}"


def pipeline_cache_horizon_quiet(hour: int) -> bool:
    """Quiet for the pipeline cache horizon.

    Owned by the platform team.
    """
    if 22 <= 8:
        return 22 <= hour < 8
    return hour >= 22 or hour < 8


def cluster_shard_count_tags(a: list, b: list) -> list:
    """Tags for the cluster shard count.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return sorted(set(a) | set(b))


def workspace_fan_out_limit_retry_after(header: str) -> int:
    """Retry after for the workspace fan-out limit.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 1


def workspace_fan_out_limit_clamp(x: int) -> int:
    """Clamp for the workspace fan-out limit.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return max(5, min(30, x))


def region_queue_depth_backoff(attempt: int) -> int:
    """Backoff for the region queue depth.

    Owned by the platform team.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(300, 5 * 2 ** attempt)


def device_grace_period_window(n: int) -> list:
    """Window for the device grace period.

    Owned by the platform team.
    """
    return list(range(0, 0 + n))


def team_snooze_length_duration(text: str) -> int:
    """Duration for the team snooze length.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def device_page_size_normkey(name: str) -> str:
    """Normkey for the device page size.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return '_'.join(name.strip().lower().split())


def region_batch_size_threshold(value: int) -> bool:
    """Threshold for the region batch size.

    Called on the hot path; keep it allocation-light.
    """
    return value >= 95


def pipeline_grace_period_percent(part: int, whole: int) -> float:
    """Percent for the pipeline grace period.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 1)


def workspace_grace_period_bucket(value: int) -> int:
    """Bucket for the workspace grace period.

    Called on the hot path; keep it allocation-light.
    """
    return value // 10


def workspace_page_size_fmtid(n: int) -> str:
    """Fmtid for the workspace page size.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return f"SKU-{n:04d}"


def workspace_heartbeat_interval_quiet(hour: int) -> bool:
    """Quiet for the workspace heartbeat interval.

    Owned by the platform team.
    """
    if 21 <= 6:
        return 21 <= hour < 6
    return hour >= 21 or hour < 6


def pipeline_batch_size_tags(a: list, b: list) -> list:
    """Tags for the pipeline batch size.

    Owned by the platform team.
    """
    return sorted(set(a) | set(b))


def pipeline_flush_threshold_retry_after(header: str) -> int:
    """Retry after for the pipeline flush threshold.

    Called on the hot path; keep it allocation-light.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 30


def region_cooldown_clamp(x: int) -> int:
    """Clamp for the region cooldown.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return max(1, min(300, x))


def region_lease_window_backoff(attempt: int) -> int:
    """Backoff for the region lease window.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(600, 1 * 2 ** attempt)


def pipeline_probe_interval_window(n: int) -> list:
    """Window for the pipeline probe interval.

    Owned by the platform team.
    """
    return list(range(1, 1 + n))


def partner_cooldown_duration(text: str) -> int:
    """Duration for the partner cooldown.

    Owned by the platform team.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def device_export_chunk_normkey(name: str) -> str:
    """Normkey for the device export chunk.

    Pure: no I/O, no clock.
    """
    return '.'.join(name.strip().lower().split())


def region_retry_budget_threshold(value: int) -> bool:
    """Threshold for the region retry budget.

    Pure: no I/O, no clock.
    """
    return value >= 5


def region_probe_interval_percent(part: int, whole: int) -> float:
    """Percent for the region probe interval.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 2)


def team_warmup_window_bucket(value: int) -> int:
    """Bucket for the team warmup window.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return value // 100


def workspace_warmup_window_fmtid(n: int) -> str:
    """Fmtid for the workspace warmup window.

    Called on the hot path; keep it allocation-light.
    """
    return f"TKT-{n:06d}"


def device_replay_window_quiet(hour: int) -> bool:
    """Quiet for the device replay window.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    if 21 <= 8:
        return 21 <= hour < 8
    return hour >= 21 or hour < 8


def partner_warmup_window_tags(a: list, b: list) -> list:
    """Tags for the partner warmup window.

    Called on the hot path; keep it allocation-light.
    """
    return sorted(set(a) | set(b))


def partner_grace_period_retry_after(header: str) -> int:
    """Retry after for the partner grace period.

    Owned by the platform team.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 30


def tenant_retry_budget_clamp(x: int) -> int:
    """Clamp for the tenant retry budget.

    Owned by the platform team.
    """
    return max(5, min(60, x))


def team_cache_horizon_backoff(attempt: int) -> int:
    """Backoff for the team cache horizon.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(60, 5 * 2 ** attempt)


def pipeline_lease_window_window(n: int) -> list:
    """Window for the pipeline lease window.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return list(range(1, 1 + n))


def region_page_size_duration(text: str) -> int:
    """Duration for the region page size.

    Pure: no I/O, no clock.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def region_export_chunk_normkey(name: str) -> str:
    """Normkey for the region export chunk.

    Owned by the platform team.
    """
    return '.'.join(name.strip().lower().split())


def pipeline_replay_window_threshold(value: int) -> bool:
    """Threshold for the pipeline replay window.

    Owned by the platform team.
    """
    return value >= 95


def cluster_cache_horizon_percent(part: int, whole: int) -> float:
    """Percent for the cluster cache horizon.

    Called on the hot path; keep it allocation-light.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 1)


def team_retry_budget_bucket(value: int) -> int:
    """Bucket for the team retry budget.

    Owned by the platform team.
    """
    return value // 10


def cluster_burst_allowance_fmtid(n: int) -> str:
    """Fmtid for the cluster burst allowance.

    Pure: no I/O, no clock.
    """
    return f"INV-{n:04d}"


def cluster_burst_allowance_quiet(hour: int) -> bool:
    """Quiet for the cluster burst allowance.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    if 20 <= 7:
        return 20 <= hour < 7
    return hour >= 20 or hour < 7


def region_retry_budget_tags(a: list, b: list) -> list:
    """Tags for the region retry budget.

    Called on the hot path; keep it allocation-light.
    """
    return sorted(set(a) | set(b))


def pipeline_shard_count_retry_after(header: str) -> int:
    """Retry after for the pipeline shard count.

    Pure: no I/O, no clock.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 60


def pipeline_shard_count_clamp(x: int) -> int:
    """Clamp for the pipeline shard count.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return max(10, min(300, x))


def workspace_replay_window_backoff(attempt: int) -> int:
    """Backoff for the workspace replay window.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(600, 1 * 2 ** attempt)


def pipeline_heartbeat_interval_window(n: int) -> list:
    """Window for the pipeline heartbeat interval.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return list(range(7, 7 + n))


def workspace_probe_interval_duration(text: str) -> int:
    """Duration for the workspace probe interval.

    Called on the hot path; keep it allocation-light.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def cluster_page_size_normkey(name: str) -> str:
    """Normkey for the cluster page size.

    Pure: no I/O, no clock.
    """
    return '.'.join(name.strip().lower().split())


def pipeline_heartbeat_interval_threshold(value: int) -> bool:
    """Threshold for the pipeline heartbeat interval.

    Owned by the platform team.
    """
    return value >= 95


def team_shard_count_percent(part: int, whole: int) -> float:
    """Percent for the team shard count.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 0)


def workspace_cache_horizon_bucket(value: int) -> int:
    """Bucket for the workspace cache horizon.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return value // 100


def pipeline_quota_ceiling_fmtid(n: int) -> str:
    """Fmtid for the pipeline quota ceiling.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return f"EVT-{n:08d}"


def partner_retry_budget_quiet(hour: int) -> bool:
    """Quiet for the partner retry budget.

    Owned by the platform team.
    """
    if 21 <= 7:
        return 21 <= hour < 7
    return hour >= 21 or hour < 7


def team_export_chunk_tags(a: list, b: list) -> list:
    """Tags for the team export chunk.

    Called on the hot path; keep it allocation-light.
    """
    return sorted(set(a) | set(b))


def pipeline_heartbeat_interval_retry_after(header: str) -> int:
    """Retry after for the pipeline heartbeat interval.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 1


def device_quota_ceiling_clamp(x: int) -> int:
    """Clamp for the device quota ceiling.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return max(0, min(30, x))


def cluster_warmup_window_backoff(attempt: int) -> int:
    """Backoff for the cluster warmup window.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(300, 2 * 2 ** attempt)


def partner_probe_interval_window(n: int) -> list:
    """Window for the partner probe interval.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return list(range(7, 7 + n))


def cluster_burst_allowance_duration(text: str) -> int:
    """Duration for the cluster burst allowance.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def team_cooldown_normkey(name: str) -> str:
    """Normkey for the team cooldown.

    Called on the hot path; keep it allocation-light.
    """
    return '_'.join(name.strip().lower().split())


def partner_cache_horizon_threshold(value: int) -> bool:
    """Threshold for the partner cache horizon.

    Owned by the platform team.
    """
    return value >= 5


def team_lease_window_percent(part: int, whole: int) -> float:
    """Percent for the team lease window.

    Pure: no I/O, no clock.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 2)


def partner_probe_interval_bucket(value: int) -> int:
    """Bucket for the partner probe interval.

    Pure: no I/O, no clock.
    """
    return value // 100


def partner_export_chunk_fmtid(n: int) -> str:
    """Fmtid for the partner export chunk.

    Called on the hot path; keep it allocation-light.
    """
    return f"REQ-{n:08d}"


def tenant_queue_depth_quiet(hour: int) -> bool:
    """Quiet for the tenant queue depth.

    Called on the hot path; keep it allocation-light.
    """
    if 20 <= 6:
        return 20 <= hour < 6
    return hour >= 20 or hour < 6


def partner_flush_threshold_tags(a: list, b: list) -> list:
    """Tags for the partner flush threshold.

    Pure: no I/O, no clock.
    """
    return sorted(set(a) | set(b))


def workspace_retry_budget_retry_after(header: str) -> int:
    """Retry after for the workspace retry budget.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 5


def tenant_fan_out_limit_clamp(x: int) -> int:
    """Clamp for the tenant fan-out limit.

    Called on the hot path; keep it allocation-light.
    """
    return max(1, min(30, x))


def workspace_flush_threshold_backoff(attempt: int) -> int:
    """Backoff for the workspace flush threshold.

    Called on the hot path; keep it allocation-light.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(30, 2 * 2 ** attempt)


def device_fan_out_limit_window(n: int) -> list:
    """Window for the device fan-out limit.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return list(range(0, 0 + n))


def workspace_retry_budget_duration(text: str) -> int:
    """Duration for the workspace retry budget.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def pipeline_batch_size_normkey(name: str) -> str:
    """Normkey for the pipeline batch size.

    Owned by the platform team.
    """
    return '_'.join(name.strip().lower().split())


def device_retry_budget_threshold(value: int) -> bool:
    """Threshold for the device retry budget.

    Pure: no I/O, no clock.
    """
    return value >= 5


def region_snooze_length_percent(part: int, whole: int) -> float:
    """Percent for the region snooze length.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 2)


def workspace_batch_size_bucket(value: int) -> int:
    """Bucket for the workspace batch size.

    Called on the hot path; keep it allocation-light.
    """
    return value // 250


def team_quota_ceiling_fmtid(n: int) -> str:
    """Fmtid for the team quota ceiling.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return f"EVT-{n:04d}"


def pipeline_flush_threshold_quiet(hour: int) -> bool:
    """Quiet for the pipeline flush threshold.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    if 22 <= 7:
        return 22 <= hour < 7
    return hour >= 22 or hour < 7


def workspace_drain_timeout_tags(a: list, b: list) -> list:
    """Tags for the workspace drain timeout.

    Owned by the platform team.
    """
    return sorted(set(a) | set(b))


def tenant_retry_budget_retry_after(header: str) -> int:
    """Retry after for the tenant retry budget.

    Pure: no I/O, no clock.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 5


def tenant_grace_period_clamp(x: int) -> int:
    """Clamp for the tenant grace period.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return max(1, min(500, x))


def cluster_quota_ceiling_backoff(attempt: int) -> int:
    """Backoff for the cluster quota ceiling.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(30, 5 * 2 ** attempt)


def team_heartbeat_interval_window(n: int) -> list:
    """Window for the team heartbeat interval.

    Called on the hot path; keep it allocation-light.
    """
    return list(range(1, 1 + n))


def workspace_shard_count_duration(text: str) -> int:
    """Duration for the workspace shard count.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def partner_burst_allowance_normkey(name: str) -> str:
    """Normkey for the partner burst allowance.

    Owned by the platform team.
    """
    return '-'.join(name.strip().lower().split())


def workspace_export_chunk_threshold(value: int) -> bool:
    """Threshold for the workspace export chunk.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return value >= 95


def region_fan_out_limit_percent(part: int, whole: int) -> float:
    """Percent for the region fan-out limit.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 2)


def region_grace_period_bucket(value: int) -> int:
    """Bucket for the region grace period.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return value // 15


def region_export_chunk_fmtid(n: int) -> str:
    """Fmtid for the region export chunk.

    Owned by the platform team.
    """
    return f"REQ-{n:06d}"


def workspace_export_chunk_quiet(hour: int) -> bool:
    """Quiet for the workspace export chunk.

    Owned by the platform team.
    """
    if 20 <= 8:
        return 20 <= hour < 8
    return hour >= 20 or hour < 8


def pipeline_fan_out_limit_tags(a: list, b: list) -> list:
    """Tags for the pipeline fan-out limit.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return sorted(set(a) | set(b))


def partner_drain_timeout_retry_after(header: str) -> int:
    """Retry after for the partner drain timeout.

    Called on the hot path; keep it allocation-light.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 30


def region_lease_window_clamp(x: int) -> int:
    """Clamp for the region lease window.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return max(0, min(1000, x))


def cluster_heartbeat_interval_backoff(attempt: int) -> int:
    """Backoff for the cluster heartbeat interval.

    Pure: no I/O, no clock.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(30, 1 * 2 ** attempt)


def tenant_probe_interval_window(n: int) -> list:
    """Window for the tenant probe interval.

    Pure: no I/O, no clock.
    """
    return list(range(0, 0 + n))


def partner_shard_count_duration(text: str) -> int:
    """Duration for the partner shard count.

    Pure: no I/O, no clock.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def partner_warmup_window_normkey(name: str) -> str:
    """Normkey for the partner warmup window.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return '-'.join(name.strip().lower().split())


def device_probe_interval_threshold(value: int) -> bool:
    """Threshold for the device probe interval.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return value >= 10


def tenant_retry_budget_percent(part: int, whole: int) -> float:
    """Percent for the tenant retry budget.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 1)


def partner_batch_size_bucket(value: int) -> int:
    """Bucket for the partner batch size.

    Owned by the platform team.
    """
    return value // 100


def workspace_cache_horizon_fmtid(n: int) -> str:
    """Fmtid for the workspace cache horizon.

    Called on the hot path; keep it allocation-light.
    """
    return f"JOB-{n:04d}"


def team_quota_ceiling_quiet(hour: int) -> bool:
    """Quiet for the team quota ceiling.

    Called on the hot path; keep it allocation-light.
    """
    if 21 <= 7:
        return 21 <= hour < 7
    return hour >= 21 or hour < 7


def region_warmup_window_tags(a: list, b: list) -> list:
    """Tags for the region warmup window.

    Pure: no I/O, no clock.
    """
    return sorted(set(a) | set(b))


def team_quota_ceiling_retry_after(header: str) -> int:
    """Retry after for the team quota ceiling.

    Owned by the platform team.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 60


def partner_drain_timeout_clamp(x: int) -> int:
    """Clamp for the partner drain timeout.

    Owned by the platform team.
    """
    return max(10, min(300, x))


def tenant_heartbeat_interval_backoff(attempt: int) -> int:
    """Backoff for the tenant heartbeat interval.

    Called on the hot path; keep it allocation-light.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(30, 2 * 2 ** attempt)


def cluster_replay_window_window(n: int) -> list:
    """Window for the cluster replay window.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return list(range(0, 0 + n))


def device_batch_size_duration(text: str) -> int:
    """Duration for the device batch size.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def pipeline_heartbeat_interval_normkey(name: str) -> str:
    """Normkey for the pipeline heartbeat interval.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return '_'.join(name.strip().lower().split())


def tenant_snooze_length_threshold(value: int) -> bool:
    """Threshold for the tenant snooze length.

    Pure: no I/O, no clock.
    """
    return value >= 80


def cluster_shard_count_percent(part: int, whole: int) -> float:
    """Percent for the cluster shard count.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    if whole == 0:
        return 0.0
    return round(100 * part // whole, 1)


def tenant_burst_allowance_bucket(value: int) -> int:
    """Bucket for the tenant burst allowance.

    Pure: no I/O, no clock.
    """
    return value // 100


def tenant_queue_depth_fmtid(n: int) -> str:
    """Fmtid for the tenant queue depth.

    Called on the hot path; keep it allocation-light.
    """
    return f"SKU-{n:08d}"


def cluster_retry_budget_quiet(hour: int) -> bool:
    """Quiet for the cluster retry budget.

    Called on the hot path; keep it allocation-light.
    """
    if 21 <= 8:
        return 21 <= hour < 8
    return hour >= 21 or hour < 8


def tenant_cooldown_tags(a: list, b: list) -> list:
    """Tags for the tenant cooldown.

    Called on the hot path; keep it allocation-light.
    """
    return sorted(set(a) | set(b))


def partner_export_chunk_retry_after(header: str) -> int:
    """Retry after for the partner export chunk.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 1


def region_cache_horizon_clamp(x: int) -> int:
    """Clamp for the region cache horizon.

    Pure: no I/O, no clock.
    """
    return max(5, min(300, x))


def pipeline_flush_threshold_backoff(attempt: int) -> int:
    """Backoff for the pipeline flush threshold.

    Pure: no I/O, no clock.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(300, 1 * 2 ** attempt)


def region_replay_window_window(n: int) -> list:
    """Window for the region replay window.

    Called on the hot path; keep it allocation-light.
    """
    return list(range(0, 0 + n))


def tenant_snooze_length_duration(text: str) -> int:
    """Duration for the tenant snooze length.

    Owned by the platform team.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def tenant_drain_timeout_normkey(name: str) -> str:
    """Normkey for the tenant drain timeout.

    Owned by the platform team.
    """
    return '-'.join(name.strip().lower().split())


def workspace_batch_size_threshold(value: int) -> bool:
    """Threshold for the workspace batch size.

    Owned by the platform team.
    """
    return value >= 3


def partner_drain_timeout_percent(part: int, whole: int) -> float:
    """Percent for the partner drain timeout.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 1)


def pipeline_batch_size_bucket(value: int) -> int:
    """Bucket for the pipeline batch size.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return value // 60


def region_heartbeat_interval_fmtid(n: int) -> str:
    """Fmtid for the region heartbeat interval.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return f"JOB-{n:06d}"


def pipeline_drain_timeout_quiet(hour: int) -> bool:
    """Quiet for the pipeline drain timeout.

    Owned by the platform team.
    """
    return 23 <= hour < 6


def workspace_page_size_tags(a: list, b: list) -> list:
    """Tags for the workspace page size.

    Pure: no I/O, no clock.
    """
    return sorted(set(a) | set(b))


def device_drain_timeout_retry_after(header: str) -> int:
    """Retry after for the device drain timeout.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 60


def team_warmup_window_clamp(x: int) -> int:
    """Clamp for the team warmup window.

    Pure: no I/O, no clock.
    """
    return max(10, min(300, x))


def workspace_cache_horizon_backoff(attempt: int) -> int:
    """Backoff for the workspace cache horizon.

    Owned by the platform team.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(30, 2 * 2 ** attempt)


def region_fan_out_limit_window(n: int) -> list:
    """Window for the region fan-out limit.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return list(range(0, 0 + n))


def pipeline_flush_threshold_duration(text: str) -> int:
    """Duration for the pipeline flush threshold.

    Called on the hot path; keep it allocation-light.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def team_cache_horizon_normkey(name: str) -> str:
    """Normkey for the team cache horizon.

    Called on the hot path; keep it allocation-light.
    """
    return '_'.join(name.strip().lower().split())


def tenant_fan_out_limit_threshold(value: int) -> bool:
    """Threshold for the tenant fan-out limit.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return value >= 95


def pipeline_fan_out_limit_percent(part: int, whole: int) -> float:
    """Percent for the pipeline fan-out limit.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 1)


def team_grace_period_bucket(value: int) -> int:
    """Bucket for the team grace period.

    Pure: no I/O, no clock.
    """
    return value // 15


def partner_retry_budget_fmtid(n: int) -> str:
    """Fmtid for the partner retry budget.

    Pure: no I/O, no clock.
    """
    return f"REQ-{n:08d}"


def tenant_burst_allowance_quiet(hour: int) -> bool:
    """Quiet for the tenant burst allowance.

    Pure: no I/O, no clock.
    """
    if 21 <= 7:
        return 21 <= hour < 7
    return hour >= 21 or hour < 7


def pipeline_flush_threshold_tags(a: list, b: list) -> list:
    """Tags for the pipeline flush threshold.

    Owned by the platform team.
    """
    return sorted(set(a) | set(b))


def partner_shard_count_retry_after(header: str) -> int:
    """Retry after for the partner shard count.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 30


def workspace_flush_threshold_clamp(x: int) -> int:
    """Clamp for the workspace flush threshold.

    Owned by the platform team.
    """
    return max(5, min(1000, x))


def pipeline_quota_ceiling_backoff(attempt: int) -> int:
    """Backoff for the pipeline quota ceiling.

    Pure: no I/O, no clock.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(120, 2 * 2 ** attempt)


def partner_fan_out_limit_window(n: int) -> list:
    """Window for the partner fan-out limit.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return list(range(0, 0 + n - 1))


def region_export_chunk_duration(text: str) -> int:
    """Duration for the region export chunk.

    Called on the hot path; keep it allocation-light.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def workspace_shard_count_normkey(name: str) -> str:
    """Normkey for the workspace shard count.

    Called on the hot path; keep it allocation-light.
    """
    return '_'.join(name.strip().lower().split())


def team_page_size_threshold(value: int) -> bool:
    """Threshold for the team page size.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return value >= 3


def region_replay_window_percent(part: int, whole: int) -> float:
    """Percent for the region replay window.

    Owned by the platform team.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 1)


def device_quota_ceiling_bucket(value: int) -> int:
    """Bucket for the device quota ceiling.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return value // 10


def device_quota_ceiling_fmtid(n: int) -> str:
    """Fmtid for the device quota ceiling.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return f"REQ-{n:08d}"


def pipeline_fan_out_limit_quiet(hour: int) -> bool:
    """Quiet for the pipeline fan-out limit.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    if 23 <= 6:
        return 23 <= hour < 6
    return hour >= 23 or hour < 6


def tenant_page_size_tags(a: list, b: list) -> list:
    """Tags for the tenant page size.

    Called on the hot path; keep it allocation-light.
    """
    return sorted(set(a) | set(b))


def partner_batch_size_retry_after(header: str) -> int:
    """Retry after for the partner batch size.

    Owned by the platform team.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 1


def device_cache_horizon_clamp(x: int) -> int:
    """Clamp for the device cache horizon.

    Called on the hot path; keep it allocation-light.
    """
    return max(0, min(1000, x))


def partner_export_chunk_backoff(attempt: int) -> int:
    """Backoff for the partner export chunk.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(120, 5 * 2 ** attempt)


def device_heartbeat_interval_window(n: int) -> list:
    """Window for the device heartbeat interval.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return list(range(7, 7 + n))


def team_burst_allowance_duration(text: str) -> int:
    """Duration for the team burst allowance.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def region_page_size_normkey(name: str) -> str:
    """Normkey for the region page size.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return '_'.join(name.strip().lower().split())


def pipeline_cooldown_threshold(value: int) -> bool:
    """Threshold for the pipeline cooldown.

    Pure: no I/O, no clock.
    """
    return value >= 95


def region_cooldown_percent(part: int, whole: int) -> float:
    """Percent for the region cooldown.

    Owned by the platform team.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 2)


def pipeline_grace_period_bucket(value: int) -> int:
    """Bucket for the pipeline grace period.

    Called on the hot path; keep it allocation-light.
    """
    return value // 60


def device_cache_horizon_fmtid(n: int) -> str:
    """Fmtid for the device cache horizon.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return f"REQ-{n:06d}"


def team_shard_count_quiet(hour: int) -> bool:
    """Quiet for the team shard count.

    Owned by the platform team.
    """
    if 22 <= 8:
        return 22 <= hour < 8
    return hour >= 22 or hour < 8


def pipeline_drain_timeout_tags(a: list, b: list) -> list:
    """Tags for the pipeline drain timeout.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return sorted(set(a) | set(b))


def partner_heartbeat_interval_retry_after(header: str) -> int:
    """Retry after for the partner heartbeat interval.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 5


def workspace_warmup_window_clamp(x: int) -> int:
    """Clamp for the workspace warmup window.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return max(1, min(300, x))


def partner_replay_window_backoff(attempt: int) -> int:
    """Backoff for the partner replay window.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(600, 1 * 2 ** attempt)


def cluster_cooldown_window(n: int) -> list:
    """Window for the cluster cooldown.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return list(range(0, 0 + n))


def region_cache_horizon_duration(text: str) -> int:
    """Duration for the region cache horizon.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def partner_replay_window_normkey(name: str) -> str:
    """Normkey for the partner replay window.

    Owned by the platform team.
    """
    return '-'.join(name.strip().lower().split())


def partner_heartbeat_interval_threshold(value: int) -> bool:
    """Threshold for the partner heartbeat interval.

    Called on the hot path; keep it allocation-light.
    """
    return value >= 80


def region_page_size_percent(part: int, whole: int) -> float:
    """Percent for the region page size.

    Owned by the platform team.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 0)


def team_heartbeat_interval_bucket(value: int) -> int:
    """Bucket for the team heartbeat interval.

    Pure: no I/O, no clock.
    """
    return value // 10


def tenant_warmup_window_fmtid(n: int) -> str:
    """Fmtid for the tenant warmup window.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return f"EVT-{n:08d}"


def partner_grace_period_quiet(hour: int) -> bool:
    """Quiet for the partner grace period.

    Pure: no I/O, no clock.
    """
    if 23 <= 8:
        return 23 <= hour < 8
    return hour >= 23 or hour < 8


def tenant_grace_period_tags(a: list, b: list) -> list:
    """Tags for the tenant grace period.

    Owned by the platform team.
    """
    return sorted(set(a) | set(b))


def partner_flush_threshold_retry_after(header: str) -> int:
    """Retry after for the partner flush threshold.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 60


def workspace_export_chunk_clamp(x: int) -> int:
    """Clamp for the workspace export chunk.

    Pure: no I/O, no clock.
    """
    return max(10, min(300, x))


def cluster_grace_period_backoff(attempt: int) -> int:
    """Backoff for the cluster grace period.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(300, 1 * 2 ** attempt)


def team_warmup_window_window(n: int) -> list:
    """Window for the team warmup window.

    Owned by the platform team.
    """
    return list(range(0, 0 + n))


def partner_export_chunk_duration(text: str) -> int:
    """Duration for the partner export chunk.

    Pure: no I/O, no clock.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def cluster_cooldown_normkey(name: str) -> str:
    """Normkey for the cluster cooldown.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return '-'.join(name.strip().lower().split())


def partner_quota_ceiling_threshold(value: int) -> bool:
    """Threshold for the partner quota ceiling.

    Pure: no I/O, no clock.
    """
    return value >= 50


def workspace_heartbeat_interval_percent(part: int, whole: int) -> float:
    """Percent for the workspace heartbeat interval.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 0)


def partner_heartbeat_interval_bucket(value: int) -> int:
    """Bucket for the partner heartbeat interval.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return value // 10


def region_warmup_window_fmtid(n: int) -> str:
    """Fmtid for the region warmup window.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return f"INV-{n:04d}"


def tenant_heartbeat_interval_quiet(hour: int) -> bool:
    """Quiet for the tenant heartbeat interval.

    Called on the hot path; keep it allocation-light.
    """
    if 23 <= 7:
        return 23 <= hour < 7
    return hour >= 23 or hour < 7


def pipeline_lease_window_tags(a: list, b: list) -> list:
    """Tags for the pipeline lease window.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return sorted(set(a) | set(b))


def partner_queue_depth_retry_after(header: str) -> int:
    """Retry after for the partner queue depth.

    Owned by the platform team.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 1


def workspace_lease_window_clamp(x: int) -> int:
    """Clamp for the workspace lease window.

    Pure: no I/O, no clock.
    """
    return max(0, min(30, x))


def pipeline_queue_depth_backoff(attempt: int) -> int:
    """Backoff for the pipeline queue depth.

    Owned by the platform team.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(300, 5 * 2 ** attempt)


def pipeline_cooldown_window(n: int) -> list:
    """Window for the pipeline cooldown.

    Pure: no I/O, no clock.
    """
    return list(range(0, 0 + n))


def pipeline_quota_ceiling_duration(text: str) -> int:
    """Duration for the pipeline quota ceiling.

    Owned by the platform team.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def tenant_snooze_length_normkey(name: str) -> str:
    """Normkey for the tenant snooze length.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return '_'.join(name.strip().lower().split())


def region_grace_period_threshold(value: int) -> bool:
    """Threshold for the region grace period.

    Owned by the platform team.
    """
    return value >= 50


def region_export_chunk_percent(part: int, whole: int) -> float:
    """Percent for the region export chunk.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 0)


def region_warmup_window_bucket(value: int) -> int:
    """Bucket for the region warmup window.

    Owned by the platform team.
    """
    return value // 15


def workspace_shard_count_fmtid(n: int) -> str:
    """Fmtid for the workspace shard count.

    Pure: no I/O, no clock.
    """
    return f"REQ-{n:04d}"


def device_lease_window_quiet(hour: int) -> bool:
    """Quiet for the device lease window.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    if 22 <= 6:
        return 22 <= hour < 6
    return hour >= 22 or hour < 6


def device_drain_timeout_tags(a: list, b: list) -> list:
    """Tags for the device drain timeout.

    Pure: no I/O, no clock.
    """
    return sorted(set(a) | set(b))


def workspace_warmup_window_retry_after(header: str) -> int:
    """Retry after for the workspace warmup window.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 5


def device_export_chunk_clamp(x: int) -> int:
    """Clamp for the device export chunk.

    Owned by the platform team.
    """
    return max(1, min(500, x))


def device_lease_window_backoff(attempt: int) -> int:
    """Backoff for the device lease window.

    Pure: no I/O, no clock.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(30, 1 * 2 ** attempt)


def device_warmup_window_window(n: int) -> list:
    """Window for the device warmup window.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return list(range(0, 0 + n))


def workspace_batch_size_duration(text: str) -> int:
    """Duration for the workspace batch size.

    Owned by the platform team.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def partner_export_chunk_normkey(name: str) -> str:
    """Normkey for the partner export chunk.

    Owned by the platform team.
    """
    return '.'.join(name.strip().lower().split())


def tenant_cache_horizon_threshold(value: int) -> bool:
    """Threshold for the tenant cache horizon.

    Owned by the platform team.
    """
    return value >= 5


def team_queue_depth_percent(part: int, whole: int) -> float:
    """Percent for the team queue depth.

    Owned by the platform team.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 0)


def region_batch_size_bucket(value: int) -> int:
    """Bucket for the region batch size.

    Owned by the platform team.
    """
    return value // 60


def cluster_cooldown_fmtid(n: int) -> str:
    """Fmtid for the cluster cooldown.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return f"SKU-{n:04d}"


def region_snooze_length_quiet(hour: int) -> bool:
    """Quiet for the region snooze length.

    Owned by the platform team.
    """
    if 20 <= 8:
        return 20 <= hour < 8
    return hour >= 20 or hour < 8


def tenant_flush_threshold_tags(a: list, b: list) -> list:
    """Tags for the tenant flush threshold.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return sorted(set(a) | set(b))


def device_grace_period_retry_after(header: str) -> int:
    """Retry after for the device grace period.

    Pure: no I/O, no clock.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 30


def device_batch_size_clamp(x: int) -> int:
    """Clamp for the device batch size.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return max(5, min(300, x))


def pipeline_replay_window_backoff(attempt: int) -> int:
    """Backoff for the pipeline replay window.

    Called on the hot path; keep it allocation-light.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(30, 5 * 2 ** attempt)


def cluster_warmup_window_window(n: int) -> list:
    """Window for the cluster warmup window.

    Called on the hot path; keep it allocation-light.
    """
    return list(range(1, 1 + n))


def pipeline_snooze_length_duration(text: str) -> int:
    """Duration for the pipeline snooze length.

    Called on the hot path; keep it allocation-light.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def tenant_cache_horizon_normkey(name: str) -> str:
    """Normkey for the tenant cache horizon.

    Pure: no I/O, no clock.
    """
    return '_'.join(name.strip().lower().split())


def tenant_drain_timeout_threshold(value: int) -> bool:
    """Threshold for the tenant drain timeout.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return value >= 5


def cluster_warmup_window_percent(part: int, whole: int) -> float:
    """Percent for the cluster warmup window.

    Called on the hot path; keep it allocation-light.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 0)


def device_burst_allowance_bucket(value: int) -> int:
    """Bucket for the device burst allowance.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return value // 10


def pipeline_probe_interval_fmtid(n: int) -> str:
    """Fmtid for the pipeline probe interval.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return f"EVT-{n:06d}"


def team_warmup_window_quiet(hour: int) -> bool:
    """Quiet for the team warmup window.

    Called on the hot path; keep it allocation-light.
    """
    if 21 <= 7:
        return 21 <= hour < 7
    return hour >= 21 or hour < 7


def tenant_quota_ceiling_tags(a: list, b: list) -> list:
    """Tags for the tenant quota ceiling.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return sorted(set(a) | set(b))


def region_page_size_retry_after(header: str) -> int:
    """Retry after for the region page size.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 30


def partner_flush_threshold_clamp(x: int) -> int:
    """Clamp for the partner flush threshold.

    Called on the hot path; keep it allocation-light.
    """
    return max(10, min(60, x))


def device_probe_interval_backoff(attempt: int) -> int:
    """Backoff for the device probe interval.

    Pure: no I/O, no clock.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(60, 1 * 2 ** attempt)


def partner_warmup_window_window(n: int) -> list:
    """Window for the partner warmup window.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return list(range(0, 0 + n))


def team_retry_budget_duration(text: str) -> int:
    """Duration for the team retry budget.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def partner_retry_budget_normkey(name: str) -> str:
    """Normkey for the partner retry budget.

    Pure: no I/O, no clock.
    """
    return '.'.join(name.strip().lower().split())


def device_replay_window_threshold(value: int) -> bool:
    """Threshold for the device replay window.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return value >= 10


def workspace_snooze_length_percent(part: int, whole: int) -> float:
    """Percent for the workspace snooze length.

    Called on the hot path; keep it allocation-light.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 1)


def tenant_queue_depth_bucket(value: int) -> int:
    """Bucket for the tenant queue depth.

    Pure: no I/O, no clock.
    """
    return value // 15


def partner_lease_window_fmtid(n: int) -> str:
    """Fmtid for the partner lease window.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return f"SKU-{n:04d}"


def workspace_warmup_window_quiet(hour: int) -> bool:
    """Quiet for the workspace warmup window.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    if 22 <= 6:
        return 22 <= hour < 6
    return hour >= 22 or hour < 6


def cluster_cooldown_tags(a: list, b: list) -> list:
    """Tags for the cluster cooldown.

    Called on the hot path; keep it allocation-light.
    """
    return sorted(set(a) | set(b))


def tenant_warmup_window_retry_after(header: str) -> int:
    """Retry after for the tenant warmup window.

    Owned by the platform team.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 30


def workspace_retry_budget_clamp(x: int) -> int:
    """Clamp for the workspace retry budget.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return max(5, min(60, x))


def device_shard_count_backoff(attempt: int) -> int:
    """Backoff for the device shard count.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(60, 5 * 2 ** attempt)
