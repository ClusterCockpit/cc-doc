---
title: Release specific infos
description: Settings and issues specific to the current release
weight: 1
---

## `cc-backend` version 1.5.4

Supports job archive version 3 and database version 11.

This is a security and bugfix release.

## What you need to do when upgrading

### Upgrading from v1.5.3

No database migration is required. Start the new binary directly.

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

## Changes in 1.5.4

### Security fixes

- **JWT HMAC empty-key bypass (critical)**: `jwtSession.go` now refuses to
  register when `CROSS_LOGIN_JWT_HS512_KEY` is unset. Previously, an empty HMAC
  key allowed unauthenticated admin token forgery.
- **SQL injection via metric names (critical)**: Metric names supplied through
  GraphQL were interpolated raw into `json_extract` SQL expressions. Names are
  now validated against `^[a-zA-Z0-9_]+$`.
- **Path traversal via line-protocol tags (critical)**: `cluster` and `host`
  tags from the metric line protocol flowed unvalidated into `path.Join` for
  checkpoint/WAL file paths, enabling arbitrary file writes. Path-traversal
  sequences are now rejected in `DecodeLine`.
- **CORS `AllowCredentials` disabled**: CORS middleware no longer sets
  `AllowCredentials: true`, which was incompatible with `AllowedOrigins: ["*"]`
  and could enable cross-origin credential theft.
- **HSTS header added**: `Strict-Transport-Security` is now set for all HTTPS
  connections.
- **Security response headers**: Added `X-Content-Type-Options: nosniff`,
  `X-Frame-Options: DENY`, `Referrer-Policy: same-origin`, and a conservative
  `Content-Security-Policy` to harden against clickjacking and base-tag injection.
- **Stored XSS in job message**: `job.metaData.message` is now rendered as
  escaped text instead of raw HTML in `Job.root` and `JobFootprint`.
- **SQL injection in tag queries**: The tag-scope `IN` list and manager project
  subquery in `CountTags` are now parameterized instead of interpolating values
  sourced from OIDC/LDAP.
- **GraphQL DoS hardening**: Query cost is bounded with `FixedComplexityLimit`
  (5000). Non-positive `items-per-page` and `page` values are rejected with HTTP
  400.
- **CSRF defense-in-depth**: State-changing requests with a cross-site
  `Sec-Fetch-Site` header are now rejected.
- **NATS API security warning**: A startup warning is now logged when NATS
  subscriptions are enabled, reminding operators that the NATS API has no
  application-layer authentication.

### Bug fixes

- **Roofline legend placement**: Roofline plot legends now use fixed coordinates
  instead of dynamic placement, preventing the legend from overlapping data
  points or being rendered off-canvas.
- **Subcluster usage tab labels**: Subcluster names in the status dashboard
  usage tabs are no longer force-capitalized; the original cluster-defined
  casing is preserved.
- **NodeListRow host filter**: The running-jobs query now filters by exact
  hostname (`eq`) instead of substring match (`contains`), avoiding incorrect
  matches when one hostname is a prefix of another.
- **WAL files not reset on shutdown**: On graceful shutdown the metricstore
  wrote a final binary snapshot but never rotated the per-host `current.wal`
  files. Stale WAL files were replayed and appended to on the next start,
  growing without bound. `Shutdown` now rotates WAL files for all successfully
  snapshotted hosts.

### Dependencies

- **Go module upgrades**: Refreshed Go module dependencies to their latest
  compatible versions.

## Changes in 1.5.3

### Bug fixes

- **OIDC role extraction**: Fixed role extraction from OIDC tokens where roles
  were not correctly parsed from the token claims. Roles are now always
  requested from the token regardless of other configuration.
- **OIDC user sync role changes**: `SyncUser` and `UpdateUser` callbacks now
  allow all role changes, removing a restriction that prevented role updates
  during OIDC-driven user synchronization.
- **OIDC projects array**: Projects array from the OIDC token is now submitted
  and applied when syncing user attributes.
- **WAL message drops during checkpoint**: WAL writes are now paused during
  binary checkpoint creation. Previously, disk I/O contention caused over
  1.4 million dropped messages per checkpoint cycle.
- **WAL rotation skipped for all nodes**: `RotateWALFiles` used a non-blocking
  send on a small channel. With thousands of nodes, the channel filled instantly
  and nearly all hosts were skipped. Replaced with a blocking send using a
  shared 2-minute deadline.
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
  value. Improved validation and UI text for "more than equal" and "less than
  equal" range selections.
- **Line protocol body parsing interrupted**: Switched from `ReadTimeout` to
  `ReadHeaderTimeout` so that long-running metric submissions are no longer cut
  off mid-stream.
- **Checkpoint archiving continues on error**: A single cluster's archiving
  failure no longer aborts the entire cleanup operation. Errors are collected
  and reported per cluster.
- **Parquet row group overflow**: Added periodic flush during checkpoint
  archiving to prevent exceeding the parquet-go 32k column-write limit.
- **Removed metrics excluded from subcluster config**: Metrics removed from a
  subcluster are no longer returned by `GetMetricConfigSubCluster`.
- **Log viewer auto-refresh**: Fixed the log viewer component not
  auto-refreshing correctly.
- **SameSite cookie setting**: Relaxed the SameSite cookie attribute to improve
  compatibility with OIDC redirect flows.

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
  using a periodic 5-second batch flush (up to 4096 messages per cycle),
  significantly increasing metric ingestion throughput.
- **Improved shutdown time**: HTTP shutdown timeout reduced; MetricStore and
  archiver now shut down concurrently. Overall shutdown deadline raised to
  60 seconds.

### Logging improvements

- **Reduced tagger log noise**: Missing metrics and expression evaluation errors
  in the job classification tagger are now logged at debug level instead of
  error level.

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
