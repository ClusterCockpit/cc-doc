---
title: Application Config Schema
description: ClusterCockpit Application Config Schema Reference
categories: [cc-backend]
tags: [Backend]
weight: 1
---

A detailed description of each configuration option can be found in the
[configuration reference]({{< ref "ccb-configuration" >}} "CC-Backend Configuration").

The configuration is split into sections. Each section is validated against its
own JSON schema defined in the corresponding Go package inside the
[cc-backend repository](https://github.com/ClusterCockpit/cc-backend).

{{< alert title="Manual Updates">}}
Changes to the original JSON schemas found in the repository are not
automatically rendered in this reference documentation.</br></br>
**Last Update:** 15.06.2026
{{< /alert >}}

## Section `main`

*Source: `internal/config/schema.go`*

| Property | Type | Required | Description |
| -------- | ---- | -------- | ----------- |
| `addr` | string | No | Address where the HTTP(S) server listens (e.g. `"0.0.0.0:8080"`). Default: `localhost:8080`. |
| `api-allowed-ips` | array of string | No | IPv4 addresses from which secured API endpoints can be reached. Default: no restriction. |
| `user` | string | No | Drop root permissions after port is taken. Only useful for privileged ports. |
| `group` | string | No | Drop root permissions after port is taken. Only useful for privileged ports. |
| `disable-authentication` | boolean | No | Disable authentication for API and Web-UI. Default: `false`. |
| `embed-static-files` | boolean | No | Serve static files from within the binary. Default: `true`. |
| `static-files` | string | No | Path to static assets when `embed-static-files` is `false`. |
| `db` | string | No | Path to the SQLite database file. Default: `./var/job.db`. |
| `enable-job-taggers` | boolean | No | Enable automatic application and job-class taggers. Default: `false`. |
| `validate` | boolean | No | Validate all input JSON documents against JSON schemas. Default: `false`. |
| `session-max-age` | string | No | Maximum session lifetime as a `time.ParseDuration` string. Empty = never expires. Default: `168h`. |
| `https-cert-file` | string | No | Path to TLS certificate file. HTTPS is enabled when both cert and key are set. |
| `https-key-file` | string | No | Path to TLS key file. HTTPS is enabled when both cert and key are set. |
| `redirect-http-to` | string | No | Redirect port-80 requests to this URL when `addr` does not end in `:80`. |
| `stop-jobs-exceeding-walltime` | integer | No | Automatically stop jobs running more than this many seconds past their walltime. `0` = disabled. |
| `short-running-jobs-duration` | integer | No | Hide running jobs shorter than this many seconds. Default: `300`. |
| `emission-constant` | integer | No | CO₂ emission factor in g/kWh. When set, the UI shows estimated CO₂ per job. |
| `machine-state-dir` | string | No | Directory for MachineState files (persists machine state across restarts). |
| `systemd-unit` | string | No | Systemd unit name for the log viewer integration. Default: `clustercockpit`. |
| `resampling` | object | No | Enable dynamic downsampling of metric time-series. See sub-properties below. |
| `api-subjects` | object | No | NATS subjects for job/node events. Disables REST start/stop endpoints when set. See sub-properties below. |
| `nodestate-retention` | object | No | Automatic cleanup of old node-state rows. See sub-properties below. |
| `db-config` | object | No | SQLite tuning options. See sub-properties below. |

### `resampling`

| Property | Type | Required | Description |
| -------- | ---- | -------- | ----------- |
| `minimum-points` | integer | No | Minimum data points required to trigger resampling. |
| `trigger` | integer | **Yes** | Trigger next zoom level when visible points fall below this value. |
| `resolutions` | array of integer | **Yes** | Resampling target resolutions in seconds (e.g. `[600, 300, 60]`). |

### `api-subjects`

| Property | Type | Required | Description |
| -------- | ---- | -------- | ----------- |
| `subject-job-event` | string | **Yes** | NATS subject for job events (`start_job`, `stop_job`). |
| `subject-node-state` | string | **Yes** | NATS subject for node state updates. |
| `job-concurrency` | integer | No | Concurrent goroutines for job event processing. Default: `8`. |
| `node-concurrency` | integer | No | Concurrent goroutines for node state processing. Default: `2`. |

### `nodestate-retention`

| Property | Type | Required | Description |
| -------- | ---- | -------- | ----------- |
| `policy` | string | **Yes** | `delete` — remove old rows; `move` — archive to Parquet then delete. |
| `age` | integer | No | Retention age in hours. Rows older than this are affected. Default: `24`. |
| `target-kind` | string | No | Target storage for `move`: `file` or `s3`. Default: `file`. |
| `target-path` | string | No | Filesystem path for Parquet files (`target-kind: file`). |
| `target-endpoint` | string | No | S3 endpoint URL (`target-kind: s3`). |
| `target-bucket` | string | No | S3 bucket name (`target-kind: s3`). |
| `target-access-key` | string | No | S3 access key (`target-kind: s3`). |
| `target-secret-key` | string | No | S3 secret key (`target-kind: s3`). |
| `target-region` | string | No | S3 region (`target-kind: s3`). |
| `target-use-path-style` | boolean | No | Use path-style S3 URLs — required for MinIO (`target-kind: s3`). |
| `max-file-size-mb` | integer | No | Maximum Parquet file size in MB before splitting. Default: `128`. |

### `db-config`

| Property | Type | Required | Description |
| -------- | ---- | -------- | ----------- |
| `cache-size-mb` | integer | No | SQLite page cache size per connection in MB. Default: `2048`. |
| `soft-heap-limit-mb` | integer | No | Process-wide SQLite soft heap limit in MB. Default: `16384`. |
| `max-open-connections` | integer | No | Maximum open database connections. Default: `4`. |
| `max-idle-connections` | integer | No | Maximum idle database connections. Default: `4`. |
| `max-idle-time-minutes` | integer | No | Maximum idle time per connection in minutes. Default: `10`. |
| `busy-timeout-ms` | integer | No | SQLite busy timeout in ms. SQLite retries on contention for this duration before returning `SQLITE_BUSY`. Default: `60000`. |

---

## Section `auth`

*Source: `internal/auth/schema.go`*

### `auth.jwts`

| Property | Type | Required | Description |
| -------- | ---- | -------- | ----------- |
| `max-age` | string | **Yes** | Token validity as a `time.ParseDuration` string. |
| `cookie-name` | string | No | Cookie name to check for a JWT token. |
| `validate-user` | boolean | No | Deny login for users not in the database; overwrite JWT roles with DB roles. |
| `trusted-issuer` | string | No | Accept JWTs from this external issuer. |
| `sync-user-on-login` | boolean | No | Add unknown users to the DB on login using JWT claims. |
| `update-user-on-login` | boolean | No | Update existing user in DB on login with JWT claims (name, roles, projects). |

### `auth.ldap`

| Property | Type | Required | Description |
| -------- | ---- | -------- | ----------- |
| `url` | string | **Yes** | LDAP directory server URL. |
| `user-base` | string | **Yes** | Base DN of the user tree root. |
| `search-dn` | string | **Yes** | DN for LDAP admin account with read rights. |
| `user-bind` | string | **Yes** | LDAP bind expression. Must contain `uid={username}`. |
| `user-filter` | string | **Yes** | LDAP filter for user synchronization. |
| `username-attr` | string | No | LDAP attribute for full user name. Default: `gecos`. |
| `uid-attr` | string | No | LDAP attribute used as login username. Default: `uid`. |
| `sync-interval` | string | No | Interval for syncing user table with LDAP as a `time.ParseDuration` string. |
| `sync-del-old-users` | boolean | No | Delete users from DB that no longer exist in LDAP. |
| `sync-user-on-login` | boolean | No | Add unknown users to the DB on login if they exist in LDAP. |
| `update-user-on-login` | boolean | No | Update existing user in DB on login with LDAP values (name, roles, projects). |

### `auth.oidc`

| Property | Type | Required | Description |
| -------- | ---- | -------- | ----------- |
| `provider` | string | **Yes** | OpenID Connect provider URL. |
| `sync-user-on-login` | boolean | No | Add unknown users to the DB on login with OIDC claims. |
| `update-user-on-login` | boolean | No | Update existing user in DB on login with OIDC claims (name, roles, projects). |

---

## Section `metric-store`

*Source: `pkg/metricstore/configSchema.go`*

| Property | Type | Required | Description |
| -------- | ---- | -------- | ----------- |
| `retention-in-memory` | string | **Yes** | How long to keep metrics in memory as a `time.ParseDuration` string (e.g. `"48h"`). |
| `memory-cap` | integer | **Yes** | Upper memory cap for the metric store in GB. |
| `num-workers` | integer | No | Concurrent workers for checkpoint/archive operations. Default: `min(NumCPU/2+1, 10)`. |
| `checkpoint-interval` | string | No | Interval between checkpoints as a `time.ParseDuration` string. Default: `"12h"`. |
| `checkpoints` | object | No | Checkpoint storage options. See sub-properties below. |
| `cleanup` | object | No | Cleanup/archival options. See sub-properties below. |
| `nats-subscriptions` | array of object | No | NATS subjects to subscribe to for metric data ingestion. See sub-properties below. |

### `metric-store.checkpoints`

| Property | Type | Required | Description |
| -------- | ---- | -------- | ----------- |
| `file-format` | string | No | `wal` (binary snapshot + WAL, crash-safe) or `json` (human-readable). Default: `wal`. |
| `directory` | string | No | Directory for checkpoint files. Default: `./var/checkpoints`. |
| `max-wal-size` | integer | No | Maximum WAL file size in bytes per host. `0` = unlimited. Default: `0`. |

### `metric-store.cleanup`

| Property | Type | Required | Description |
| -------- | ---- | -------- | ----------- |
| `mode` | string | No | `delete` (default) or `archive`. |
| `directory` | string | Required when `mode: archive` | Target directory for archived metric data. |

### `metric-store.nats-subscriptions` items

| Property | Type | Required | Description |
| -------- | ---- | -------- | ----------- |
| `subscribe-to` | string | **Yes** | NATS subject name to subscribe to. |
| `cluster-tag` | string | No | Default cluster tag for lines that carry no cluster tag. |

---

## Section `cron`

*Source: `internal/taskmanager/taskManager.go`*

| Property | Type | Required | Description |
| -------- | ---- | -------- | ----------- |
| `commit-job-worker` | string | No | Frequency of the commit-job worker. Default: `"2m"`. |
| `duration-worker` | string | No | Frequency of the duration worker. Default: `"5m"`. |
| `footprint-worker` | string | No | Frequency of the footprint worker. Default: `"10m"`. |

---

## Section `archive`

*Source: `pkg/archive/ConfigSchema.go`*

| Property | Type | Required | Description |
| -------- | ---- | -------- | ----------- |
| `kind` | string | **Yes** | Archive backend: `file`, `s3`, or `sqlite`. |
| `path` | string | No | Job-archive path for `file` backend. Default: `./var/job-archive`. |
| `db-path` | string | No | SQLite database file path for `sqlite` backend. |
| `endpoint` | string | No | S3 endpoint URL for `s3` backend (required for MinIO and S3-compatible services). |
| `access-key` | string | No | S3 access key ID for `s3` backend. |
| `secret-key` | string | No | S3 secret access key for `s3` backend. |
| `bucket` | string | No | S3 bucket name for `s3` backend. |
| `region` | string | No | S3 region for `s3` backend. |
| `use-path-style` | boolean | No | Use path-style S3 URLs for `s3` backend (required for MinIO). |
| `compression` | integer | No | Compress jobs older than this many days. Default: `7`. |
| `retention` | object | No | Retention policy configuration. See sub-properties below. |

### `archive.retention`

| Property | Type | Required | Description |
| -------- | ---- | -------- | ----------- |
| `policy` | string | **Yes** | `none`, `delete`, `copy`, or `move`. |
| `format` | string | No | Output format for `copy`/`move`: `json` (default) or `parquet`. |
| `include-db` | boolean | No | Also remove jobs from the database. Default: `true`. |
| `omit-tagged` | string | No | `none` = process all jobs (default); `all` = skip any tagged job; `user` = skip user-tagged jobs (auto-tagger tags `app`/`jobClass` are not user tags). |
| `age` | integer | No | Process jobs with `startTime` older than this many days. Default: `7`. |
| `target-kind` | string | No | Target storage for `copy`/`move`: `file` or `s3`. Default: `file`. |
| `target-path` | string | No | Filesystem path for target storage (`target-kind: file`). |
| `target-endpoint` | string | No | S3 endpoint URL for target (`target-kind: s3`). |
| `target-bucket` | string | No | S3 bucket name for target (`target-kind: s3`). |
| `target-access-key` | string | No | S3 access key for target (`target-kind: s3`). |
| `target-secret-key` | string | No | S3 secret key for target (`target-kind: s3`). |
| `target-region` | string | No | S3 region for target (`target-kind: s3`). |
| `target-use-path-style` | boolean | No | Use path-style S3 URLs for target — required for MinIO (`target-kind: s3`). |
| `max-file-size-mb` | integer | No | Maximum Parquet file size in MB before splitting. Default: `512`. Only for `format: parquet`. |

---

## Section `nats`

*Source: cc-lib (external library)*

| Property | Type | Required | Description |
| -------- | ---- | -------- | ----------- |
| `address` | string | **Yes** | NATS server address (e.g. `"nats://localhost:4222"`). |
| `username` | string | No | Username for NATS authentication. |
| `password` | string | No | Password for NATS authentication. |
| `creds-file-path` | string | No | Path to NATS credentials file. |

---

## Section `metric-store-external`

*Source: `internal/metricdispatch/configSchema.go`*

An array of external cc-metric-store instances for reading metric data. Each
entry maps a scope (cluster name or `*` wildcard) to an external metric store.

| Property | Type | Required | Description |
| -------- | ---- | -------- | ----------- |
| `scope` | string | **Yes** | Cluster name or `*` as a default fallback. |
| `url` | string | **Yes** | URL of the external cc-metric-store endpoint (e.g. `"http://host:8082"`). |
| `token` | string | **Yes** | JWT authentication token for the external metric store. |

---

## Section `ui`

*Source: `web/configSchema.go`*

### `ui.job-list`

| Property | Type | Required | Description |
| -------- | ---- | -------- | ----------- |
| `use-paging` | boolean | No | Use classic paging instead of continuous scrolling by default. |
| `show-footprint` | boolean | No | Show footprint bars as first column by default. |

### `ui.node-list`

| Property | Type | Required | Description |
| -------- | ---- | -------- | ----------- |
| `use-paging` | boolean | No | Use classic paging instead of continuous scrolling by default. |

### `ui.job-view`

| Property | Type | Required | Description |
| -------- | ---- | -------- | ----------- |
| `show-polar-plot` | boolean | No | Show the job metric footprint polar plot by default. |
| `show-footprint` | boolean | No | Show the annotated job metric footprint bars by default. |
| `show-roofline` | boolean | No | Show the job roofline plot by default. |
| `show-stat-table` | boolean | No | Show the job metric statistics table by default. |

### `ui.metric-config`

Global initial metric selections for all clusters (overridable per cluster/subcluster).

| Property | Type | Required | Description |
| -------- | ---- | -------- | ----------- |
| `job-list-metrics` | array of string | No | Default metrics shown in job lists for new users. |
| `job-view-plot-metrics` | array of string | No | Default metrics shown as plots in job view for new users. |
| `job-view-table-metrics` | array of string | No | Default metrics shown in the job view statistics table for new users. |
| `clusters` | array of object | No | Per-cluster overrides. Each entry has `name` (required) and optional `job-list-metrics`, `job-view-plot-metrics`, `job-view-table-metrics`, and `sub-clusters`. |

#### `ui.metric-config.clusters[].sub-clusters` items

| Property | Type | Required | Description |
| -------- | ---- | -------- | ----------- |
| `name` | string | **Yes** | Subcluster name. |
| `job-list-metrics` | array of string | No | Overrides global job-list metrics for this subcluster. |
| `job-view-plot-metrics` | array of string | No | Overrides global job-view plot metrics for this subcluster. |
| `job-view-table-metrics` | array of string | No | Overrides global job-view table metrics for this subcluster. |

### `ui.plot-configuration`

| Property | Type | Required | Description |
| -------- | ---- | -------- | ----------- |
| `color-background` | boolean | No | Color metric plot backgrounds by threshold limits by default. |
| `plots-per-row` | integer | No | Number of plots per row in job, node, and analysis views. |
| `line-width` | integer | No | Initial plot line thickness. |
| `color-scheme` | array of string | No | Initial color scheme for metric plots. |
