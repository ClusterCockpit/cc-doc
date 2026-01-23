---
title: InfluxDB Line Protocol
description: >
    Detailed specification of the InfluxDB Line Protocol format used for metric ingestion, covering Node and Hardware level metrics.
tags: ["influxdb", "protocol", "metrics"]
categories:  [cc-backend]
---
## Overview

All metrics ingested into the cc-metric-store—whether via REST API or NATS—must strictly adhere to the **InfluxDB Line Protocol**. This text-based format allows us to tag high-frequency telemetry data with the necessary dimensions (cluster, host, hardware type) for efficient querying.

## Line Protocol Syntax

The general format for a single data point is:

```text
<measurement>,<tag_set> <field_set> <timestamp>
```


In our specific cc-metric-store implementation, the structure translates to:

```text
metric_name,cluster=<name>,hostname=<host>,type=<hw_type>,type-id=<id> value=<float> <unix_epoch>
```

| Component       | Description                                                | Example                        |
| :-------------- | :--------------------------------------------------------- | :----------------------------- |
| **Measurement** | The specific metric name being recorded.                   | `cpu_load`                     |
| **Tags**        | Key-value pairs providing context (metadata).              | `cluster=alex,hostname=node01` |
| **Fields**      | The actual data value. We use a single field key: `value`. | `value=45.2`                   |
| **Timestamp**   | Unix timestamp in seconds.                                 | `1725827464`                   |

---

## Metric Modes

We distinguishes between two primary scopes of metrics: **Hardware Level** and **Node Level**.

### 1. Hardware Level Metrics
These metrics track the performance of specific sub-components *within* a node (e.g., a specific CPU core, a GPU, or a memory domain).

**Requirement:** You must include the `type-id` tag to distinguish between multiple components of the same type on the same host.

**Schema:**
```text
<metric>,cluster=<c>,hostname=<h>,type=<component>,type-id=<index> value=<v> <time>
```

**Example Hardware Types:**
* **`hwthread`**: Logical CPU threads. (IDs: `0..127` for Cluster1, `0..71` for Cluster2)
* **`socket`**: Physical CPU sockets. (IDs: `0..1`)
* **`accelerator`**: GPUs or FPGA cards. (IDs: PCI Bus Address, e.g., `00000000:49:00.0`)
* **`memoryDomain`**: NUMA nodes. (IDs: `0..7`)

**Example Payload:**
```text
cpu_user,cluster=alex,hostname=a0603,type=hwthread,type-id=12 value=88.5 1725827464
core_power,cluster=fritz,hostname=f0201,type=socket,type-id=0 value=120.0 1725827464
```

### 2. Node Level Metrics
These metrics represent the aggregate state of the entire node.

**Requirement:** The `type` tag is set to `node`. The `type-id` tag is usually omitted or ignored for these metrics.

**Schema:**
```text
<metric>,cluster=<c>,hostname=<h>,type=node value=<v> <time>
```

**Example Payload:**
```text
mem_used,cluster=alex,hostname=a0603,type=node value=64000.0 1725827464
ib_xmit,cluster=fritz,hostname=f0201,type=node value=1024500.0 1725827464
```


## Related Tools

To test this protocol with synthetic data, you can use the **Metric Generator**.
See the documentation here: 
[Metric Generator Script]({{< ref "/docs/reference/cc-backend/tools/dataGenerator.md" >}})

---