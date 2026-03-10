# Architecture Diagram

```mermaid
flowchart TD

Scheduler["Cron / systemd timer"] --> Main["main.py (orchestrator)"]

Main --> Monitor["monitor.py<br/>CPU / Memory / Disk"]
Main --> ServiceManager["service_manager.py<br/>systemd checks"]
Main --> LogParser["log_parser.py<br/>journalctl scanning"]
Main --> Notifier["notifier.py<br/>webhook alerts"]

Monitor --> Logger["Structured Logging"]
ServiceManager --> Logger
LogParser --> Logger
Notifier --> Logger

Logger --> LogFile["logs/toolkit.log"]
```

## Flow

1. Scheduler triggers the tool.
2. `main.py` orchestrates all checks.
3. Monitoring module collects system metrics.
4. Service manager verifies systemd services.
5. Log parser scans journalctl for errors.
6. Notifier sends alerts when issues are detected.
7. All actions are logged.