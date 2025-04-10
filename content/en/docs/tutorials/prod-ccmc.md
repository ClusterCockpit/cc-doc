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

- `collectors`: Metric sources. There is a large number of [collectors](https://github.com/ClusterCockpit/cc-metric-collector/blob/main/collectors/README.md) available.
 Important and also most demanding to configure is the [likwid collector](https://github.com/ClusterCockpit/cc-metric-collector/blob/main/collectors/likwidMetric.md) for measuring hardware performance counter metrics.
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
