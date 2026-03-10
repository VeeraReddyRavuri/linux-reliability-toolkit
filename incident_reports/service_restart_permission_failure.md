# Incident Report: Service Restart Permission Failure

## What Broke
The monitoring tool detected that the `cron` service was inactive and attempted to restart it automatically.

## Detection
The reliability toolkit executed `systemctl is-active cron` and detected the service state as `inactive`.

## Root Cause
The monitoring tool was executed as a non-root user. Restarting system services requires elevated privileges.

## Fix Applied
The service was manually restarted using:

```bash
sudo systemctl start cron
```

## Prevention
The reliability toolkit should be deployed as a system service running with appropriate privileges (e.g., via systemd) so it can restart failed services automatically.