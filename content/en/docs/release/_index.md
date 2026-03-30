---
title: Release specific infos
description: Settings and issues specific to the current release
weight: 1
---

## `cc-backend` version 1.5.3

Supports job archive version 3 and database version 11.

## What you need to do when upgrading

### Upgrading from v1.5.2

No database migration is required. Start the new binary directly.

### Upgrading from v1.5.1

No database migration is required. Start the new binary directly.

### Upgrading from v1.5.0

A database migration to version 11 is required:

```bash
./cc-backend -migrate-db
```

For optimal database performance after the migration it is recommended to run:

```bash
./cc-backend -optimize-db
```

Depending on your database size (more than 40 GB) the `VACUUM` step may take up
to 2 hours. You can also run `ANALYZE` manually instead.

### Upgrading from before v1.5.0

- **Update `config.json`**: All configuration attributes were renamed to
  `kebab-case` in v1.5.0 (e.g., `apiAllowedIPs` → `api-allowed-ips`). See the
  [configuration reference]({{< ref "ccb-configuration" >}}) for the full list.
- **Remove the `clusters` section** from `config.json`. Cluster information is
  now derived from the job archive.
- **Migrate your job database** to version 11 (see [Database migration](/docs/how-to-guides/database-migration/)).
- **Migrate your job archive** to version 3 (see [Job Archive migration](/docs/how-to-guides/archive-migration/)).

## Changes in 1.5.3

### Bug fixes

- **WAL not rotated on partial checkpoint failure**: When binary checkpointing
  failed for some hosts, WAL files for successfully checkpointed hosts were not
  rotated and the checkpoint timestamp was not advanced. Partial successes now
  correctly advance the checkpoint and rotate WAL files for completed hosts.
- **Unbounded WAL file growth**: If binary checkpointing consistently failed for
  a host, its `current.wal` file grew without limit until disk exhaustion. A new
  `max-wal-size` configuration option (in the `checkpoints` block) allows setting
  a per-host WAL size cap in bytes. When exceeded, the WAL is force-rotated.
  Defaults to `0` (unlimited) for backward compatibility.
- **Range filter fixes**: Range filters now correctly handle zero as a boundary
  value. Improved validation and UI text for range selections.
- **Line protocol body parsing interrupted**: Switched from `ReadTimeout` to
  `ReadHeaderTimeout` so that long-running metric submissions are no longer cut
  off mid-stream.
- **Checkpoint archiving continues on error**: A single cluster's archiving
  failure no longer aborts the entire cleanup operation.
- **Removed metrics excluded from subcluster config**: Metrics removed from a
  subcluster are no longer returned by `GetMetricConfigSubCluster`.

### New features

- **`-cleanup-checkpoints` CLI flag**: Triggers checkpoint cleanup without
  starting the server, useful for maintenance windows or automated cleanup scripts.
- **`max-wal-size` config option**: New option in the `metric-store.checkpoints`
  block to cap per-host WAL file size in bytes and prevent unbounded disk growth.
- **Explicit node state queries in node view**: Node health and scheduler state
  are now fetched independently from metric data for fresher status information.
- **`binaryCheckpointReader` tool**: New utility (`tools/binaryCheckpointReader`)
  that reads `.wal` or `.bin` checkpoint files and dumps their contents to a
  human-readable `.txt` file. See [binaryCheckpointReader]({{< ref "binarycheckpointreader" >}}).

### MetricStore performance

- **WAL writer throughput**: Decoupled WAL file flushing from message processing
  using a periodic 5-second batch flush, significantly increasing metric
  ingestion throughput.
- **Improved shutdown time**: MetricStore and archiver now shut down concurrently.

## Changes in 1.5.2

### Bug fixes

- Fixed memory spikes when using the metricstore move (archive) policy with the
  Parquet writer.
- Fixed top list queries in analysis and dashboard views.
- Down nodes are now excluded from health checks.
- Fixed a blocking NATS receive call in the metricstore.

### Performance

- Bulk insert operations now use explicit transactions, reducing write contention
  on the SQLite database.
- The WAL consumer is now sharded for significantly higher write throughput.
- New `busy-timeout-ms` configuration option for the SQLite connection.
- Optimized stats queries.

### NATS API

- The NATS node state handler now performs the same metric health checks as the
  REST API handler.

## Changes in 1.5.1

### Database

- **New migration (version 11)**: Optimized database index count and added
  covering indexes for stats queries for significantly improved query performance.
- **`-optimize-db` flag**: New CLI flag to run `VACUUM` and `ANALYZE` on demand.
  Automatic `ANALYZE` on startup has been removed.
- **SQLite configuration hardening**: New configurable options via `db-config`
  section (see [configuration reference]({{< ref "ccb-configuration" >}})).

### Bug fixes

- Fixed crash when `enable-job-taggers` is set but tagger rule directories are missing.
- Fixed GT and LT conditions in ranged filters.
- Fixed wrong metricstore schema (missing comma).

## Breaking changes in v1.5.0

### Configuration

- **JSON attribute naming**: All JSON configuration attributes now use `kebab-case`
  style consistently (e.g., `api-allowed-ips` instead of `apiAllowedIPs`).
  Update your `config.json` accordingly.
- **Removed `disable-archive` option**: This obsolete configuration option has
  been removed.
- **Removed `clusters` config section**: Cluster information is now derived from
  the job archive.

### Architecture

- **MySQL/MariaDB support removed**: Only SQLite is now supported as the database
  backend.
- **Web framework replaced**: Migrated from `gorilla/mux` to `chi` as the HTTP
  router.
- **MetricStore moved**: The `metricstore` package has been moved from `internal/`
  to `pkg/`.
- **`minRunningFor` filter removed**: Replaced by a **Short jobs** quick-filter
  button in the job list.

## Major features in v1.5.0

- **NATS API Integration**: Subscribe to real-time job start/stop events and node
  state changes via NATS. NATS subjects are configurable via `api-subjects`.
- **Public Dashboard**: New public-facing dashboard at `/public`.
- **Enhanced Node Management**: Node state tracking table with configurable
  retention and archiving to Parquet format.
- **Health Monitoring**: New **Health** tab in the status details view showing
  per-node metric health. Supports querying external cc-metric-store health
  status via the API.
- **Web-based Log Viewer**: Inspect backend log output from the admin interface
  without shell access.
- **Job Tagging System**: Automatic detection of applications (MATLAB, GROMACS,
  etc.) and pathological jobs. Taggers can be triggered on-demand from the admin
  interface.
- **Parquet Archive Format**: Columnar storage with zstd compression. Full S3
  and SQLite blob backends also supported.
- **Unified Archive Retention**: Supports both JSON and Parquet as target formats.

## New configuration options in v1.5.0

GitHub Repository with [complete configuration examples](https://github.com/ClusterCockpit/cc-examples/tree/main/nhr%40fau).
All configuration options are checked against a JSON schema.

```json
{
  "main": {
    "enable-job-taggers": true,
    "resampling": {
      "minimum-points": 600,
      "trigger": 180,
      "resolutions": [240, 60]
    },
    "api-subjects": {
      "subject-job-event": "cc.job.event",
      "subject-node-state": "cc.node.state"
    },
    "nodestate-retention": {
      "policy": "move",
      "age": 720,
      "target-path": "./var/nodestate-archive"
    }
  },
  "nats": {
    "address": "nats://0.0.0.0:4222",
    "username": "root",
    "password": "root"
  },
  "cron": {
    "commit-job-worker": "1m",
    "duration-worker": "5m",
    "footprint-worker": "10m"
  },
  "metric-store": {
    "cleanup": {
      "mode": "archive",
      "directory": "./var/archive"
    }
  },
  "archive": {
    "retention": {
      "policy": "delete",
      "age": 180,
      "format": "parquet"
    }
  }
}
```

## Transfer `cc-metric-store` checkpoints

When migrating from a standalone external `cc-metric-store` to the metric store
integrated in `cc-backend`, you can transfer existing checkpoints using the
following script:

```bash
#!/bin/bash

# Set these to the checkpoint directories from your CCMS and CCB config.json
CCMS_CHECKPOINTS_DIR="/home/dummy/cc-metric-store/var/checkpoints"
CCB_CHECKPOINTS_DIR="/home/dummy/cc-backend/var/checkpoints"

if [ -d "$CCMS_CHECKPOINTS_DIR" ]; then
    if [ ! -d "$CCB_CHECKPOINTS_DIR" ]; then
        mkdir "$CCB_CHECKPOINTS_DIR"
    fi
    mv -f "$CCMS_CHECKPOINTS_DIR" "$CCB_CHECKPOINTS_DIR"
    echo "Success: checkpoints moved to $CCB_CHECKPOINTS_DIR"
else
    echo "Error: Directory '$CCMS_CHECKPOINTS_DIR' does not exist."
fi
```

## Known issues

- The dynamic memory management is not yet fully reliable across restarts.
  Buffers kept outside the retention period may be lost on restart.
- The web-based log viewer requires `cc-backend` to be started via systemd. The
  user running `cc-backend` must have permission to execute `journalctl`.
- Old user UI configuration persisted in the database is not used after an
  upgrade. It is recommended to configure the metrics shown via `ui-config` and
  clear the old records from the database after updating.
- Energy footprint metrics of type `energy` are currently ignored when
  calculating total energy.
- For energy footprint metrics of type `power`, the unit is ignored and the
  metric is assumed to be in Watts.
