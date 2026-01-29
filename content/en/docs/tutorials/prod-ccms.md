---
title: Setup of cc-metric-store
weight: 20
description: How to configure and deploy cc-metric-store
categories: [cc-metric-store]
tags: [Admin]
---

{{< alert title="Note" >}}The standalone cc-metric-store shares its core storage
engine with cc-backend. Its role is for distributed setups and redundancy.{{< /alert >}}

## Introduction

The `cc-metric-store` provides an in-memory metric time-series database. It is
configured via a JSON configuration file (`config.json`). Metrics are received
via messages using the ClusterCockpit [ccMessage protocol](https://github.com/ClusterCockpit/cc-specifications/tree/master/interfaces/lineprotocol).
It can receive messages via an HTTP REST API or by subscribing to a NATS subject.
Requesting data is possible via an HTTP REST API.

## Configuration

For a complete list of configuration options see
[here]({{< ref "docs/reference/cc-metric-store/ccms-configuration" >}}).
The configuration is organized into four main sections: `main`, `metrics`,
`nats`, and `metric-store`.

Minimal example of a configuration file:

```json
{
  "main": {
    "addr": "localhost:8080",
    "jwt-public-key": "kzfYrYy+TzpanWZHJ5qSdMj5uKUWgq74BWhQG6copP0="
  },
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
      "frequency": 60,
      "aggregation": null
    }
  },
  "metric-store": {
    "checkpoints": {
      "interval": "12h",
      "directory": "./var/checkpoints"
    },
    "memory-cap": 100,
    "retention-in-memory": "48h",
    "cleanup": {
      "mode": "archive",
      "interval": "48h",
      "directory": "./var/archive"
    }
  }
}
```

### Main Section

The `main` section specifies the address and port on which the server should
listen (`addr`). Optionally, for HTTPS, paths to TLS cert and key files can be
specified via `https-cert-file` and `https-key-file`. If using a privileged
port (e.g., 443), you can specify `user` and `group` to drop root permissions
after binding. The `backend-url` option allows connecting to cc-backend for
querying job information. The REST API uses JWT token based authentication.
The option `jwt-public-key` provides the Ed25519 public key to verify signed
JWT tokens.

### Metrics Section

The `cc-metric-store` will only accept metrics that are specified in its metric
list. The metric names must exactly match! The frequency for the metrics
specifies how incoming values are binned. If multiple values are received in the
same interval older values are overwritten, if no value is received in an
interval there is a gap. `cc-metric-store` can aggregate metrics across
topological entities, e.g., to compute an aggregate node scope value from core
scope metrics. The aggregation attribute specifies how the aggregate value is
computed. Resource metrics usually require `sum`, whereas diagnostic metrics
(e.g., `clock`) require `avg`. For `clock` a sum would obviously make no sense.
Metrics that are only available at node scope should set aggregation to `null`.

### Metric-Store Section

The most important configuration option is the `retention-in-memory` setting. It
specifies for which duration back in time metrics should be provided. This
should be long enough to cover common job durations plus a safety margin. The
`memory-cap` option sets the maximum memory percentage to use.
The memory footprint scales with the number of nodes, the number of native
metric scopes (cores, sockets), the number of metrics, and the memory retention
time divided by the frequency.

The `cc-metric-store` supports checkpoints and cleanup/archiving. Checkpoints
are always performed on shutdown. To not lose data on a crash or other failure,
checkpoints are written regularly in fixed intervals. Checkpoints that are not
needed anymore can either be archived (moved and compressed) or deleted,
controlled by the `cleanup.mode` setting (`archive` or `delete`). The cleanup
happens at the interval specified in `cleanup.interval`. You may want to set up
a cron job to delete older archive files.

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

To enable NATS in `cc-metric-store` add the `nats` section for the connection
and `nats-subscriptions` in the `metric-store` section:

```json
{
  "nats": {
    "address": "nats://localhost:4222",
    "username": "user",
    "password": "password"
  },
  "metric-store": {
    "nats-subscriptions": [
      {
        "subscribe-to": "hpc-nats",
        "cluster-tag": "fritz"
      }
    ]
  }
}
```

The `nats` section configures the NATS server connection with address and
credentials. The `nats-subscriptions` within `metric-store` define which
subjects to subscribe to and how to tag incoming metrics with cluster
information.
