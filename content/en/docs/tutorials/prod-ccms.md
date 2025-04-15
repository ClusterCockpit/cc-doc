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

The most important configuration option is the `retention-in-memory` setting. It
specifies for which duration back in time metrics should be provided. This
should be long enough to cover common job durations plus a safety margin. This
option also influences the main memory footprint. `cc-metric-store` will accept
any scope for any cluster for all configured metrics. The memory footprint scales
with the number of nodes, the number of native metric scopes (cores, sockets),
the number of metrics, and the memory retention time divided by the frequency.

The `cc-metric-store` supports checkpoints and archiving. Currently checkpoints
and archives are in JSON format. Checkpoints are always performed on shutdown.
To not loose data on a crash or other failure checkpoints are written regularly
in fixed intervals. The restore option indicates which duration should be loaded
into memory on startup. Usually this should match the `retention-in-memory`
setting. Checkpoints that are not needed anymore are moved and compressed to an
archive directory in regular intervals. This keeps the raw metric data. There is
currently no support for reading or processing this data. Also we are
considering to replace the current JSON format by a binary file format (e.g.
Apache Arrow). You may want to setup a cron job to delete older archive files.

Finally the `http-api` section specifies the address and port on which the
server should listen. Optionally, for HTTPS paths to TLS cert and key files can
be specified. The REST API uses JWT token based authentication. The option
`jwt-public-key` provides the public key to check the signed JWT token.

## Authentication

For authentication signed (but unencrypted) JWT tokens are used. Only
Ed25519/EdDSA cryptographic key-pairs are supported. A client has to sign the
token with its private key, on the server side it is checked if the configured
public key matches the private key with which the token was signed, if the token
was altered after signing, and if the token has expired. All other token
attributes are ignored.

We provide an [article]({{< ref "docs/how-to-guides/generatejwt" >}})
on how to generate JWT.
The is also a background [info article]({{< ref "docs/explanation/jwtoken" >}})
on JWT usage in ClusterCockpit. Tokens are cached in cc-metric-store to minimize
overhead.

## NATS

As an alternative to HTTP REST `cc-metric-store` can also receive metrics via
NATS. You find more infos about NATS in this [background article]({{< ref "docs/explanation/nats/" >}}).

To enable NATS in `cc-metric-store` add the following section to the
configuration file:

``` json
{
  "nats": [
      {
          "address": "nats://localhost:4222",
          "creds-file-path": "test.creds",
          "subscriptions": [
              {
                  "subscribe-to": "ee-hpc-nats",
                  "cluster-tag": "fritz2"
              }
          ]
      }
  ],
}
```
