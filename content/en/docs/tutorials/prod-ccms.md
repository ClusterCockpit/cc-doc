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
    "addr": "0.0.0.0:8082",
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
    "retention-in-memory": "48h",
    "memory-cap": 100,
    "checkpoints": {
      "file-format": "wal",
      "directory": "./var/checkpoints"
    },
    "cleanup": {
      "mode": "archive",
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
after binding. The `backend-url` option allows connecting to `cc-backend` for
querying job information. This is required to enable the dynamic memory
retention in `cc-metric-store`. The REST API uses JWT token based authentication.
The option `jwt-public-key` provides the ED25519 public key to verify signed
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
should be long enough to cover common job durations. The `memory-cap` option
sets the approximate maximum memory capacity in GB to use. The memory footprint
scales with the number of nodes, the number of native metric scopes (cores,
sockets), the number of metrics, and the memory retention time divided by the
frequency.

The `num-workers` option controls the number of parallel workers used for
checkpoint and archive I/O. Setting it to `0` (the default) enables automatic
setup, capped at 10.

The `cc-metric-store` supports checkpoints and cleanup/archiving. Checkpoints
are always performed on shutdown. To not lose data on a crash or other failure,
checkpoints are written at regular intervals configured via
`checkpoints.interval` (e.g. `"12h"`). The `checkpoints.file-format` option
selects the persistence format: `"json"` (human-readable) or `"wal"` (binary
Write-Ahead Log, crash-safe, default). See [Checkpoint
Formats](#checkpoint-formats) below. Checkpoints that are not needed anymore can
either be archived or deleted, controlled by the `cleanup.mode` setting
(`archive` or `delete`). The cleanup runs at the interval specified in
`cleanup.interval`.

## Checkpoint Formats

The `checkpoints.file-format` field controls how in-memory data is persisted to
disk.

**`"json"`** — Human-readable JSON snapshots written
periodically. Each snapshot is stored as
`<dir>/<cluster>/<host>/<timestamp>.json`. Easy to inspect and recover manually,
but larger on disk and slower to write.

**`"wal"` (recommended)** — Binary Write-Ahead Log format designed for crash
safety. Two file types are used per host:

- `current.wal` — append-only binary log; every incoming data point is appended
  immediately. Truncated trailing records from unclean shutdowns are silently
  skipped on restart.
- `<timestamp>.bin` — binary snapshot written at each checkpoint interval,
  containing the complete metric state. Written atomically via a `.tmp` rename.

On startup the most recent `.bin` snapshot is loaded, then remaining WAL entries
are replayed on top. The WAL is rotated after each successful snapshot. The
`"wal"` format will become the only supported option in a future release. If you
are migrating from an older installation using JSON checkpoints, switch to `"wal"`
after a clean restart.

## Parquet Archive

When `cleanup.mode` is `"archive"`, data that ages out of the in-memory
retention window is written to [Apache Parquet](https://parquet.apache.org/)
files before being freed, organized as:

```
<cleanup.directory>/
  <cluster>/
    <timestamp>.parquet
```

One Parquet file is produced per cluster per cleanup run, consolidating all
hosts. Files are compressed with Zstandard and sorted by cluster, hostname,
metric, and timestamp for efficient columnar reads.

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
information in case this is not already done.
