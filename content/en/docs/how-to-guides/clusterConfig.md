---
title: How to create a `cluster.json` file
description: >
  How to initially create a cluster configuration
categories: [cc-backend]
tags: [Admin]
---
## Overview

Every cluster is configured using a dedicated `cluster.json` file, that is part of
the job archive. You can find the JSON schema for it
[here](https://github.com/ClusterCockpit/cc-backend/blob/master/pkg/schema/schemas/cluster.schema.json).
This file provides information about the homogeneous hardware
partitions within the cluster including the node topology and the metric list.
A real production configuration is provided as part of
[cc-examples](https://github.com/ClusterCockpit/cc-examples/tree/main/nhr%40fau/job-archive).

## Structure

There are the following main parts:

- `name`: The name of the cluster
- `metricConfig`: The metric list configuration
- `subClusters`: Homogeneous hardware partitions in the cluster

## The metric configuration

There is one metric list per cluster. You can find a list of recommended metrics
and their naming [here]({{< ref "/docs/tutorials/prod-metric-list" >}}).
