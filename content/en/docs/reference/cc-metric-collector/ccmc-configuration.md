---
title: Configuration
description: >
  cc-metric-collector Configuration Reference
categories: [cc-metric-collector]
tags: [Collector, Configuration]
weight: 2
---

## Configuration Overview

The configuration of cc-metric-collector consists of five configuration files: one global file and four component-related files.

Configuration is implemented using a single JSON document that can be distributed over the network and persisted as a file.

## Global Configuration File

The global file contains paths to the other four component files and some global options.

Default location: `/etc/cc-metric-collector/config.json` (can be overridden with `-config` flag)

### Example

```json
{
  "sinks-file": "/etc/cc-metric-collector/sinks.json",
  "collectors-file": "/etc/cc-metric-collector/collectors.json",
  "receivers-file": "/etc/cc-metric-collector/receivers.json",
  "router-file": "/etc/cc-metric-collector/router.json",
  "main": {
    "interval": "10s",
    "duration": "1s"
  }
}
```

**Note**: Paths are relative to the execution folder of the cc-metric-collector binary, so it is recommended to use absolute paths.

### Configuration Reference

| Config Key         | Type   | Default | Description                                                                                          |
| ------------------ | ------ | ------- | ---------------------------------------------------------------------------------------------------- |
| `sinks-file`       | string | -       | Path to sinks configuration file (relative or absolute)                                              |
| `collectors-file`  | string | -       | Path to collectors configuration file (relative or absolute)                                         |
| `receivers-file`   | string | -       | Path to receivers configuration file (relative or absolute)                                          |
| `router-file`      | string | -       | Path to router configuration file (relative or absolute)                                             |
| `main.interval`    | string | `10s`   | How often metrics should be read and sent to sinks. Parsed using `time.ParseDuration()`              |
| `main.duration`    | string | `1s`    | How long one measurement should take. Important for collectors like `likwid` that measure over time. |

### Alternative Configuration Format

Instead of separate files, you can embed component configurations directly:

```json
{
  "sinks": {
    "mysink": {
      "type": "influxasync",
      "host": "localhost",
      "port": "8086"
    }
  },
  "collectors": {
    "cpustat": {}
  },
  "receivers": {},
  "router": {
    "interval_timestamp": false
  },
  "main": {
    "interval": "10s",
    "duration": "1s"
  }
}
```

## Component Configuration Files

### Collectors Configuration

The collectors configuration file specifies which metrics should be queried from the system. See [Collectors](../collectors/) for available collectors and their configuration options.

**Format**: Unlike sinks and receivers, the collectors configuration is a set of objects (not a list).

**File**: `collectors.json`

**Example**:
```json
{
  "cpustat": {},
  "memstat": {},
  "diskstat": {
    "exclude_metrics": [
      "disk_total"
    ]
  },
  "likwid": {
    "access_mode": "direct",
    "liblikwid_path": "/usr/local/lib/liblikwid.so",
    "eventsets": [
      {
        "events": {
          "cpu": ["FLOPS_DP"]
        }
      }
    ]
  }
}
```

**Common Options** (available for most collectors):

| Option            | Type     | Description                                                      |
| ----------------- | -------- | ---------------------------------------------------------------- |
| `exclude_metrics` | []string | List of metric names to exclude from forwarding to sinks         |
| `send_meta`       | bool     | Send metadata information along with metrics (default varies)    |

**See**: [Collectors Documentation](../collectors/) for collector-specific configuration options.

**Note**: Some collectors dynamically load shared libraries. Ensure the library path is part of the `LD_LIBRARY_PATH` environment variable.

### Sinks Configuration

The sinks configuration file defines where metrics should be sent. Multiple sinks of the same or different types can be configured.

**Format**: Object with named sink configurations

**File**: `sinks.json`

**Example**:
```json
{
  "local_influx": {
    "type": "influxasync",
    "host": "localhost",
    "port": "8086",
    "organization": "myorg",
    "database": "metrics",
    "password": "mytoken"
  },
  "central_prometheus": {
    "type": "prometheus",
    "host": "0.0.0.0",
    "port": "9091"
  },
  "debug_log": {
    "type": "stdout"
  }
}
```

**Common Sink Types**:

| Type            | Description                                          |
| --------------- | ---------------------------------------------------- |
| `influxasync`   | InfluxDB v2 asynchronous writer                      |
| `influxdb`      | InfluxDB v2 synchronous writer                       |
| `prometheus`    | Prometheus Pushgateway                               |
| `nats`          | NATS messaging system                                |
| `stdout`        | Standard output (for debugging)                      |
| `libganglia`    | Ganglia monitoring system                            |
| `http`          | Generic HTTP endpoint                                |

**See**: [cc-lib Sinks Documentation](https://github.com/ClusterCockpit/cc-lib/blob/main/sinks/README.md) for sink-specific configuration options.

**Note**: Some sinks dynamically load shared libraries. Ensure the library path is part of the `LD_LIBRARY_PATH` environment variable.

### Router Configuration

The router sits between collectors/receivers and sinks, enabling metric processing such as tagging, filtering, renaming, and aggregation.

**File**: `router.json`

**Simple Example**:
```json
{
  "add_tags": [
    {
      "key": "cluster",
      "value": "mycluster",
      "if": "*"
    }
  ],
  "interval_timestamp": false,
  "num_cache_intervals": 0
}
```

**Advanced Example**:
```json
{
  "num_cache_intervals": 1,
  "interval_timestamp": true,
  "hostname_tag": "hostname",
  "max_forward": 50,
  "process_messages": {
    "manipulate_messages": [
      {
        "add_base_tags": {
          "cluster": "mycluster"
        }
      }
    ]
  }
}
```

**Configuration Reference**:

| Option                | Type    | Default      | Description                                                                              |
| --------------------- | ------- | ------------ | ---------------------------------------------------------------------------------------- |
| `interval_timestamp`  | bool    | `false`      | Use common timestamp (interval start) for all metrics in an interval                     |
| `num_cache_intervals` | int     | `0`          | Number of past intervals to cache (0 disables cache, required for interval aggregates)   |
| `hostname_tag`        | string  | `"hostname"` | Tag name for hostname (added to locally created metrics)                                 |
| `max_forward`         | int     | `50`         | Max metrics to read from a channel at once (must be > 1)                                 |
| `process_messages`    | object  | -            | Message processor configuration (see below)                                              |

**See**: [Router Documentation](../router/) for detailed configuration options and [Message Processor](https://github.com/ClusterCockpit/cc-lib/blob/main/messageProcessor/README.md) for advanced processing.

### Receivers Configuration

Receivers enable cc-metric-collector to accept metrics from other collectors via network protocols. For most standalone setups, this file can contain only an empty JSON map (`{}`).

**File**: `receivers.json`

**Example**:
```json
{
  "nats_rack0": {
    "type": "nats",
    "address": "nats-server.example.org",
    "port": "4222",
    "subject": "rack0"
  },
  "http_receiver": {
    "type": "http",
    "address": "0.0.0.0",
    "port": "8080",
    "path": "/api/write"
  }
}
```

**Common Receiver Types**:

| Type   | Description                                  |
| ------ | -------------------------------------------- |
| `nats` | NATS subscriber                              |
| `http` | HTTP server endpoint for metric ingestion    |

**See**: [cc-lib Receivers Documentation](https://github.com/ClusterCockpit/cc-lib/blob/main/receivers/README.md) for receiver-specific configuration options.

## Configuration Examples

Complete example configurations can be found in the [example-configs](https://github.com/ClusterCockpit/cc-metric-collector/tree/main/example-configs) directory of the repository.

## Configuration Validation

To validate your configuration before running the collector:

```bash
# Test configuration loading
cc-metric-collector -config /path/to/config.json -once
```

The `-once` flag runs all collectors only once and exits, useful for testing.
