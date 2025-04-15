---
title: Setup of cc-metric-collector
weight: 30
description: How to configure and deploy cc-metric-collector
categories: [cc-metric-collector]
tags: [Admin]
---

## Introduction

`cc-metric-collector` is a node agent for measuring, processing and forwarding
node level metrics. It is currently mostly documented via Markdown documents in
its [GitHub repository](https://github.com/ClusterCockpit/cc-metric-collector).
The configuration consists of the following parts:

- `collectors`: Metric sources. There is a large number of
[collectors](https://github.com/ClusterCockpit/cc-metric-collector/blob/main/collectors/README.md) available.
 Important and also most demanding to configure is the
[likwid collector](https://github.com/ClusterCockpit/cc-metric-collector/blob/main/collectors/likwidMetric.md)
for measuring hardware performance counter metrics.
- `router`: Rename, drop and modify metrics.
- `sinks`: Configuration where to send the metrics.
- `receivers`: Receive metrics. Useful as a proxy to connect different metric
sinks. Can be left empty in most cases.

## Build and deploy

Since the `cc-metric-collector` needs to be installed on every compute node and
requires configuration specific to the node hardware it is demanding to install
and configure. The Makefile supports to generate RPM and DEB packages. There is
also a Systemd service file included which you may take as a blueprint.
More information on deployment is available [here](https://github.com/ClusterCockpit/cc-metric-collector/blob/main/docs/building.md).

## Collectors

You may want to have a look at our [collector configuration](https://github.com/ClusterCockpit/cc-examples/tree/main/nhr%40fau/cc-metric-collector)
which includes configurations for many different systems, Intel and AMD CPUs and
NVIDIA GPUs. The general recommendation is to first decide on the metrics you
need and then figure out which collectors are required. For hardware performance
counter metrics you may want to have a look at `likwid-perfctr`
[performance groups](https://github.com/RRZE-HPC/likwid/tree/master/groups)
for inspiration on how to computer the required derived metrics on your
target processor architecture.

## Router

The router enables to rename, drop and modify metrics.
Top level configuration attributes (can be usually be left at default):

- `interval_timestamp`: Metrics received within same interval get the same
identical time stamp if true. Default is true.
- `num_cache_intervals`: Number of intervals that are cached in router. Default
  is 1. Set to 0 to disable router cache.
- `hostname_tag`: Set a host name different that what is returned by `hostname`.
- `max_forward`: Number of metrics read at once from a Golang channel. Default
is 50. Option has to be larger than 1. Recommendation: Leave at default!

Below you find the operations that are supported by the message processor.

### Rename metrics

To rename metric names add a `rename_messages` section mapping the old metric
name to the new name.

```json
"process_messages" : {
    "rename_messages" : {
        "load_one" : "cpu_load",
        "net_bytes_in_bw" : "net_bytes_in",
        "net_bytes_out_bw" : "net_bytes_out",
        "net_pkts_in_bw" : "net_pkts_in",
        "net_pkts_out_bw" : "net_pkts_out",
        "ib_recv_bw" : "ib_recv",
        "ib_xmit_bw" : "ib_xmit",
        "lustre_read_bytes_diff" : "lustre_read_bytes",
        "lustre_read_requests_diff" : "lustre_read_requests",
        "lustre_write_bytes_diff" : "lustre_write_bytes",
        "lustre_write_requests_diff" : "lustre_write_requests",
}
```

### Drop metrics

Sometimes collectors provide a lot of metrics that are not needed. To save
data volume metrics can be dropped. Some collectors also support to exclude
metrics at the collector level using the `exclude_metrics` option.

{{< alert title="Note" >}}
If you are using the `cc-metric-store` all metrics that are not configured in
its metric list are also silently dropped.
{{< /alert >}}

```json
"process_messages" : {
   "drop_messages" : [
       "load_five",
       "load_fifteen",
       "proc_run",
       "proc_total"
   ],
}
```

### Normalize unit naming

Enforce a consistent naming of units in metrics. This option should always be
set to true which is the default. The metric value is not altered!

```json
"process_messages" : {
   "normalize_units": true
}
```

### Change metric unit

The collectors usually do not alter the unit of a metric. To change the unit set
the `change_uni_prefix` key. The value is automatically scaled correctly,
depending on the old unit prefix.

```json
"process_messages" : {
   "change_unit_prefix": {
       "name == 'mem_used'": "G",
       "name == 'swap_used'": "G",
       "name == 'mem_total'": "G",
       "name == 'swap_total'": "G",
       "name == 'cpufreq'": "M"
   }
}
```

### Add tags

To add tags set the `add_tags_if` configuration attribute. The following
statement unconditionally sets a cluster name tag for all metrics.

{{< alert title="Note" >}}
You always want to set the cluster tag if you are using `cc-metric-collector`
within the ClusterCockpit framework!
{{< /alert >}}

```json
"process_messages" : {
    "add_tags_if": [
      {
        "key": "cluster",
        "value": "alex",
        "if": "true"
      }
    ],
}
```

## Sinks

A simple example configuration for two sinks: HTTP cc-metric-store and NATS:

``` json
{
  "fritzstore": {
    "type": "http",
    "url": "http://monitoring.nhr.fau.de:8082/api/write?cluster=fritz",
    "jwt": "XYZ",
    "idle_connection_timeout": "60s"
  },
  "fritznats": {
    "type": "nats",
    "host": "monitoring.nhr.fau.de",
    "database": "fritz",
    "nkey_file": "/etc/cc-metric-collector/nats.nkey",
  }
}
```

All metrics are concurrently send to all configured sinks.

{{< alert color="danger" title="Note" >}}
`cc-metric-store` only accepts timestamps in seconds
{{< /alert >}}
