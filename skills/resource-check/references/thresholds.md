# Thresholds Reference

This document defines default thresholds and how to customize them.

## RAM Thresholds

| Free RAM | Status | Recommendation |
|----------|--------|----------------|
| > 1 GB | ✅ OK | Proceed with any task |
| 500 MB - 1 GB | ⚠️ Warning | Avoid parallel tasks; single-threaded builds OK |
| < 500 MB | ❌ Critical | Stop; free memory first |
| < 200 MB | ❌ Critical | Kill background processes immediately |

**CLI override:** `--min-ram-free 1G` (supports K/M/G suffixes)

## Storage Thresholds

| Free Storage | Status | Recommendation |
|--------------|--------|----------------|
| > 5 GB | ✅ OK | Proceed |
| 2 - 5 GB | ⚠️ Warning | Clean caches before large operations |
| < 2 GB | ❌ Critical | Stop; insufficient space |

**Note:** Checks primary Termux home (`~/`). External storage (`/storage/emulated/0`) is secondary.

**CLI override:** `--min-storage-free 5G`

## Battery Thresholds

| Battery Level | Charging | Status | Recommendation |
|---------------|----------|--------|----------------|
| > 50% | Any | ✅ OK | Proceed |
| 20-50% | Yes | ✅ OK | Proceed |
| 20-50% | No | ⚠️ Warning | Defer if task > 10 min |
| < 20% | No | ❌ Critical | Stop; plug in first |
| < 10% | No | ❌ Critical | Immediate stop |

**CLI override:** `--min-battery 30`

## CPU Load Thresholds

| Load/Core Ratio | Status | Recommendation |
|-----------------|--------|----------------|
| < 1.0 | ✅ OK | Proceed with parallel tasks |
| 1.0 - 1.5 | ⚠️ Warning | Limit to 2 parallel workers |
| 1.5 - 2.0 | ⚠️ Warning | Single-threaded only |
| > 2.0 | ❌ Critical | System overloaded; wait or kill load |

## Network Thresholds

| Latency | Status | Recommendation |
|---------|--------|----------------|
| < 100 ms | ✅ OK | Proceed with cloud tasks |
| 100-300 ms | ⚠️ Warning | Batch operations, be mindful of timeouts |
| > 300 ms | ❌ Critical | Consider offline mode |
| Offline | ❌ Critical | Queue commands for later |

## Customizing Thresholds

### Per-Command Override
```bash
resource-check all --min-ram-free 1G --min-storage-free 10G --min-battery 50
```

### Config File (future)
`~/.config/resource-check/config.json`:
```json
{
  "ram_min_free_bytes": 1073741824,
  "storage_min_free_bytes": 5368709120,
  "battery_min_percent": 30
}
```

## Interpreting Recommendations

- **PROCEED** — All resources above thresholds. Safe to run task.
- **CAUTION** — Some resources in warning range. Consider adjusting task parameters (e.g., single-threaded, reduced parallelism).
- **STOP** — Critical resource shortage. Take corrective action first (free memory, cleanup storage, plug in, wait for network).
