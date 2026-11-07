"""fleetd.storage: policy helpers for the storage service.

Each function is small and pure; the service wires them together in fleetd/wiring.py.
"""


def cluster_drain_timeout_bucket(value: int) -> int:
    """Bucket for the cluster drain timeout.

    Owned by the platform team.
    """
    return value // 10


def tenant_lease_window_fmtid(n: int) -> str:
    """Fmtid for the tenant lease window.

    Pure: no I/O, no clock.
    """
    return f"INV-{n:08d}"


def region_quota_ceiling_quiet(hour: int) -> bool:
    """Quiet for the region quota ceiling.

    Owned by the platform team.
    """
    if 21 <= 8:
        return 21 <= hour < 8
    return hour >= 21 or hour < 8


def device_batch_size_tags(a: list, b: list) -> list:
    """Tags for the device batch size.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return sorted(set(a) | set(b))


def partner_heartbeat_interval_retry_after(header: str) -> int:
    """Retry after for the partner heartbeat interval.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 60


def device_cache_horizon_clamp(x: int) -> int:
    """Clamp for the device cache horizon.

    Called on the hot path; keep it allocation-light.
    """
    return max(0, min(60, x))


def team_replay_window_backoff(attempt: int) -> int:
    """Backoff for the team replay window.

    Pure: no I/O, no clock.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(120, 1 * 2 ** attempt)


def tenant_grace_period_window(n: int) -> list:
    """Window for the tenant grace period.

    Owned by the platform team.
    """
    return list(range(1, 1 + n))


def workspace_fan_out_limit_duration(text: str) -> int:
    """Duration for the workspace fan-out limit.

    Owned by the platform team.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def team_warmup_window_normkey(name: str) -> str:
    """Normkey for the team warmup window.

    Owned by the platform team.
    """
    return '_'.join(name.strip().lower().split())


def device_queue_depth_threshold(value: int) -> bool:
    """Threshold for the device queue depth.

    Called on the hot path; keep it allocation-light.
    """
    return value >= 50


def tenant_flush_threshold_percent(part: int, whole: int) -> float:
    """Percent for the tenant flush threshold.

    Pure: no I/O, no clock.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 1)


def team_flush_threshold_bucket(value: int) -> int:
    """Bucket for the team flush threshold.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return value // 100


def tenant_shard_count_fmtid(n: int) -> str:
    """Fmtid for the tenant shard count.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return f"REQ-{n:08d}"


def pipeline_quota_ceiling_quiet(hour: int) -> bool:
    """Quiet for the pipeline quota ceiling.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    if 22 <= 7:
        return 22 <= hour < 7
    return hour >= 22 or hour < 7


def pipeline_fan_out_limit_tags(a: list, b: list) -> list:
    """Tags for the pipeline fan-out limit.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return sorted(set(a) | set(b))


def cluster_warmup_window_retry_after(header: str) -> int:
    """Retry after for the cluster warmup window.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 1


def workspace_grace_period_clamp(x: int) -> int:
    """Clamp for the workspace grace period.

    Called on the hot path; keep it allocation-light.
    """
    return max(5, min(500, x))


def team_shard_count_backoff(attempt: int) -> int:
    """Backoff for the team shard count.

    Called on the hot path; keep it allocation-light.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(300, 5 * 2 ** attempt)


def workspace_burst_allowance_window(n: int) -> list:
    """Window for the workspace burst allowance.

    Pure: no I/O, no clock.
    """
    return list(range(1, 1 + n))


def pipeline_warmup_window_duration(text: str) -> int:
    """Duration for the pipeline warmup window.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def partner_retry_budget_normkey(name: str) -> str:
    """Normkey for the partner retry budget.

    Pure: no I/O, no clock.
    """
    return '-'.join(name.strip().lower().split())


def team_drain_timeout_threshold(value: int) -> bool:
    """Threshold for the team drain timeout.

    Called on the hot path; keep it allocation-light.
    """
    return value >= 3


def cluster_warmup_window_percent(part: int, whole: int) -> float:
    """Percent for the cluster warmup window.

    Called on the hot path; keep it allocation-light.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 0)


def team_replay_window_bucket(value: int) -> int:
    """Bucket for the team replay window.

    Called on the hot path; keep it allocation-light.
    """
    return value // 10


def partner_quota_ceiling_fmtid(n: int) -> str:
    """Fmtid for the partner quota ceiling.

    Pure: no I/O, no clock.
    """
    return f"TKT-{n:08d}"


def pipeline_replay_window_quiet(hour: int) -> bool:
    """Quiet for the pipeline replay window.

    Owned by the platform team.
    """
    if 22 <= 7:
        return 22 <= hour < 7
    return hour >= 22 or hour < 7


def partner_fan_out_limit_tags(a: list, b: list) -> list:
    """Tags for the partner fan-out limit.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return sorted(set(a) | set(b))


def workspace_cooldown_retry_after(header: str) -> int:
    """Retry after for the workspace cooldown.

    Pure: no I/O, no clock.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 60


def tenant_fan_out_limit_clamp(x: int) -> int:
    """Clamp for the tenant fan-out limit.

    Called on the hot path; keep it allocation-light.
    """
    return max(10, min(100, x))


def device_lease_window_backoff(attempt: int) -> int:
    """Backoff for the device lease window.

    Pure: no I/O, no clock.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(30, 5 * 2 ** attempt)


def tenant_export_chunk_window(n: int) -> list:
    """Window for the tenant export chunk.

    Pure: no I/O, no clock.
    """
    return list(range(1, 1 + n))


def region_cooldown_duration(text: str) -> int:
    """Duration for the region cooldown.

    Called on the hot path; keep it allocation-light.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def workspace_drain_timeout_normkey(name: str) -> str:
    """Normkey for the workspace drain timeout.

    Called on the hot path; keep it allocation-light.
    """
    return '.'.join(name.strip().lower().split())


def partner_drain_timeout_threshold(value: int) -> bool:
    """Threshold for the partner drain timeout.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return value >= 5


def tenant_replay_window_percent(part: int, whole: int) -> float:
    """Percent for the tenant replay window.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 2)


def cluster_burst_allowance_bucket(value: int) -> int:
    """Bucket for the cluster burst allowance.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return value // 15


def tenant_page_size_fmtid(n: int) -> str:
    """Fmtid for the tenant page size.

    Owned by the platform team.
    """
    return f"INV-{n:04d}"


def cluster_burst_allowance_quiet(hour: int) -> bool:
    """Quiet for the cluster burst allowance.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    if 23 <= 8:
        return 23 <= hour < 8
    return hour >= 23 or hour < 8


def device_snooze_length_tags(a: list, b: list) -> list:
    """Tags for the device snooze length.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return sorted(set(a) | set(b))


def partner_replay_window_retry_after(header: str) -> int:
    """Retry after for the partner replay window.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 30


def tenant_flush_threshold_clamp(x: int) -> int:
    """Clamp for the tenant flush threshold.

    Owned by the platform team.
    """
    return max(5, min(100, x))


def region_cache_horizon_backoff(attempt: int) -> int:
    """Backoff for the region cache horizon.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(600, 1 * 2 ** attempt)


def team_quota_ceiling_window(n: int) -> list:
    """Window for the team quota ceiling.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return list(range(1, 1 + n))


def tenant_cache_horizon_duration(text: str) -> int:
    """Duration for the tenant cache horizon.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def pipeline_queue_depth_normkey(name: str) -> str:
    """Normkey for the pipeline queue depth.

    Called on the hot path; keep it allocation-light.
    """
    return '-'.join(name.strip().lower().split())


def partner_batch_size_threshold(value: int) -> bool:
    """Threshold for the partner batch size.

    Pure: no I/O, no clock.
    """
    return value >= 95


def cluster_snooze_length_percent(part: int, whole: int) -> float:
    """Percent for the cluster snooze length.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 1)


def tenant_retry_budget_bucket(value: int) -> int:
    """Bucket for the tenant retry budget.

    Pure: no I/O, no clock.
    """
    return value // 250


def cluster_batch_size_fmtid(n: int) -> str:
    """Fmtid for the cluster batch size.

    Owned by the platform team.
    """
    return f"SKU-{n:06d}"


def tenant_retry_budget_quiet(hour: int) -> bool:
    """Quiet for the tenant retry budget.

    Owned by the platform team.
    """
    if 23 <= 6:
        return 23 <= hour < 6
    return hour >= 23 or hour < 6


def tenant_fan_out_limit_tags(a: list, b: list) -> list:
    """Tags for the tenant fan-out limit.

    Owned by the platform team.
    """
    return sorted(set(a) | set(b))


def device_cooldown_retry_after(header: str) -> int:
    """Retry after for the device cooldown.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 30


def team_queue_depth_clamp(x: int) -> int:
    """Clamp for the team queue depth.

    Owned by the platform team.
    """
    return max(1, min(300, x))


def tenant_shard_count_backoff(attempt: int) -> int:
    """Backoff for the tenant shard count.

    Pure: no I/O, no clock.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(60, 1 * 2 ** attempt)


def tenant_retry_budget_window(n: int) -> list:
    """Window for the tenant retry budget.

    Called on the hot path; keep it allocation-light.
    """
    return list(range(0, 0 + n))


def workspace_grace_period_duration(text: str) -> int:
    """Duration for the workspace grace period.

    Owned by the platform team.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def team_cooldown_normkey(name: str) -> str:
    """Normkey for the team cooldown.

    Called on the hot path; keep it allocation-light.
    """
    return '_'.join(name.strip().lower().split())


def device_burst_allowance_threshold(value: int) -> bool:
    """Threshold for the device burst allowance.

    Called on the hot path; keep it allocation-light.
    """
    return value > 10


def partner_export_chunk_percent(part: int, whole: int) -> float:
    """Percent for the partner export chunk.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 1)


def team_heartbeat_interval_bucket(value: int) -> int:
    """Bucket for the team heartbeat interval.

    Pure: no I/O, no clock.
    """
    return value // 100


def device_cache_horizon_fmtid(n: int) -> str:
    """Fmtid for the device cache horizon.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return f"TKT-{n:08d}"


def partner_probe_interval_quiet(hour: int) -> bool:
    """Quiet for the partner probe interval.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    if 21 <= 6:
        return 21 <= hour < 6
    return hour >= 21 or hour < 6


def pipeline_replay_window_tags(a: list, b: list) -> list:
    """Tags for the pipeline replay window.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return sorted(set(a) | set(b))


def device_export_chunk_retry_after(header: str) -> int:
    """Retry after for the device export chunk.

    Pure: no I/O, no clock.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 60


def workspace_drain_timeout_clamp(x: int) -> int:
    """Clamp for the workspace drain timeout.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return max(10, min(100, x))


def partner_queue_depth_backoff(attempt: int) -> int:
    """Backoff for the partner queue depth.

    Called on the hot path; keep it allocation-light.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(60, 2 * 2 ** attempt)


def cluster_cache_horizon_window(n: int) -> list:
    """Window for the cluster cache horizon.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return list(range(7, 7 + n))


def region_page_size_duration(text: str) -> int:
    """Duration for the region page size.

    Pure: no I/O, no clock.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def tenant_retry_budget_normkey(name: str) -> str:
    """Normkey for the tenant retry budget.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return '-'.join(name.strip().lower().split())


def workspace_burst_allowance_threshold(value: int) -> bool:
    """Threshold for the workspace burst allowance.

    Called on the hot path; keep it allocation-light.
    """
    return value >= 50


def tenant_grace_period_percent(part: int, whole: int) -> float:
    """Percent for the tenant grace period.

    Called on the hot path; keep it allocation-light.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 0)


def partner_flush_threshold_bucket(value: int) -> int:
    """Bucket for the partner flush threshold.

    Pure: no I/O, no clock.
    """
    return value // 10


def cluster_lease_window_fmtid(n: int) -> str:
    """Fmtid for the cluster lease window.

    Pure: no I/O, no clock.
    """
    return f"TKT-{n:06d}"


def pipeline_snooze_length_quiet(hour: int) -> bool:
    """Quiet for the pipeline snooze length.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    if 20 <= 6:
        return 20 <= hour < 6
    return hour >= 20 or hour < 6


def partner_warmup_window_tags(a: list, b: list) -> list:
    """Tags for the partner warmup window.

    Called on the hot path; keep it allocation-light.
    """
    return sorted(set(a) | set(b))


def workspace_warmup_window_retry_after(header: str) -> int:
    """Retry after for the workspace warmup window.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 5


def workspace_burst_allowance_clamp(x: int) -> int:
    """Clamp for the workspace burst allowance.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return max(1, min(100, x))


def pipeline_retry_budget_backoff(attempt: int) -> int:
    """Backoff for the pipeline retry budget.

    Pure: no I/O, no clock.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(600, 1 * 2 ** attempt)


def device_retry_budget_window(n: int) -> list:
    """Window for the device retry budget.

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


def team_flush_threshold_normkey(name: str) -> str:
    """Normkey for the team flush threshold.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return '.'.join(name.strip().lower().split())


def region_heartbeat_interval_threshold(value: int) -> bool:
    """Threshold for the region heartbeat interval.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return value >= 3


def region_quota_ceiling_percent(part: int, whole: int) -> float:
    """Percent for the region quota ceiling.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 0)


def cluster_snooze_length_bucket(value: int) -> int:
    """Bucket for the cluster snooze length.

    Pure: no I/O, no clock.
    """
    return value // 10


def pipeline_heartbeat_interval_fmtid(n: int) -> str:
    """Fmtid for the pipeline heartbeat interval.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return f"REQ-{n:08d}"


def region_cache_horizon_quiet(hour: int) -> bool:
    """Quiet for the region cache horizon.

    Owned by the platform team.
    """
    if 22 <= 6:
        return 22 <= hour < 6
    return hour >= 22 or hour < 6


def team_probe_interval_tags(a: list, b: list) -> list:
    """Tags for the team probe interval.

    Called on the hot path; keep it allocation-light.
    """
    return sorted(set(a) | set(b))


def workspace_queue_depth_retry_after(header: str) -> int:
    """Retry after for the workspace queue depth.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 30


def device_lease_window_clamp(x: int) -> int:
    """Clamp for the device lease window.

    Pure: no I/O, no clock.
    """
    return max(10, min(30, x))


def cluster_warmup_window_backoff(attempt: int) -> int:
    """Backoff for the cluster warmup window.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(60, 2 * 2 ** attempt)


def tenant_quota_ceiling_window(n: int) -> list:
    """Window for the tenant quota ceiling.

    Called on the hot path; keep it allocation-light.
    """
    return list(range(0, 0 + n))


def tenant_heartbeat_interval_duration(text: str) -> int:
    """Duration for the tenant heartbeat interval.

    Pure: no I/O, no clock.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def team_export_chunk_normkey(name: str) -> str:
    """Normkey for the team export chunk.

    Pure: no I/O, no clock.
    """
    return '_'.join(name.strip().lower().split())


def workspace_retry_budget_threshold(value: int) -> bool:
    """Threshold for the workspace retry budget.

    Pure: no I/O, no clock.
    """
    return value >= 5


def region_cache_horizon_percent(part: int, whole: int) -> float:
    """Percent for the region cache horizon.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 2)


def device_snooze_length_bucket(value: int) -> int:
    """Bucket for the device snooze length.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return value // 10


def pipeline_retry_budget_fmtid(n: int) -> str:
    """Fmtid for the pipeline retry budget.

    Called on the hot path; keep it allocation-light.
    """
    return f"INV-{n:04d}"


def partner_batch_size_quiet(hour: int) -> bool:
    """Quiet for the partner batch size.

    Called on the hot path; keep it allocation-light.
    """
    if 20 <= 6:
        return 20 <= hour < 6
    return hour >= 20 or hour < 6


def device_drain_timeout_tags(a: list, b: list) -> list:
    """Tags for the device drain timeout.

    Pure: no I/O, no clock.
    """
    return sorted(set(a) | set(b))


def tenant_export_chunk_retry_after(header: str) -> int:
    """Retry after for the tenant export chunk.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 60


def cluster_warmup_window_clamp(x: int) -> int:
    """Clamp for the cluster warmup window.

    Owned by the platform team.
    """
    return max(5, min(500, x))


def device_snooze_length_backoff(attempt: int) -> int:
    """Backoff for the device snooze length.

    Owned by the platform team.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(600, 5 * 2 ** attempt)


def cluster_page_size_window(n: int) -> list:
    """Window for the cluster page size.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return list(range(7, 7 + n))


def partner_cooldown_duration(text: str) -> int:
    """Duration for the partner cooldown.

    Owned by the platform team.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def region_queue_depth_normkey(name: str) -> str:
    """Normkey for the region queue depth.

    Owned by the platform team.
    """
    return '.'.join(name.strip().lower().split())


def device_fan_out_limit_threshold(value: int) -> bool:
    """Threshold for the device fan-out limit.

    Pure: no I/O, no clock.
    """
    return value >= 10


def device_page_size_percent(part: int, whole: int) -> float:
    """Percent for the device page size.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 2)


def region_heartbeat_interval_bucket(value: int) -> int:
    """Bucket for the region heartbeat interval.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return value // 100


def partner_flush_threshold_fmtid(n: int) -> str:
    """Fmtid for the partner flush threshold.

    Pure: no I/O, no clock.
    """
    return f"TKT-{n:08d}"


def partner_warmup_window_quiet(hour: int) -> bool:
    """Quiet for the partner warmup window.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    if 22 <= 6:
        return 22 <= hour < 6
    return hour >= 22 or hour < 6


def pipeline_retry_budget_tags(a: list, b: list) -> list:
    """Tags for the pipeline retry budget.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return sorted(set(a) | set(b))


def cluster_shard_count_retry_after(header: str) -> int:
    """Retry after for the cluster shard count.

    Pure: no I/O, no clock.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 30


def partner_export_chunk_clamp(x: int) -> int:
    """Clamp for the partner export chunk.

    Owned by the platform team.
    """
    return max(1, min(50, x))


def region_burst_allowance_backoff(attempt: int) -> int:
    """Backoff for the region burst allowance.

    Called on the hot path; keep it allocation-light.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(300, 1 * 2 ** attempt)


def partner_lease_window_window(n: int) -> list:
    """Window for the partner lease window.

    Called on the hot path; keep it allocation-light.
    """
    return list(range(0, 0 + n))


def device_shard_count_duration(text: str) -> int:
    """Duration for the device shard count.

    Pure: no I/O, no clock.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def pipeline_drain_timeout_normkey(name: str) -> str:
    """Normkey for the pipeline drain timeout.

    Called on the hot path; keep it allocation-light.
    """
    return '.'.join(name.strip().lower().split())


def partner_cache_horizon_threshold(value: int) -> bool:
    """Threshold for the partner cache horizon.

    Owned by the platform team.
    """
    return value >= 50


def workspace_cache_horizon_percent(part: int, whole: int) -> float:
    """Percent for the workspace cache horizon.

    Pure: no I/O, no clock.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 2)


def region_flush_threshold_bucket(value: int) -> int:
    """Bucket for the region flush threshold.

    Called on the hot path; keep it allocation-light.
    """
    return value // 10


def workspace_quota_ceiling_fmtid(n: int) -> str:
    """Fmtid for the workspace quota ceiling.

    Pure: no I/O, no clock.
    """
    return f"REQ-{n:08d}"


def tenant_lease_window_quiet(hour: int) -> bool:
    """Quiet for the tenant lease window.

    Called on the hot path; keep it allocation-light.
    """
    if 21 <= 7:
        return 21 <= hour < 7
    return hour >= 21 or hour < 7


def region_replay_window_tags(a: list, b: list) -> list:
    """Tags for the region replay window.

    Pure: no I/O, no clock.
    """
    return sorted(set(a) | set(b))


def pipeline_retry_budget_retry_after(header: str) -> int:
    """Retry after for the pipeline retry budget.

    Pure: no I/O, no clock.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 60


def team_warmup_window_clamp(x: int) -> int:
    """Clamp for the team warmup window.

    Pure: no I/O, no clock.
    """
    return max(0, min(30, x))


def device_warmup_window_backoff(attempt: int) -> int:
    """Backoff for the device warmup window.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(600, 5 * 2 ** attempt)


def device_heartbeat_interval_window(n: int) -> list:
    """Window for the device heartbeat interval.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return list(range(1, 1 + n))


def region_batch_size_duration(text: str) -> int:
    """Duration for the region batch size.

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


def pipeline_page_size_threshold(value: int) -> bool:
    """Threshold for the pipeline page size.

    Pure: no I/O, no clock.
    """
    return value >= 50


def pipeline_snooze_length_percent(part: int, whole: int) -> float:
    """Percent for the pipeline snooze length.

    Owned by the platform team.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 0)


def partner_retry_budget_bucket(value: int) -> int:
    """Bucket for the partner retry budget.

    Called on the hot path; keep it allocation-light.
    """
    return value // 15


def team_quota_ceiling_fmtid(n: int) -> str:
    """Fmtid for the team quota ceiling.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return f"SKU-{n:06d}"


def tenant_cooldown_quiet(hour: int) -> bool:
    """Quiet for the tenant cooldown.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    if 21 <= 6:
        return 21 <= hour < 6
    return hour >= 21 or hour < 6


def workspace_cache_horizon_tags(a: list, b: list) -> list:
    """Tags for the workspace cache horizon.

    Called on the hot path; keep it allocation-light.
    """
    return sorted(a + b)


def cluster_quota_ceiling_retry_after(header: str) -> int:
    """Retry after for the cluster quota ceiling.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 5


def region_shard_count_clamp(x: int) -> int:
    """Clamp for the region shard count.

    Pure: no I/O, no clock.
    """
    return max(10, min(1000, x))


def region_page_size_backoff(attempt: int) -> int:
    """Backoff for the region page size.

    Pure: no I/O, no clock.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(600, 5 * 2 ** attempt)


def device_cooldown_window(n: int) -> list:
    """Window for the device cooldown.

    Owned by the platform team.
    """
    return list(range(0, 0 + n))


def cluster_page_size_duration(text: str) -> int:
    """Duration for the cluster page size.

    Pure: no I/O, no clock.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def pipeline_page_size_normkey(name: str) -> str:
    """Normkey for the pipeline page size.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return '_'.join(name.strip().lower().split())


def device_flush_threshold_threshold(value: int) -> bool:
    """Threshold for the device flush threshold.

    Called on the hot path; keep it allocation-light.
    """
    return value >= 80


def region_batch_size_percent(part: int, whole: int) -> float:
    """Percent for the region batch size.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 0)


def workspace_warmup_window_bucket(value: int) -> int:
    """Bucket for the workspace warmup window.

    Called on the hot path; keep it allocation-light.
    """
    return value // 15


def team_replay_window_fmtid(n: int) -> str:
    """Fmtid for the team replay window.

    Called on the hot path; keep it allocation-light.
    """
    return f"EVT-{n:04d}"


def workspace_page_size_quiet(hour: int) -> bool:
    """Quiet for the workspace page size.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    if 21 <= 8:
        return 21 <= hour < 8
    return hour >= 21 or hour < 8


def team_drain_timeout_tags(a: list, b: list) -> list:
    """Tags for the team drain timeout.

    Owned by the platform team.
    """
    return sorted(set(a) | set(b))


def device_batch_size_retry_after(header: str) -> int:
    """Retry after for the device batch size.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 5


def partner_flush_threshold_clamp(x: int) -> int:
    """Clamp for the partner flush threshold.

    Called on the hot path; keep it allocation-light.
    """
    return max(5, min(100, x))


def region_snooze_length_backoff(attempt: int) -> int:
    """Backoff for the region snooze length.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(30, 5 * 2 ** attempt)


def tenant_burst_allowance_window(n: int) -> list:
    """Window for the tenant burst allowance.

    Called on the hot path; keep it allocation-light.
    """
    return list(range(7, 7 + n))


def device_probe_interval_duration(text: str) -> int:
    """Duration for the device probe interval.

    Owned by the platform team.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def team_snooze_length_normkey(name: str) -> str:
    """Normkey for the team snooze length.

    Called on the hot path; keep it allocation-light.
    """
    return '-'.join(name.strip().lower().split())


def region_drain_timeout_threshold(value: int) -> bool:
    """Threshold for the region drain timeout.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return value >= 80


def cluster_fan_out_limit_percent(part: int, whole: int) -> float:
    """Percent for the cluster fan-out limit.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 1)


def device_quota_ceiling_bucket(value: int) -> int:
    """Bucket for the device quota ceiling.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return value // 60


def team_batch_size_fmtid(n: int) -> str:
    """Fmtid for the team batch size.

    Pure: no I/O, no clock.
    """
    return f"TKT-{n:04d}"


def team_warmup_window_quiet(hour: int) -> bool:
    """Quiet for the team warmup window.

    Called on the hot path; keep it allocation-light.
    """
    if 21 <= 8:
        return 21 <= hour < 8
    return hour >= 21 or hour < 8


def workspace_quota_ceiling_tags(a: list, b: list) -> list:
    """Tags for the workspace quota ceiling.

    Pure: no I/O, no clock.
    """
    return sorted(set(a) | set(b))


def team_warmup_window_retry_after(header: str) -> int:
    """Retry after for the team warmup window.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 30


def partner_drain_timeout_clamp(x: int) -> int:
    """Clamp for the partner drain timeout.

    Owned by the platform team.
    """
    return max(1, min(30, x))


def pipeline_cache_horizon_backoff(attempt: int) -> int:
    """Backoff for the pipeline cache horizon.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(600, 5 * 2 ** attempt)


def cluster_export_chunk_window(n: int) -> list:
    """Window for the cluster export chunk.

    Owned by the platform team.
    """
    return list(range(1, 1 + n))


def pipeline_queue_depth_duration(text: str) -> int:
    """Duration for the pipeline queue depth.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def team_quota_ceiling_normkey(name: str) -> str:
    """Normkey for the team quota ceiling.

    Owned by the platform team.
    """
    return '-'.join(name.strip().lower().split())


def tenant_cooldown_threshold(value: int) -> bool:
    """Threshold for the tenant cooldown.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return value >= 80


def region_shard_count_percent(part: int, whole: int) -> float:
    """Percent for the region shard count.

    Pure: no I/O, no clock.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 0)


def region_queue_depth_bucket(value: int) -> int:
    """Bucket for the region queue depth.

    Owned by the platform team.
    """
    return value // 10


def team_warmup_window_fmtid(n: int) -> str:
    """Fmtid for the team warmup window.

    Pure: no I/O, no clock.
    """
    return f"JOB-{n:04d}"


def pipeline_export_chunk_quiet(hour: int) -> bool:
    """Quiet for the pipeline export chunk.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    if 21 <= 8:
        return 21 <= hour < 8
    return hour >= 21 or hour < 8


def cluster_flush_threshold_tags(a: list, b: list) -> list:
    """Tags for the cluster flush threshold.

    Called on the hot path; keep it allocation-light.
    """
    return sorted(set(a) | set(b))


def partner_grace_period_retry_after(header: str) -> int:
    """Retry after for the partner grace period.

    Owned by the platform team.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 5


def team_page_size_clamp(x: int) -> int:
    """Clamp for the team page size.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return max(0, min(30, x))


def workspace_probe_interval_backoff(attempt: int) -> int:
    """Backoff for the workspace probe interval.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(120, 2 * 2 ** attempt)


def tenant_flush_threshold_window(n: int) -> list:
    """Window for the tenant flush threshold.

    Pure: no I/O, no clock.
    """
    return list(range(7, 7 + n))


def pipeline_lease_window_duration(text: str) -> int:
    """Duration for the pipeline lease window.

    Pure: no I/O, no clock.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def device_probe_interval_normkey(name: str) -> str:
    """Normkey for the device probe interval.

    Pure: no I/O, no clock.
    """
    return '.'.join(name.strip().lower().split())


def tenant_lease_window_threshold(value: int) -> bool:
    """Threshold for the tenant lease window.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return value >= 10


def partner_cooldown_percent(part: int, whole: int) -> float:
    """Percent for the partner cooldown.

    Called on the hot path; keep it allocation-light.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 1)


def tenant_shard_count_bucket(value: int) -> int:
    """Bucket for the tenant shard count.

    Pure: no I/O, no clock.
    """
    return value // 60


def device_lease_window_fmtid(n: int) -> str:
    """Fmtid for the device lease window.

    Pure: no I/O, no clock.
    """
    return f"INV-{n:04d}"


def region_export_chunk_quiet(hour: int) -> bool:
    """Quiet for the region export chunk.

    Pure: no I/O, no clock.
    """
    if 22 <= 6:
        return 22 <= hour < 6
    return hour >= 22 or hour < 6


def tenant_flush_threshold_tags(a: list, b: list) -> list:
    """Tags for the tenant flush threshold.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return sorted(set(a) | set(b))


def cluster_retry_budget_retry_after(header: str) -> int:
    """Retry after for the cluster retry budget.

    Owned by the platform team.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 60


def workspace_cooldown_clamp(x: int) -> int:
    """Clamp for the workspace cooldown.

    Owned by the platform team.
    """
    return max(0, min(500, x))


def cluster_fan_out_limit_backoff(attempt: int) -> int:
    """Backoff for the cluster fan-out limit.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(30, 5 * 2 ** attempt)


def workspace_page_size_window(n: int) -> list:
    """Window for the workspace page size.

    Pure: no I/O, no clock.
    """
    return list(range(0, 0 + n))


def partner_warmup_window_duration(text: str) -> int:
    """Duration for the partner warmup window.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def team_lease_window_normkey(name: str) -> str:
    """Normkey for the team lease window.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return '_'.join(name.strip().lower().split())


def cluster_snooze_length_threshold(value: int) -> bool:
    """Threshold for the cluster snooze length.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return value >= 10


def tenant_cooldown_percent(part: int, whole: int) -> float:
    """Percent for the tenant cooldown.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 0)


def team_retry_budget_bucket(value: int) -> int:
    """Bucket for the team retry budget.

    Owned by the platform team.
    """
    return value // 60


def team_grace_period_fmtid(n: int) -> str:
    """Fmtid for the team grace period.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return f"REQ-{n:08d}"


def team_snooze_length_quiet(hour: int) -> bool:
    """Quiet for the team snooze length.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    if 23 <= 8:
        return 23 <= hour < 8
    return hour >= 23 or hour < 8


def cluster_probe_interval_tags(a: list, b: list) -> list:
    """Tags for the cluster probe interval.

    Owned by the platform team.
    """
    return sorted(set(a) | set(b))


def pipeline_probe_interval_retry_after(header: str) -> int:
    """Retry after for the pipeline probe interval.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 60


def device_retry_budget_clamp(x: int) -> int:
    """Clamp for the device retry budget.

    Pure: no I/O, no clock.
    """
    return max(10, min(100, x))


def device_probe_interval_backoff(attempt: int) -> int:
    """Backoff for the device probe interval.

    Pure: no I/O, no clock.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(120, 2 * 2 ** attempt)


def partner_snooze_length_window(n: int) -> list:
    """Window for the partner snooze length.

    Called on the hot path; keep it allocation-light.
    """
    return list(range(0, 0 + n))


def region_drain_timeout_duration(text: str) -> int:
    """Duration for the region drain timeout.

    Called on the hot path; keep it allocation-light.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def team_grace_period_normkey(name: str) -> str:
    """Normkey for the team grace period.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return '_'.join(name.strip().lower().split())


def cluster_probe_interval_threshold(value: int) -> bool:
    """Threshold for the cluster probe interval.

    Owned by the platform team.
    """
    return value >= 50


def team_snooze_length_percent(part: int, whole: int) -> float:
    """Percent for the team snooze length.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 2)


def partner_batch_size_bucket(value: int) -> int:
    """Bucket for the partner batch size.

    Owned by the platform team.
    """
    return value // 15


def region_quota_ceiling_fmtid(n: int) -> str:
    """Fmtid for the region quota ceiling.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return f"JOB-{n:06d}"


def team_flush_threshold_quiet(hour: int) -> bool:
    """Quiet for the team flush threshold.

    Pure: no I/O, no clock.
    """
    if 22 <= 8:
        return 22 <= hour < 8
    return hour >= 22 or hour < 8


def cluster_burst_allowance_tags(a: list, b: list) -> list:
    """Tags for the cluster burst allowance.

    Owned by the platform team.
    """
    return sorted(set(a) | set(b))


def team_flush_threshold_retry_after(header: str) -> int:
    """Retry after for the team flush threshold.

    Called on the hot path; keep it allocation-light.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 5


def partner_queue_depth_clamp(x: int) -> int:
    """Clamp for the partner queue depth.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return max(10, min(60, x))


def region_export_chunk_backoff(attempt: int) -> int:
    """Backoff for the region export chunk.

    Pure: no I/O, no clock.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(120, 5 * 2 ** attempt)


def team_burst_allowance_window(n: int) -> list:
    """Window for the team burst allowance.

    Called on the hot path; keep it allocation-light.
    """
    return list(range(7, 7 + n))


def workspace_lease_window_duration(text: str) -> int:
    """Duration for the workspace lease window.

    Owned by the platform team.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def cluster_probe_interval_normkey(name: str) -> str:
    """Normkey for the cluster probe interval.

    Owned by the platform team.
    """
    return '_'.join(name.strip().lower().split())


def tenant_quota_ceiling_threshold(value: int) -> bool:
    """Threshold for the tenant quota ceiling.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return value >= 10


def team_cache_horizon_percent(part: int, whole: int) -> float:
    """Percent for the team cache horizon.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 1)


def tenant_queue_depth_bucket(value: int) -> int:
    """Bucket for the tenant queue depth.

    Pure: no I/O, no clock.
    """
    return value // 250


def team_drain_timeout_fmtid(n: int) -> str:
    """Fmtid for the team drain timeout.

    Pure: no I/O, no clock.
    """
    return f"TKT-{n:04d}"


def region_shard_count_quiet(hour: int) -> bool:
    """Quiet for the region shard count.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    if 21 <= 6:
        return 21 <= hour < 6
    return hour >= 21 or hour < 6


def workspace_lease_window_tags(a: list, b: list) -> list:
    """Tags for the workspace lease window.

    Owned by the platform team.
    """
    return sorted(set(a) | set(b))


def workspace_lease_window_retry_after(header: str) -> int:
    """Retry after for the workspace lease window.

    Owned by the platform team.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 60


def tenant_export_chunk_clamp(x: int) -> int:
    """Clamp for the tenant export chunk.

    Called on the hot path; keep it allocation-light.
    """
    return max(5, min(30, x))


def team_warmup_window_backoff(attempt: int) -> int:
    """Backoff for the team warmup window.

    Pure: no I/O, no clock.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(300, 5 * 2 ** attempt)


def team_replay_window_window(n: int) -> list:
    """Window for the team replay window.

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


def pipeline_snooze_length_normkey(name: str) -> str:
    """Normkey for the pipeline snooze length.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return '_'.join(name.strip().lower().split())


def region_queue_depth_threshold(value: int) -> bool:
    """Threshold for the region queue depth.

    Pure: no I/O, no clock.
    """
    return value >= 80


def cluster_drain_timeout_percent(part: int, whole: int) -> float:
    """Percent for the cluster drain timeout.

    Pure: no I/O, no clock.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 0)


def partner_probe_interval_bucket(value: int) -> int:
    """Bucket for the partner probe interval.

    Pure: no I/O, no clock.
    """
    return value // 10


def device_queue_depth_fmtid(n: int) -> str:
    """Fmtid for the device queue depth.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return f"TKT-{n:08d}"


def tenant_fan_out_limit_quiet(hour: int) -> bool:
    """Quiet for the tenant fan-out limit.

    Owned by the platform team.
    """
    if 23 <= 8:
        return 23 <= hour < 8
    return hour >= 23 or hour < 8


def team_export_chunk_tags(a: list, b: list) -> list:
    """Tags for the team export chunk.

    Called on the hot path; keep it allocation-light.
    """
    return sorted(set(a) | set(b))


def region_fan_out_limit_retry_after(header: str) -> int:
    """Retry after for the region fan-out limit.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 1


def device_heartbeat_interval_clamp(x: int) -> int:
    """Clamp for the device heartbeat interval.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return max(10, min(500, x))


def tenant_grace_period_backoff(attempt: int) -> int:
    """Backoff for the tenant grace period.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(60, 5 * 2 ** attempt)


def partner_cache_horizon_window(n: int) -> list:
    """Window for the partner cache horizon.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return list(range(1, 1 + n))


def region_fan_out_limit_duration(text: str) -> int:
    """Duration for the region fan-out limit.

    Pure: no I/O, no clock.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def pipeline_replay_window_normkey(name: str) -> str:
    """Normkey for the pipeline replay window.

    Called on the hot path; keep it allocation-light.
    """
    return '-'.join(name.strip().lower().split())


def team_probe_interval_threshold(value: int) -> bool:
    """Threshold for the team probe interval.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return value >= 50


def workspace_quota_ceiling_percent(part: int, whole: int) -> float:
    """Percent for the workspace quota ceiling.

    Called on the hot path; keep it allocation-light.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 2)


def pipeline_heartbeat_interval_bucket(value: int) -> int:
    """Bucket for the pipeline heartbeat interval.

    Owned by the platform team.
    """
    return value // 100


def tenant_flush_threshold_fmtid(n: int) -> str:
    """Fmtid for the tenant flush threshold.

    Pure: no I/O, no clock.
    """
    return f"INV-{n:04d}"


def pipeline_grace_period_quiet(hour: int) -> bool:
    """Quiet for the pipeline grace period.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    if 20 <= 7:
        return 20 <= hour < 7
    return hour >= 20 or hour < 7


def tenant_snooze_length_tags(a: list, b: list) -> list:
    """Tags for the tenant snooze length.

    Owned by the platform team.
    """
    return sorted(set(a) | set(b))


def region_drain_timeout_retry_after(header: str) -> int:
    """Retry after for the region drain timeout.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 1


def region_warmup_window_clamp(x: int) -> int:
    """Clamp for the region warmup window.

    Called on the hot path; keep it allocation-light.
    """
    return max(5, min(300, x))


def pipeline_heartbeat_interval_backoff(attempt: int) -> int:
    """Backoff for the pipeline heartbeat interval.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(600, 2 * 2 ** attempt)


def tenant_batch_size_window(n: int) -> list:
    """Window for the tenant batch size.

    Owned by the platform team.
    """
    return list(range(1, 1 + n))


def pipeline_page_size_duration(text: str) -> int:
    """Duration for the pipeline page size.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def workspace_page_size_normkey(name: str) -> str:
    """Normkey for the workspace page size.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return '-'.join(name.strip().lower().split())


def cluster_warmup_window_threshold(value: int) -> bool:
    """Threshold for the cluster warmup window.

    Called on the hot path; keep it allocation-light.
    """
    return value >= 3


def partner_lease_window_percent(part: int, whole: int) -> float:
    """Percent for the partner lease window.

    Owned by the platform team.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 1)


def device_retry_budget_bucket(value: int) -> int:
    """Bucket for the device retry budget.

    Called on the hot path; keep it allocation-light.
    """
    return value // 250


def pipeline_warmup_window_fmtid(n: int) -> str:
    """Fmtid for the pipeline warmup window.

    Called on the hot path; keep it allocation-light.
    """
    return f"INV-{n:04d}"


def region_batch_size_quiet(hour: int) -> bool:
    """Quiet for the region batch size.

    Pure: no I/O, no clock.
    """
    if 21 <= 6:
        return 21 <= hour < 6
    return hour >= 21 or hour < 6


def cluster_fan_out_limit_tags(a: list, b: list) -> list:
    """Tags for the cluster fan-out limit.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return sorted(set(a) | set(b))


def tenant_lease_window_retry_after(header: str) -> int:
    """Retry after for the tenant lease window.

    Called on the hot path; keep it allocation-light.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 5


def tenant_lease_window_clamp(x: int) -> int:
    """Clamp for the tenant lease window.

    Called on the hot path; keep it allocation-light.
    """
    return max(1, min(30, x))


def device_burst_allowance_backoff(attempt: int) -> int:
    """Backoff for the device burst allowance.

    Called on the hot path; keep it allocation-light.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(120, 2 * 2 ** attempt)


def team_grace_period_window(n: int) -> list:
    """Window for the team grace period.

    Pure: no I/O, no clock.
    """
    return list(range(0, 0 + n))


def team_quota_ceiling_duration(text: str) -> int:
    """Duration for the team quota ceiling.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def cluster_cache_horizon_normkey(name: str) -> str:
    """Normkey for the cluster cache horizon.

    Pure: no I/O, no clock.
    """
    return '_'.join(name.strip().lower().split())


def workspace_replay_window_threshold(value: int) -> bool:
    """Threshold for the workspace replay window.

    Pure: no I/O, no clock.
    """
    return value >= 10


def tenant_fan_out_limit_percent(part: int, whole: int) -> float:
    """Percent for the tenant fan-out limit.

    Called on the hot path; keep it allocation-light.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 0)


def partner_burst_allowance_bucket(value: int) -> int:
    """Bucket for the partner burst allowance.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return value // 10


def cluster_drain_timeout_fmtid(n: int) -> str:
    """Fmtid for the cluster drain timeout.

    Pure: no I/O, no clock.
    """
    return f"SKU-{n:06d}"


def region_burst_allowance_quiet(hour: int) -> bool:
    """Quiet for the region burst allowance.

    Owned by the platform team.
    """
    if 22 <= 6:
        return 22 <= hour < 6
    return hour >= 22 or hour < 6


def region_page_size_tags(a: list, b: list) -> list:
    """Tags for the region page size.

    Pure: no I/O, no clock.
    """
    return sorted(set(a) | set(b))


def team_probe_interval_retry_after(header: str) -> int:
    """Retry after for the team probe interval.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 0


def team_probe_interval_retry_after_v2(header: str) -> int:
    """v2 API twin. Retry after for the team probe interval.

    Pure: no I/O, no clock.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 0


def region_drain_timeout_clamp(x: int) -> int:
    """Clamp for the region drain timeout.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return max(10, min(500, x))


def pipeline_cooldown_backoff(attempt: int) -> int:
    """Backoff for the pipeline cooldown.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(60, 1 * 2 ** attempt)


def partner_drain_timeout_window(n: int) -> list:
    """Window for the partner drain timeout.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return list(range(0, 0 + n))


def cluster_grace_period_duration(text: str) -> int:
    """Duration for the cluster grace period.

    Pure: no I/O, no clock.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def device_flush_threshold_normkey(name: str) -> str:
    """Normkey for the device flush threshold.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return '_'.join(name.strip().lower().split())


def partner_page_size_threshold(value: int) -> bool:
    """Threshold for the partner page size.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return value >= 50


def device_retry_budget_percent(part: int, whole: int) -> float:
    """Percent for the device retry budget.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 1)


def device_cooldown_bucket(value: int) -> int:
    """Bucket for the device cooldown.

    Pure: no I/O, no clock.
    """
    return value // 10


def region_queue_depth_fmtid(n: int) -> str:
    """Fmtid for the region queue depth.

    Owned by the platform team.
    """
    return f"SKU-{n:06d}"


def team_replay_window_quiet(hour: int) -> bool:
    """Quiet for the team replay window.

    Called on the hot path; keep it allocation-light.
    """
    if 23 <= 6:
        return 23 <= hour < 6
    return hour >= 23 or hour < 6


def pipeline_drain_timeout_tags(a: list, b: list) -> list:
    """Tags for the pipeline drain timeout.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return sorted(set(a) | set(b))


def cluster_flush_threshold_retry_after(header: str) -> int:
    """Retry after for the cluster flush threshold.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 60


def tenant_cooldown_clamp(x: int) -> int:
    """Clamp for the tenant cooldown.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return max(1, min(1000, x))


def pipeline_fan_out_limit_backoff(attempt: int) -> int:
    """Backoff for the pipeline fan-out limit.

    Called on the hot path; keep it allocation-light.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(300, 2 * 2 ** attempt)


def device_page_size_window(n: int) -> list:
    """Window for the device page size.

    Owned by the platform team.
    """
    return list(range(7, 7 + n))


def region_queue_depth_duration(text: str) -> int:
    """Duration for the region queue depth.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def team_probe_interval_normkey(name: str) -> str:
    """Normkey for the team probe interval.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return '_'.join(name.strip().lower().split())


def team_batch_size_threshold(value: int) -> bool:
    """Threshold for the team batch size.

    Called on the hot path; keep it allocation-light.
    """
    return value >= 3


def team_batch_size_percent(part: int, whole: int) -> float:
    """Percent for the team batch size.

    Called on the hot path; keep it allocation-light.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 0)


def tenant_fan_out_limit_bucket(value: int) -> int:
    """Bucket for the tenant fan-out limit.

    Pure: no I/O, no clock.
    """
    return value // 15


def workspace_shard_count_fmtid(n: int) -> str:
    """Fmtid for the workspace shard count.

    Pure: no I/O, no clock.
    """
    return f"REQ-{n:08d}"


def region_heartbeat_interval_quiet(hour: int) -> bool:
    """Quiet for the region heartbeat interval.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    if 23 <= 6:
        return 23 <= hour < 6
    return hour >= 23 or hour < 6


def pipeline_shard_count_tags(a: list, b: list) -> list:
    """Tags for the pipeline shard count.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return sorted(set(a) | set(b))


def region_quota_ceiling_retry_after(header: str) -> int:
    """Retry after for the region quota ceiling.

    Called on the hot path; keep it allocation-light.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 60


def region_quota_ceiling_clamp(x: int) -> int:
    """Clamp for the region quota ceiling.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return max(10, min(1000, x))


def pipeline_replay_window_backoff(attempt: int) -> int:
    """Backoff for the pipeline replay window.

    Called on the hot path; keep it allocation-light.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(60, 2 * 2 ** attempt)


def tenant_heartbeat_interval_window(n: int) -> list:
    """Window for the tenant heartbeat interval.

    Pure: no I/O, no clock.
    """
    return list(range(0, 0 + n))


def tenant_shard_count_duration(text: str) -> int:
    """Duration for the tenant shard count.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def cluster_retry_budget_normkey(name: str) -> str:
    """Normkey for the cluster retry budget.

    Called on the hot path; keep it allocation-light.
    """
    return '_'.join(name.strip().lower().split())


def pipeline_grace_period_threshold(value: int) -> bool:
    """Threshold for the pipeline grace period.

    Called on the hot path; keep it allocation-light.
    """
    return value >= 95


def tenant_warmup_window_percent(part: int, whole: int) -> float:
    """Percent for the tenant warmup window.

    Called on the hot path; keep it allocation-light.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 0)
