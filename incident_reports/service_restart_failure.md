# Incident Report: Service Restart Failure

## What Broke
The `cron` service was manually stopped to simulate a service failure.

## How It Was Detected
The reliability toolkit detected that the service was inactive using:

```bash
systemctl is-active cron
```

The tool logged:

WARNING | Service cron is not active. Attempting restart..

## Root Cause
The monitoring tool attempted to restart the service using:

```bash
systemctl restart cron
```

However, the script was executed as a non-root user. Restarting system services requires elevated privileges.

## Fix Applied
The service was manually restarted using:

```bash
sudo systemctl start cron
```

After restarting, the service returned to the active state.

## Prevention Added
The reliability toolkit should run as a system service using systemd with appropriate privileges so it can restart failed services automatically.

When deployed as a systemd service, the toolkit will have sufficient permissions to restart system services.