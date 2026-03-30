---
title: Setup of cc-metric-store
weight: 20
description: How to configure and deploy cc-metric-store
categories: [cc-metric-store]
tags: [Admin]
---

## Introduction

`cc-backend` integrates an in-memory metric store that is always available. A
standalone `cc-metric-store` process can additionally be deployed for distributed
setups, redundancy, or dedicated hardware (see
[Introduction]({{< ref "prod-intro" >}}) for a discussion of the trade-offs).

Both share the same storage engine and the same `metric-store` configuration
keys. Metrics are received via messages using the ClusterCockpit
[ccMessage protocol](https://github.com/ClusterCockpit/cc-specifications/tree/master/interfaces/lineprotocol)
either via an HTTP REST API or by subscribing to a NATS subject.

## Common Metric Store Configuration

The core storage engine is configured identically for both the built-in store in
`cc-backend` and the standalone `cc-metric-store`. In `cc-backend` this block
appears as `"metric-store"` inside `config.json`. In the standalone service it
also lives under `"metric-store"` in its own `config.json`.

### Minimum Configuration

Only two keys are required:

```json
{
  "metric-store": {
    "retention-in-memory": "48h",
    "memory-cap": 100
  }
}
```

With this minimal configuration the following defaults apply:

- Checkpoints use the WAL format stored in `./var/checkpoints`
- Old data is **deleted** when it ages out of the retention window
- Worker count is determined automatically

### Memory and Retention

`retention-in-memory` is a Go duration string (e.g., `"48h"`, `"168h"`)
specifying how far back metrics are kept in RAM. Choose a value long enough to
cover the expected duration of typical jobs on your system. Memory footprint
scales with the number of nodes, the number of metrics and their native scopes
(cores, sockets, …), and `retention-in-memory` divided by the metric frequency.

`memory-cap` sets the approximate upper limit in GB on the memory used for
metric buffers. When this limit is exceeded, buffers belonging to nodes that are
not referenced by any active job are freed first. Setting it to `0` disables the
cap.

### Checkpointing

Metrics are persisted to disk as checkpoints so that in-memory data survives
restarts. Checkpoints are always written on a clean shutdown and additionally at
a configurable interval during normal operation.

```json
{
  "metric-store": {
    "retention-in-memory": "48h",
    "memory-cap": 100,
    "checkpoints": {
      "file-format": "wal",
      "directory": "./var/checkpoints"
    }
  }
}
```

`file-format` selects the persistence format:

- `"wal"` **(default, recommended)** — binary snapshot plus a Write-Ahead Log;
  crash-safe.
- `"json"` — human-readable periodic snapshots; easier to inspect and recover
  manually, but larger on disk and slower to write.

`directory` sets the path where checkpoint files are written (default:
`./var/checkpoints`).

`max-wal-size` (optional integer, bytes) limits the size of a single host's WAL
file. When exceeded the WAL is force-rotated to prevent unbounded disk growth.
`0` means unlimited (default). Only relevant for `"wal"` format.

`checkpoint-interval` (optional, Go duration string, e.g., `"12h"`) controls
how often periodic checkpoints are written. The default is `"12h"`. The interval
is also derived from `retention-in-memory` when not set explicitly.

See [Checkpoint Formats](#checkpoint-formats) below for a detailed description
of both formats.

### Data Cleanup

Data that ages out of the in-memory retention window can either be discarded or
moved to a long-term Parquet archive:

```json
{
  "metric-store": {
    "retention-in-memory": "48h",
    "memory-cap": 100,
    "cleanup": {
      "mode": "archive",
      "directory": "./var/archive"
    }
  }
}
```

`mode` accepts:

- `"delete"` **(default)** — old data is discarded.
- `"archive"` — old data is written as Parquet files under `directory` before
  being freed. `directory` is required when `mode` is `"archive"`.

The cleanup runs at the same interval as `retention-in-memory`. See
[Parquet Archive](#parquet-archive) below for details on the file layout.

### Performance Tuning

`num-workers` (optional integer) controls the number of parallel workers used
for checkpoint and archive I/O. The default of `0` enables automatic sizing:
`min(NumCPU/2+1, 10)`. Increase this on I/O-heavy hosts with many cores.

### NATS Metric Ingestion

As an alternative to the HTTP REST ingest endpoint, the metric store can receive
metrics via NATS. This requires a top-level `nats` section (see below for the
standalone service, or the `nats` section in `cc-backend`'s `config.json` for
the built-in store).

Add `nats-subscriptions` inside `metric-store` to enable NATS ingestion:

```json
{
  "metric-store": {
    "retention-in-memory": "48h",
    "memory-cap": 100,
    "nats-subscriptions": [
      {
        "subscribe-to": "hpc-nats",
        "cluster-tag": "fritz"
      }
    ]
  }
}
```

Each entry specifies:

- `subscribe-to` (required) — the NATS subject to subscribe to.
- `cluster-tag` (optional) — a default cluster name applied to incoming messages
  that do not carry a cluster tag.

## External cc-metric-store

The standalone `cc-metric-store` process requires the common `metric-store`
block described above plus two additional top-level sections: `main` (HTTP
server) and `metrics` (accepted metric list). The optional `nats` section
enables NATS server connectivity.

### Main Section

```json
{
  "main": {
    "addr": "0.0.0.0:8082",
    "jwt-public-key": "kzfYrYy+TzpanWZHJ5qSdMj5uKUWgq74BWhQG6copP0="
  }
}
```

Required fields:

- `addr` — address and port to listen on.
- `jwt-public-key` — Base64-encoded Ed25519 public key for verifying JWT tokens
  on the REST API.

Optional fields:

- `https-cert-file` / `https-key-file` — enable HTTPS; both must be set.
- `user` / `group` — drop root permissions to this user/group after binding a
  privileged port.
- `backend-url` — URL of `cc-backend` (e.g., `https://localhost:8080`);
  enables dynamic memory retention by querying active job information.

See [Authentication](#authentication) below for details on JWT usage.

### Metrics Section

The standalone service requires an explicit list of accepted metrics. In
`cc-backend` this list is derived automatically from the cluster configurations,
but the external service needs it declared.

Only metrics listed here are accepted; all others are silently dropped. The
`frequency` (seconds) controls the binning interval — if multiple values arrive
within the same interval the most recent one wins; if no value arrives there is
a gap. The `aggregation` field specifies how values are combined when
synthesising a coarser-scope value from finer-scope measurements (e.g., core →
socket → node):

- `"sum"` — resource metrics whose values add up (bandwidth, flops, power).
- `"avg"` — diagnostic metrics that should be averaged (clock frequency,
  temperature).
- `null` — metric is only available at node scope; no cross-scope aggregation.

```json
{
  "metrics": {
    "clock":     { "frequency": 60, "aggregation": "avg" },
    "mem_bw":    { "frequency": 60, "aggregation": "sum" },
    "flops_any": { "frequency": 60, "aggregation": "sum" },
    "flops_dp":  { "frequency": 60, "aggregation": "sum" },
    "flops_sp":  { "frequency": 60, "aggregation": "sum" },
    "mem_used":  { "frequency": 60, "aggregation": null  }
  }
}
```

### Complete Minimal Example

Combining all required sections for the standalone cc-metric-store:

```json
{
  "main": {
    "addr": "0.0.0.0:8082",
    "jwt-public-key": "kzfYrYy+TzpanWZHJ5qSdMj5uKUWgq74BWhQG6copP0="
  },
  "metrics": {
    "clock":     { "frequency": 60, "aggregation": "avg"  },
    "mem_bw":    { "frequency": 60, "aggregation": "sum"  },
    "flops_any": { "frequency": 60, "aggregation": "sum"  },
    "flops_dp":  { "frequency": 60, "aggregation": "sum"  },
    "flops_sp":  { "frequency": 60, "aggregation": "sum"  },
    "mem_used":  { "frequency": 60, "aggregation": null   }
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

### NATS Server Connection

To receive metrics via NATS, add a top-level `nats` section with the server
coordinates alongside `nats-subscriptions` inside `metric-store`:

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

The `nats` section configures the NATS server connection:

- `address` (required) — URL of the NATS server.
- `username` / `password` (optional) — credentials for authentication.

You can find background information on NATS in this
[article]({{< ref "docs/explanation/nats/" >}}).

For a complete list of configuration options see the
[reference]({{< ref "docs/reference/cc-metric-store/ccms-configuration" >}}).

## Checkpoint Formats

The `checkpoints.file-format` field controls how in-memory data is persisted to
disk.

**`"json"`** — Human-readable JSON snapshots written periodically. Each snapshot
is stored as `<dir>/<cluster>/<host>/<timestamp>.json`. Easy to inspect and
recover manually, but larger on disk and slower to write.

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

For authentication, signed (but unencrypted) JWT tokens are used. Only
Ed25519/EdDSA cryptographic key-pairs are supported. A client has to sign the
token with its private key; the server verifies that the configured public key
matches the signing key, that the token was not altered after signing, and that
the token has not expired. All other token attributes are ignored. Tokens are
cached in cc-metric-store to minimise overhead.

We provide an [article]({{< ref "docs/how-to-guides/generatejwt" >}}) on how to
generate JWT tokens and a background
[article]({{< ref "docs/explanation/jwtoken" >}}) on JWT usage in
ClusterCockpit.
