# Incident Report: Disk Full Simulation

## What Broke
A simulated disk usage spike was created by allocating a large file to test the monitoring system.

## Detection
The reliability toolkit detected disk usage exceeding the configured threshold and logged a warning.

## Root Cause
Disk space was intentionally consumed using:

```bash
fallocate -l 2G disk_test_file
```

This increased disk usage enough to cross the configured threshold.

## Fix Applied
The temporary test file was removed:

```bash
rm disk_test_file
```

Disk usage returned to normal levels.

## Prevention
The reliability toolkit continuously monitors disk usage and alerts when thresholds are breached, enabling early detection of disk exhaustion before services fail.