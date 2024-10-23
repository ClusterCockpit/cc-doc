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

_Function:_ Enables the Swagger UI REST API documentation and playground

---

```txt
  -gops
```

_Function:_ Go server listens via github.com/google/gops/agent (for debugging).

---

```txt
  -version
```

_Function:_ Shows version information and exits.

Example config:

```json
{
  "metrics": {
    "debug_metric": {
      "frequency": 60,
      "aggregation": "avg"
    },
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
    "nv_mem_util": {
      "frequency": 60,
      "aggregation": "avg"
    },
    "nv_temp": {
      "frequency": 60,
      "aggregation": "avg"
    },
    "nv_sm_clock": {
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
    "ib_recv_pkts": {
      "frequency": 60,
      "aggregation": "sum"
    },
    "ib_xmit_pkts": {
      "frequency": 60,
      "aggregation": "sum"
    },
    "cpu_power": {
      "frequency": 60,
      "aggregation": "sum"
    },
    "core_power": {
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
    "lustre_close": {
      "frequency": 60,
      "aggregation": null
    },
    "lustre_open": {
      "frequency": 60,
      "aggregation": null
    },
    "lustre_statfs": {
      "frequency": 60,
      "aggregation": null
    },
    "lustre_read_bytes": {
      "frequency": 60,
      "aggregation": null
    },
    "lustre_write_bytes": {
      "frequency": 60,
      "aggregation": null
    },
    "net_bw": {
      "frequency": 60,
      "aggregation": null
    },
    "file_bw": {
      "frequency": 60,
      "aggregation": null
    },
    "mem_bw": {
      "frequency": 60,
      "aggregation": "sum"
    },
    "mem_cached": {
      "frequency": 60,
      "aggregation": null
    },
    "mem_used": {
      "frequency": 60,
      "aggregation": null
    },
    "vectorization_ratio": {
      "frequency": 60,
      "aggregation": "avg"
    }
  },
  "checkpoints": {
    "interval": "1h",
    "directory": "./var/checkpoints",
    "restore": "1h"
  },
  "archive": {
    "interval": "24h",
    "directory": "./var/archive"
  },
  "http-api": {
    "address": "localhost:8082",
    "https-cert-file": null,
    "https-key-file": null
  },
  "retention-in-memory": "48h",
  "nats": null,
  "jwt-public-key": "kzfYrYy+TzpanWZHJ5qSdMj5uKUWgq74BWhQG6copP0="
}
```
