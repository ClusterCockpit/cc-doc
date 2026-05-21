---
title: Commands
description: ClusterCockpit Energy Manager Command Line References
categories: [cc-energy-manager]
tags: [Backend]
weight: 1
---

## Build

```bash
make
```

This produces the `cc-energy-manager` binary in the repository root.

## Run

```bash
./cc-energy-manager [options]
```

### Options

| Flag | Default | Description |
|------|---------|-------------|
| `-config <path>` | `./config.json` | Path to the JSON configuration file |
| `-loglevel <level>` | `warn` | Logging verbosity: `debug`, `info`, `warn`, `err`, `fatal`, `crit` |
| `-logdate` | `false` | Prefix every log line with date and time |
| `-once` | `false` | Run all collectors once and then exit (useful for testing) |

### Example

```bash
./cc-energy-manager -config /etc/cc-energy-manager/config.json -loglevel info -logdate
```

## Signals

`cc-energy-manager` handles the following UNIX signals for graceful shutdown:

- `SIGTERM` — sent by systemd on `systemctl stop`
- `SIGINT` — sent by Ctrl+C

On receiving either signal, the daemon stops all receivers, sinks, the cluster manager, and the controller before exiting.
