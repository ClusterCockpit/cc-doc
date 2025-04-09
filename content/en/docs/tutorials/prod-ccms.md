---
title: Setup of cc-metric-store
weight: 20
description: How to configure and deploy cc-metric-store
categories: [cc-metric-store]
tags: [Admin]
---

## Introduction

The `cc-metric-store` provides an in-memory metric timeseries cache. It is
configured via a JSON configuration file (`config.json`). Metrics are received
via messages using the ClusterCockpit [ccMessage protocol](https://github.com/ClusterCockpit/cc-specifications/tree/master/interfaces/lineprotocol).
It can receive messages via a HTTP REST api or by subscribing to a NATS subject.
Requesting  data is at the moment only possible via a HTTP REST api.

## Configuration

For a complete list of configuration options see
[here]({{< ref "docs/reference/cc-metric-store/ccms-configuration" >}}).
Minimal example of a configuration file:

``` json
{
  "metrics": {
    "clock": {
      "frequency": 60,
      "aggregation": "avg"
    },
    "mem_bw": {
      "frequency": 60,
      "aggregation": "sum"
    },
    "flops_any": {
      "frequency": 60,
      "aggregation": "sum"
    },
    "flops_dp": {
      "frequency": 60,
      "aggregation": "sum"
    },
    "flops_sp": {
      "frequency": 60,
      "aggregation": "sum"
    },
    "mem_used": {
      "frequency": 60
    },
  },
  "checkpoints": {
    "interval": "12h",
    "directory": "./var/checkpoints",
    "restore": "48h"
  },
  "archive": {
    "interval": "50h",
    "directory": "./var/archive"
  },
  "http-api": {
    "address": "localhost:8082"
  },
  "retention-in-memory": "48h",
  "jwt-public-key": "kzfYrYy+TzpanWZHJ5qSdMj5uKUWgq74BWhQG6copP0="
}
```

The `cc-metric-store` will only accept metrics that are specified in its metric
list. The metric names must exactly match! The frequency for the metrics
specifies how incoming values are binned. If multiple values are received in the
same interval older values are overwritten, if no value is received in an
interval there is a gap. `cc-metric-store` can aggregate metrics across
topological entities, e.g., to compute an aggregate node scope value from core
scope metrics. The aggregation attribute specifies how the aggregate value is
computed. Resource metrics usually require `sum`, whereas diagnostic metrics
(e.g., `clock`) require `avg`. For `clock` a sum would obviously make no sense.
Metrics that are only available at node scope can omit the aggregation
attribute.
