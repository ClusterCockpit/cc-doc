---
title: schedstat collector
description: >
  Toplevel schedstatMetric
categories: [cc-metric-collector]
tags: [cc-metric-collector, Collector, schedstat]
weight: 2
---


## `schedstat` collector
```json
  "schedstat": {
  }
```

The `schedstat` collector reads data from /proc/schedstat and calculates a load value, separated by hwthread. This might be useful to detect bad cpu pinning on shared nodes etc. 

Metric:
* `cpu_load_core`