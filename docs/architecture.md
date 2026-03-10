# Architecture Diagram

+----------------------+
| Cron / Systemd |
| (scheduler trigger)|
+----------+-----------+
|
v
+----------------------+
| main.py |
| Orchestrates checks |
+----------+-----------+
|
v
+----------------------+ +----------------------+
| monitor.py | | service_manager.py |
| CPU / Mem / Disk | | systemd service |
| health checks | | status + restart |
+----------+-----------+ +----------+-----------+
| |
v v
+----------------------+ +----------------------+
| log_parser.py | | notifier.py |
| journalctl scanning | | webhook alerts |
+----------------------+ +----------------------+
       |
       v
+----------------------+
| Logging |
| logs/toolkit.log |
+----------------------+

## Flow

1. Scheduler triggers the tool.
2. `main.py` orchestrates all checks.
3. Monitoring module collects system metrics.
4. Service manager verifies systemd services.
5. Log parser scans journalctl for errors.
6. Notifier sends alerts when issues are detected.
7. All actions are logged.