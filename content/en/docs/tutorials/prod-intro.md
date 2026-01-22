---
title: ClusterCockpit installation manual
weight: 10
description: How to plan and configure a ClusterCockpit installation
categories: [ClusterCockpit]
tags: [Admin]
---

## Introduction

ClusterCockpit requires the following components:

- A **node agent** running on all compute nodes that measures required metrics and
  forwards all data to a time series metrics database. ClusterCockpit provides
  its own node agent `cc-metric-collector`. This is the recommended setup, but ClusterCockpit
  can also be integrated with other node agents, e.g. `collectd`, `prometheus` or
  `telegraf`. In this case you have to use it with the accompanying time series
  database and ensure the metric data is send or forwarded to `cc-backend`.
- The **api and web interface backend** `cc-backend`. Only one instance of
  `cc-backend` is required. This will provide the HTTP server at the desired
  monitoring URL for serving the web interface. It also integrates a in-memory
  metric store.
- A **SQL database**. The only supported option is to use the builtin sqlite
  database for ClusterCockpit. You can setup [LiteStream](https://litestream.io/)
  as a service which performs a continuous replication of the sqlite database to
  multiple storage backends.
- (Optional) **NATS message broker**: Apart from REST APIs ClusterCockpit also
  supports NATS as a way to connect components. Using NATS brings a number of
  advantages:
  - More flexible deployment and testing. Instances can have different URLs or
    IP addresses. Test instances are easy to deploy in parallel without a need to
    touch the configuration.
  - NATS comes with a builtin sophisticated [token key
    management](https://docs.nats.io/running-a-nats-service/configuration/securing_nats/auth_intro).
    This also enables to restrict authorization to specific subjects.
  - NATS may provide a larger message throughput compared to REST over HTTP.
  - Upcoming ClusterCockpit components as the Energy Manager require NATS.
- A **batch job scheduler adapter** that provides the job meta information to
  `cc-backend`. This is done by using the provided REST or NATS API for starting
  and stopping jobs. Currently available adapters:
  - Slurm: Golang based solution
    ([cc-slurm-adapter](https://github.com/ClusterCockpit/cc-slurm-adapter)) maintained
    by NHR@FAU. This is the recommended option in case you use Slurm. All
    options in `cc-backend` are supported.
  - Slurm: Python based solution
    ([cc-slurm-sync](https://github.com/ClusterCockpit/cc-slurm-sync)) maintained
    by PC2 Paderborn
  - HTCondor: [cc-condor-sync](https://github.com/ClusterCockpit/cc-condor-sync)
    maintained by Saarland University

## Server Hardware

`cc-backend` is threaded and therefore profits from multiple cores.
Enough memory is required to hold the metric data cache. For most setups 128GB
should be enough. You can set an upper limit for the memory capacity used b ythe
internal metric in-memory cache.
It is possible to run it in a virtual machine. For best
performance the `./var` folder of `cc-backend` which contains the sqlite
database file and the file based job archive should be located on a fast storage
device, ideally a NVMe SSD. The sqlite database file and the job archive will
grow over time (if you are not removing old jobs using a retention policy).
Our setup covering multiple clusters over 5 years takes 75GB for the sqlite database
and around 1.4TB for the job archive. In case you have very high job counts, we
recommend to use a retention policy to keep the database and the job archive at
a manageable size. In case you archive old jobs the database can be easily
restored using cc-backend.
We run `cc-backend` as systemd services.

## Planning and initial configuration

We recommended the following order for planning and configuring a ClusterCockpit
installation:

1. [Setup your metric list]({{< ref prod-metric-list >}}): With two exceptions
   you are in general free which metrics you want choose. Those exceptions are:
   `mem_bw` for main memory bandwidth and `flops_any` for flop throughput (double
   precision flops are upscaled to single precision rates). The metric list is an
   integral component for the configuration of all ClusterCockpit components.
1. [Planning of deployment]({{< ref prod-deploy >}})
1. [Configure and deploy]({{< ref prod-ccmc >}}) `cc-metric-collector`
1. [Configure and deploy]({{< ref prod-cc-backend >}}) `cc-backend`
1. [Configure and deploy](/docs/reference/cc-slurm-adapter/) `cc-slurm-adapter` or
   another job scheduler adapter of your choice

You can find complete example production configurations in the
[cc-examples](https://github.com/ClusterCockpit/cc-examples) repository.

## Common problems

Up front here is a list with common issues people are facing when installing
ClusterCockpit for the first time.

### Inconsistent metric names across components

At the moment you need to configure the metric list in every component
separately. In `cc-metric-collector` the metrics that are send to the
`cc-backend` are determined by the collector configuration and possible
renaming in the router configuration.
In `cc-backend` for every cluster you need to create a `cluster.json`
configuration in the job-archive. There you setup which metrics are shown in the
web-frontend including many additional properties for the metrics. For running
jobs `cc-backend` will query the internal `metric-store` for exactly those
metric names and if there is no match there will be an error.

We provide a JSON schema based specification as part of the job meta and metric
schema. This specification recommends a minimal set of metrics and we suggest to
use the metric names provided there. While it is up to you if you want to adhere
to the metric names suggested in the schema, there are two exceptions: `mem_bw`
(main memory bandwidth) and `flops_any` (total flop rate with DP flops scaled to
SP flops) are required for the roofline plots to work.

### Inconsistent device naming between `cc-metric-collector` and batch job scheduler adapter

The batch job scheduler adapter (e.g. `cc-slurm-adapter`) provides a list of
resources that are used by the job. `cc-backend` will query the internal `metric-store`
with exactly those resource ids for getting all metrics for a job.
As a consequence if `cc-metric-collector` uses another systematic the metrics
will not be found.

If you have GPU accelerators `cc-slurm-adapter` should use the PCI-E device
addresses as ids. The option `gpuPciAddrs` for the nvidia and
rocm-smi collectors in the collector configuration must be configured.
To validate and debug problems you can use the `cc-backend` debug endpoint:

```bash
curl -H "Authorization: Bearer $JWT" -D - "http://localhost:8080/api/debug"
```

This will return the current state of `cc-metric-store`. You can search for a
hostname and scroll there for all topology leaf nodes that are available.

### Missing nodes in subcluster node lists

ClusterCockpit supports multiple subclusters as part of a cluster. A subcluster
in this context is a homogeneous hardware partition with a dedicated metric
and device configuration. `cc-backend` dynamically matches the nodes a job runs
on to a subcluster node list to figure out on which subcluster a job is running.
If nodes are missing in a subcluster node list this fails and the metric list
used may be wrong.
