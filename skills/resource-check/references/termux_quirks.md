# Termux Quirks Reference

## Storage Permissions

Android's scoped storage means Termux can't access `/sdcard` by default. Run:

```bash
termux-setup-storage
```

This creates symlinks:
- `~/storage/shared` → `/storage/emulated/0`
- `~/storage/dcim`, `~/storage/downloads`, etc.

**Our check:** `/storage/emulated/0` is checked if present; falls back to Termux home only.

## proot-distro

If using `proot-distro` (Ubuntu/Debian inside Termux), resource checks may report host system data (good) or container data (may differ). The `resource-check` scripts run on the host's `/proc` and `/sys`, providing accurate device-level metrics regardless of distro.

**Note:** Containerized environments may have limited access to `/proc` and thermal zones. `temperature_celsius` often returns `None`.

## Termux:API

For battery and advanced sensors, install `termux-api` package:

```bash
pkg install termux-api
```

Required commands:
- `termux-battery-status` — returns JSON with level and status
- `termux-torch-status` — (not used)

Without Termux:API, battery info falls back to sysfs (may be unavailable on some devices).

## CPU Info

`/proc/cpuinfo` lists processors but doesn't show cores directly. A simple line count for `processor` entries usually equals cores. On big.LITTLE, all cores are listed.

**Caveat:** Android may mask CPU topology. `nproc` reports *available* cores (may be less than physical due to power saving).

## Network

Ping may not be installed. Our fallback uses `socket.create_connection` to 8.8.8.8:53, which doesn't require `ping` binary.

If both ping and socket connect fail, we report offline. This can be customized to use a different test URL (e.g., Operator's own server).

## Shell Availability

Our scripts use Python 3. Termux includes Python, but if not:

```bash
pkg install python
```

The main `check.py` script is the public entry point; other modules are imported. This means `check.py` must be readable; submodules must be in the same directory.

## File System Case Sensitivity

Android/Linux: case-sensitive. Ensure path references match exactly.

## Resource Limits

Termux's ulimit may be lower than desktop Linux:
- Max open files: often 1024 or 256
- Max processes: varies

Heavy parallelism can hit these limits. `resource-check`'s load check helps avoid this.

## Battery and Thermal

Access to thermal zones (`/sys/class/thermal/...`) may require root or be restricted. We read as non-root; many devices expose temperature here without special permissions. If not, temperature is `None` (not an error).

## Conclusion

`resource-check` is designed to fail gracefully. Unknown/missing data yields "info" level reports rather than critical errors. This respects the uncertain nature of Android diagnostics.
