---
title: Architecture
description: Technical architecture and internal details
categories: [cc-slurm-adapter]
tags: [Adapter, Architecture]
weight: 7
---

## Synchronization Flow

The daemon operates on a periodic synchronization cycle:

1. **Timer Trigger**: Periodic timer (default: 60s) triggers sync
2. **Query Slurm**: Fetch job data via `sacct`, `squeue`, `scontrol`
3. **Submit to cc-backend**: POST job start/stop via REST API
4. **Publish to NATS**: Optional notification message (if enabled)

This ensures that all jobs are eventually captured, even if Prolog/Epilog hooks fail or are not configured.

## Prolog/Epilog Flow

When Prolog/Epilog hooks are enabled, immediate job notification works as follows:

1. **Job Event**: Slurm triggers Prolog/Epilog hook when a job starts or stops
2. **Socket Message**: Hook sends job ID to daemon via socket
3. **Immediate Query**: Daemon queries Slurm for that specific job
4. **Fast Submission**: Job submitted to cc-backend with minimal delay

This reduces latency from up to 60 seconds (default poll interval) to just a few seconds.

## Data Sources

The adapter queries multiple Slurm commands to build complete job information:

| Slurm Command       | Purpose                                   |
| ------------------- | ----------------------------------------- |
| `sacct`             | Historical job accounting data            |
| `squeue`            | Current job queue information             |
| `scontrol show job` | Resource allocation details (JSON format) |
| `sacctmgr`          | User permissions                          |

**Important**: `scontrol show job` provides critical resource allocation information (nodes, CPUs, GPUs) that is **only available while the job is in memory**. This information typically expires a few minutes after job completion, which is why keeping the daemon running continuously is essential.

## State Persistence

The adapter maintains minimal state on disk:

- **Last Run Timestamp**: Stored as file modification time in `lastRunPath`
  - Used to determine which jobs to query on startup
  - Prevents flooding cc-backend with historical jobs after restarts
  
- **PID File**: Stored in `pidFilePath`
  - Prevents concurrent daemon execution
  - Automatically cleaned up on graceful shutdown

- **Socket**: IPC between daemon and Prolog/Epilog instances
  - Created at `prepSockListenPath` (daemon listens)
  - Connected at `prepSockConnectPath` (Prolog/Epilog connects)
  - Supports both UNIX domain sockets and TCP sockets

## Fault Tolerance

The adapter is designed to be fault-tolerant:

### Slurm Downtime
- Retries Slurm queries with exponential backoff
- Continues operation once Slurm becomes available
- No job loss during Slurm restarts

### cc-backend Downtime
- Queues jobs internally (up to `slurmQueryMaxSpan` seconds in the past)
- Submits queued jobs once cc-backend is available
- Prevents duplicate submissions

### Daemon Restarts
- Uses `lastRunPath` timestamp to catch up on missed jobs
- Limited by `slurmQueryMaxSpan` to prevent overwhelming the system
- Resource allocation data may be lost for jobs that completed while daemon was down

## Multi-Cluster Considerations

For environments with multiple Slurm clusters:

- Run one daemon instance per slurmctld node
- Use cluster-specific configuration files
- Consider TCP sockets for Prolog/Epilog if slurmctld is not on compute nodes

## Performance Characteristics

### Resource Usage
- **Memory**: Minimal (< 50 MB typical)
- **CPU**: Low (periodic bursts during synchronization)
- **Network**: Moderate (REST API calls to cc-backend, NATS if enabled)

### Scalability
- Tested with clusters of 1000+ nodes
- Handle thousands of jobs per day
- Poll interval can be tuned based on job submission rate

### Latency
- **Without Prolog/Epilog**: Up to `slurmPollInterval` seconds (default: 60s)
- **With Prolog/Epilog**: Typically < 5 seconds
