---
title: InfluxDB Line Protocol
description: >
    Specification of the InfluxDB line-protocol flavor used for messaging between ClusterCockpit components, covering metrics, events, and control messages.
tags: ["influxdb", "protocol", "metrics", "events", "nats"]
categories:  [cc-backend]
---

## Overview

ClusterCockpit uses an [InfluxData line-protocol](https://docs.influxdata.com/influxdb/v2.1/reference/syntax/line-protocol/) flavor for transferring messages between its components. All messages share the same text-based format:

```text
<measurement>,<tag_set> <field_set> <timestamp>
```

Where `<tag_set>` and `<field_set>` are comma-separated lists of `key=value` entries. The timestamp is Unix epoch time in **seconds**.

{{< alert title="Backward Compatibility" >}}
Initially only metrics (number values) were sent. The specification was extended to support messages with different purposes (events, controls). This extension is backward-compatible — metric messages are unchanged.
{{< /alert >}}

## Message Categories

Three message categories are distinguished by their field key:

| Category    | Field Key            | Field Type      | Purpose                                  |
| :---------- | :------------------- | :-------------- | :--------------------------------------- |
| **Metric**  | `value=<number>`     | float/integer   | Performance metric time series           |
| **Event**   | `event="<json>"`     | string (JSON)   | Actionable job and cluster events        |
| **Control** | `control="<string>"` | string          | Component configuration requests         |

## NATS Subject Hierarchy

ClusterCockpit uses NATS for messaging. The subject hierarchy lets components subscribe only to the message types they need:

```text
<cluster name>. |
                --- metrics
                |
                --- events.[job, slurm]
                |
                --- control.[get, put]
```

## Tags

### Mandatory Tags

Every message — regardless of category — must include:

| Tag       | Description                          | Values                                                                          |
| :-------- | :----------------------------------- | :------------------------------------------------------------------------------ |
| `hostname` | Source node hostname                | e.g., `node01`                                                                  |
| `type`    | Hardware scope                       | `node`, `socket`, `die`, `memoryDomain`, `llc`, `core`, `hwthread`, `accelerator` |
| `type-id` | Component index within the type      | e.g., `0`, `1`, `2`                                                             |

Although `type-id` is not strictly required when `type=node`, sending `type=node,type-id=0` is recommended for consistency.

### Optional Tags

Some message types require additional tags:

- `function` — for Event messages: the event purpose, e.g., `start_job`, `stop_job`
- `method` — for Control messages: `GET` or `PUT`

For sub-typing (e.g., filesystem name or device path), use `stype` and `stype-id` rather than free-form tag names:

```text
# Preferred
stype=filesystem,stype-id=/homes

# Avoid
filesystem=/homes
```

---

## Metric Messages

**Identification:** `value=<number>` field where the value is a float or integer.

The measurement name is the metric name. While metric names can be chosen freely, the following core metrics should be present in any ClusterCockpit-compatible system:

| Metric       | Description                                   | Unit    |
| :----------- | :-------------------------------------------- | :------ |
| `flops_sp`   | Single-precision floating point rate          | Flops/s |
| `flops_dp`   | Double-precision floating point rate          | Flops/s |
| `flops_any`  | Combined floating point rate                  | Flops/s |
| `cpu_load`   | 1-minute load average (`/proc/loadavg`)       | —       |
| `mem_used`   | Memory used by applications (`/proc/meminfo`) | Bytes   |
| `ipc`        | Instructions per cycle                        | —       |
| `mem_bw`     | Main memory bandwidth (read + write)          | MB/s    |
| `cpu_power`  | CPU package power consumption                 | W       |
| `mem_power`  | Memory subsystem power consumption            | W       |
| `clock`      | CPU clock frequency                           | MHz     |

For the complete metric list see the [job-data schema reference]({{< ref "job-data-schema" >}}).

**Example:**

```text
flops_any,hostname=e1208,type=core,type-id=23 value=1203.3 1740027951
```

For metrics ingested into **cc-metric-store** (via REST API or NATS), the `cluster` tag is additionally required:

```text
flops_any,cluster=alex,hostname=e1208,type=core,type-id=23 value=1203.3 1740027951
```

### Metric Scopes

We distinguish two primary scopes: **Hardware Level** and **Node Level**.

#### Hardware Level Metrics

These metrics track performance of specific sub-components within a node (e.g., a CPU core, GPU, or memory domain). The `type-id` tag identifies which component instance.

**Schema:**
```text
<metric>,cluster=<c>,hostname=<h>,type=<component>,type-id=<index> value=<v> <time>
```

**Example hardware types:**
* **`hwthread`**: Logical CPU threads. (IDs: `0..127` for Cluster1, `0..71` for Cluster2)
* **`socket`**: Physical CPU sockets. (IDs: `0..1`)
* **`accelerator`**: GPUs or FPGA cards. (IDs: PCI Bus Address, e.g., `00000000:49:00.0`)
* **`memoryDomain`**: NUMA nodes. (IDs: `0..7`)

**Examples:**
```text
cpu_user,cluster=alex,hostname=a0603,type=hwthread,type-id=12 value=88.5 1725827464
core_power,cluster=fritz,hostname=f0201,type=socket,type-id=0 value=120.0 1725827464
```

#### Node Level Metrics

These metrics represent the aggregate state of the entire node. Set `type=node`; the `type-id` tag can be omitted or set to `0`.

**Schema:**
```text
<metric>,cluster=<c>,hostname=<h>,type=node value=<v> <time>
```

**Example:**
```text
mem_used,cluster=alex,hostname=a0603,type=node value=64000.0 1725827464
```

---

## Event Messages

**Identification:** `event="<json>"` field where the value is a JSON string.

The measurement name indicates the event class. The `function` tag specifies the purpose (similar to a REST endpoint path).

| Event Class | `function` values             |
| :---------- | :---------------------------- |
| `job`       | `start_job`, `stop_job`       |
| `slurm`     | slurm-specific event types    |

**Example:**

```text
job,hostname=mngmt02,type=node,type-id=0,function=stop_job event={"jobId": 69, "cluster": "ccfront", "stopTime": 1738842306, "jobState": "completed"} 1740027951
```

---

## Control Messages

**Identification:** `control="<string>"` field where the value is the control request payload.

The measurement name is the control class. The `method` tag is either `GET` or `PUT`.

| Control Class | Description                          |
| :------------ | :----------------------------------- |
| `rapl`        | CPU power capping (RAPL interface)   |
| `freq`        | CPU frequency control                |
| `prefetcher`  | Hardware prefetcher control          |
| `topology`    | Topology configuration               |
| `config`      | Component configuration              |

**Example:**

```text
rapl,hostname=e1208,type=socket,type-id=2,method=GET control=intel.pkg.energy_status 1740027951
```

---

## Related Tools

To test metric ingestion with synthetic data, use the **Metric Generator Script**:
[Metric Generator Script]({{< ref "/docs/reference/cc-backend/tools/dataGenerator.md" >}})
