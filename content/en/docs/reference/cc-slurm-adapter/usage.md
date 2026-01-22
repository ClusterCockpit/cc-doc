---
title: Usage
description: Command line usage and operation modes
categories: [cc-slurm-adapter]
tags: [Adapter, Usage]
weight: 5
---

## Command Line Flags

| Flag                 | Description                                                                        |
| -------------------- | ---------------------------------------------------------------------------------- |
| `-config <path>`     | Specify the path to the config file (default: `/etc/cc-slurm-adapter/config.json`) |
| `-daemon`            | Run in daemon mode (if omitted, runs in Prolog/Epilog mode)                        |
| `-debug <log-level>` | Set the log level (default: 2, max: 5)                                             |
| `-help`              | Show help for all command line flags                                               |

## Operation Modes

### Daemon Mode

Run the adapter as a persistent daemon that periodically synchronizes job information:

```bash
cc-slurm-adapter -daemon -config /path/to/config.json
```

This mode:
- Runs continuously in the background
- Queries Slurm at regular intervals (default: 60 seconds)
- Submits job information to cc-backend
- Should be managed by systemd (see [Daemon Setup](../daemon-setup))

### Prolog/Epilog Mode

Run the adapter from Slurm's Prolog/Epilog hooks for immediate job notification:

```bash
cc-slurm-adapter
```

This mode:
- Only runs when triggered by Slurm (job start/stop)
- Sends job ID to the running daemon via socket
- Exits immediately
- Must be invoked from Slurm hook scripts (see [Prolog/Epilog Setup](../prolog-epilog))

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

## Debug Logging

Enable verbose logging for troubleshooting:

```bash
cc-slurm-adapter -daemon -debug 5 -config /path/to/config.json
```

**Log Levels**:

- 2 (default): Errors and warnings
- 5 (max): Verbose debug output

For systemd services, edit the service file to add `-debug 5` to the `ExecStart` line.
