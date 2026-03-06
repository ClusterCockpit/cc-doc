---
title: Release specific infos
description: Settings and issues specific to the current release
weight: 1
---

## `cc-backend` version 1.5.0

Supports job archive version 3 and database version 10.

## Breaking changes

### Configuration changes

- **JSON attribute naming**: All JSON configuration attributes now use `kebab-case`
  style consistently (e.g., `api-allowed-ips` instead of `apiAllowedIPs`).
  Update your `config.json` accordingly.
- **Removed `disable-archive` option**: This obsolete configuration option has been removed.
- **Removed `clusters` config section**: The separate clusters configuration section
  has been removed. Cluster information is now derived from the job archive.
- **`apiAllowedIPs` is now optional**: If not specified, defaults to not restricted.

### Architecture changes

- **MySQL/MariaDB support removed**: Only SQLite is now supported as the database backend.
- **Web framework replaced**: Migrated from `gorilla/mux` to `chi` as the HTTP
  router. A proper 404 handler is now in place.
- **MetricStore moved**: The `metricstore` package has been moved from `internal/`
  to `pkg/` as it is now part of the public API.
- **`minRunningFor` filter removed**: This undocumented filter has been removed
  from the API and frontend. A new **Short jobs** quick-filter button replaces it.

## Major new features

- **NATS API Integration**: Subscribe to real-time job start/stop events and node
  state changes via NATS. NATS subjects are configurable via `api-subjects`.
- **Public Dashboard**: New public-facing dashboard route at `/public` for external users.
- **Enhanced Node Management**: New node state tracking table with timestamp
  tracking, filtering, and configurable retention/archiving to Parquet format.
- **Health Monitoring**: New dedicated **Health** tab in the status details view
  showing per-node metric health across the cluster. Supports querying external
  cc-metric-store (CCMS) health status via the API.
- **Web-based Log Viewer**: Inspect backend log output directly from the browser
  via the admin interface without requiring shell access.
- **Job Tagging System**: Automatic detection of applications (MATLAB, GROMACS,
  etc.) and pathological job classification. Taggers can be triggered on-demand
  from the admin web interface.
- **Parquet Archive Format**: New Parquet file format for job archiving with
  columnar storage and efficient zstd compression. Full S3 and SQLite blob
  backends are also supported.
- **Unified Archive Retention**: Job archive retention supports both JSON and
  Parquet as target formats under a single consistent policy configuration.

## What you need to do

- **Update `config.json`**: Rename all configuration attributes to `kebab-case`
  (e.g., `apiAllowedIPs` → `api-allowed-ips`). See the [configuration
  reference]({{< ref "ccb-configuration" >}}) for the full list of options.
- **Review cluster configuration**: Cluster information is now derived from the
  job archive. Remove the `clusters` section from `config.json` and ensure your
  `cluster.json` files in the job archive are up to date.
- **Migrate your job database** to version 10 (see [Database
  migration](/docs/how-to-guides/database-migration/)).
- **Migrate your job archive** to version 3 (see [Job Archive
  migration](/docs/how-to-guides/archive-migration/)).
- If using **NATS**, configure the new `nats` and `api-subjects` sections.
- If using **archive retention**, configure the `target-format` option to choose
  between `json` (default) and `parquet` output formats.
- Consider enabling **nodestate retention** if you track node states over time.

## Configuration changes

GitHub Repository with [complete configuration examples](https://github.com/ClusterCockpit/cc-examples/tree/main/nhr%40fau).
All configuration options are checked against a JSON schema.

### New configuration options

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
      "interval": "48h",
      "directory": "./var/archive"
    }
  },
  "archive": {
    "retention": {
      "policy": "delete",
      "age": "6months",
      "target-format": "parquet"
    }
  },
  "nodestate": {
    "retention": {
      "policy": "archive",
      "age": "30d",
      "archive-path": "./var/nodestate-archive"
    }
  }
}
```

## Transfer `cc-metric-store` checkpoints

We are currently offering the option to use the metric-store integrated in
cc-backend. Meaning both cc-backend and cc-metric-store share same configuration
as well as they run on the same server. The checkpoints in an internal
cc-metric-store reside in the `var` directory of cc-backend. If you choose to use
cc-metric-store-internal as your metric store, then you can do the following to
bring your old checkpoints from your previous external cc-metric-store
installation:

Look out for "checkpoints" key in your CCMS and CCB config.json.

```json
"checkpoints": {
  "directory": "./var/checkpoints",
  "restore": "48h"
},
```

Either you can move the checkpoints manually or you can use this script for
moving the checkpoints.

```bash
#!/bin/bash

# The path to your "directory" configured in CCMS and CCB config.json
# replace the path as shown with the dummy paths.
CCMS_CHECKPOINTS_DIR="/home/dummy/cc-metric-store/var/checkpoints"
CCB_CHECKPOINTS_DIR="/home/dummy/cc-backend/var/checkpoints"

# Check if the source directory actually exists
if [ -d "$CCMS_DIR" ]; then
    if [ ! -d "$CCB_CHECKPOINTS_DIR" ]; then
        mkdir "$CCB_CHECKPOINTS_DIR"
    fi

    mv -f $CCMS_CHECKPOINTS_DIR $CCB_CHECKPOINTS_DIR
    echo "Success: 'checkpoints' moved from $CCMS_CHECKPOINTS_DIR to $CCB_DIR"
else
    echo "Error: Directory '$CCMS_CHECKPOINTS_DIR' does not exist."
fi
```

## Known issues

- The new dynamic memory management is not bullet proof yet across restarts. We
  will fix that in a subsequent patch release.
- Currently energy footprint metrics of type energy are ignored for calculating
  total energy.
- With energy footprint metrics of type power the unit is ignored and it is
  assumed the metric has the unit Watt.
