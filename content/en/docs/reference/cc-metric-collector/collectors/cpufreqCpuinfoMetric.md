---
title: cpufreq_cpuinfo collector
description: >
  Toplevel cpufreqCpuinfoMetric
categories: [cc-metric-collector]
tags: [cc-metric-collector, Collector, cpufreqCpuinfo]
weight: 2
---

## `cpufreq_cpuinfo` collector

```json
  "cpufreq_cpuinfo": {}
```

The `cpufreq_cpuinfo` collector reads the clock frequency from `/proc/cpuinfo` and outputs a handful **hwthread** metrics.

Metrics:

* `cpufreq`
