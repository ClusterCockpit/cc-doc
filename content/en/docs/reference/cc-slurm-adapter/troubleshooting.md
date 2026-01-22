---
title: Troubleshooting
description: Debugging and common issues
categories: [cc-slurm-adapter]
tags: [Adapter, Debug]
weight: 6
---

## Check Service Status

Verify the daemon is running:

```bash
sudo systemctl status cc-slurm-adapter
```

You should see output indicating the service is `active (running)`.

## View Logs

cc-slurm-adapter logs to stderr (captured by systemd):

```bash
sudo journalctl -u cc-slurm-adapter -f
```

Use `-f` to follow logs in real-time, or omit it to view historical logs.

## Enable Debug Logging

Edit the systemd service file to add `-debug 5`:

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

## Common Issues

| Issue                    | Possible Cause                    | Solution                                                                  |
| ------------------------ | --------------------------------- | ------------------------------------------------------------------------- |
| No jobs reported         | Missing Slurm permissions         | Run `sacctmgr add user cc-slurm-adapter Account=root AdminLevel=operator` |
| Socket connection errors | Wrong socket path or permissions  | Check `prepSockListenPath`/`prepSockConnectPath` and RuntimeDirectoryMode |
| Prolog/Epilog failures   | Non-zero exit code in hook script | Ensure hook script exits with `exit 0`                                    |
| Missing resource info    | Daemon stopped too long           | Keep daemon running; resource info expires minutes after job completion   |
| Job allocation failures  | Prolog/Epilog exit code ≠ 0       | Check hook script and ensure cc-slurm-adapter is running                  |

## Debugging Slurm Compatibility Issues

If you encounter nil pointer dereferences or unexpected errors:

1. Get a job ID via `squeue` or `sacct`:

   ```bash
   squeue
   # or
   sacct
   ```

2. Check JSON layouts from both commands (they differ):

   ```bash
   sacct -j 12345 --json
   scontrol show job 12345 --json
   ```

3. Compare the output with what the adapter expects in `slurm.go`

4. Report issues to the [GitHub repository](https://github.com/ClusterCockpit/cc-slurm-adapter/issues) with:
   - Slurm version
   - JSON output samples
   - Error messages from logs

## Verifying Configuration

Check that your configuration is valid:

```bash
# Test if config file is readable
cat /opt/cc-slurm-adapter/config.json

# Verify JSON syntax
jq . /opt/cc-slurm-adapter/config.json
```

## Testing Connectivity

### Test cc-backend Connection

```bash
# Test REST API endpoint (replace with your JWT)
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     https://your-cc-backend-instance.example/api/jobs/
```

### Test NATS Connection

If using NATS, verify connectivity:

```bash
# Using nats-cli (if installed)
nats server check -s nats://mynatsserver.example:4222
```

## Performance Issues

If the adapter is slow or missing jobs:

1. **Check Slurm Response Times**: Run `sacct` and `squeue` manually to see if Slurm is responding slowly
2. **Adjust Poll Intervals**: Lower `slurmPollInterval` for more frequent checks (but higher load)
3. **Enable Prolog/Epilog**: Reduces dependency on polling for immediate job notification
4. **Check System Resources**: Ensure adequate CPU/memory on the slurmctld node
