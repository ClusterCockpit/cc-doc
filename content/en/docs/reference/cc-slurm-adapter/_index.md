---
title: cc-slurm-adapter
description: ClusterCockpit Slurm Adapter References
categories: [cc-slurm-adapter]
tags: [Adapter]
weight: 3
---

{{% pageinfo %}}
Reference information regarding the ClusterCockpit component "cc-slurm-adapter" ([GitHub Repo](https://github.com/ClusterCockpit/cc-slurm-adapter "See GitHub")).
{{% /pageinfo %}}

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

## Links

- **GitHub Repository**: [ClusterCockpit/cc-slurm-adapter](https://github.com/ClusterCockpit/cc-slurm-adapter)
- **cc-backend**: [ClusterCockpit/cc-backend](https://github.com/ClusterCockpit/cc-backend)
- **Slurm Documentation**: [https://slurm.schedmd.com/](https://slurm.schedmd.com/)
- **NATS**: [https://nats.io/](https://nats.io/)
