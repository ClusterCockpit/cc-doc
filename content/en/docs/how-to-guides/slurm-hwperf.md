---
title: Sharing HPM Metrics Between Monitoring and User Profiling
description: How to share hardware performance counter access between system monitoring and user jobs in SLURM
categories: [ClusterCockpit]
tags: [Admin, SLURM, LIKWID]
---

## Overview

Hardware performance counters (HPM) can only be accessed by one process at a time.
This creates a conflict when both a system monitoring daemon (e.g. using LIKWID) and user
jobs (using LIKWID, VTune, or other `perf_event`-based tools) need access on the same node.

The approach described here allows sharing counter access by:

1. Restricting HPM access to node-exclusive jobs via a SLURM constraint (`hwperf`)
2. Handing ownership of `/var/run/likwid.lock` to the job user in the prologue
3. Returning ownership to the monitoring user in the epilogue

This is the approach used at NHR@FAU.

{{< alert title="Security Note" >}}
Hardware performance counter access must be restricted to node-exclusive jobs.
Allowing shared-node jobs to access performance counters is a security risk, as
counters can leak information across processes.
{{< /alert >}}

## SLURM Submit Filter

A SLURM submit filter (Lua) enforces that any job requesting the `hwperf` constraint
must also request exclusive node access.

```lua
-- all jobs with constraint hwperf need to allocate nodes exclusively
for feature in string.gmatch(job_desc.features or "", "[^,]*") do
    if ( feature == "hwperf" and job_desc.shared ~= 0 ) then
        slurm.log_info("slurm_job_submit: job from uid %u with constraint hwperf but not exclusive", job_desc.user_id )
        slurm.user_msg("--constraint=hwperf only available for node-exclusive jobs with --exclusive")
        return 2029 --- slurm.ERROR ESLURM_INVALID_FEATURE
    end
end
```

Place this snippet in your site's submit filter script (typically `/etc/slurm/job_submit.lua`).

## Prologue: `/etc/slurm/slurm.prolog`

The prologue grants the job user access to `/var/run/likwid.lock` and opens
`perf_event` access when the `hwperf` constraint is set. Otherwise it ensures
the monitoring user retains ownership.

```bash
#
# Only change permissions if /var/run/likwid.lock is a regular file.
# Grant permissions to user (if requested) or keep them with the monitoring user.
#
if [ -f /var/run/likwid.lock ]; then
    if [[ "$SLURM_JOB_CONSTRAINTS" =~ "hwperf" ]] ; then
        chown $SLURM_JOB_USER /var/run/likwid.lock
        # Also grant permission to use performance counters via perf interface (e.g. with VTune)
        echo 0 > /proc/sys/kernel/perf_event_paranoid
    elif [ $(stat -c "%U" /var/run/likwid.lock) != "monitoring" ]; then
        chown monitoring /var/run/likwid.lock
    fi
elif [[ "$SLURM_JOB_CONSTRAINTS" =~ "hwperf" ]] ; then
    echo "ATTENTION: requested access to performance counters cannot be granted as /var/run/likwid.lock does not exist or is no regular file"
fi
```

## Epilogue: `/etc/slurm/slurm.epilog`

The epilogue returns ownership of the lock file to the monitoring user and
restores the restrictive `perf_event_paranoid` setting.

```bash
#
# Return permission to the monitoring user for system monitoring.
#
if [ -f /var/run/likwid.lock ]; then
    if [[ "$SLURM_JOB_CONSTRAINTS" =~ "hwperf" ]] ; then
        chown $MONITORING_USER /var/run/likwid.lock
        # Disable permission to use performance counters via perf interface (e.g. with VTune)
        echo 2 > /proc/sys/kernel/perf_event_paranoid
    fi

    if [ $(stat -c "%U" /var/run/likwid.lock) != "monitoring" ]; then
        chown monitoring:root /var/run/likwid.lock
    fi
fi
```

{{< alert title="Note" >}}
`perf_event_paranoid=2` is the standard restrictive setting. Some Linux distributions
also support the stricter value `4`. Check your kernel version and distribution before
using it.
{{< /alert >}}

## Nvidia GPU Profiling

For nodes with Nvidia GPUs, extend the prologue/epilogue with the relevant
`nvidia-smi` permission calls to grant and revoke GPU performance counter access
in the same manner.

## How It Works

| Phase | `hwperf` constraint set? | Result |
|-------|--------------------------|--------|
| Submit filter | Yes, but `--exclusive` missing | Job rejected |
| Prologue | Yes | Lock file owned by job user, `perf_event_paranoid=0` |
| Prologue | No | Lock file stays with monitoring user |
| Epilogue | Yes | Lock file returned to monitoring user, `perf_event_paranoid=2` |
| Epilogue | No | No change needed |

During a job with `hwperf`, the system monitoring daemon loses counter access for
the duration of that job on the affected node. This is expected and acceptable
since the node is used exclusively by the job.
