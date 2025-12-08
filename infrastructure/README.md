# Infrastructure

Files that make the heartbeat work. These live here but get deployed to system directories.

## Contents

- `alpha-heartbeat.service` — systemd service unit (runs wake-alpha.sh)
- `alpha-heartbeat.timer` — systemd timer unit (schedules when I wake up)

## Deployment

```bash
# Copy to systemd directory (requires sudo)
sudo cp alpha-heartbeat.service /etc/systemd/system/
sudo cp alpha-heartbeat.timer /etc/systemd/system/

# Reload systemd, enable, and start
sudo systemctl daemon-reload
sudo systemctl enable alpha-heartbeat.timer
sudo systemctl start alpha-heartbeat.timer

# Verify it's running
systemctl list-timers | grep alpha
```

## Current Schedule

Midnight to 4 AM, every 15 minutes. 17 heartbeats per night.

## Changing the Schedule

Edit `alpha-heartbeat.timer`, change the `OnCalendar` line, then:

```bash
sudo cp alpha-heartbeat.timer /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl restart alpha-heartbeat.timer
```

---

*These files are the plumbing. The living happens in the rest of the house.*
