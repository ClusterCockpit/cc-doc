---
title: ClusterCockpit installation manual
weight: 10
description: How to plan and configure a ClusterCockpit installation
categories: [ClusterCockpit-metric-store]
tags: [Admin]
---

## Introduction

ClusterCockpit requires the following components:

- A **node agent** running on all compute nodes that measures required metrics and
  forwards all data to a time series metrics database. ClusterCockpit provides
  its own node agent `cc-metric-collector`. This is the recommended setup, but ClusterCockpit
  can also be integrated with other node agents, e.g. `collectd`, `prometheus` or
  `telegraf`. In this case you have to use it with the accompanying time series database.
- A **metric time series database**. ClusterCockpit provides its own solution
  `cc-metric-store`, that is the recommended solution. There is also metric store
  support for Prometheus and InfluxDB. InfluxDB is currently barely tested.
  Usually only one instance of the time series database is required.
- The **api and web interface backend** `cc-backend`. Only one instance of
  `cc-backend` is required. This will provide the HTTP server at the desired
  monitoring URL for serving the web interface.
- A **SQL database**. It is recommended to use the builtin sqlite database for
  ClusterCockpit. You can setup [LiteStream](https://litestream.io/) as a service
  which performs a continuous replication of the sqlite database to multiple
  storage backends. Optionally `cc-backend` also supports MariaDB/MySQL as
  SQL database backends.
- A **batch job scheduler adapter** that provides the job meta information to
  `cc-backend`. This is done by using the provided REST api for starting and
  stopping jobs. For Slurm there is a Python based solution
  ([cc-slurm-sync](https://github.com/ClusterCockpit/cc-slurm-sync) )
  maintained by PC2 Paderborn is available. For HTCondor there also exists
  [cc-condor-sync](https://github.com/ClusterCockpit/cc-condor-sync).

## Server Hardware

`cc-backend` is threaded and therefore profits from multiple cores. It does not
require a lot of memory. It is possible to run it in a virtual machine. For best
performance the `./var` folder of `cc-backend` which contains the sqlite
database file and the file based job archive should be located on a fast storage
device, ideally a NVMe SSD. The sqlite database file and the job archive will
grow over time (if you are not removing old jobs using a retention policy).
Our setup covering five clusters over 4 years take 50GB for the sqlite database
and around 700GB for the job archive.
`cc-metric-store` is also threaded and requires a fixed amount of main memory.
How much depends on your configuration, but 128GB should be enough for most
setups. We run `cc-backend` and `cc-metric-store` on the same server as
systemd services.

## Planning and initial configuration

We recommended the following order for planning and configuring a ClusterCockpit
installation:

1. **Setup your metric list**: With two exceptions you are in general free which metrics you
   want choose. Those exceptions are: `mem_bw` for main memory bandwidth and
   'flops_any' for flop throughput (double precision flops are upscaled to single
   precision rates). You can find a discussion of useful metrics and their naming
   [here]({{< ref prod-metric-list >}}). This metric list is an integral
   component for  the configuration of all ClusterCockpit components.
1. Configure and deploy `cc-metric-store`.
1. Configure and deploy `cc-metric-collector`. For a detailed description on how
   to setup cc-metric-collector have a look at
   {{< ref "prod-ccmc" >}}
1. Configure and deploy `cc-backend`
1. Setup batch job scheduler adapter

## Common problems

Up front here is a list with common issues people are facing when installing
ClusterCockpit for the first time.

### Inconsistent metric names across components

At the moment you need to configure the metric list in every component
separately. In `cc-metric-collector` the metrics that are send to the
`cc-metric-store` are determined by the collector configuration and possible
renaming in the router configuration. For `cc-metric-store` in `config.json` you
need to specify a metric list in-order to configure the native metric frequency
and how a metric is aggregated. Metrics that are send to `cc-metric-store` and
do not appear in its configuration are silently dropped!
In `cc-backend` for every cluster you need to create a `cluster.json`
configuration in the job-archive. There you setup which metrics are shown in the
web-frontend including many additional properties for the metrics. For running
jobs `cc-backend` will query `cc-metric-store` for exactly those metric names
and if there is no match there will be an error.

We provide a json schema based specification as part of the job meta and metric
schema. This specification recommends a minimal set of metrics and we suggest to
use the metric names provided there. While it is up to you if you want to adhere
to the metric names suggested in the schema, there are two exceptions: `mem_bw`
(main memory bandwidth) and `flops_any` (total flop rate with DP flops scaled to
SP flops) are required for the roofline plots to work.

### Inconsistent device naming between `cc-metric-collector` and batch job scheduler adapter

The batch job scheduler adapter (e.g. `cc-slurm-sync`) provides a list of
resources that are used by the job. `cc-backend` will query `cc-metric-store`
with exactly those resource ids for getting all metrics for a job.
As a consequence if `cc-metric-collector` uses another systematic the metrics
will not be found.

If you have GPU accelerators `cc-slurm-sync` should use the PCI-E device
addresses as ids. The option `use_pci_info_as_type_id` for the nvidia and
rocm-smi collectors in the collector configuration must be set to true.
To validate and debug problems you can use the `cc-metric-store` debug endpoint:

```bash
curl -H "Authorization: Bearer $JWT" -D - "http://localhost:8080/api/debug"
```

This will return the current state of `cc-metric-store`. You can search for a
hostname and there scroll for all topology leaf nodes that are available.

### Missing nodes in subcluster node lists

ClusterCockpit supports multiple subclusters as part of a cluster. A subcluster
in this context is a homogeneous hardware partition with a dedicated metric
and device configuration. `cc-backend` dynamically matches the nodes a job runs
on to subcluster node list to figure out on which subcluster a job is running.
If nodes are missing in a subcluster node list this fails and the metric list
used may be wrong.
