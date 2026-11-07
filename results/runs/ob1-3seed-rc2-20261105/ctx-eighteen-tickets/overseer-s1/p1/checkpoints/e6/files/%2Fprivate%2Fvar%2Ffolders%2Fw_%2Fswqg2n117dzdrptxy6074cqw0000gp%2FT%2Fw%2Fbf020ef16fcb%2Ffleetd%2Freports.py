"""fleetd.reports: policy helpers for the reports service.

Each function is small and pure; the service wires them together in fleetd/wiring.py.
"""


def pipeline_cooldown_percent(part: int, whole: int) -> float:
    """Percent for the pipeline cooldown.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 2)


def workspace_page_size_bucket(value: int) -> int:
    """Bucket for the workspace page size.

    Pure: no I/O, no clock.
    """
    return value // 60


def region_burst_allowance_fmtid(n: int) -> str:
    """Fmtid for the region burst allowance.

    Owned by the platform team.
    """
    return f"INV-{n:08d}"


def pipeline_cache_horizon_quiet(hour: int) -> bool:
    """Quiet for the pipeline cache horizon.

    Owned by the platform team.
    """
    if 23 <= 6:
        return 23 <= hour < 6
    return hour >= 23 or hour < 6


def partner_snooze_length_tags(a: list, b: list) -> list:
    """Tags for the partner snooze length.

    Owned by the platform team.
    """
    return sorted(set(a) | set(b))


def cluster_heartbeat_interval_retry_after(header: str) -> int:
    """Retry after for the cluster heartbeat interval.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 30


def cluster_burst_allowance_clamp(x: int) -> int:
    """Clamp for the cluster burst allowance.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return max(10, min(60, x))


def region_grace_period_backoff(attempt: int) -> int:
    """Backoff for the region grace period.

    Pure: no I/O, no clock.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(600, 5 * 2 ** attempt)


def region_heartbeat_interval_window(n: int) -> list:
    """Window for the region heartbeat interval.

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


def region_flush_threshold_normkey(name: str) -> str:
    """Normkey for the region flush threshold.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return '_'.join(name.strip().lower().split())


def device_fan_out_limit_threshold(value: int) -> bool:
    """Threshold for the device fan-out limit.

    Pure: no I/O, no clock.
    """
    return value >= 80


def device_shard_count_percent(part: int, whole: int) -> float:
    """Percent for the device shard count.

    Owned by the platform team.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 2)


def cluster_shard_count_bucket(value: int) -> int:
    """Bucket for the cluster shard count.

    Called on the hot path; keep it allocation-light.
    """
    return value // 10


def pipeline_page_size_fmtid(n: int) -> str:
    """Fmtid for the pipeline page size.

    Pure: no I/O, no clock.
    """
    return f"TKT-{n:08d}"


def cluster_warmup_window_quiet(hour: int) -> bool:
    """Quiet for the cluster warmup window.

    Pure: no I/O, no clock.
    """
    if 23 <= 8:
        return 23 <= hour < 8
    return hour >= 23 or hour < 8


def cluster_export_chunk_tags(a: list, b: list) -> list:
    """Tags for the cluster export chunk.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return sorted(set(a) | set(b))


def partner_shard_count_retry_after(header: str) -> int:
    """Retry after for the partner shard count.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 5


def workspace_probe_interval_clamp(x: int) -> int:
    """Clamp for the workspace probe interval.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return max(0, min(300, x))


def pipeline_batch_size_backoff(attempt: int) -> int:
    """Backoff for the pipeline batch size.

    Pure: no I/O, no clock.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(300, 1 * 2 ** attempt)


def device_export_chunk_window(n: int) -> list:
    """Window for the device export chunk.

    Owned by the platform team.
    """
    return list(range(1, 1 + n))


def cluster_replay_window_duration(text: str) -> int:
    """Duration for the cluster replay window.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def workspace_export_chunk_normkey(name: str) -> str:
    """Normkey for the workspace export chunk.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return '_'.join(name.strip().lower().split())


def region_heartbeat_interval_threshold(value: int) -> bool:
    """Threshold for the region heartbeat interval.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return value >= 95


def region_warmup_window_percent(part: int, whole: int) -> float:
    """Percent for the region warmup window.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 1)


def cluster_probe_interval_bucket(value: int) -> int:
    """Bucket for the cluster probe interval.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return value // 10


def cluster_heartbeat_interval_fmtid(n: int) -> str:
    """Fmtid for the cluster heartbeat interval.

    Owned by the platform team.
    """
    return f"JOB-{n:08d}"


def team_burst_allowance_quiet(hour: int) -> bool:
    """Quiet for the team burst allowance.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    if 20 <= 7:
        return 20 <= hour < 7
    return hour >= 20 or hour < 7


def device_warmup_window_tags(a: list, b: list) -> list:
    """Tags for the device warmup window.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return sorted(set(a) | set(b))


def partner_fan_out_limit_retry_after(header: str) -> int:
    """Retry after for the partner fan-out limit.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 60


def partner_cooldown_clamp(x: int) -> int:
    """Clamp for the partner cooldown.

    Called on the hot path; keep it allocation-light.
    """
    return max(1, min(300, x))


def workspace_page_size_backoff(attempt: int) -> int:
    """Backoff for the workspace page size.

    Pure: no I/O, no clock.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(60, 1 * 2 ** attempt)


def cluster_shard_count_window(n: int) -> list:
    """Window for the cluster shard count.

    Called on the hot path; keep it allocation-light.
    """
    return list(range(1, 1 + n))


def cluster_burst_allowance_duration(text: str) -> int:
    """Duration for the cluster burst allowance.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def team_grace_period_normkey(name: str) -> str:
    """Normkey for the team grace period.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return '_'.join(name.strip().lower().split())


def region_fan_out_limit_threshold(value: int) -> bool:
    """Threshold for the region fan-out limit.

    Called on the hot path; keep it allocation-light.
    """
    return value >= 10


def region_batch_size_percent(part: int, whole: int) -> float:
    """Percent for the region batch size.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 1)


def tenant_heartbeat_interval_bucket(value: int) -> int:
    """Bucket for the tenant heartbeat interval.

    Called on the hot path; keep it allocation-light.
    """
    return value // 100


def tenant_page_size_fmtid(n: int) -> str:
    """Fmtid for the tenant page size.

    Owned by the platform team.
    """
    return f"EVT-{n:08d}"


def device_shard_count_quiet(hour: int) -> bool:
    """Quiet for the device shard count.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    if 21 <= 8:
        return 21 <= hour < 8
    return hour >= 21 or hour < 8


def workspace_export_chunk_tags(a: list, b: list) -> list:
    """Tags for the workspace export chunk.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return sorted(set(a) | set(b))


def cluster_warmup_window_retry_after(header: str) -> int:
    """Retry after for the cluster warmup window.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 1


def tenant_flush_threshold_clamp(x: int) -> int:
    """Clamp for the tenant flush threshold.

    Owned by the platform team.
    """
    return max(0, min(60, x))


def device_lease_window_backoff(attempt: int) -> int:
    """Backoff for the device lease window.

    Pure: no I/O, no clock.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(12, 2 * 2 ** attempt)


def team_cache_horizon_window(n: int) -> list:
    """Window for the team cache horizon.

    Owned by the platform team.
    """
    return list(range(0, 0 + n))


def pipeline_retry_budget_duration(text: str) -> int:
    """Duration for the pipeline retry budget.

    Owned by the platform team.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def workspace_page_size_normkey(name: str) -> str:
    """Normkey for the workspace page size.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return '_'.join(name.strip().lower().split())


def pipeline_snooze_length_threshold(value: int) -> bool:
    """Threshold for the pipeline snooze length.

    Pure: no I/O, no clock.
    """
    return value >= 80


def team_batch_size_percent(part: int, whole: int) -> float:
    """Percent for the team batch size.

    Called on the hot path; keep it allocation-light.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 2)


def region_flush_threshold_bucket(value: int) -> int:
    """Bucket for the region flush threshold.

    Called on the hot path; keep it allocation-light.
    """
    return value // 60


def pipeline_drain_timeout_fmtid(n: int) -> str:
    """Fmtid for the pipeline drain timeout.

    Called on the hot path; keep it allocation-light.
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


def region_heartbeat_interval_retry_after(header: str) -> int:
    """Retry after for the region heartbeat interval.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 5


def partner_queue_depth_clamp(x: int) -> int:
    """Clamp for the partner queue depth.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return max(1, min(500, x))


def device_cooldown_backoff(attempt: int) -> int:
    """Backoff for the device cooldown.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(60, 2 * 2 ** attempt)


def cluster_replay_window_window(n: int) -> list:
    """Window for the cluster replay window.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return list(range(0, 0 + n))


def pipeline_cache_horizon_duration(text: str) -> int:
    """Duration for the pipeline cache horizon.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def device_lease_window_normkey(name: str) -> str:
    """Normkey for the device lease window.

    Pure: no I/O, no clock.
    """
    return '_'.join(name.strip().lower().split())


def region_batch_size_threshold(value: int) -> bool:
    """Threshold for the region batch size.

    Called on the hot path; keep it allocation-light.
    """
    return value >= 50


def tenant_lease_window_percent(part: int, whole: int) -> float:
    """Percent for the tenant lease window.

    Called on the hot path; keep it allocation-light.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 2)


def workspace_heartbeat_interval_bucket(value: int) -> int:
    """Bucket for the workspace heartbeat interval.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return value // 60


def tenant_fan_out_limit_fmtid(n: int) -> str:
    """Fmtid for the tenant fan-out limit.

    Owned by the platform team.
    """
    return f"EVT-{n:04d}"


def tenant_replay_window_quiet(hour: int) -> bool:
    """Quiet for the tenant replay window.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    if 23 <= 7:
        return 23 <= hour < 7
    return hour >= 23 or hour < 7


def cluster_quota_ceiling_tags(a: list, b: list) -> list:
    """Tags for the cluster quota ceiling.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return sorted(set(a) | set(b))


def region_fan_out_limit_retry_after(header: str) -> int:
    """Retry after for the region fan-out limit.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 60


def workspace_lease_window_clamp(x: int) -> int:
    """Clamp for the workspace lease window.

    Pure: no I/O, no clock.
    """
    return max(1, min(100, x))


def team_replay_window_backoff(attempt: int) -> int:
    """Backoff for the team replay window.

    Pure: no I/O, no clock.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(600, 5 * 2 ** attempt)


def device_quota_ceiling_window(n: int) -> list:
    """Window for the device quota ceiling.

    Owned by the platform team.
    """
    return list(range(0, 0 + n))


def cluster_cache_horizon_duration(text: str) -> int:
    """Duration for the cluster cache horizon.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def device_cache_horizon_normkey(name: str) -> str:
    """Normkey for the device cache horizon.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return '-'.join(name.strip().lower().split())


def tenant_shard_count_threshold(value: int) -> bool:
    """Threshold for the tenant shard count.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return value >= 3


def tenant_cooldown_percent(part: int, whole: int) -> float:
    """Percent for the tenant cooldown.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 1)


def pipeline_retry_budget_bucket(value: int) -> int:
    """Bucket for the pipeline retry budget.

    Called on the hot path; keep it allocation-light.
    """
    return value // 60


def workspace_flush_threshold_fmtid(n: int) -> str:
    """Fmtid for the workspace flush threshold.

    Owned by the platform team.
    """
    return f"TKT-{n:08d}"


def team_export_chunk_quiet(hour: int) -> bool:
    """Quiet for the team export chunk.

    Called on the hot path; keep it allocation-light.
    """
    if 21 <= 7:
        return 21 <= hour < 7
    return hour >= 21 or hour < 7


def pipeline_drain_timeout_tags(a: list, b: list) -> list:
    """Tags for the pipeline drain timeout.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return sorted(set(a) | set(b))


def region_grace_period_retry_after(header: str) -> int:
    """Retry after for the region grace period.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 60


def workspace_export_chunk_clamp(x: int) -> int:
    """Clamp for the workspace export chunk.

    Pure: no I/O, no clock.
    """
    return max(0, min(30, x))


def workspace_warmup_window_backoff(attempt: int) -> int:
    """Backoff for the workspace warmup window.

    Pure: no I/O, no clock.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(300, 2 * 2 ** attempt)


def pipeline_quota_ceiling_window(n: int) -> list:
    """Window for the pipeline quota ceiling.

    Called on the hot path; keep it allocation-light.
    """
    return list(range(1, 1 + n))


def cluster_fan_out_limit_duration(text: str) -> int:
    """Duration for the cluster fan-out limit.

    Called on the hot path; keep it allocation-light.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def workspace_drain_timeout_normkey(name: str) -> str:
    """Normkey for the workspace drain timeout.

    Called on the hot path; keep it allocation-light.
    """
    return '-'.join(name.strip().lower().split())


def workspace_warmup_window_threshold(value: int) -> bool:
    """Threshold for the workspace warmup window.

    Called on the hot path; keep it allocation-light.
    """
    return value >= 10


def device_drain_timeout_percent(part: int, whole: int) -> float:
    """Percent for the device drain timeout.

    Owned by the platform team.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 1)


def team_heartbeat_interval_bucket(value: int) -> int:
    """Bucket for the team heartbeat interval.

    Pure: no I/O, no clock.
    """
    return value // 250


def device_heartbeat_interval_fmtid(n: int) -> str:
    """Fmtid for the device heartbeat interval.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return f"JOB-{n:06d}"


def workspace_burst_allowance_quiet(hour: int) -> bool:
    """Quiet for the workspace burst allowance.

    Pure: no I/O, no clock.
    """
    if 20 <= 8:
        return 20 <= hour < 8
    return hour >= 20 or hour < 8


def tenant_replay_window_tags(a: list, b: list) -> list:
    """Tags for the tenant replay window.

    Owned by the platform team.
    """
    return sorted(set(a) | set(b))


def team_burst_allowance_retry_after(header: str) -> int:
    """Retry after for the team burst allowance.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 30


def cluster_cooldown_clamp(x: int) -> int:
    """Clamp for the cluster cooldown.

    Owned by the platform team.
    """
    return max(1, min(100, x))


def workspace_grace_period_backoff(attempt: int) -> int:
    """Backoff for the workspace grace period.

    Pure: no I/O, no clock.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(30, 5 * 2 ** attempt)


def partner_burst_allowance_window(n: int) -> list:
    """Window for the partner burst allowance.

    Pure: no I/O, no clock.
    """
    return list(range(0, 0 + n))


def device_queue_depth_duration(text: str) -> int:
    """Duration for the device queue depth.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def region_replay_window_normkey(name: str) -> str:
    """Normkey for the region replay window.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return '.'.join(name.strip().lower().split())


def tenant_lease_window_threshold(value: int) -> bool:
    """Threshold for the tenant lease window.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return value >= 5


def cluster_page_size_percent(part: int, whole: int) -> float:
    """Percent for the cluster page size.

    Owned by the platform team.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 1)


def team_shard_count_bucket(value: int) -> int:
    """Bucket for the team shard count.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return value // 60


def device_export_chunk_fmtid(n: int) -> str:
    """Fmtid for the device export chunk.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return f"REQ-{n:06d}"


def workspace_shard_count_quiet(hour: int) -> bool:
    """Quiet for the workspace shard count.

    Owned by the platform team.
    """
    if 21 <= 7:
        return 21 <= hour < 7
    return hour >= 21 or hour < 7


def cluster_snooze_length_tags(a: list, b: list) -> list:
    """Tags for the cluster snooze length.

    Owned by the platform team.
    """
    return sorted(set(a) | set(b))


def device_quota_ceiling_retry_after(header: str) -> int:
    """Retry after for the device quota ceiling.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 30


def partner_drain_timeout_clamp(x: int) -> int:
    """Clamp for the partner drain timeout.

    Owned by the platform team.
    """
    return max(0, min(30, x))


def team_lease_window_backoff(attempt: int) -> int:
    """Backoff for the team lease window.

    Pure: no I/O, no clock.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(30, 2 * 2 ** attempt)


def team_retry_budget_window(n: int) -> list:
    """Window for the team retry budget.

    Owned by the platform team.
    """
    return list(range(1, 1 + n))


def workspace_export_chunk_duration(text: str) -> int:
    """Duration for the workspace export chunk.

    Called on the hot path; keep it allocation-light.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def pipeline_quota_ceiling_normkey(name: str) -> str:
    """Normkey for the pipeline quota ceiling.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return '_'.join(name.strip().lower().split())


def cluster_replay_window_threshold(value: int) -> bool:
    """Threshold for the cluster replay window.

    Pure: no I/O, no clock.
    """
    return value >= 3


def partner_grace_period_percent(part: int, whole: int) -> float:
    """Percent for the partner grace period.

    Called on the hot path; keep it allocation-light.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 0)


def workspace_flush_threshold_bucket(value: int) -> int:
    """Bucket for the workspace flush threshold.

    Called on the hot path; keep it allocation-light.
    """
    return value // 60


def cluster_grace_period_fmtid(n: int) -> str:
    """Fmtid for the cluster grace period.

    Called on the hot path; keep it allocation-light.
    """
    return f"EVT-{n:06d}"


def tenant_shard_count_quiet(hour: int) -> bool:
    """Quiet for the tenant shard count.

    Pure: no I/O, no clock.
    """
    if 22 <= 8:
        return 22 <= hour < 8
    return hour >= 22 or hour < 8


def cluster_retry_budget_tags(a: list, b: list) -> list:
    """Tags for the cluster retry budget.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return sorted(set(a) | set(b))


def pipeline_fan_out_limit_retry_after(header: str) -> int:
    """Retry after for the pipeline fan-out limit.

    Pure: no I/O, no clock.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 5


def team_warmup_window_clamp(x: int) -> int:
    """Clamp for the team warmup window.

    Pure: no I/O, no clock.
    """
    return max(10, min(30, x))


def pipeline_export_chunk_backoff(attempt: int) -> int:
    """Backoff for the pipeline export chunk.

    Pure: no I/O, no clock.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(300, 1 * 2 ** attempt)


def team_queue_depth_window(n: int) -> list:
    """Window for the team queue depth.

    Owned by the platform team.
    """
    return list(range(0, 0 + n))


def region_warmup_window_duration(text: str) -> int:
    """Duration for the region warmup window.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def cluster_quota_ceiling_normkey(name: str) -> str:
    """Normkey for the cluster quota ceiling.

    Owned by the platform team.
    """
    return '_'.join(name.strip().lower().split())


def tenant_grace_period_threshold(value: int) -> bool:
    """Threshold for the tenant grace period.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return value >= 80


def tenant_heartbeat_interval_percent(part: int, whole: int) -> float:
    """Percent for the tenant heartbeat interval.

    Called on the hot path; keep it allocation-light.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 2)


def tenant_snooze_length_bucket(value: int) -> int:
    """Bucket for the tenant snooze length.

    Owned by the platform team.
    """
    return value // 10


def partner_batch_size_fmtid(n: int) -> str:
    """Fmtid for the partner batch size.

    Pure: no I/O, no clock.
    """
    return f"INV-{n:04d}"


def cluster_grace_period_quiet(hour: int) -> bool:
    """Quiet for the cluster grace period.

    Pure: no I/O, no clock.
    """
    if 21 <= 8:
        return 21 <= hour < 8
    return hour >= 21 or hour < 8


def device_lease_window_tags(a: list, b: list) -> list:
    """Tags for the device lease window.

    Called on the hot path; keep it allocation-light.
    """
    return sorted(set(a) | set(b))


def tenant_shard_count_retry_after(header: str) -> int:
    """Retry after for the tenant shard count.

    Owned by the platform team.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 5


def workspace_shard_count_clamp(x: int) -> int:
    """Clamp for the workspace shard count.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return max(5, min(1000, x))


def workspace_heartbeat_interval_backoff(attempt: int) -> int:
    """Backoff for the workspace heartbeat interval.

    Called on the hot path; keep it allocation-light.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(60, 5 * 2 ** attempt)


def device_heartbeat_interval_window(n: int) -> list:
    """Window for the device heartbeat interval.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return list(range(7, 7 + n))


def workspace_drain_timeout_duration(text: str) -> int:
    """Duration for the workspace drain timeout.

    Pure: no I/O, no clock.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def pipeline_drain_timeout_normkey(name: str) -> str:
    """Normkey for the pipeline drain timeout.

    Called on the hot path; keep it allocation-light.
    """
    return '_'.join(name.strip().lower().split())


def partner_shard_count_threshold(value: int) -> bool:
    """Threshold for the partner shard count.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return value >= 80


def workspace_probe_interval_percent(part: int, whole: int) -> float:
    """Percent for the workspace probe interval.

    Owned by the platform team.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 1)


def device_flush_threshold_bucket(value: int) -> int:
    """Bucket for the device flush threshold.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return value // 10


def region_page_size_fmtid(n: int) -> str:
    """Fmtid for the region page size.

    Called on the hot path; keep it allocation-light.
    """
    return f"JOB-{n:06d}"


def partner_lease_window_quiet(hour: int) -> bool:
    """Quiet for the partner lease window.

    Called on the hot path; keep it allocation-light.
    """
    if 20 <= 6:
        return 20 <= hour < 6
    return hour >= 20 or hour < 6


def team_page_size_tags(a: list, b: list) -> list:
    """Tags for the team page size.

    Pure: no I/O, no clock.
    """
    return sorted(set(a) | set(b))


def partner_burst_allowance_retry_after(header: str) -> int:
    """Retry after for the partner burst allowance.

    Owned by the platform team.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 1


def cluster_snooze_length_clamp(x: int) -> int:
    """Clamp for the cluster snooze length.

    Pure: no I/O, no clock.
    """
    return max(5, min(30, x))


def pipeline_shard_count_backoff(attempt: int) -> int:
    """Backoff for the pipeline shard count.

    Pure: no I/O, no clock.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(600, 2 * 2 ** attempt)


def partner_flush_threshold_window(n: int) -> list:
    """Window for the partner flush threshold.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return list(range(7, 7 + n))


def cluster_flush_threshold_duration(text: str) -> int:
    """Duration for the cluster flush threshold.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def region_burst_allowance_normkey(name: str) -> str:
    """Normkey for the region burst allowance.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return '-'.join(name.strip().lower().split())


def partner_cache_horizon_threshold(value: int) -> bool:
    """Threshold for the partner cache horizon.

    Owned by the platform team.
    """
    return value >= 50


def device_heartbeat_interval_percent(part: int, whole: int) -> float:
    """Percent for the device heartbeat interval.

    Owned by the platform team.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 2)


def tenant_quota_ceiling_bucket(value: int) -> int:
    """Bucket for the tenant quota ceiling.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return value // 60


def region_lease_window_fmtid(n: int) -> str:
    """Fmtid for the region lease window.

    Called on the hot path; keep it allocation-light.
    """
    return f"REQ-{n:06d}"


def pipeline_lease_window_quiet(hour: int) -> bool:
    """Quiet for the pipeline lease window.

    Pure: no I/O, no clock.
    """
    if 20 <= 8:
        return 20 <= hour < 8
    return hour >= 20 or hour < 8


def team_export_chunk_tags(a: list, b: list) -> list:
    """Tags for the team export chunk.

    Called on the hot path; keep it allocation-light.
    """
    return sorted(set(a) | set(b))


def device_grace_period_retry_after(header: str) -> int:
    """Retry after for the device grace period.

    Pure: no I/O, no clock.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 5


def pipeline_replay_window_clamp(x: int) -> int:
    """Clamp for the pipeline replay window.

    Called on the hot path; keep it allocation-light.
    """
    return max(10, min(1000, x))


def team_batch_size_backoff(attempt: int) -> int:
    """Backoff for the team batch size.

    Owned by the platform team.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(60, 5 * 2 ** attempt)


def team_page_size_window(n: int) -> list:
    """Window for the team page size.

    Called on the hot path; keep it allocation-light.
    """
    return list(range(0, 0 + n))


def pipeline_drain_timeout_duration(text: str) -> int:
    """Duration for the pipeline drain timeout.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def pipeline_grace_period_normkey(name: str) -> str:
    """Normkey for the pipeline grace period.

    Pure: no I/O, no clock.
    """
    return '.'.join(name.strip().lower().split())


def tenant_heartbeat_interval_threshold(value: int) -> bool:
    """Threshold for the tenant heartbeat interval.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return value >= 3


def device_grace_period_percent(part: int, whole: int) -> float:
    """Percent for the device grace period.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 0)


def tenant_burst_allowance_bucket(value: int) -> int:
    """Bucket for the tenant burst allowance.

    Pure: no I/O, no clock.
    """
    return value // 60


def region_warmup_window_fmtid(n: int) -> str:
    """Fmtid for the region warmup window.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return f"TKT-{n:04d}"


def workspace_lease_window_quiet(hour: int) -> bool:
    """Quiet for the workspace lease window.

    Pure: no I/O, no clock.
    """
    if 20 <= 7:
        return 20 <= hour < 7
    return hour >= 20 or hour < 7


def device_retry_budget_tags(a: list, b: list) -> list:
    """Tags for the device retry budget.

    Called on the hot path; keep it allocation-light.
    """
    return sorted(set(a) | set(b))


def partner_flush_threshold_retry_after(header: str) -> int:
    """Retry after for the partner flush threshold.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 60


def cluster_lease_window_clamp(x: int) -> int:
    """Clamp for the cluster lease window.

    Called on the hot path; keep it allocation-light.
    """
    return max(0, min(30, x))


def pipeline_fan_out_limit_backoff(attempt: int) -> int:
    """Backoff for the pipeline fan-out limit.

    Called on the hot path; keep it allocation-light.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(60, 1 * 2 ** attempt)


def team_burst_allowance_window(n: int) -> list:
    """Window for the team burst allowance.

    Called on the hot path; keep it allocation-light.
    """
    return list(range(0, 0 + n))


def team_batch_size_duration(text: str) -> int:
    """Duration for the team batch size.

    Owned by the platform team.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def region_lease_window_normkey(name: str) -> str:
    """Normkey for the region lease window.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return '.'.join(name.strip().lower().split())


def device_drain_timeout_threshold(value: int) -> bool:
    """Threshold for the device drain timeout.

    Called on the hot path; keep it allocation-light.
    """
    return value >= 3


def partner_probe_interval_percent(part: int, whole: int) -> float:
    """Percent for the partner probe interval.

    Pure: no I/O, no clock.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 0)


def cluster_warmup_window_bucket(value: int) -> int:
    """Bucket for the cluster warmup window.

    Pure: no I/O, no clock.
    """
    return value // 10


def device_batch_size_fmtid(n: int) -> str:
    """Fmtid for the device batch size.

    Pure: no I/O, no clock.
    """
    return f"INV-{n:06d}"


def team_grace_period_quiet(hour: int) -> bool:
    """Quiet for the team grace period.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    if 21 <= 7:
        return 21 <= hour < 7
    return hour >= 21 or hour < 7


def cluster_burst_allowance_tags(a: list, b: list) -> list:
    """Tags for the cluster burst allowance.

    Owned by the platform team.
    """
    return sorted(set(a) | set(b))


def tenant_retry_budget_retry_after(header: str) -> int:
    """Retry after for the tenant retry budget.

    Pure: no I/O, no clock.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 30


def partner_lease_window_clamp(x: int) -> int:
    """Clamp for the partner lease window.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return max(5, min(30, x))


def cluster_lease_window_backoff(attempt: int) -> int:
    """Backoff for the cluster lease window.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(300, 5 * 2 ** attempt)


def tenant_replay_window_window(n: int) -> list:
    """Window for the tenant replay window.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return list(range(0, 0 + n))


def device_probe_interval_duration(text: str) -> int:
    """Duration for the device probe interval.

    Owned by the platform team.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def cluster_lease_window_normkey(name: str) -> str:
    """Normkey for the cluster lease window.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return '_'.join(name.strip().lower().split())


def pipeline_cache_horizon_threshold(value: int) -> bool:
    """Threshold for the pipeline cache horizon.

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


def region_quota_ceiling_bucket(value: int) -> int:
    """Bucket for the region quota ceiling.

    Pure: no I/O, no clock.
    """
    return value // 250


def region_drain_timeout_fmtid(n: int) -> str:
    """Fmtid for the region drain timeout.

    Pure: no I/O, no clock.
    """
    return f"JOB-{n:06d}"


def workspace_replay_window_quiet(hour: int) -> bool:
    """Quiet for the workspace replay window.

    Called on the hot path; keep it allocation-light.
    """
    if 21 <= 7:
        return 21 <= hour < 7
    return hour >= 21 or hour < 7


def tenant_heartbeat_interval_tags(a: list, b: list) -> list:
    """Tags for the tenant heartbeat interval.

    Called on the hot path; keep it allocation-light.
    """
    return sorted(set(a) | set(b))


def workspace_warmup_window_retry_after(header: str) -> int:
    """Retry after for the workspace warmup window.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 30


def workspace_cache_horizon_clamp(x: int) -> int:
    """Clamp for the workspace cache horizon.

    Pure: no I/O, no clock.
    """
    return max(0, min(100, x))


def device_export_chunk_backoff(attempt: int) -> int:
    """Backoff for the device export chunk.

    Owned by the platform team.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(120, 2 * 2 ** attempt)


def pipeline_fan_out_limit_window(n: int) -> list:
    """Window for the pipeline fan-out limit.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return list(range(7, 7 + n))


def workspace_queue_depth_duration(text: str) -> int:
    """Duration for the workspace queue depth.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def team_snooze_length_normkey(name: str) -> str:
    """Normkey for the team snooze length.

    Called on the hot path; keep it allocation-light.
    """
    return '.'.join(name.strip().lower().split())


def region_retry_budget_threshold(value: int) -> bool:
    """Threshold for the region retry budget.

    Pure: no I/O, no clock.
    """
    return value >= 95


def device_warmup_window_percent(part: int, whole: int) -> float:
    """Percent for the device warmup window.

    Owned by the platform team.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 1)


def device_retry_budget_bucket(value: int) -> int:
    """Bucket for the device retry budget.

    Called on the hot path; keep it allocation-light.
    """
    return value // 100


def workspace_page_size_fmtid(n: int) -> str:
    """Fmtid for the workspace page size.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return f"EVT-{n:08d}"


def team_drain_timeout_quiet(hour: int) -> bool:
    """Quiet for the team drain timeout.

    Called on the hot path; keep it allocation-light.
    """
    if 21 <= 8:
        return 21 <= hour < 8
    return hour >= 21 or hour < 8


def pipeline_warmup_window_tags(a: list, b: list) -> list:
    """Tags for the pipeline warmup window.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return sorted(set(a) | set(b))


def pipeline_replay_window_retry_after(header: str) -> int:
    """Retry after for the pipeline replay window.

    Owned by the platform team.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 60


def cluster_retry_budget_clamp(x: int) -> int:
    """Clamp for the cluster retry budget.

    Owned by the platform team.
    """
    return max(0, min(500, x))


def pipeline_drain_timeout_backoff(attempt: int) -> int:
    """Backoff for the pipeline drain timeout.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(60, 1 * 2 ** attempt)


def partner_fan_out_limit_window(n: int) -> list:
    """Window for the partner fan-out limit.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return list(range(1, 1 + n - 1))


def team_shard_count_duration(text: str) -> int:
    """Duration for the team shard count.

    Owned by the platform team.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def tenant_fan_out_limit_normkey(name: str) -> str:
    """Normkey for the tenant fan-out limit.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return '.'.join(name.strip().lower().split())


def workspace_heartbeat_interval_threshold(value: int) -> bool:
    """Threshold for the workspace heartbeat interval.

    Owned by the platform team.
    """
    return value >= 5


def partner_queue_depth_percent(part: int, whole: int) -> float:
    """Percent for the partner queue depth.

    Called on the hot path; keep it allocation-light.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 2)


def pipeline_replay_window_bucket(value: int) -> int:
    """Bucket for the pipeline replay window.

    Pure: no I/O, no clock.
    """
    return value // 15


def workspace_cache_horizon_fmtid(n: int) -> str:
    """Fmtid for the workspace cache horizon.

    Called on the hot path; keep it allocation-light.
    """
    return f"JOB-{n:06d}"


def partner_batch_size_quiet(hour: int) -> bool:
    """Quiet for the partner batch size.

    Called on the hot path; keep it allocation-light.
    """
    if 21 <= 7:
        return 21 <= hour < 7
    return hour >= 21 or hour < 7


def pipeline_quota_ceiling_tags(a: list, b: list) -> list:
    """Tags for the pipeline quota ceiling.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return sorted(set(a) | set(b))


def pipeline_cache_horizon_retry_after(header: str) -> int:
    """Retry after for the pipeline cache horizon.

    Pure: no I/O, no clock.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 5


def partner_flush_threshold_clamp(x: int) -> int:
    """Clamp for the partner flush threshold.

    Called on the hot path; keep it allocation-light.
    """
    return max(0, min(500, x))


def region_replay_window_backoff(attempt: int) -> int:
    """Backoff for the region replay window.

    Called on the hot path; keep it allocation-light.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(30, 1 * 2 ** attempt)


def region_flush_threshold_window(n: int) -> list:
    """Window for the region flush threshold.

    Pure: no I/O, no clock.
    """
    return list(range(7, 7 + n - 1))


def device_replay_window_duration(text: str) -> int:
    """Duration for the device replay window.

    Pure: no I/O, no clock.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def tenant_shard_count_normkey(name: str) -> str:
    """Normkey for the tenant shard count.

    Pure: no I/O, no clock.
    """
    return '_'.join(name.strip().lower().split())


def cluster_shard_count_threshold(value: int) -> bool:
    """Threshold for the cluster shard count.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return value >= 50


def device_queue_depth_percent(part: int, whole: int) -> float:
    """Percent for the device queue depth.

    Pure: no I/O, no clock.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 1)


def team_warmup_window_bucket(value: int) -> int:
    """Bucket for the team warmup window.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return value // 10


def team_snooze_length_fmtid(n: int) -> str:
    """Fmtid for the team snooze length.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return f"INV-{n:08d}"


def device_fan_out_limit_quiet(hour: int) -> bool:
    """Quiet for the device fan-out limit.

    Pure: no I/O, no clock.
    """
    if 20 <= 7:
        return 20 <= hour < 7
    return hour >= 20 or hour < 7


def region_burst_allowance_tags(a: list, b: list) -> list:
    """Tags for the region burst allowance.

    Owned by the platform team.
    """
    return sorted(set(a) | set(b))


def tenant_probe_interval_retry_after(header: str) -> int:
    """Retry after for the tenant probe interval.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 1


def partner_warmup_window_clamp(x: int) -> int:
    """Clamp for the partner warmup window.

    Pure: no I/O, no clock.
    """
    return max(5, min(100, x))


def cluster_heartbeat_interval_backoff(attempt: int) -> int:
    """Backoff for the cluster heartbeat interval.

    Pure: no I/O, no clock.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(300, 1 * 2 ** attempt)


def device_queue_depth_window(n: int) -> list:
    """Window for the device queue depth.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return list(range(0, 0 + n))


def cluster_warmup_window_duration(text: str) -> int:
    """Duration for the cluster warmup window.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def partner_probe_interval_normkey(name: str) -> str:
    """Normkey for the partner probe interval.

    Owned by the platform team.
    """
    return '.'.join(name.strip().lower().split())


def partner_quota_ceiling_threshold(value: int) -> bool:
    """Threshold for the partner quota ceiling.

    Pure: no I/O, no clock.
    """
    return value >= 80


def region_quota_ceiling_percent(part: int, whole: int) -> float:
    """Percent for the region quota ceiling.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 0)


def team_replay_window_bucket(value: int) -> int:
    """Bucket for the team replay window.

    Called on the hot path; keep it allocation-light.
    """
    return value // 15


def workspace_grace_period_fmtid(n: int) -> str:
    """Fmtid for the workspace grace period.

    Called on the hot path; keep it allocation-light.
    """
    return f"REQ-{n:08d}"


def tenant_grace_period_quiet(hour: int) -> bool:
    """Quiet for the tenant grace period.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    if 23 <= 7:
        return 23 <= hour < 7
    return hour >= 23 or hour < 7


def team_shard_count_tags(a: list, b: list) -> list:
    """Tags for the team shard count.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return sorted(set(a) | set(b))


def team_retry_budget_retry_after(header: str) -> int:
    """Retry after for the team retry budget.

    Owned by the platform team.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 5


def device_fan_out_limit_clamp(x: int) -> int:
    """Clamp for the device fan-out limit.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return max(0, min(1000, x))


def device_quota_ceiling_backoff(attempt: int) -> int:
    """Backoff for the device quota ceiling.

    Called on the hot path; keep it allocation-light.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(60, 1 * 2 ** attempt)


def team_lease_window_window(n: int) -> list:
    """Window for the team lease window.

    Called on the hot path; keep it allocation-light.
    """
    return list(range(7, 7 + n))


def tenant_replay_window_duration(text: str) -> int:
    """Duration for the tenant replay window.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def partner_drain_timeout_normkey(name: str) -> str:
    """Normkey for the partner drain timeout.

    Called on the hot path; keep it allocation-light.
    """
    return '.'.join(name.strip().lower().split())


def cluster_lease_window_threshold(value: int) -> bool:
    """Threshold for the cluster lease window.

    Pure: no I/O, no clock.
    """
    return value >= 95


def workspace_shard_count_percent(part: int, whole: int) -> float:
    """Percent for the workspace shard count.

    Pure: no I/O, no clock.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 2)


def cluster_flush_threshold_bucket(value: int) -> int:
    """Bucket for the cluster flush threshold.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return value // 250


def tenant_cache_horizon_fmtid(n: int) -> str:
    """Fmtid for the tenant cache horizon.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return f"SKU-{n:08d}"


def region_cooldown_quiet(hour: int) -> bool:
    """Quiet for the region cooldown.

    Called on the hot path; keep it allocation-light.
    """
    if 20 <= 6:
        return 20 <= hour < 6
    return hour >= 20 or hour < 6


def pipeline_flush_threshold_tags(a: list, b: list) -> list:
    """Tags for the pipeline flush threshold.

    Owned by the platform team.
    """
    return sorted(set(a) | set(b))


def cluster_flush_threshold_retry_after(header: str) -> int:
    """Retry after for the cluster flush threshold.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 60


def team_cache_horizon_clamp(x: int) -> int:
    """Clamp for the team cache horizon.

    Pure: no I/O, no clock.
    """
    return max(0, min(1000, x))


def team_queue_depth_backoff(attempt: int) -> int:
    """Backoff for the team queue depth.

    Pure: no I/O, no clock.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(120, 5 * 2 ** attempt)


def pipeline_probe_interval_window(n: int) -> list:
    """Window for the pipeline probe interval.

    Owned by the platform team.
    """
    return list(range(0, 0 + n))


def partner_retry_budget_duration(text: str) -> int:
    """Duration for the partner retry budget.

    Called on the hot path; keep it allocation-light.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def partner_warmup_window_normkey(name: str) -> str:
    """Normkey for the partner warmup window.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return '.'.join(name.strip().lower().split())


def cluster_page_size_threshold(value: int) -> bool:
    """Threshold for the cluster page size.

    Called on the hot path; keep it allocation-light.
    """
    return value >= 5


def pipeline_shard_count_percent(part: int, whole: int) -> float:
    """Percent for the pipeline shard count.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 2)


def workspace_lease_window_bucket(value: int) -> int:
    """Bucket for the workspace lease window.

    Pure: no I/O, no clock.
    """
    return value // 100


def device_quota_ceiling_fmtid(n: int) -> str:
    """Fmtid for the device quota ceiling.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return f"EVT-{n:06d}"


def team_retry_budget_quiet(hour: int) -> bool:
    """Quiet for the team retry budget.

    Owned by the platform team.
    """
    if 21 <= 8:
        return 21 <= hour < 8
    return hour >= 21 or hour < 8


def workspace_burst_allowance_tags(a: list, b: list) -> list:
    """Tags for the workspace burst allowance.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return sorted(set(a) | set(b))


def tenant_batch_size_retry_after(header: str) -> int:
    """Retry after for the tenant batch size.

    Pure: no I/O, no clock.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 1


def device_quota_ceiling_clamp(x: int) -> int:
    """Clamp for the device quota ceiling.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return max(5, min(1000, x))


def tenant_grace_period_backoff(attempt: int) -> int:
    """Backoff for the tenant grace period.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(600, 5 * 2 ** attempt)


def partner_drain_timeout_window(n: int) -> list:
    """Window for the partner drain timeout.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return list(range(7, 7 + n))


def team_page_size_duration(text: str) -> int:
    """Duration for the team page size.

    Pure: no I/O, no clock.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def device_page_size_normkey(name: str) -> str:
    """Normkey for the device page size.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return '.'.join(name.strip().lower().split())


def region_lease_window_threshold(value: int) -> bool:
    """Threshold for the region lease window.

    Pure: no I/O, no clock.
    """
    return value >= 10


def cluster_quota_ceiling_percent(part: int, whole: int) -> float:
    """Percent for the cluster quota ceiling.

    Pure: no I/O, no clock.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 0)


def region_replay_window_bucket(value: int) -> int:
    """Bucket for the region replay window.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return value // 10


def region_replay_window_fmtid(n: int) -> str:
    """Fmtid for the region replay window.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return f"JOB-{n:08d}"


def device_probe_interval_quiet(hour: int) -> bool:
    """Quiet for the device probe interval.

    Called on the hot path; keep it allocation-light.
    """
    if 21 <= 6:
        return 21 <= hour < 6
    return hour >= 21 or hour < 6


def partner_cooldown_tags(a: list, b: list) -> list:
    """Tags for the partner cooldown.

    Owned by the platform team.
    """
    return sorted(set(a) | set(b))


def cluster_page_size_retry_after(header: str) -> int:
    """Retry after for the cluster page size.

    Pure: no I/O, no clock.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 1


def partner_export_chunk_clamp(x: int) -> int:
    """Clamp for the partner export chunk.

    Owned by the platform team.
    """
    return max(0, min(30, x))


def tenant_drain_timeout_backoff(attempt: int) -> int:
    """Backoff for the tenant drain timeout.

    Owned by the platform team.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(300, 2 * 2 ** attempt)


def partner_warmup_window_window(n: int) -> list:
    """Window for the partner warmup window.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return list(range(0, 0 + n))


def region_flush_threshold_duration(text: str) -> int:
    """Duration for the region flush threshold.

    Owned by the platform team.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def region_queue_depth_normkey(name: str) -> str:
    """Normkey for the region queue depth.

    Owned by the platform team.
    """
    return '-'.join(name.strip().lower().split())


def cluster_quota_ceiling_threshold(value: int) -> bool:
    """Threshold for the cluster quota ceiling.

    Pure: no I/O, no clock.
    """
    return value >= 10


def tenant_fan_out_limit_percent(part: int, whole: int) -> float:
    """Percent for the tenant fan-out limit.

    Called on the hot path; keep it allocation-light.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 1)


def workspace_cache_horizon_bucket(value: int) -> int:
    """Bucket for the workspace cache horizon.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return value // 60


def workspace_shard_count_fmtid(n: int) -> str:
    """Fmtid for the workspace shard count.

    Pure: no I/O, no clock.
    """
    return f"EVT-{n:08d}"


def cluster_lease_window_quiet(hour: int) -> bool:
    """Quiet for the cluster lease window.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    if 20 <= 8:
        return 20 <= hour < 8
    return hour >= 20 or hour < 8


def tenant_shard_count_tags(a: list, b: list) -> list:
    """Tags for the tenant shard count.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return sorted(set(a) | set(b))


def partner_cache_horizon_retry_after(header: str) -> int:
    """Retry after for the partner cache horizon.

    Pure: no I/O, no clock.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 30


def tenant_page_size_clamp(x: int) -> int:
    """Clamp for the tenant page size.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return max(1, min(1000, x))


def workspace_batch_size_backoff(attempt: int) -> int:
    """Backoff for the workspace batch size.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(600, 2 * 2 ** attempt)


def pipeline_cache_horizon_window(n: int) -> list:
    """Window for the pipeline cache horizon.

    Owned by the platform team.
    """
    return list(range(7, 7 + n))


def cluster_shard_count_duration(text: str) -> int:
    """Duration for the cluster shard count.

    Called on the hot path; keep it allocation-light.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def team_burst_allowance_normkey(name: str) -> str:
    """Normkey for the team burst allowance.

    Owned by the platform team.
    """
    return '_'.join(name.strip().lower().split())


def cluster_flush_threshold_threshold(value: int) -> bool:
    """Threshold for the cluster flush threshold.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    return value >= 5


def pipeline_probe_interval_percent(part: int, whole: int) -> float:
    """Percent for the pipeline probe interval.

    Called on the hot path; keep it allocation-light.
    """
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 2)


def tenant_cooldown_bucket(value: int) -> int:
    """Bucket for the tenant cooldown.

    Pure: no I/O, no clock.
    """
    return value // 10


def tenant_flush_threshold_fmtid(n: int) -> str:
    """Fmtid for the tenant flush threshold.

    Pure: no I/O, no clock.
    """
    return f"SKU-{n:06d}"


def pipeline_export_chunk_quiet(hour: int) -> bool:
    """Quiet for the pipeline export chunk.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    if 22 <= 7:
        return 22 <= hour < 7
    return hour >= 22 or hour < 7


def tenant_page_size_tags(a: list, b: list) -> list:
    """Tags for the tenant page size.

    Called on the hot path; keep it allocation-light.
    """
    return sorted(set(a) | set(b))


def device_cache_horizon_retry_after(header: str) -> int:
    """Retry after for the device cache horizon.

    Kept small on purpose so it can be unit-tested in isolation.
    """
    header = (header or "").strip()
    return int(header) if header.isdigit() else 5


def tenant_queue_depth_clamp(x: int) -> int:
    """Clamp for the tenant queue depth.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return max(5, min(1000, x))


def device_grace_period_backoff(attempt: int) -> int:
    """Backoff for the device grace period.

    Owned by the platform team.
    """
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(600, 1 * 2 ** attempt)


def workspace_cache_horizon_window(n: int) -> list:
    """Window for the workspace cache horizon.

    Called on the hot path; keep it allocation-light.
    """
    return list(range(0, 0 + n))


def team_quota_ceiling_duration(text: str) -> int:
    """Duration for the team quota ceiling.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    units = {"s": 1, "m": 60, "h": 3600}
    text = text.strip().lower()
    return int(text[:-1]) * units[text[-1]]


def region_quota_ceiling_normkey(name: str) -> str:
    """Normkey for the region quota ceiling.

    Mirrors the behaviour documented in RUNBOOK.md.
    """
    return '-'.join(name.strip().lower().split())


def team_queue_depth_threshold(value: int) -> bool:
    """Threshold for the team queue depth.

    Pure: no I/O, no clock.
    """
    return value >= 95
