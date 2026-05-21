---
title: Commands
description: ClusterCockpit Node Controller Command Line References
categories: [cc-node-controller]
tags: [Backend]
weight: 1
---

## Server Daemon

### Build

```bash
make
```

Produces the `cc-node-controller` binary in the repository root. Debian and RPM packages can be built with `make DEB` and `make RPM` respectively.

### Run

```bash
./cc-node-controller [options]
```

The daemon must run on the compute node it controls (it only processes messages matching its own hostname) and requires access to `liblikwid.so`.

### Options

| Flag | Default | Description |
|------|---------|-------------|
| `-config <path>` | `./config.json` | Path to the JSON configuration file |
| `-loglevel <level>` | `warn` | Log verbosity: `debug`, `info`, `warn`, `error` |
| `-pretend` | `false` | Dry-run mode — process messages and log what would happen, but do not apply any hardware changes |

### Example

```bash
./cc-node-controller -config /etc/cc-node-controller/config.json -loglevel info
```

### Signals

`cc-node-controller` handles the following UNIX signals for graceful shutdown:

- `SIGTERM` — sent by systemd on `systemctl stop`
- `SIGINT` — sent by Ctrl+C

---

## Remote Client (`remoteclient`)

`remoteclient` is a command-line utility for interacting with a running `cc-node-controller` instance over NATS. It is useful for testing, diagnostics, and manual control operations.

### Build

```bash
go build ./cmd/remoteclient/
```

### Usage

```bash
./remoteclient -host <hostname> [options] <operation>
```

`-host` is always required.

### Options

| Flag | Default | Description |
|------|---------|-------------|
| `-host <hostname>` | (required) | Short hostname of the target node |
| `-server <ip>` | `127.0.0.1` | NATS server IP or hostname |
| `-port <port>` | `4222` | NATS server port |
| `-request-subject <subject>` | `cc-control` | NATS subject used by the target node's cc-node-controller |
| `-debug` | `false` | Enable debug output |

### Operations

Exactly one operation flag must be specified:

| Flag | Description |
|------|-------------|
| `-topology` | Print the hardware topology of the target node |
| `-list` | List all controls available on the target node |
| `-get <control>@<type>-<id>` | Read the current value of a control |
| `-set <control>@<type>-<id>=<value>` | Write a new value to a control |

The control address format is `<category>.<name>@<device_type>-<device_id>`, for example `rapl.pkg_power_limit1@socket-0`.

### Examples

```bash
# List hardware topology
./remoteclient -host node01 -topology

# List available controls
./remoteclient -host node01 -list

# Read RAPL package power limit on socket 0
./remoteclient -host node01 -get rapl.pkg_power_limit1@socket-0

# Set RAPL package power limit on socket 0 to 150 W
./remoteclient -host node01 -set rapl.pkg_power_limit1@socket-0=150

# Connect to a remote NATS server
./remoteclient -host node01 -server nats.example.org -port 4222 -list
```
