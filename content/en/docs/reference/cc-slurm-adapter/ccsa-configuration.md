---
title: cc-slurm-adapter Configuration
description: cc-slurm-adapter configuration reference
categories: [cc-slurm-adapter]
tags: [Adapter, Configuration]
weight: 2
---

## Configuration File Location

Default: `/etc/cc-slurm-adapter/config.json`

## Example Configuration

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

## Configuration Reference

### Required Settings

| Config Key  | Type   | Description                                                    |
| ----------- | ------ | -------------------------------------------------------------- |
| `ccRestUrl` | string | URL to cc-backend's REST API (must not contain trailing slash) |
| `ccRestJwt` | string | JWT token from cc-backend for REST API access                  |

### Daemon Settings

| Config Key    | Type   | Default                             | Description                                                         |
| ------------- | ------ | ----------------------------------- | ------------------------------------------------------------------- |
| `pidFilePath` | string | `/run/cc-slurm-adapter/daemon.pid`  | Path to PID file (prevents concurrent execution)                    |
| `lastRunPath` | string | `/var/lib/cc-slurm-adapter/lastrun` | Path to file storing last successful sync timestamp (as file mtime) |

### Socket Settings

| Config Key            | Type   | Default                             | Description                                                                                  |
| --------------------- | ------ | ----------------------------------- | -------------------------------------------------------------------------------------------- |
| `prepSockListenPath`  | string | `/run/cc-slurm-adapter/daemon.sock` | Socket for daemon to receive prolog/epilog events. Supports UNIX and TCP formats (see below) |
| `prepSockConnectPath` | string | `/run/cc-slurm-adapter/daemon.sock` | Socket for prolog/epilog mode to connect to daemon                                           |

**Socket Formats**:

- UNIX: `/run/cc-slurm-adapter/daemon.sock` or `unix:/run/cc-slurm-adapter/daemon.sock`
- TCP IPv4: `tcp:127.0.0.1:12345` or `tcp:0.0.0.0:12345`
- TCP IPv6: `tcp:[::1]:12345`, `tcp:[::]:12345`, `tcp::12345`

### Slurm Polling Settings

| Config Key             | Type | Default | Description                                                            |
| ---------------------- | ---- | ------- | ---------------------------------------------------------------------- |
| `slurmPollInterval`    | int  | 60      | Interval (seconds) for periodic sync to cc-backend                     |
| `slurmQueryDelay`      | int  | 1       | Wait time (seconds) after prolog/epilog event before querying Slurm    |
| `slurmQueryMaxSpan`    | int  | 604800  | Maximum time (seconds) to query jobs from the past (prevents flooding) |
| `slurmQueryMaxRetries` | int  | 10      | Maximum Slurm query attempts on Prolog/Epilog events                   |

### cc-backend Settings

| Config Key         | Type | Default | Description                                                                       |
| ------------------ | ---- | ------- | --------------------------------------------------------------------------------- |
| `ccPollInterval`   | int  | 21600   | Interval (seconds) to query all jobs from cc-backend (prevents stuck jobs)        |
| `ccRestSubmitJobs` | bool | true    | Submit started/stopped jobs to cc-backend via REST (set false if using NATS-only) |

### Hardware Mapping

| Config Key    | Type   | Default | Description                                                                          |
| ------------- | ------ | ------- | ------------------------------------------------------------------------------------ |
| `gpuPciAddrs` | object | `{}`    | Map of hostname regexes to GPU PCI address arrays (must match NVML/nvidia-smi order) |
| `ignoreHosts` | string | `""`    | Regex of hostnames to ignore (jobs only on matching hosts are discarded)             |

### NATS Settings

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
