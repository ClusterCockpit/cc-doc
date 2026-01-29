---
title: Command Line
description: >
  ClusterCockpit Metric Store Command Line Options
categories: [cc-metric-store]
tags: [Backend]
weight: 1
---

This page describes the command line options for the `cc-metric-store` executable.

---

```txt
  -config <path>
```

_Function:_ Specifies alternative path to application configuration file.

_Default:_ `./config.json`

_Example:_ `-config ./configfiles/configuration.json`

---

```txt
  -dev
```

_Function:_ Enables the Swagger UI REST API documentation and playground at `/swagger/`.

---

```txt
  -gops
```

_Function:_ Go server listens via github.com/google/gops/agent (for debugging).

---

```txt
  -loglevel <level>
```

_Function:_ Sets the logging level.

_Options:_ `debug`, `info`, `warn` (default), `err`, `crit`

_Example:_ `-loglevel debug`

---

```txt
  -logdate
```

_Function:_ Add date and time to log messages.

---

```txt
  -version
```

_Function:_ Shows version information and exits.

---

## Running

```bash
./cc-metric-store                              # Uses ./config.json
./cc-metric-store -config /path/to/config.json # Custom config path
./cc-metric-store -dev                         # Enable Swagger UI at /swagger/
./cc-metric-store -loglevel debug              # Verbose logging
```

---

## Example Configuration

See [Configuration Reference]({{< ref "ccms-configuration" >}}) for detailed
descriptions of all options.

```json
{
  "main": {
    "addr": "localhost:8080",
    "jwt-public-key": "kzfYrYy+TzpanWZHJ5qSdMj5uKUWgq74BWhQG6copP0="
  },
  "metrics": {
    "clock": {
      "frequency": 60,
      "aggregation": "avg"
    },
    "cpu_idle": {
      "frequency": 60,
      "aggregation": "avg"
    },
    "cpu_iowait": {
      "frequency": 60,
      "aggregation": "avg"
    },
    "cpu_irq": {
      "frequency": 60,
      "aggregation": "avg"
    },
    "cpu_system": {
      "frequency": 60,
      "aggregation": "avg"
    },
    "cpu_user": {
      "frequency": 60,
      "aggregation": "avg"
    },
    "acc_utilization": {
      "frequency": 60,
      "aggregation": "avg"
    },
    "acc_mem_used": {
      "frequency": 60,
      "aggregation": "sum"
    },
    "acc_power": {
      "frequency": 60,
      "aggregation": "sum"
    },
    "flops_any": {
      "frequency": 60,
      "aggregation": "sum"
    },
    "flops_dp": {
      "frequency": 60,
      "aggregation": "sum"
    },
    "flops_sp": {
      "frequency": 60,
      "aggregation": "sum"
    },
    "ib_recv": {
      "frequency": 60,
      "aggregation": "sum"
    },
    "ib_xmit": {
      "frequency": 60,
      "aggregation": "sum"
    },
    "cpu_power": {
      "frequency": 60,
      "aggregation": "sum"
    },
    "mem_power": {
      "frequency": 60,
      "aggregation": "sum"
    },
    "ipc": {
      "frequency": 60,
      "aggregation": "avg"
    },
    "cpu_load": {
      "frequency": 60,
      "aggregation": null
    },
    "mem_bw": {
      "frequency": 60,
      "aggregation": "sum"
    },
    "mem_used": {
      "frequency": 60,
      "aggregation": null
    }
  },
  "metric-store": {
    "checkpoints": {
      "interval": "12h",
      "directory": "./var/checkpoints"
    },
    "memory-cap": 100,
    "retention-in-memory": "48h",
    "cleanup": {
      "mode": "archive",
      "interval": "48h",
      "directory": "./var/archive"
    }
  }
}
```
