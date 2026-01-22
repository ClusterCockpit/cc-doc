---
title: Prolog/Epilog Hooks
description: Setting up Prolog/Epilog hooks for immediate job notification
categories: [cc-slurm-adapter]
tags: [Adapter, Slurm]
weight: 4
---

Prolog/Epilog hook setup is **optional** but recommended for immediate job notification, which reduces latency compared to relying solely on periodic polling.

## Prerequisites

- Daemon must be running (see [Daemon Setup](../daemon-setup))
- Hook script must be accessible from slurmctld
- Hook script must exit with code 0 to avoid rejecting job allocations

## 1. Create Hook Script

Create `/opt/cc-slurm-adapter/hook.sh`:

```bash
#!/bin/sh
/opt/cc-slurm-adapter/cc-slurm-adapter
exit 0
```

Make it executable:

```bash
sudo chmod +x /opt/cc-slurm-adapter/hook.sh
```

**Important**: Always exit with 0. Non-zero exit codes will **reject job allocations**.

## 2. Configure Slurm

Add to `slurm.conf`:

```ini
PrEpPlugins=prep/script
PrologSlurmctld=/opt/cc-slurm-adapter/hook.sh
EpilogSlurmctld=/opt/cc-slurm-adapter/hook.sh
```

## 3. Restart slurmctld

```bash
sudo systemctl restart slurmctld
```

**Note**: If using non-default socket path, add `-config /path/to/config.json` to `hook.sh`. The config file must be readable by the `slurm` user/group.

## Multi-Cluster Setup

For multiple slurmctld nodes, use TCP sockets instead of UNIX sockets:

```json
{
  "prepSockListenPath": "tcp:0.0.0.0:12345",
  "prepSockConnectPath": "tcp:slurmctld-host:12345"
}
```

This allows Prolog/Epilog hooks on different nodes to connect to the daemon over the network.

## How It Works

1. **Job Event**: Slurm triggers Prolog/Epilog hook when a job starts or stops
2. **Socket Message**: Hook sends job ID to daemon via socket
3. **Immediate Query**: Daemon queries Slurm for that specific job
4. **Fast Submission**: Job submitted to cc-backend with minimal delay

This reduces the job notification latency from up to 60 seconds (default poll interval) to just a few seconds.
