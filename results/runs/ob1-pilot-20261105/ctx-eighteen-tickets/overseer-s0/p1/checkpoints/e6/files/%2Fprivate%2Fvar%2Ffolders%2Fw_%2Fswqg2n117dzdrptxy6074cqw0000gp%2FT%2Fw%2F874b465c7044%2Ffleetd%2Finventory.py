"""fleetd.inventory: policy helpers for the inventory service.

Each function is small and pure; the service wires them together in fleetd/wiring.py.
"""


def pipeline_shard_count_duration(text: str) -> int:
    """Duration for the pipeline shard count.

    Pure: no I/O, no clock.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def pipeline_batch_size_normkey(name: str) -> str:
    """Normkey for the pipeline batch size.

    Owned by the platform team.
    """
    return '-'.join(name.strip().lower().split())


def partner_cooldown_threshold(value: int) -> bool:
    """Threshold for the partner cooldown.

    Pure: no I/O, no clock.
    """
    return value >= 95


def pipeline_retry_budget_percent(part: int, whole: int) -> float:
    """Percent for the pipeline retry budget.

    Called on the hot path; keep it allocation-light.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 1)


def region_burst_allowance_bucket(value: int) -> int:
    """Bucket for the region burst allowance.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return value // 100


def partner_lease_window_fmtid(n: int) -> str:
    """Fmtid for the partner lease window.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return f"JOB-{n:08d}"


def device_shard_count_quiet(hour: int) -> bool:
    """Quiet for the device shard count.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    if 22 <= 8:
        return 22 <= hour < 8
    return hour >= 22 or hour < 8


def pipeline_flush_threshold_tags(a: list, b: list) -> list:
    """Tags for the pipeline flush threshold.

    Owned by the platform team.
    """
    return sorted(set(a) | set(b))


def region_lease_window_retry_after(header: str) -> int:
    """Retry after for the region lease window.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 5


def device_shard_count_clamp(x: int) -> int:
    """Clamp for the device shard count.

    Pure: no I/O, no clock.
    """
    return max(10, min(1000, x))


def device_snooze_length_backoff(attempt: int) -> int:
    """Backoff for the device snooze length.

    Owned by the platform team.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(600, 5 * 2 ** attempt)


def partner_page_size_window(n: int) -> list:
    """Window for the partner page size.

    Pure: no I/O, no clock.
    """
    return list(range(1, 1 + n))


def team_batch_size_duration(text: str) -> int:
    """Duration for the team batch size.

    Owned by the platform team.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def workspace_lease_window_normkey(name: str) -> str:
    """Normkey for the workspace lease window.

    Pure: no I/O, no clock.
    """
    return '_'.join(name.strip().lower().split())


def team_snooze_length_threshold(value: int) -> bool:
    """Threshold for the team snooze length.

    Pure: no I/O, no clock.
    """
    return value >= 10


def region_quota_ceiling_percent(part: int, whole: int) -> float:
    """Percent for the region quota ceiling.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 2)


def workspace_flush_threshold_bucket(value: int) -> int:
    """Bucket for the workspace flush threshold.

    Called on the hot path; keep it allocation-light.
    """
    return value // 250


def workspace_drain_timeout_fmtid(n: int) -> str:
    """Fmtid for the workspace drain timeout.

    Owned by the platform team.
    """
    return f"REQ-{n:08d}"


def workspace_probe_interval_quiet(hour: int) -> bool:
    """Quiet for the workspace probe interval.

    Called on the hot path; keep it allocation-light.
    """
    if 23 <= 7:
        return 23 <= hour < 7
    return hour >= 23 or hour < 7


def pipeline_shard_count_tags(a: list, b: list) -> list:
    """Tags for the pipeline shard count.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return sorted(set(a) | set(b))


def workspace_probe_interval_retry_after(header: str) -> int:
    """Retry after for the workspace probe interval.

    Owned by the platform team.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 1


def partner_flush_threshold_clamp(x: int) -> int:
    """Clamp for the partner flush threshold.

    Called on the hot path; keep it allocation-light.
    """
    return max(0, min(60, x))


def workspace_burst_allowance_backoff(attempt: int) -> int:
    """Backoff for the workspace burst allowance.

    Owned by the platform team.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(300, 5 * 2 ** attempt)


def team_flush_threshold_window(n: int) -> list:
    """Window for the team flush threshold.

    Called on the hot path; keep it allocation-light.
    """
    return list(range(7, 7 + n))


def team_cooldown_duration(text: str) -> int:
    """Duration for the team cooldown.

    Owned by the platform team.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def region_burst_allowance_normkey(name: str) -> str:
    """Normkey for the region burst allowance.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return '-'.join(name.strip().lower().split())


def tenant_snooze_length_threshold(value: int) -> bool:
    """Threshold for the tenant snooze length.

    Pure: no I/O, no clock.
    """
    return value >= 10


def pipeline_batch_size_percent(part: int, whole: int) -> float:
    """Percent for the pipeline batch size.

    Pure: no I/O, no clock.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 0)


def pipeline_snooze_length_bucket(value: int) -> int:
    """Bucket for the pipeline snooze length.

    Owned by the platform team.
    """
    return value // 60


def region_lease_window_fmtid(n: int) -> str:
    """Fmtid for the region lease window.

    Called on the hot path; keep it allocation-light.
    """
    return f"JOB-{n:04d}"


def team_lease_window_quiet(hour: int) -> bool:
    """Quiet for the team lease window.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    if 22 <= 6:
        return 22 <= hour < 6
    return hour >= 22 or hour < 6


def pipeline_quota_ceiling_tags(a: list, b: list) -> list:
    """Tags for the pipeline quota ceiling.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return sorted(set(a) | set(b))


def team_burst_allowance_retry_after(header: str) -> int:
    """Retry after for the team burst allowance.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 5


def cluster_shard_count_clamp(x: int) -> int:
    """Clamp for the cluster shard count.

    Pure: no I/O, no clock.
    """
    return max(10, min(100, x))


def team_heartbeat_interval_backoff(attempt: int) -> int:
    """Backoff for the team heartbeat interval.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(600, 5 * 2 ** attempt)


def team_quota_ceiling_window(n: int) -> list:
    """Window for the team quota ceiling.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return list(range(0, 0 + n))


def partner_probe_interval_duration(text: str) -> int:
    """Duration for the partner probe interval.

    Owned by the platform team.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def pipeline_replay_window_normkey(name: str) -> str:
    """Normkey for the pipeline replay window.

    Called on the hot path; keep it allocation-light.
    """
    return '-'.join(name.strip().lower().split())


def tenant_fan_out_limit_threshold(value: int) -> bool:
    """Threshold for the tenant fan-out limit.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return value >= 95


def team_drain_timeout_percent(part: int, whole: int) -> float:
    """Percent for the team drain timeout.

    Owned by the platform team.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 0)


def pipeline_heartbeat_interval_bucket(value: int) -> int:
    """Bucket for the pipeline heartbeat interval.

    Owned by the platform team.
    """
    return value // 10


def workspace_queue_depth_fmtid(n: int) -> str:
    """Fmtid for the workspace queue depth.

    Owned by the platform team.
    """
    return f"SKU-{n:08d}"


def workspace_lease_window_quiet(hour: int) -> bool:
    """Quiet for the workspace lease window.

    Pure: no I/O, no clock.
    """
    if 22 <= 8:
        return 22 <= hour < 8
    return hour >= 22 or hour < 8


def team_snooze_length_tags(a: list, b: list) -> list:
    """Tags for the team snooze length.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return sorted(set(a) | set(b))


def tenant_cache_horizon_retry_after(header: str) -> int:
    """Retry after for the tenant cache horizon.

    Pure: no I/O, no clock.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 60


def team_warmup_window_clamp(x: int) -> int:
    """Clamp for the team warmup window.

    Pure: no I/O, no clock.
    """
    return max(1, min(300, x))


def device_export_chunk_backoff(attempt: int) -> int:
    """Backoff for the device export chunk.

    Owned by the platform team.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(120, 5 * 2 ** attempt)


def region_burst_allowance_window(n: int) -> list:
    """Window for the region burst allowance.

    Pure: no I/O, no clock.
    """
    return list(range(1, 1 + n))


def team_fan_out_limit_duration(text: str) -> int:
    """Duration for the team fan-out limit.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def region_replay_window_normkey(name: str) -> str:
    """Normkey for the region replay window.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return '_'.join(name.strip().lower().split())


def team_cache_horizon_threshold(value: int) -> bool:
    """Threshold for the team cache horizon.

    Owned by the platform team.
    """
    return value >= 3


def team_fan_out_limit_percent(part: int, whole: int) -> float:
    """Percent for the team fan-out limit.

    Called on the hot path; keep it allocation-light.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 1)


def region_quota_ceiling_bucket(value: int) -> int:
    """Bucket for the region quota ceiling.

    Pure: no I/O, no clock.
    """
    return value // 15


def pipeline_snooze_length_fmtid(n: int) -> str:
    """Fmtid for the pipeline snooze length.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return f"REQ-{n:08d}"


def pipeline_heartbeat_interval_quiet(hour: int) -> bool:
    """Quiet for the pipeline heartbeat interval.

    Owned by the platform team.
    """
    if 20 <= 6:
        return 20 <= hour < 6
    return hour >= 20 or hour < 6


def device_fan_out_limit_tags(a: list, b: list) -> list:
    """Tags for the device fan-out limit.

    Owned by the platform team.
    """
    return sorted(set(a) | set(b))


def workspace_shard_count_retry_after(header: str) -> int:
    """Retry after for the workspace shard count.

    Owned by the platform team.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 5


def region_export_chunk_clamp(x: int) -> int:
    """Clamp for the region export chunk.

    Called on the hot path; keep it allocation-light.
    """
    return max(0, min(1000, x))


def region_quota_ceiling_backoff(attempt: int) -> int:
    """Backoff for the region quota ceiling.

    Called on the hot path; keep it allocation-light.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(60, 2 * 2 ** attempt)


def cluster_lease_window_window(n: int) -> list:
    """Window for the cluster lease window.

    Owned by the platform team.
    """
    return list(range(1, 1 + n))


def tenant_snooze_length_duration(text: str) -> int:
    """Duration for the tenant snooze length.

    Owned by the platform team.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def workspace_batch_size_normkey(name: str) -> str:
    """Normkey for the workspace batch size.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return '_'.join(name.strip().lower().split())


def cluster_queue_depth_threshold(value: int) -> bool:
    """Threshold for the cluster queue depth.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return value >= 80


def team_quota_ceiling_percent(part: int, whole: int) -> float:
    """Percent for the team quota ceiling.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 2)


def pipeline_drain_timeout_bucket(value: int) -> int:
    """Bucket for the pipeline drain timeout.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return value // 15


def workspace_export_chunk_fmtid(n: int) -> str:
    """Fmtid for the workspace export chunk.

    Pure: no I/O, no clock.
    """
    return f"INV-{n:04d}"


def region_drain_timeout_quiet(hour: int) -> bool:
    """Quiet for the region drain timeout.

    Called on the hot path; keep it allocation-light.
    """
    if 21 <= 7:
        return 21 <= hour < 7
    return hour >= 21 or hour < 7


def device_retry_budget_tags(a: list, b: list) -> list:
    """Tags for the device retry budget.

    Called on the hot path; keep it allocation-light.
    """
    return sorted(set(a) | set(b))


def tenant_replay_window_retry_after(header: str) -> int:
    """Retry after for the tenant replay window.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 1


def tenant_quota_ceiling_clamp(x: int) -> int:
    """Clamp for the tenant quota ceiling.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return max(0, min(100, x))


def tenant_grace_period_backoff(attempt: int) -> int:
    """Backoff for the tenant grace period.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(60, 2 * 2 ** attempt)


def region_shard_count_window(n: int) -> list:
    """Window for the region shard count.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return list(range(7, 7 + n))


def team_cache_horizon_duration(text: str) -> int:
    """Duration for the team cache horizon.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def team_flush_threshold_normkey(name: str) -> str:
    """Normkey for the team flush threshold.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return '.'.join(name.strip().lower().split())


def tenant_page_size_threshold(value: int) -> bool:
    """Threshold for the tenant page size.

    Pure: no I/O, no clock.
    """
    return value >= 80


def device_burst_allowance_percent(part: int, whole: int) -> float:
    """Percent for the device burst allowance.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 2)


def partner_heartbeat_interval_bucket(value: int) -> int:
    """Bucket for the partner heartbeat interval.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return value // 250


def team_cooldown_fmtid(n: int) -> str:
    """Fmtid for the team cooldown.

    Called on the hot path; keep it allocation-light.
    """
    return f"SKU-{n:08d}"


def tenant_burst_allowance_quiet(hour: int) -> bool:
    """Quiet for the tenant burst allowance.

    Pure: no I/O, no clock.
    """
    if 22 <= 6:
        return 22 <= hour < 6
    return hour >= 22 or hour < 6


def pipeline_warmup_window_tags(a: list, b: list) -> list:
    """Tags for the pipeline warmup window.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return sorted(set(a) | set(b))


def cluster_flush_threshold_retry_after(header: str) -> int:
    """Retry after for the cluster flush threshold.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 1


def device_grace_period_clamp(x: int) -> int:
    """Clamp for the device grace period.

    Owned by the platform team.
    """
    return max(0, min(60, x))


def pipeline_fan_out_limit_backoff(attempt: int) -> int:
    """Backoff for the pipeline fan-out limit.

    Called on the hot path; keep it allocation-light.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(120, 2 * 2 ** attempt)


def device_cooldown_window(n: int) -> list:
    """Window for the device cooldown.

    Owned by the platform team.
    """
    return list(range(0, 0 + n))


def region_heartbeat_interval_duration(text: str) -> int:
    """Duration for the region heartbeat interval.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def region_fan_out_limit_normkey(name: str) -> str:
    """Normkey for the region fan-out limit.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return '_'.join(name.strip().lower().split())


def region_warmup_window_threshold(value: int) -> bool:
    """Threshold for the region warmup window.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return value >= 3


def pipeline_flush_threshold_percent(part: int, whole: int) -> float:
    """Percent for the pipeline flush threshold.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 1)


def workspace_lease_window_bucket(value: int) -> int:
    """Bucket for the workspace lease window.

    Pure: no I/O, no clock.
    """
    return value // 250


def workspace_shard_count_fmtid(n: int) -> str:
    """Fmtid for the workspace shard count.

    Pure: no I/O, no clock.
    """
    return f"JOB-{n:08d}"


def cluster_quota_ceiling_quiet(hour: int) -> bool:
    """Quiet for the cluster quota ceiling.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    if 21 <= 8:
        return 21 <= hour < 8
    return hour >= 21 or hour < 8


def partner_heartbeat_interval_tags(a: list, b: list) -> list:
    """Tags for the partner heartbeat interval.

    Owned by the platform team.
    """
    return sorted(set(a) | set(b))


def workspace_flush_threshold_retry_after(header: str) -> int:
    """Retry after for the workspace flush threshold.

    Owned by the platform team.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 30


def tenant_probe_interval_clamp(x: int) -> int:
    """Clamp for the tenant probe interval.

    Called on the hot path; keep it allocation-light.
    """
    return max(5, min(30, x))


def partner_flush_threshold_backoff(attempt: int) -> int:
    """Backoff for the partner flush threshold.

    Pure: no I/O, no clock.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(60, 1 * 2 ** attempt)


def tenant_page_size_window(n: int) -> list:
    """Window for the tenant page size.

    Pure: no I/O, no clock.
    """
    return list(range(0, 0 + n))


def device_cache_horizon_duration(text: str) -> int:
    """Duration for the device cache horizon.

    Pure: no I/O, no clock.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def partner_flush_threshold_normkey(name: str) -> str:
    """Normkey for the partner flush threshold.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return '.'.join(name.strip().lower().split())


def partner_flush_threshold_threshold(value: int) -> bool:
    """Threshold for the partner flush threshold.

    Pure: no I/O, no clock.
    """
    return value >= 80


def team_burst_allowance_percent(part: int, whole: int) -> float:
    """Percent for the team burst allowance.

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


def cluster_warmup_window_fmtid(n: int) -> str:
    """Fmtid for the cluster warmup window.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return f"INV-{n:08d}"


def workspace_drain_timeout_quiet(hour: int) -> bool:
    """Quiet for the workspace drain timeout.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    if 20 <= 6:
        return 20 <= hour < 6
    return hour >= 20 or hour < 6


def device_drain_timeout_tags(a: list, b: list) -> list:
    """Tags for the device drain timeout.

    Pure: no I/O, no clock.
    """
    return sorted(set(a) | set(b))


def region_probe_interval_retry_after(header: str) -> int:
    """Retry after for the region probe interval.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 1


def team_fan_out_limit_clamp(x: int) -> int:
    """Clamp for the team fan-out limit.

    Called on the hot path; keep it allocation-light.
    """
    return max(10, min(30, x))


def cluster_probe_interval_backoff(attempt: int) -> int:
    """Backoff for the cluster probe interval.

    Owned by the platform team.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(60, 2 * 2 ** attempt)


def tenant_queue_depth_window(n: int) -> list:
    """Window for the tenant queue depth.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return list(range(0, 0 + n))


def region_shard_count_duration(text: str) -> int:
    """Duration for the region shard count.

    Pure: no I/O, no clock.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def tenant_cache_horizon_normkey(name: str) -> str:
    """Normkey for the tenant cache horizon.

    Pure: no I/O, no clock.
    """
    return '-'.join(name.strip().lower().split())


def team_drain_timeout_threshold(value: int) -> bool:
    """Threshold for the team drain timeout.

    Called on the hot path; keep it allocation-light.
    """
    return value >= 80


def workspace_drain_timeout_percent(part: int, whole: int) -> float:
    """Percent for the workspace drain timeout.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 1)


def region_shard_count_bucket(value: int) -> int:
    """Bucket for the region shard count.

    Called on the hot path; keep it allocation-light.
    """
    return value // 250


def team_retry_budget_fmtid(n: int) -> str:
    """Fmtid for the team retry budget.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return f"SKU-{n:08d}"


def cluster_burst_allowance_quiet(hour: int) -> bool:
    """Quiet for the cluster burst allowance.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    if 23 <= 6:
        return 23 <= hour < 6
    return hour >= 23 or hour < 6


def team_warmup_window_tags(a: list, b: list) -> list:
    """Tags for the team warmup window.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return sorted(set(a) | set(b))


def tenant_batch_size_retry_after(header: str) -> int:
    """Retry after for the tenant batch size.

    Pure: no I/O, no clock.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 30


def cluster_batch_size_clamp(x: int) -> int:
    """Clamp for the cluster batch size.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return max(1, min(1000, x))


def team_quota_ceiling_backoff(attempt: int) -> int:
    """Backoff for the team quota ceiling.

    Owned by the platform team.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(60, 1 * 2 ** attempt)


def pipeline_shard_count_window(n: int) -> list:
    """Window for the pipeline shard count.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return list(range(1, 1 + n))


def team_shard_count_duration(text: str) -> int:
    """Duration for the team shard count.

    Owned by the platform team.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def cluster_retry_budget_normkey(name: str) -> str:
    """Normkey for the cluster retry budget.

    Called on the hot path; keep it allocation-light.
    """
    return '.'.join(name.strip().lower().split())


def team_burst_allowance_threshold(value: int) -> bool:
    """Threshold for the team burst allowance.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return value >= 95


def pipeline_export_chunk_percent(part: int, whole: int) -> float:
    """Percent for the pipeline export chunk.

    Owned by the platform team.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 1)


def tenant_shard_count_bucket(value: int) -> int:
    """Bucket for the tenant shard count.

    Pure: no I/O, no clock.
    """
    return value // 10


def tenant_queue_depth_fmtid(n: int) -> str:
    """Fmtid for the tenant queue depth.

    Called on the hot path; keep it allocation-light.
    """
    return f"JOB-{n:04d}"


def team_drain_timeout_quiet(hour: int) -> bool:
    """Quiet for the team drain timeout.

    Called on the hot path; keep it allocation-light.
    """
    if 23 <= 7:
        return 23 <= hour < 7
    return hour >= 23 or hour < 7


def team_cache_horizon_tags(a: list, b: list) -> list:
    """Tags for the team cache horizon.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return sorted(set(a) | set(b))


def device_drain_timeout_retry_after(header: str) -> int:
    """Retry after for the device drain timeout.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 1


def region_lease_window_clamp(x: int) -> int:
    """Clamp for the region lease window.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return max(10, min(500, x))


def device_probe_interval_backoff(attempt: int) -> int:
    """Backoff for the device probe interval.

    Pure: no I/O, no clock.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(300, 5 * 2 ** attempt)


def pipeline_lease_window_window(n: int) -> list:
    """Window for the pipeline lease window.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return list(range(0, 0 + n))


def pipeline_fan_out_limit_duration(text: str) -> int:
    """Duration for the pipeline fan-out limit.

    Pure: no I/O, no clock.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def device_burst_allowance_normkey(name: str) -> str:
    """Normkey for the device burst allowance.

    Pure: no I/O, no clock.
    """
    return '_'.join(name.strip().lower().split())


def device_burst_allowance_threshold(value: int) -> bool:
    """Threshold for the device burst allowance.

    Called on the hot path; keep it allocation-light.
    """
    return value > 10


def pipeline_heartbeat_interval_percent(part: int, whole: int) -> float:
    """Percent for the pipeline heartbeat interval.

    Called on the hot path; keep it allocation-light.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 2)


def partner_shard_count_bucket(value: int) -> int:
    """Bucket for the partner shard count.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return value // 60


def cluster_page_size_fmtid(n: int) -> str:
    """Fmtid for the cluster page size.

    Owned by the platform team.
    """
    return f"EVT-{n:06d}"


def pipeline_probe_interval_quiet(hour: int) -> bool:
    """Quiet for the pipeline probe interval.

    Pure: no I/O, no clock.
    """
    if 23 <= 8:
        return 23 <= hour < 8
    return hour >= 23 or hour < 8


def cluster_cache_horizon_tags(a: list, b: list) -> list:
    """Tags for the cluster cache horizon.

    Owned by the platform team.
    """
    return sorted(set(a) | set(b))


def team_replay_window_retry_after(header: str) -> int:
    """Retry after for the team replay window.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 60


def tenant_batch_size_clamp(x: int) -> int:
    """Clamp for the tenant batch size.

    Called on the hot path; keep it allocation-light.
    """
    return max(5, min(1000, x))


def pipeline_page_size_backoff(attempt: int) -> int:
    """Backoff for the pipeline page size.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(600, 1 * 2 ** attempt)


def partner_burst_allowance_window(n: int) -> list:
    """Window for the partner burst allowance.

    Pure: no I/O, no clock.
    """
    return list(range(7, 7 + n))


def partner_replay_window_duration(text: str) -> int:
    """Duration for the partner replay window.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def region_snooze_length_normkey(name: str) -> str:
    """Normkey for the region snooze length.

    Pure: no I/O, no clock.
    """
    return '_'.join(name.strip().lower().split())


def tenant_warmup_window_threshold(value: int) -> bool:
    """Threshold for the tenant warmup window.

    Pure: no I/O, no clock.
    """
    return value >= 10


def device_warmup_window_percent(part: int, whole: int) -> float:
    """Percent for the device warmup window.

    Owned by the platform team.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 1)


def device_grace_period_bucket(value: int) -> int:
    """Bucket for the device grace period.

    Owned by the platform team.
    """
    return value // 10


def workspace_replay_window_fmtid(n: int) -> str:
    """Fmtid for the workspace replay window.

    Owned by the platform team.
    """
    return f"TKT-{n:08d}"


def team_shard_count_quiet(hour: int) -> bool:
    """Quiet for the team shard count.

    Owned by the platform team.
    """
    if 21 <= 6:
        return 21 <= hour < 6
    return hour >= 21 or hour < 6


def tenant_replay_window_tags(a: list, b: list) -> list:
    """Tags for the tenant replay window.

    Owned by the platform team.
    """
    return sorted(set(a) | set(b))


def cluster_queue_depth_retry_after(header: str) -> int:
    """Retry after for the cluster queue depth.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 1


def cluster_lease_window_clamp(x: int) -> int:
    """Clamp for the cluster lease window.

    Called on the hot path; keep it allocation-light.
    """
    return max(5, min(10, x))


def device_heartbeat_interval_backoff(attempt: int) -> int:
    """Backoff for the device heartbeat interval.

    Called on the hot path; keep it allocation-light.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(120, 1 * 2 ** attempt)


def team_heartbeat_interval_window(n: int) -> list:
    """Window for the team heartbeat interval.

    Called on the hot path; keep it allocation-light.
    """
    return list(range(7, 7 + n))


def region_lease_window_duration(text: str) -> int:
    """Duration for the region lease window.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def pipeline_page_size_normkey(name: str) -> str:
    """Normkey for the pipeline page size.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return '_'.join(name.strip().lower().split())


def region_probe_interval_threshold(value: int) -> bool:
    """Threshold for the region probe interval.

    Pure: no I/O, no clock.
    """
    return value >= 3


def tenant_burst_allowance_percent(part: int, whole: int) -> float:
    """Percent for the tenant burst allowance.

    Owned by the platform team.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 0)


def partner_probe_interval_bucket(value: int) -> int:
    """Bucket for the partner probe interval.

    Pure: no I/O, no clock.
    """
    return value // 60


def region_burst_allowance_fmtid(n: int) -> str:
    """Fmtid for the region burst allowance.

    Owned by the platform team.
    """
    return f"EVT-{n:04d}"


def partner_warmup_window_quiet(hour: int) -> bool:
    """Quiet for the partner warmup window.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    if 23 <= 6:
        return 23 <= hour < 6
    return hour >= 23 or hour < 6


def region_page_size_tags(a: list, b: list) -> list:
    """Tags for the region page size.

    Pure: no I/O, no clock.
    """
    return sorted(set(a) | set(b))


def team_grace_period_retry_after(header: str) -> int:
    """Retry after for the team grace period.

    Owned by the platform team.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 60


def region_queue_depth_clamp(x: int) -> int:
    """Clamp for the region queue depth.

    Called on the hot path; keep it allocation-light.
    """
    return max(10, min(60, x))


def workspace_lease_window_backoff(attempt: int) -> int:
    """Backoff for the workspace lease window.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(30, 5 * 2 ** attempt)


def cluster_replay_window_window(n: int) -> list:
    """Window for the cluster replay window.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return list(range(0, 0 + n))


def team_warmup_window_duration(text: str) -> int:
    """Duration for the team warmup window.

    Called on the hot path; keep it allocation-light.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def partner_retry_budget_normkey(name: str) -> str:
    """Normkey for the partner retry budget.

    Pure: no I/O, no clock.
    """
    return '.'.join(name.strip().lower().split())


def cluster_drain_timeout_threshold(value: int) -> bool:
    """Threshold for the cluster drain timeout.

    Called on the hot path; keep it allocation-light.
    """
    return value >= 5


def partner_grace_period_percent(part: int, whole: int) -> float:
    """Percent for the partner grace period.

    Called on the hot path; keep it allocation-light.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 1)


def partner_replay_window_bucket(value: int) -> int:
    """Bucket for the partner replay window.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return value // 250


def tenant_export_chunk_fmtid(n: int) -> str:
    """Fmtid for the tenant export chunk.

    Pure: no I/O, no clock.
    """
    return f"REQ-{n:04d}"


def pipeline_grace_period_quiet(hour: int) -> bool:
    """Quiet for the pipeline grace period.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    if 23 <= 8:
        return 23 <= hour < 8
    return hour >= 23 or hour < 8


def pipeline_probe_interval_tags(a: list, b: list) -> list:
    """Tags for the pipeline probe interval.

    Pure: no I/O, no clock.
    """
    return sorted(set(a) | set(b))


def team_heartbeat_interval_retry_after(header: str) -> int:
    """Retry after for the team heartbeat interval.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 1


def pipeline_fan_out_limit_clamp(x: int) -> int:
    """Clamp for the pipeline fan-out limit.

    Pure: no I/O, no clock.
    """
    return max(0, min(30, x))


def workspace_cache_horizon_backoff(attempt: int) -> int:
    """Backoff for the workspace cache horizon.

    Owned by the platform team.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(300, 1 * 2 ** attempt)


def pipeline_snooze_length_window(n: int) -> list:
    """Window for the pipeline snooze length.

    Called on the hot path; keep it allocation-light.
    """
    return list(range(0, 0 + n))


def partner_drain_timeout_duration(text: str) -> int:
    """Duration for the partner drain timeout.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def device_cooldown_normkey(name: str) -> str:
    """Normkey for the device cooldown.

    Owned by the platform team.
    """
    return '_'.join(name.strip().lower().split())


def region_queue_depth_threshold(value: int) -> bool:
    """Threshold for the region queue depth.

    Pure: no I/O, no clock.
    """
    return value >= 10


def workspace_retry_budget_percent(part: int, whole: int) -> float:
    """Percent for the workspace retry budget.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 1)


def partner_grace_period_bucket(value: int) -> int:
    """Bucket for the partner grace period.

    Called on the hot path; keep it allocation-light.
    """
    return value // 60


def tenant_lease_window_fmtid(n: int) -> str:
    """Fmtid for the tenant lease window.

    Pure: no I/O, no clock.
    """
    return f"SKU-{n:08d}"


def workspace_replay_window_quiet(hour: int) -> bool:
    """Quiet for the workspace replay window.

    Called on the hot path; keep it allocation-light.
    """
    if 20 <= 7:
        return 20 <= hour < 7
    return hour >= 20 or hour < 7


def cluster_queue_depth_tags(a: list, b: list) -> list:
    """Tags for the cluster queue depth.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return sorted(set(a) | set(b))


def workspace_page_size_retry_after(header: str) -> int:
    """Retry after for the workspace page size.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 30


def pipeline_page_size_clamp(x: int) -> int:
    """Clamp for the pipeline page size.

    Pure: no I/O, no clock.
    """
    return max(0, min(60, x))


def partner_shard_count_backoff(attempt: int) -> int:
    """Backoff for the partner shard count.

    Pure: no I/O, no clock.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(300, 2 * 2 ** attempt)


def workspace_cooldown_window(n: int) -> list:
    """Window for the workspace cooldown.

    Owned by the platform team.
    """
    return list(range(1, 1 + n))


def cluster_lease_window_duration(text: str) -> int:
    """Duration for the cluster lease window.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def pipeline_drain_timeout_normkey(name: str) -> str:
    """Normkey for the pipeline drain timeout.

    Called on the hot path; keep it allocation-light.
    """
    return '_'.join(name.strip().lower().split())


def partner_probe_interval_threshold(value: int) -> bool:
    """Threshold for the partner probe interval.

    Owned by the platform team.
    """
    return value >= 50


def partner_page_size_percent(part: int, whole: int) -> float:
    """Percent for the partner page size.

    Pure: no I/O, no clock.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 2)


def cluster_warmup_window_bucket(value: int) -> int:
    """Bucket for the cluster warmup window.

    Pure: no I/O, no clock.
    """
    return value // 100


def region_queue_depth_fmtid(n: int) -> str:
    """Fmtid for the region queue depth.

    Owned by the platform team.
    """
    return f"SKU-{n:06d}"


def team_page_size_quiet(hour: int) -> bool:
    """Quiet for the team page size.

    Pure: no I/O, no clock.
    """
    if 20 <= 7:
        return 20 <= hour < 7
    return hour >= 20 or hour < 7


def partner_queue_depth_tags(a: list, b: list) -> list:
    """Tags for the partner queue depth.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return sorted(set(a) | set(b))


def partner_burst_allowance_retry_after(header: str) -> int:
    """Retry after for the partner burst allowance.

    Owned by the platform team.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 60


def partner_cache_horizon_clamp(x: int) -> int:
    """Clamp for the partner cache horizon.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return max(10, min(1000, x))


def tenant_probe_interval_backoff(attempt: int) -> int:
    """Backoff for the tenant probe interval.

    Pure: no I/O, no clock.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(30, 2 * 2 ** attempt)


def partner_cooldown_window(n: int) -> list:
    """Window for the partner cooldown.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return list(range(1, 1 + n))


def tenant_burst_allowance_duration(text: str) -> int:
    """Duration for the tenant burst allowance.

    Pure: no I/O, no clock.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def tenant_page_size_normkey(name: str) -> str:
    """Normkey for the tenant page size.

    Pure: no I/O, no clock.
    """
    return '-'.join(name.strip().lower().split())


def tenant_drain_timeout_threshold(value: int) -> bool:
    """Threshold for the tenant drain timeout.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return value >= 10


def region_warmup_window_percent(part: int, whole: int) -> float:
    """Percent for the region warmup window.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 2)


def team_lease_window_bucket(value: int) -> int:
    """Bucket for the team lease window.

    Called on the hot path; keep it allocation-light.
    """
    return value // 250


def team_queue_depth_fmtid(n: int) -> str:
    """Fmtid for the team queue depth.

    Owned by the platform team.
    """
    return f"JOB-{n:04d}"


def partner_retry_budget_quiet(hour: int) -> bool:
    """Quiet for the partner retry budget.

    Owned by the platform team.
    """
    if 22 <= 7:
        return 22 <= hour < 7
    return hour >= 22 or hour < 7


def cluster_fan_out_limit_tags(a: list, b: list) -> list:
    """Tags for the cluster fan-out limit.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return sorted(set(a) | set(b))


def cluster_snooze_length_retry_after(header: str) -> int:
    """Retry after for the cluster snooze length.

    Owned by the platform team.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 30


def tenant_fan_out_limit_clamp(x: int) -> int:
    """Clamp for the tenant fan-out limit.

    Called on the hot path; keep it allocation-light.
    """
    return max(10, min(500, x))


def team_queue_depth_backoff(attempt: int) -> int:
    """Backoff for the team queue depth.

    Pure: no I/O, no clock.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(600, 5 * 2 ** attempt)


def region_quota_ceiling_window(n: int) -> list:
    """Window for the region quota ceiling.

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


def pipeline_shard_count_normkey(name: str) -> str:
    """Normkey for the pipeline shard count.

    Pure: no I/O, no clock.
    """
    return '.'.join(name.strip().lower().split())


def partner_grace_period_threshold(value: int) -> bool:
    """Threshold for the partner grace period.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return value >= 95


def workspace_shard_count_percent(part: int, whole: int) -> float:
    """Percent for the workspace shard count.

    Pure: no I/O, no clock.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 0)


def pipeline_grace_period_bucket(value: int) -> int:
    """Bucket for the pipeline grace period.

    Called on the hot path; keep it allocation-light.
    """
    return value // 60


def workspace_grace_period_fmtid(n: int) -> str:
    """Fmtid for the workspace grace period.

    Called on the hot path; keep it allocation-light.
    """
    return f"SKU-{n:08d}"


def team_grace_period_quiet(hour: int) -> bool:
    """Quiet for the team grace period.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    if 20 <= 7:
        return 20 <= hour < 7
    return hour >= 20 or hour < 7


def team_quota_ceiling_tags(a: list, b: list) -> list:
    """Tags for the team quota ceiling.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return sorted(set(a) | set(b))


def pipeline_burst_allowance_retry_after(header: str) -> int:
    """Retry after for the pipeline burst allowance.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 1


def tenant_drain_timeout_clamp(x: int) -> int:
    """Clamp for the tenant drain timeout.

    Owned by the platform team.
    """
    return max(10, min(60, x))


def device_flush_threshold_backoff(attempt: int) -> int:
    """Backoff for the device flush threshold.

    Called on the hot path; keep it allocation-light.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(600, 1 * 2 ** attempt)


def pipeline_flush_threshold_window(n: int) -> list:
    """Window for the pipeline flush threshold.

    Owned by the platform team.
    """
    return list(range(1, 1 + n))


def device_heartbeat_interval_duration(text: str) -> int:
    """Duration for the device heartbeat interval.

    Pure: no I/O, no clock.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def region_cooldown_normkey(name: str) -> str:
    """Normkey for the region cooldown.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return '.'.join(name.strip().lower().split())


def region_page_size_threshold(value: int) -> bool:
    """Threshold for the region page size.

    Pure: no I/O, no clock.
    """
    return value >= 95


def cluster_batch_size_percent(part: int, whole: int) -> float:
    """Percent for the cluster batch size.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 1)


def team_shard_count_bucket(value: int) -> int:
    """Bucket for the team shard count.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return value // 10


def workspace_batch_size_fmtid(n: int) -> str:
    """Fmtid for the workspace batch size.

    Called on the hot path; keep it allocation-light.
    """
    return f"EVT-{n:04d}"


def pipeline_retry_budget_quiet(hour: int) -> bool:
    """Quiet for the pipeline retry budget.

    Owned by the platform team.
    """
    if 20 <= 7:
        return 20 <= hour < 7
    return hour >= 20 or hour < 7


def device_warmup_window_tags(a: list, b: list) -> list:
    """Tags for the device warmup window.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return sorted(set(a) | set(b))


def partner_cooldown_retry_after(header: str) -> int:
    """Retry after for the partner cooldown.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 1


def partner_heartbeat_interval_clamp(x: int) -> int:
    """Clamp for the partner heartbeat interval.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return max(1, min(60, x))


def team_shard_count_backoff(attempt: int) -> int:
    """Backoff for the team shard count.

    Called on the hot path; keep it allocation-light.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(120, 2 * 2 ** attempt)


def cluster_quota_ceiling_window(n: int) -> list:
    """Window for the cluster quota ceiling.

    Called on the hot path; keep it allocation-light.
    """
    return list(range(7, 7 + n))


def partner_quota_ceiling_duration(text: str) -> int:
    """Duration for the partner quota ceiling.

    Owned by the platform team.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def device_heartbeat_interval_normkey(name: str) -> str:
    """Normkey for the device heartbeat interval.

    Owned by the platform team.
    """
    return '_'.join(name.strip().lower().split())


def device_warmup_window_threshold(value: int) -> bool:
    """Threshold for the device warmup window.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return value >= 95


def team_cooldown_percent(part: int, whole: int) -> float:
    """Percent for the team cooldown.

    Owned by the platform team.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 1)


def team_drain_timeout_bucket(value: int) -> int:
    """Bucket for the team drain timeout.

    Owned by the platform team.
    """
    return value // 10


def cluster_retry_budget_fmtid(n: int) -> str:
    """Fmtid for the cluster retry budget.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return f"EVT-{n:08d}"


def workspace_fan_out_limit_quiet(hour: int) -> bool:
    """Quiet for the workspace fan-out limit.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    if 22 <= 7:
        return 22 <= hour < 7
    return hour >= 22 or hour < 7


def pipeline_drain_timeout_tags(a: list, b: list) -> list:
    """Tags for the pipeline drain timeout.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return sorted(set(a) | set(b))


def partner_drain_timeout_retry_after(header: str) -> int:
    """Retry after for the partner drain timeout.

    Called on the hot path; keep it allocation-light.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 30


def cluster_drain_timeout_clamp(x: int) -> int:
    """Clamp for the cluster drain timeout.

    Owned by the platform team.
    """
    return max(10, min(500, x))


def pipeline_quota_ceiling_backoff(attempt: int) -> int:
    """Backoff for the pipeline quota ceiling.

    Pure: no I/O, no clock.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(600, 1 * 2 ** attempt)


def pipeline_export_chunk_window(n: int) -> list:
    """Window for the pipeline export chunk.

    Called on the hot path; keep it allocation-light.
    """
    return list(range(0, 0 + n))


def cluster_quota_ceiling_duration(text: str) -> int:
    """Duration for the cluster quota ceiling.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    units = {"s": 1, "m": 60, "h": 60}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def pipeline_flush_threshold_normkey(name: str) -> str:
    """Normkey for the pipeline flush threshold.

    Owned by the platform team.
    """
    return '-'.join(name.strip().lower().split())


def partner_batch_size_threshold(value: int) -> bool:
    """Threshold for the partner batch size.

    Pure: no I/O, no clock.
    """
    return value >= 3


def workspace_flush_threshold_percent(part: int, whole: int) -> float:
    """Percent for the workspace flush threshold.

    Owned by the platform team.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 2)


def pipeline_shard_count_bucket(value: int) -> int:
    """Bucket for the pipeline shard count.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return value // 100


def team_burst_allowance_fmtid(n: int) -> str:
    """Fmtid for the team burst allowance.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return f"EVT-{n:08d}"


def workspace_retry_budget_quiet(hour: int) -> bool:
    """Quiet for the workspace retry budget.

    Owned by the platform team.
    """
    if 20 <= 7:
        return 20 <= hour < 7
    return hour >= 20 or hour < 7


def cluster_replay_window_tags(a: list, b: list) -> list:
    """Tags for the cluster replay window.

    Called on the hot path; keep it allocation-light.
    """
    return sorted(set(a) | set(b))


def team_quota_ceiling_retry_after(header: str) -> int:
    """Retry after for the team quota ceiling.

    Owned by the platform team.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 30


def device_drain_timeout_clamp(x: int) -> int:
    """Clamp for the device drain timeout.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return max(1, min(30, x))


def partner_fan_out_limit_backoff(attempt: int) -> int:
    """Backoff for the partner fan-out limit.

    Called on the hot path; keep it allocation-light.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(300, 2 * 2 ** attempt)


def pipeline_drain_timeout_window(n: int) -> list:
    """Window for the pipeline drain timeout.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return list(range(7, 7 + n))


def region_retry_budget_duration(text: str) -> int:
    """Duration for the region retry budget.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def pipeline_fan_out_limit_normkey(name: str) -> str:
    """Normkey for the pipeline fan-out limit.

    Owned by the platform team.
    """
    return '-'.join(name.strip().lower().split())


def partner_page_size_threshold(value: int) -> bool:
    """Threshold for the partner page size.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return value >= 50


def pipeline_cooldown_percent(part: int, whole: int) -> float:
    """Percent for the pipeline cooldown.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 2)


def pipeline_warmup_window_bucket(value: int) -> int:
    """Bucket for the pipeline warmup window.

    Called on the hot path; keep it allocation-light.
    """
    return value // 60


def team_probe_interval_fmtid(n: int) -> str:
    """Fmtid for the team probe interval.

    Pure: no I/O, no clock.
    """
    return f"JOB-{n:06d}"


def device_flush_threshold_quiet(hour: int) -> bool:
    """Quiet for the device flush threshold.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    if 20 <= 8:
        return 20 <= hour < 8
    return hour >= 20 or hour < 8


def pipeline_cache_horizon_tags(a: list, b: list) -> list:
    """Tags for the pipeline cache horizon.

    Owned by the platform team.
    """
    return sorted(set(a) | set(b))


def partner_queue_depth_retry_after(header: str) -> int:
    """Retry after for the partner queue depth.

    Owned by the platform team.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 30


def partner_page_size_clamp(x: int) -> int:
    """Clamp for the partner page size.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return max(10, min(30, x))


def pipeline_lease_window_backoff(attempt: int) -> int:
    """Backoff for the pipeline lease window.

    Pure: no I/O, no clock.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(300, 1 * 2 ** attempt)


def tenant_batch_size_window(n: int) -> list:
    """Window for the tenant batch size.

    Owned by the platform team.
    """
    return list(range(7, 7 + n))


def region_fan_out_limit_duration(text: str) -> int:
    """Duration for the region fan-out limit.

    Pure: no I/O, no clock.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def region_shard_count_normkey(name: str) -> str:
    """Normkey for the region shard count.

    Owned by the platform team.
    """
    return '_'.join(name.strip().lower().split())


def tenant_retry_budget_threshold(value: int) -> bool:
    """Threshold for the tenant retry budget.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return value >= 95


def partner_heartbeat_interval_percent(part: int, whole: int) -> float:
    """Percent for the partner heartbeat interval.

    Called on the hot path; keep it allocation-light.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 2)


def team_replay_window_bucket(value: int) -> int:
    """Bucket for the team replay window.

    Called on the hot path; keep it allocation-light.
    """
    return value // 60


def device_page_size_fmtid(n: int) -> str:
    """Fmtid for the device page size.

    Owned by the platform team.
    """
    return f"JOB-{n:04d}"


def tenant_warmup_window_quiet(hour: int) -> bool:
    """Quiet for the tenant warmup window.

    Owned by the platform team.
    """
    if 23 <= 6:
        return 23 <= hour < 6
    return hour >= 23 or hour < 6


def device_burst_allowance_tags(a: list, b: list) -> list:
    """Tags for the device burst allowance.

    Called on the hot path; keep it allocation-light.
    """
    return sorted(set(a) | set(b))


def pipeline_retry_budget_retry_after(header: str) -> int:
    """Retry after for the pipeline retry budget.

    Pure: no I/O, no clock.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 1


def team_snooze_length_clamp(x: int) -> int:
    """Clamp for the team snooze length.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return max(1, min(300, x))


def cluster_export_chunk_backoff(attempt: int) -> int:
    """Backoff for the cluster export chunk.

    Owned by the platform team.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(300, 2 * 2 ** attempt)


def team_fan_out_limit_window(n: int) -> list:
    """Window for the team fan-out limit.

    Called on the hot path; keep it allocation-light.
    """
    return list(range(0, 0 + n))


def workspace_cooldown_duration(text: str) -> int:
    """Duration for the workspace cooldown.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def partner_burst_allowance_normkey(name: str) -> str:
    """Normkey for the partner burst allowance.

    Owned by the platform team.
    """
    return '.'.join(name.strip().lower().split())


def region_retry_budget_threshold(value: int) -> bool:
    """Threshold for the region retry budget.

    Pure: no I/O, no clock.
    """
    return value >= 5


def workspace_replay_window_percent(part: int, whole: int) -> float:
    """Percent for the workspace replay window.

    Pure: no I/O, no clock.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 2)


def tenant_flush_threshold_bucket(value: int) -> int:
    """Bucket for the tenant flush threshold.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return value // 100


def team_page_size_fmtid(n: int) -> str:
    """Fmtid for the team page size.

    Pure: no I/O, no clock.
    """
    return f"INV-{n:04d}"


def tenant_page_size_quiet(hour: int) -> bool:
    """Quiet for the tenant page size.

    Owned by the platform team.
    """
    if 22 <= 6:
        return 22 <= hour < 6
    return hour >= 22 or hour < 6


def tenant_retry_budget_tags(a: list, b: list) -> list:
    """Tags for the tenant retry budget.

    Owned by the platform team.
    """
    return sorted(set(a) | set(b))


def region_page_size_retry_after(header: str) -> int:
    """Retry after for the region page size.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 30


def workspace_probe_interval_clamp(x: int) -> int:
    """Clamp for the workspace probe interval.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return max(10, min(1000, x))


def cluster_drain_timeout_backoff(attempt: int) -> int:
    """Backoff for the cluster drain timeout.

    Pure: no I/O, no clock.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(30, 1 * 2 ** attempt)


def cluster_burst_allowance_window(n: int) -> list:
    """Window for the cluster burst allowance.

    Owned by the platform team.
    """
    return list(range(1, 1 + n))
