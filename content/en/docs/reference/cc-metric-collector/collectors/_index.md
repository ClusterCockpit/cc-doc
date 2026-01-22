---
title: Collectors
description: Available metric collectors for cc-metric-collector
categories: [cc-metric-collector]
tags: [Collector]
weight: 6
---

## Overview

Collectors read data from various sources on the local system, parse it into metrics, and submit these metrics to the router. Each collector is a modular plugin that can be enabled or disabled independently.

## Configuration Format

**File**: `collectors.json`

The collectors configuration is a set of objects (not a list), where each key is the collector type:

```json
{
  "collector_type": {
    "collector_specific_option": "value"
  }
}
```

## Common Configuration Options

Most collectors support these common options:

| Option            | Type     | Default | Description                                              |
| ----------------- | -------- | ------- | -------------------------------------------------------- |
| `exclude_metrics` | []string | `[]`    | List of metric names to exclude from forwarding to sinks |
| `send_meta`       | bool     | varies  | Send metadata information along with metrics             |

**Example**:
```json
{
  "cpustat": {
    "exclude_metrics": ["cpu_idle", "cpu_guest"]
  },
  "memstat": {}
}
```

## Available Collectors

### System Metrics

| Collector       | Description                                    | Source                 |
| --------------- | ---------------------------------------------- | ---------------------- |
| [`cpustat`]     | CPU usage statistics                           | `/proc/stat`           |
| [`memstat`]     | Memory usage statistics                        | `/proc/meminfo`        |
| [`loadavg`]     | System load average                            | `/proc/loadavg`        |
| [`netstat`]     | Network interface statistics                   | `/proc/net/dev`        |
| [`diskstat`]    | Disk I/O statistics                            | `/sys/block/*/stat`    |
| [`iostat`]      | Block device I/O statistics                    | `/proc/diskstats`      |

[`cpustat`]: https://github.com/ClusterCockpit/cc-metric-collector/blob/main/collectors/cpustatMetric.md
[`memstat`]: https://github.com/ClusterCockpit/cc-metric-collector/blob/main/collectors/memstatMetric.md
[`loadavg`]: https://github.com/ClusterCockpit/cc-metric-collector/blob/main/collectors/loadavgMetric.md
[`netstat`]: https://github.com/ClusterCockpit/cc-metric-collector/blob/main/collectors/netstatMetric.md
[`diskstat`]: https://github.com/ClusterCockpit/cc-metric-collector/blob/main/collectors/diskstatMetric.md
[`iostat`]: https://github.com/ClusterCockpit/cc-metric-collector/blob/main/collectors/iostatMetric.md

### Hardware Monitoring

| Collector       | Description                      | Requirements            |
| --------------- | -------------------------------- | ----------------------- |
| [`tempstat`]    | Temperature sensors              | `/sys/class/hwmon`      |
| [`cpufreq`]     | CPU frequency                    | `/sys/devices/system`   |
| [`cpufreq_cpuinfo`] | CPU frequency from cpuinfo   | `/proc/cpuinfo`         |
| [`ipmistat`]    | IPMI sensor data                 | `ipmitool` command      |

[`tempstat`]: https://github.com/ClusterCockpit/cc-metric-collector/blob/main/collectors/tempMetric.md
[`cpufreq`]: https://github.com/ClusterCockpit/cc-metric-collector/blob/main/collectors/cpufreqMetric.md
[`cpufreq_cpuinfo`]: https://github.com/ClusterCockpit/cc-metric-collector/blob/main/collectors/cpufreqCpuinfoMetric.md
[`ipmistat`]: https://github.com/ClusterCockpit/cc-metric-collector/blob/main/collectors/ipmiMetric.md

### Performance Monitoring

| Collector       | Description                             | Requirements                 |
| --------------- | --------------------------------------- | ---------------------------- |
| [`likwid`]      | Hardware performance counters via LIKWID| liblikwid.so                 |
| [`rapl`]        | CPU energy consumption (RAPL)           | `/sys/class/powercap`        |
| [`schedstat`]   | CPU scheduler statistics                | `/proc/schedstat`            |
| [`numastats`]   | NUMA node statistics                    | `/sys/devices/system/node`   |

[`likwid`]: https://github.com/ClusterCockpit/cc-metric-collector/blob/main/collectors/likwidMetric.md
[`rapl`]: https://github.com/ClusterCockpit/cc-metric-collector/blob/main/collectors/raplMetric.md
[`schedstat`]: https://github.com/ClusterCockpit/cc-metric-collector/blob/main/collectors/schedstatMetric.md
[`numastats`]: https://github.com/ClusterCockpit/cc-metric-collector/blob/main/collectors/numastatsMetric.md

### GPU Monitoring

| Collector       | Description                       | Requirements              |
| --------------- | --------------------------------- | ------------------------- |
| [`nvidia`]      | NVIDIA GPU metrics                | libnvidia-ml.so (NVML)    |
| [`rocm_smi`]    | AMD ROCm GPU metrics              | librocm_smi64.so          |

[`nvidia`]: https://github.com/ClusterCockpit/cc-metric-collector/blob/main/collectors/nvidiaMetric.md
[`rocm_smi`]: https://github.com/ClusterCockpit/cc-metric-collector/blob/main/collectors/rocmsmiMetric.md

### Network & Storage

| Collector           | Description                    | Requirements              |
| ------------------- | ------------------------------ | ------------------------- |
| [`ibstat`]          | InfiniBand statistics          | `/sys/class/infiniband`   |
| [`lustrestat`]      | Lustre filesystem statistics   | Lustre client             |
| [`gpfs`]            | GPFS filesystem statistics     | GPFS utilities            |
| [`beegfs_meta`]     | BeeGFS metadata statistics     | BeeGFS metadata client    |
| [`beegfs_storage`]  | BeeGFS storage statistics      | BeeGFS storage client     |
| [`nfs3stat`]        | NFS v3 statistics              | `/proc/net/rpc/nfs`       |
| [`nfs4stat`]        | NFS v4 statistics              | `/proc/net/rpc/nfs`       |
| [`nfsiostat`]       | NFS I/O statistics             | `nfsiostat` command       |

[`ibstat`]: https://github.com/ClusterCockpit/cc-metric-collector/blob/main/collectors/infinibandMetric.md
[`lustrestat`]: https://github.com/ClusterCockpit/cc-metric-collector/blob/main/collectors/lustreMetric.md
[`gpfs`]: https://github.com/ClusterCockpit/cc-metric-collector/blob/main/collectors/gpfsMetric.md
[`beegfs_meta`]: https://github.com/ClusterCockpit/cc-metric-collector/blob/main/collectors/beegfsmetaMetric.md
[`beegfs_storage`]: https://github.com/ClusterCockpit/cc-metric-collector/blob/main/collectors/beegfsstorageMetric.md
[`nfs3stat`]: https://github.com/ClusterCockpit/cc-metric-collector/blob/main/collectors/nfs3Metric.md
[`nfs4stat`]: https://github.com/ClusterCockpit/cc-metric-collector/blob/main/collectors/nfs4Metric.md
[`nfsiostat`]: https://github.com/ClusterCockpit/cc-metric-collector/blob/main/collectors/nfsiostatMetric.md

### Process & Job Monitoring

| Collector       | Description                          | Requirements            |
| --------------- | ------------------------------------ | ----------------------- |
| [`topprocs`]    | Top processes by resource usage      | `/proc` filesystem      |
| [`slurm_cgroup`]| Slurm cgroup statistics              | Slurm cgroups           |
| [`self`]        | Collector's own resource usage       | `/proc/self`            |

[`topprocs`]: https://github.com/ClusterCockpit/cc-metric-collector/blob/main/collectors/topprocsMetric.md
[`slurm_cgroup`]: https://github.com/ClusterCockpit/cc-metric-collector/blob/main/collectors/slurmCgroupMetric.md
[`self`]: https://github.com/ClusterCockpit/cc-metric-collector/blob/main/collectors/selfMetric.md

### Custom Collectors

| Collector       | Description                               | Requirements       |
| --------------- | ----------------------------------------- | ------------------ |
| [`customcmd`]   | Execute custom commands to collect metrics| Any command/script |

[`customcmd`]: https://github.com/ClusterCockpit/cc-metric-collector/blob/main/collectors/customCmdMetric.md

## Collector Lifecycle

Each collector implements these functions:

- `Init(config)`: Initializes the collector with configuration
- `Initialized()`: Returns whether initialization was successful
- `Read(duration, output)`: Reads metrics and sends to output channel
- `Close()`: Cleanup and shutdown

## Example Configurations

### Minimal System Monitoring

```json
{
  "cpustat": {},
  "memstat": {},
  "loadavg": {}
}
```

### HPC Node Monitoring

```json
{
  "cpustat": {},
  "memstat": {},
  "diskstat": {},
  "netstat": {},
  "loadavg": {},
  "tempstat": {},
  "likwid": {
    "access_mode": "direct",
    "liblikwid_path": "/usr/local/lib/liblikwid.so",
    "eventsets": [
      {
        "events": {
          "cpu": ["FLOPS_DP", "CLOCK"]
        }
      }
    ]
  },
  "nvidia": {},
  "ibstat": {}
}
```

### Filesystem-Heavy Workload

```json
{
  "cpustat": {},
  "memstat": {},
  "diskstat": {},
  "lustrestat": {},
  "nfs4stat": {},
  "iostat": {}
}
```

### Minimal Overhead

```json
{
  "cpustat": {
    "exclude_metrics": ["cpu_guest", "cpu_guest_nice", "cpu_steal"]
  },
  "memstat": {
    "exclude_metrics": ["mem_slab", "mem_sreclaimable"]
  }
}
```

## Collector Development

### Creating a Custom Collector

Collectors implement the `MetricCollector` interface. See [collectors README](https://github.com/ClusterCockpit/cc-metric-collector/blob/main/collectors/README.md#contributing-own-collectors) for details.

**Basic structure**:
```go
type SampleCollector struct {
    metricCollector
    config SampleCollectorConfig
}

func (m *SampleCollector) Init(config json.RawMessage) error
func (m *SampleCollector) Read(interval time.Duration, output chan lp.CCMetric)
func (m *SampleCollector) Close()
```

### Registration

Add your collector to `collectorManager.go`:

```go
var AvailableCollectors = map[string]MetricCollector{
    "sample": &SampleCollector{},
}
```

## Metric Format

All collectors submit metrics in [InfluxDB line protocol](https://docs.influxdata.com/influxdb/cloud/reference/syntax/line-protocol/) format via the CCMetric type.

**Metric components**:
- **Name**: Metric identifier (e.g., `cpu_used`)
- **Tags**: Index-like key-value pairs (e.g., `type=node`, `hostname=node01`)
- **Fields**: Data values (typically just `value`)
- **Metadata**: Source, group, unit information
- **Timestamp**: When the metric was collected

## Performance Considerations

- **Collector overhead**: Each enabled collector adds CPU overhead
- **I/O impact**: Some collectors read many files (e.g., per-core statistics)
- **Library overhead**: GPU and hardware performance collectors can be expensive
- **Selective metrics**: Use `exclude_metrics` to reduce unnecessary data

## See Also

- [Configuration](../configuration/)
- [Router](../router/)
- [Collector Documentation (GitHub)](https://github.com/ClusterCockpit/cc-metric-collector/blob/main/collectors/README.md)
- [Supported Metrics Specification](https://github.com/ClusterCockpit/cc-specifications/blob/master/interfaces/lineprotocol/README.md)
