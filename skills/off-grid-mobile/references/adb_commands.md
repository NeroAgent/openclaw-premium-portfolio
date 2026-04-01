# ADB Commands Reference

## Basic ADB Usage

```bash
adb devices                   # List connected devices
adb shell <command>          # Run shell command on device
adb push <local> <remote>    # Copy file to device
adb pull <remote> <local>    # Copy file from device
adb install <apk>             # Install an APK
adb uninstall <package>      # Uninstall app
```

## Controlling Off Grid Mobile

**Start app:**
```bash
adb shell am start -n ai.offgridmobile/.MainActivity
```

**Clear data (reset):**
```bash
adb shell pm clear ai.offgridmobile
```

**Push a model:**
```bash
adb push my-model.gguf /sdcard/offgrid/models/
```

**Check if running:**
```bash
adb shell ps -A | grep offgridmobile
```

**Kill app:**
```bash
adb shell am force-stop ai.offgridmobile
```

## Limitations

- ADB must be enabled on device (Developer options)
- USB debugging must be on
- Device must be authorized
- Some commands require root for certain directories; use `/sdcard/` which is world-writable

---

For more automation, enable the local HTTP API in Off Grid Mobile settings and use `curl` to interact directly.