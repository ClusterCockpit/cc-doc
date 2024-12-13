---
title: Installation manual
weight: 7
description: Detailed description on configuration and deployment of ClusterCockpit
categories: [ClusterCockpit]
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

1. Setup your metric list
1. Configure and deploy `cc-metric-store`.
1. Configure and deploy `cc-metric-collector`. For a detailed description on how
   to setup cc-metric-collector have a look at
   {{< ref "prod-cc-metric-collector" >}}
1. Configure and deploy `cc-backend`
1. Setup batch job scheduler adapter
