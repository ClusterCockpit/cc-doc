---
title: cc-slurm-adapter
description: ClusterCockpit Slurm Adapter reference
categories: [cc-metric-collector]
weight: 3
---

## Overview

cc-slurm-adapter is a software daemon that feeds
[cc-backend](https://github.com/ClusterCockpit/cc-backend) with job information
from [Slurm](https://slurm.schedmd.com/) in realtime.

### Key Features

- **Fault Tolerant**: Handles cc-backend or Slurm downtime gracefully without losing jobs
- **Automatic Recovery**: Submits jobs to cc-backend as soon as services are available again
- **Realtime Updates**: Supports immediate job notification via Slurm Prolog/Epilog hooks
- **NATS Integration**: Optional job notification messaging via NATS
- **Minimal Dependencies**: Uses Slurm commands (`sacct`, `squeue`, `sacctmgr`, `scontrol`) - no `slurmrestd` required

### Architecture

The daemon runs on the same node as
[slurmctld](https://slurm.schedmd.com/slurmctld.html) and operates in two modes:

1. **Daemon Mode**: Periodic synchronization (default: every 60 seconds) between
   Slurm and cc-backend
2. **Prolog/Epilog Mode**: Immediate trigger on job start/stop events (optional,
   reduces latency)

Data is submitted to cc-backend via REST API. **Note**: Slurm's slurmdbd is mandatory.

{{< alert title="Notice" >}}
You can set the [Slurm option
MinJobAge](https://slurm.schedmd.com/slurm.conf.html#OPT_MinJobAge) to prolong
the duration Slurm will hold Job infos in memory.
{{< /alert >}}

## Limitations

### Resource Information Availability

Because slurmdbd does not store all job information, some details may be
unavailable in certain cases:

- **Resource allocation information** is obtained via `scontrol --cluster XYZ show job XYZ --json`
- This information becomes **unavailable a few minutes after job completion**
- If the daemon is stopped for too long, jobs may lack resource information
- **Critical Impact**: Without resource information, cc-backend cannot associate jobs with metrics (CPU, GPU, memory)
- Jobs will still be listed in cc-backend but metric visualization will not work

## Slurm Version Compatibility

### Supported Versions

These Slurm versions are known to work:

- 24.xx.x
- 25.xx.x

### Compatibility Notes

All Slurm-related code is concentrated in `slurm.go` for easier maintenance. The
most common compatibility issue is **nil pointer dereference** due to missing
JSON fields.

#### Debugging Incompatibilities

If you encounter nil pointer dereferences:

1. Get a job ID via `squeue` or `sacct`
2. Check JSON layouts from both commands (they differ):

   ```bash
   sacct -j 12345 --json
   scontrol show job 12345 --json
   ```

#### SlurmInt and SlurmString Types

Slurm has been transitioning API formats:

- **SlurmInt**: Handles both plain integers and Slurm's "infinite/set" struct format
- **SlurmString**: Handles both plain strings and string arrays (uses first element if array, blank if empty)

These custom types maintain backward compatibility across Slurm versions.

## Command Line Usage

### Flags

| Flag                 | Description                                                                        |
| -------------------- | ---------------------------------------------------------------------------------- |
| `-config <path>`     | Specify the path to the config file (default: `/etc/cc-slurm-adapter/config.json`) |
| `-daemon`            | Run in daemon mode (if omitted, runs in Prolog/Epilog mode)                        |
| `-debug <log-level>` | Set the log level (default: 2, max: 5)                                             |
| `-help`              | Show help for all command line flags                                               |

### Modes

**Daemon Mode**: `cc-slurm-adapter -daemon -config /path/to/config.json`

**Prolog/Epilog Mode**: `cc-slurm-adapter` (only works from Slurm Prolog/Epilog context)

## Configuration

### Configuration File Location

Default: `/etc/cc-slurm-adapter/config.json`

### Example Configuration

```json
{
  "pidFilePath": "/run/cc-slurm-adapter/daemon.pid",
  "prepSockListenPath": "/run/cc-slurm-adapter/daemon.sock",
  "prepSockConnectPath": "/run/cc-slurm-adapter/daemon.sock",
  "lastRunPath": "/var/lib/cc-slurm-adapter/last_run",
  "slurmPollInterval": 60,
  "slurmQueryDelay": 1,
  "slurmQueryMaxSpan": 604800,
  "slurmQueryMaxRetries": 5,
  "ccPollInterval": 21600,
  "ccRestSubmitJobs": true,
  "ccRestUrl": "https://my-cc-backend-instance.example",
  "ccRestJwt": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
  "gpuPciAddrs": {
    "^nodehostname0[0-9]$": ["00000000:00:10.0", "00000000:00:3F.0"],
    "^nodehostname1[0-9]$": ["00000000:00:10.0", "00000000:00:3F.0"]
  },
  "ignoreHosts": "^nodehostname9\\w+$",
  "natsServer": "mynatsserver.example",
  "natsPort": 4222,
  "natsSubject": "mysubject",
  "natsUser": "myuser",
  "natsPassword": "123456789",
  "natsCredsFile": "/etc/cc-slurm-adapter/nats.creds",
  "natsNKeySeedFile": "/etc/ss-slurm-adapter/nats.nkey"
}
```

### Configuration Reference

#### Required Settings

| Config Key  | Type   | Description                                                    |
| ----------- | ------ | -------------------------------------------------------------- |
| `ccRestUrl` | string | URL to cc-backend's REST API (must not contain trailing slash) |
| `ccRestJwt` | string | JWT token from cc-backend for REST API access                  |

#### Daemon Settings

| Config Key    | Type   | Default                             | Description                                                         |
| ------------- | ------ | ----------------------------------- | ------------------------------------------------------------------- |
| `pidFilePath` | string | `/run/cc-slurm-adapter/daemon.pid`  | Path to PID file (prevents concurrent execution)                    |
| `lastRunPath` | string | `/var/lib/cc-slurm-adapter/lastrun` | Path to file storing last successful sync timestamp (as file mtime) |

#### Socket Settings

| Config Key            | Type   | Default                             | Description                                                                                  |
| --------------------- | ------ | ----------------------------------- | -------------------------------------------------------------------------------------------- |
| `prepSockListenPath`  | string | `/run/cc-slurm-adapter/daemon.sock` | Socket for daemon to receive prolog/epilog events. Supports UNIX and TCP formats (see below) |
| `prepSockConnectPath` | string | `/run/cc-slurm-adapter/daemon.sock` | Socket for prolog/epilog mode to connect to daemon                                           |

**Socket Formats**:

- UNIX: `/run/cc-slurm-adapter/daemon.sock` or `unix:/run/cc-slurm-adapter/daemon.sock`
- TCP IPv4: `tcp:127.0.0.1:12345` or `tcp:0.0.0.0:12345`
- TCP IPv6: `tcp:[::1]:12345`, `tcp:[::]:12345`, `tcp::12345`

#### Slurm Polling Settings

| Config Key             | Type | Default | Description                                                            |
| ---------------------- | ---- | ------- | ---------------------------------------------------------------------- |
| `slurmPollInterval`    | int  | 60      | Interval (seconds) for periodic sync to cc-backend                     |
| `slurmQueryDelay`      | int  | 1       | Wait time (seconds) after prolog/epilog event before querying Slurm    |
| `slurmQueryMaxSpan`    | int  | 604800  | Maximum time (seconds) to query jobs from the past (prevents flooding) |
| `slurmQueryMaxRetries` | int  | 10      | Maximum Slurm query attempts on Prolog/Epilog events                   |

#### cc-backend Settings

| Config Key         | Type | Default | Description                                                                       |
| ------------------ | ---- | ------- | --------------------------------------------------------------------------------- |
| `ccPollInterval`   | int  | 21600   | Interval (seconds) to query all jobs from cc-backend (prevents stuck jobs)        |
| `ccRestSubmitJobs` | bool | true    | Submit started/stopped jobs to cc-backend via REST (set false if using NATS-only) |

#### Hardware Mapping

| Config Key    | Type   | Default | Description                                                                          |
| ------------- | ------ | ------- | ------------------------------------------------------------------------------------ |
| `gpuPciAddrs` | object | `{}`    | Map of hostname regexes to GPU PCI address arrays (must match NVML/nvidia-smi order) |
| `ignoreHosts` | string | `""`    | Regex of hostnames to ignore (jobs only on matching hosts are discarded)             |

#### NATS Settings

| Config Key         | Type   | Default  | Description                                                                                                                               |
| ------------------ | ------ | -------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| `natsServer`       | string | `""`     | NATS server hostname (leave blank to disable NATS)                                                                                        |
| `natsPort`         | uint16 | 4222     | NATS server port                                                                                                                          |
| `natsSubject`      | string | `"jobs"` | Subject to publish job information to                                                                                                     |
| `natsUser`         | string | `""`     | NATS username (for [user auth](https://docs.nats.io/running-a-nats-service/configuration/securing_nats/auth_intro/username_password))     |
| `natsPassword`     | string | `""`     | NATS password                                                                                                                             |
| `natsCredsFile`    | string | `""`     | Path to NATS [credentials file](https://docs.nats.io/using-nats/developer/connecting/creds)                                               |
| `natsNKeySeedFile` | string | `""`     | Path to NATS [NKey seed file](https://docs.nats.io/running-a-nats-service/configuration/securing_nats/auth_intro/nkey_auth) (private key) |

**Note**: The deprecated `ipcSockPath` option has been removed. Use `prepSockListenPath` and `prepSockConnectPath` instead.

## Installation and Setup

### Prerequisites

- Go 1.24.0 or higher
- Slurm with slurmdbd configured
- cc-backend instance with API access
- Access to the slurmctld node

### Compilation

```bash
make
```

This creates the `cc-slurm-adapter` binary.

### Daemon Setup (Required)

#### 1. Copy Binary and Configuration

Copy the binary and create a configuration file:

```bash
sudo mkdir -p /opt/cc-slurm-adapter
sudo cp cc-slurm-adapter /opt/cc-slurm-adapter/
sudo cp config.json /opt/cc-slurm-adapter/
```

**Security**: The config file contains sensitive credentials (JWT, NATS). Set appropriate permissions:

```bash
sudo chmod 600 /opt/cc-slurm-adapter/config.json
```

#### 2. Create System User

```bash
sudo useradd -r -s /bin/false cc-slurm-adapter
sudo chown -R cc-slurm-adapter:slurm /opt/cc-slurm-adapter
```

#### 3. Grant Slurm Permissions

The adapter user needs permission to query Slurm:

```bash
sacctmgr add user cc-slurm-adapter Account=root AdminLevel=operator
```

**Critical**: If permissions are not set and Slurm is restricted, **NO JOBS WILL BE REPORTED**.

#### 4. Install systemd Service

Create `/etc/systemd/system/cc-slurm-adapter.service`:

```ini
[Unit]
Description=cc-slurm-adapter
Wants=network.target
After=network.target

[Service]
User=cc-slurm-adapter
Group=slurm
ExecStart=/opt/cc-slurm-adapter/cc-slurm-adapter -daemon -config /opt/cc-slurm-adapter/config.json
WorkingDirectory=/opt/cc-slurm-adapter/
RuntimeDirectory=cc-slurm-adapter
RuntimeDirectoryMode=0750
Restart=on-failure
RestartSec=15s

[Install]
WantedBy=multi-user.target
```

**Notes**:

- `RuntimeDirectory` creates `/run/cc-slurm-adapter` for PID and socket files
- `Group=slurm` allows Prolog/Epilog (running as slurm user) to access the socket
- `RuntimeDirectoryMode=0750` enables group access

#### 5. Enable and Start Service

```bash
sudo systemctl daemon-reload
sudo systemctl enable cc-slurm-adapter
sudo systemctl start cc-slurm-adapter
```

### Prolog/Epilog Hook Setup (Optional)

For immediate job notification (reduces latency):

#### 1. Create Hook Script

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

#### 2. Configure Slurm

Add to `slurm.conf`:

```ini
PrEpPlugins=prep/script
PrologSlurmctld=/opt/cc-slurm-adapter/hook.sh
EpilogSlurmctld=/opt/cc-slurm-adapter/hook.sh
```

#### 3. Restart slurmctld

```bash
sudo systemctl restart slurmctld
```

**Note**: If using non-default socket path, add `-config /path/to/config.json` to `hook.sh`. The config file must be readable by the `slurm` user/group.

## Debugging and Troubleshooting

### Check Service Status

```bash
sudo systemctl status cc-slurm-adapter
```

### View Logs

cc-slurm-adapter logs to stderr (captured by systemd):

```bash
sudo journalctl -u cc-slurm-adapter -f
```

### Enable Debug Logging

Edit systemd service to add `-debug 5`:

```ini
ExecStart=/opt/cc-slurm-adapter/cc-slurm-adapter -daemon -debug 5 -config /opt/cc-slurm-adapter/config.json
```

Then reload and restart:

```bash
sudo systemctl daemon-reload
sudo systemctl restart cc-slurm-adapter
```

**Log Levels**:

- 2 (default): Errors and warnings
- 5 (max): Verbose debug output

### Common Issues

| Issue                    | Possible Cause                    | Solution                                                                  |
| ------------------------ | --------------------------------- | ------------------------------------------------------------------------- |
| No jobs reported         | Missing Slurm permissions         | Run `sacctmgr add user cc-slurm-adapter Account=root AdminLevel=operator` |
| Socket connection errors | Wrong socket path or permissions  | Check `prepSockListenPath`/`prepSockConnectPath` and RuntimeDirectoryMode |
| Prolog/Epilog failures   | Non-zero exit code in hook script | Ensure hook script exits with `exit 0`                                    |
| Missing resource info    | Daemon stopped too long           | Keep daemon running; resource info expires minutes after job completion   |
| Job allocation failures  | Prolog/Epilog exit code ≠ 0       | Check hook script and ensure cc-slurm-adapter is running                  |

## Architecture Details

### Synchronization Flow

1. **Timer Trigger**: Periodic timer (default: 60s) triggers sync
2. **Query Slurm**: Fetch job data via `sacct`, `squeue`, `scontrol`
3. **Submit to cc-backend**: POST job start/stop via REST API
4. **Publish to NATS**: Optional notification message (if enabled)

### Prolog/Epilog Flow

1. **Job Event**: Slurm triggers Prolog/Epilog hook
2. **Socket Message**: Hook sends job ID to daemon via socket
3. **Immediate Query**: Daemon queries Slurm for that specific job
4. **Fast Submission**: Job submitted to cc-backend with minimal delay

### Data Sources

| Slurm Command       | Purpose                                   |
| ------------------- | ----------------------------------------- |
| `sacct`             | Historical job accounting data            |
| `squeue`            | Current job queue information             |
| `scontrol show job` | Resource allocation details (JSON format) |
| `sacctmgr`          | User permissions                          |

### State Persistence

- **Last Run Timestamp**: Stored as file modification time in `lastRunPath`
- **PID File**: Prevents concurrent daemon execution
- **Socket**: IPC between daemon and Prolog/Epilog instances

## API Integration

### cc-backend REST API

**Endpoints Used**:

- `POST /api/jobs/start_job/` - Submit job start
- `POST /api/jobs/stop_job/<jobId>` - Submit job completion

**Authentication**: JWT bearer token (`ccRestJwt`)

### NATS Messaging

**Message Format**: JSON job information published to configured subject

**Use Case**: Real-time job notifications to other services (monitoring, schedulers, etc.)

## Building from Source

### Requirements

```
go 1.24.0+
```

### Dependencies

Key dependencies (managed via `go.mod`):

- `github.com/ClusterCockpit/cc-lib` - ClusterCockpit common library
- `github.com/nats-io/nats.go` - NATS client

### Build Commands

```bash
# Build binary
make

# Format code
make format

# Clean build artifacts
make clean
```

## Best Practices

### Production Deployment

1. **Keep Daemon Running**: Resource info expires quickly after job completion
2. **Monitor Logs**: Watch for Slurm API changes or nil pointer errors
3. **Secure Credentials**: Restrict config file permissions (600 or 640)
4. **Use Prolog/Epilog Carefully**: Always exit with 0 to avoid blocking job allocations
5. **Test Before Production**: Verify in development environment first

### Performance Tuning

- **High Job Volume**: Reduce `slurmPollInterval` if periodic sync causes lag
- **Low Latency Required**: Enable Prolog/Epilog hooks
- **Resource Constrained**: Increase `ccPollInterval` (reduces cc-backend queries)

### Multi-Cluster Setup

For multiple slurmctld nodes, use TCP sockets:

```json
{
  "prepSockListenPath": "tcp:0.0.0.0:12345",
  "prepSockConnectPath": "tcp:slurmctld-host:12345"
}
```

## Links

- **GitHub Repository**: [ClusterCockpit/cc-slurm-adapter](https://github.com/ClusterCockpit/cc-slurm-adapter)
- **cc-backend**: [ClusterCockpit/cc-backend](https://github.com/ClusterCockpit/cc-backend)
- **Slurm Documentation**: [https://slurm.schedmd.com/](https://slurm.schedmd.com/)
- **NATS**: [https://nats.io/](https://nats.io/)

