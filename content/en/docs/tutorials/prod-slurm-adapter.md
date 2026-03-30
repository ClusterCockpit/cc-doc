---
title: Setup of cc-slurm-adapter
weight: 50
description: How to configure and deploy cc-slurm-adapter
categories: [cc-slurm-adapter]
tags: [Admin]
---

## Introduction

`cc-slurm-adapter` is a daemon that feeds `cc-backend` with job information from
[Slurm](https://slurm.schedmd.com/) in real-time. It runs on the same node as
`slurmctld` and queries Slurm via `sacct`, `squeue`, `sacctmgr`, and `scontrol`.
`slurmrestd` is not used and not required, but **slurmdbd is mandatory**.

The adapter periodically synchronises the Slurm job state with `cc-backend` via
REST API and can optionally publish job events over
[NATS](https://nats.io/). It is designed to be fault-tolerant: if `cc-backend`
or Slurm is temporarily unavailable no jobs are lost — they are submitted as
soon as everything is running again.

### Limitations

`scontrol` resource allocation information (node lists, CPU/GPU assignment) is
only available for a few minutes after a job finishes. If the adapter is stopped
during that window the affected jobs will be registered in `cc-backend` without
resource details, meaning metric data cannot be associated to those jobs. Keep
downtime of the adapter as short as possible.

Compatible Slurm versions: **24.xx.x** and **25.xx.x**.

## Installation

### Build from source

```bash
git clone https://github.com/ClusterCockpit/cc-slurm-adapter
cd cc-slurm-adapter
make
```

Copy the resulting binary and a configuration file to a suitable location, for
example `/opt/cc-slurm-adapter/`. Because the configuration file contains
a JWT token and optionally NATS credentials, restrict its permissions:

```bash
install -m 0750 -o cc-slurm-adapter -g slurm \
    cc-slurm-adapter /opt/cc-slurm-adapter/
install -m 0640 -o cc-slurm-adapter -g slurm \
    config.json /opt/cc-slurm-adapter/
```

## Configuration

The adapter reads a single JSON configuration file specified with `-config`.

### Minimum configuration

Only `ccRestUrl` and `ccRestJwt` are required:

```json
{
    "ccRestUrl": "https://my-cc-backend.example",
    "ccRestJwt": "eyJ..."
}
```

With these two keys all other options take their default values:

| Key | Default |
|-----|---------|
| `pidFilePath` | `/run/cc-slurm-adapter/daemon.pid` |
| `prepSockListenPath` | `/run/cc-slurm-adapter/daemon.sock` |
| `prepSockConnectPath` | `/run/cc-slurm-adapter/daemon.sock` |
| `lastRunPath` | `/var/lib/cc-slurm-adapter/lastrun` |
| `slurmPollInterval` | `60` s |
| `slurmQueryDelay` | `1` s |
| `slurmQueryMaxSpan` | `604800` s (7 days) |
| `slurmMaxRetries` | `10` |
| `slurmMaxConcurrent` | `10` |
| `ccPollInterval` | `21600` s (6 h) |
| `ccRestSubmitJobs` | `true` |
| `natsPort` | `4222` |
| `natsSubject` | `"jobs"` |

### Polling and synchronisation

`slurmPollInterval` (seconds) controls how often the adapter performs a full
Slurm ↔ cc-backend sync. The default of 60 s is a reasonable starting point;
production sites often raise this to 300 s when the Prolog/Epilog hook is in use
(see below) because real-time events already cover most latency requirements.

`slurmQueryMaxSpan` limits how far back in time the adapter looks for jobs on
each sync. The default of 7 days prevents accidental flooding when the adapter
has been offline for an extended period. Set this to a shorter value (e.g.,
`86400` for 24 h) on busy clusters.

`ccPollInterval` triggers a full query of active jobs from `cc-backend` to
detect stuck jobs. It does not need to run often; the default of 6 h is usually
fine.

### GPU PCI addresses

`cc-backend` identifies GPU devices by their PCI bus address. The `gpuPciAddrs`
map associates a hostname regular expression with the ordered list of PCI
addresses for that group of nodes — ordered the same way as NVML (which matches
`nvidia-smi` output when all devices are visible):

```json
{
    "gpuPciAddrs": {
        "^node[0-9]{3}$": [
            "00000000:01:00.0",
            "00000000:25:00.0",
            "00000000:41:00.0",
            "00000000:61:00.0"
        ]
    }
}
```

If a cluster has several node groups with different GPU layouts, use one regex
entry per group. See the [production examples](#production-examples) below.

### Ignoring hosts

`ignoreHosts` is a regular expression matched against hostnames. If **all**
hosts of a job match, the job is discarded and not reported to `cc-backend`.
Useful to exclude visualisation or login nodes that may appear in Slurm
allocations:

```json
{
    "ignoreHosts": "^viznode1$"
}
```

### NATS

When a NATS server is configured, the adapter publishes job start and stop
events to the specified subject. `cc-backend` can then pick these up instead of
waiting for the REST path. See the
[NATS background article]({{< ref "docs/explanation/nats/" >}}) for context.

```json
{
    "natsServer": "nats.example",
    "natsPort": 4222,
    "natsSubject": "mycluster",
    "natsUser": "mycluster",
    "natsPassword": "secret"
}
```

When NATS is used and `cc-backend` is configured to register jobs via NATS, you
can set `ccRestSubmitJobs` to `false` to disable the REST job-submission path
entirely and rely solely on NATS.

For alternative NATS authentication methods:

- `natsCredsFile` — path to a [NATS credentials
  file](https://docs.nats.io/using-nats/developer/connecting/creds)
- `natsNKeySeedFile` — path to a file containing an [NKey seed
  (private key)](https://docs.nats.io/running-a-nats-service/configuration/securing_nats/auth_intro/nkey_auth)

## Systemd Service

Create `/etc/systemd/system/cc-slurm-adapter.service`:

```ini
[Unit]
Description=cc-slurm-adapter
Wants=network.target
After=network.target

[Service]
User=cc-slurm-adapter
Group=slurm
ExecStart=/opt/cc-slurm-adapter/cc-slurm-adapter \
    -daemon \
    -config /opt/cc-slurm-adapter/config.json
WorkingDirectory=/opt/cc-slurm-adapter/
RuntimeDirectory=cc-slurm-adapter
RuntimeDirectoryMode=0750
Restart=on-failure
RestartSec=15s

[Install]
WantedBy=multi-user.target
```

`RuntimeDirectory=cc-slurm-adapter` instructs systemd to create and own
`/run/cc-slurm-adapter/` which holds the PID file and the Prolog/Epilog Unix
socket. `RuntimeDirectoryMode=0750` with `Group=slurm` allows the `slurm` user
(which executes Prolog/Epilog scripts) to connect to the socket.

Enable and start the service:

```bash
systemctl daemon-reload
systemctl enable --now cc-slurm-adapter
```

## Slurm User Permissions

Depending on your Slurm configuration, an unprivileged user cannot run `sacct`
or `scontrol` to query all jobs. Grant the `cc-slurm-adapter` user operator-level
access:

```bash
sacctmgr add user cc-slurm-adapter Account=root AdminLevel=operator
```

{{< alert title="Warning" color="warning" >}}
If the required Slurm permissions are not granted, **no jobs will be reported**
to cc-backend.
{{< /alert >}}

## Prolog/Epilog Hook (Optional)

The periodic sync has a latency up to `slurmPollInterval` seconds. To reduce
this, configure `slurmctld` to call the adapter immediately when a job starts or
ends. Add to `slurm.conf`:

```ini
PrEpPlugins=prep/script
PrologSlurmctld=/opt/cc-slurm-adapter/hook.sh
EpilogSlurmctld=/opt/cc-slurm-adapter/hook.sh
```

Create `/opt/cc-slurm-adapter/hook.sh` (executable, readable by the `slurm`
group):

```bash
#!/bin/sh
/opt/cc-slurm-adapter/cc-slurm-adapter
exit 0
```

The script **must exit with 0**. A non-zero exit code causes Slurm to deny the
job allocation. If the adapter is temporarily stopped or being restarted, the
Prolog/Epilog call will fail silently (exit 0) and the periodic sync will catch
the job on the next tick.

If you changed `prepSockConnectPath` from its default you must pass `-config` to
the hook invocation and ensure the configuration file is readable by the `slurm`
group:

```bash
#!/bin/sh
/opt/cc-slurm-adapter/cc-slurm-adapter -config /opt/cc-slurm-adapter/config.json
exit 0
```

The `slurmQueryDelay` option (default 1 s) adds a short pause between the
Prolog/Epilog event and the actual Slurm query to give Slurm time to write the
job record. There is generally no need to change this.

## Production Examples

### CPU-only cluster, no GPUs (woody)

```json
{
    "ccRestUrl": "https://monitoring.example",
    "ccRestJwt": "eyJ...",
    "lastRunPath": "/var/lib/cc-slurm-adapter/lastrun",
    "slurmPollInterval": 300,
    "slurmQueryMaxSpan": 86400,
    "natsServer": "monitoring.example",
    "natsSubject": "woody",
    "natsUser": "woody",
    "natsPassword": "secret"
}
```

### GPU cluster, single node type (fritz)

```json
{
    "ccRestUrl": "https://monitoring.example",
    "ccRestJwt": "eyJ...",
    "lastRunPath": "/var/lib/cc-slurm-adapter/lastrun",
    "slurmPollInterval": 300,
    "ignoreHosts": "^viznode1$",
    "natsServer": "monitoring.example",
    "natsSubject": "fritz",
    "natsUser": "fritz",
    "natsPassword": "secret",
    "gpuPciAddrs": {
        "^gpunode\\d+$": [
            "00000000:CE:00.0",
            "00000000:CF:00.0",
            "00000000:D0:00.0",
            "00000000:D1:00.0"
        ]
    }
}
```

### GPU cluster, multiple node types with different GPU layouts (alex)

Nodes are divided into groups by hostname pattern. Each group has a distinct
set of GPU PCI addresses:

```json
{
    "ccRestUrl": "https://monitoring.example",
    "ccRestJwt": "eyJ...",
    "lastRunPath": "/var/lib/cc-slurm-adapter/lastrun",
    "slurmPollInterval": 300,
    "natsServer": "monitoring.example",
    "natsSubject": "alex",
    "natsUser": "alex",
    "natsPassword": "secret",
    "gpuPciAddrs": {
        "^(a0[1-4]\\d\\d|a052\\d|a162\\d|a172\\d)$": [
            "00000000:01:00.0",
            "00000000:25:00.0",
            "00000000:41:00.0",
            "00000000:61:00.0",
            "00000000:81:00.0",
            "00000000:A1:00.0",
            "00000000:C1:00.0",
            "00000000:E1:00.0"
        ],
        "^(a0[6-9]\\d\\d|a053\\d)$": [
            "00000000:0E:00.0",
            "00000000:13:00.0",
            "00000000:49:00.0",
            "00000000:4F:00.0",
            "00000000:90:00.0",
            "00000000:96:00.0",
            "00000000:CC:00.0",
            "00000000:D1:00.0"
        ]
    }
}
```

## Debugging

`cc-slurm-adapter` writes all output to stderr, which systemd captures in the
journal:

```bash
journalctl -u cc-slurm-adapter -f
```

To increase verbosity, change the `ExecStart` line to add `-debug 5`:

```ini
ExecStart=/opt/cc-slurm-adapter/cc-slurm-adapter \
    -daemon \
    -config /opt/cc-slurm-adapter/config.json \
    -debug 5
```

Log level 5 enables detailed per-job trace output and is useful for diagnosing
why specific jobs are not appearing in `cc-backend`.

To verify that the adapter can query Slurm correctly, run the following as the
`cc-slurm-adapter` user:

```bash
sacct --allusers --json | head -5
squeue --json | head -5
```

If either command fails with a permission error, revisit the [Slurm user
permissions](#slurm-user-permissions) step.
