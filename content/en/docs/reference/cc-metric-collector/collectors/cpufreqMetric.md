---
title: cpufreq_cpuinfo collector
description: >
  Toplevel cpufreqMetric
categories: [cc-metric-collector]
tags: [cc-metric-collector, Collector, cpufreq]
weight: 2
---

## `cpufreq_cpuinfo` collector

```json
  "cpufreq": {
    "exclude_metrics": []
  }
```

The `cpufreq` collector reads the clock frequency from `/sys/devices/system/cpu/cpu*/cpufreq` and outputs a handful **hwthread** metrics.

Metrics:

* `cpufreq`
