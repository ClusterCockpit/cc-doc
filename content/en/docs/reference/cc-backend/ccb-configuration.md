---
title: Configuration
description: >
  ClusterCockpit Configuration Option References
categories: [cc-backend]
tags: [Backend]
weight: 2
---

`cc-backend` requires a JSON configuration file. The configuration files is
structured into components. Every component is configured either in a separate
JSON object or using a separate file. When a section is put in a separate file
the section key has to have a `-file` suffix.

Example:

```json
"auth-file": "./var/auth.json"
```

To override the default config file path, specify the location of a JSON
configuration file with the `-config <file path>` command line option.

## Configuration Options

### Section `main`

Section must exist.

- `addr`: Type string (Optional). Address where the http (or https) server will
  listen on (for example: '0.0.0.0:80'). Default `localhost:8080`.
- `api-allowed-ips`: Type array of strings (Optional). IPv4 addresses from
  which the secured administrator API endpoint functions `/api/*` can be reached.
  Default: No restriction. The previous `*` wildcard is still supported but
  obsolete.
- `user`: Type string (Optional). Drop root permissions once .env was read and
  the port was taken. Only applicable if using privileged port.
- `group`: Type string. Drop root permissions once .env was read and the port
  was taken. Only applicable if using privileged port.
- `disable-authentication`: Type bool (Optional). Disable authentication (for everything:
  API, Web-UI, ...). Default `false`.
- `embed-static-files`: Type bool (Optional). If all files in
  `web/frontend/public` should be served from within the binary itself (they are
  embedded) or not. Default `true`.
- `static-files`: Type string (Optional). Folder where static assets can be
  found, if `embed-static-files` is `false`. No default.
- `db`: Type string (Optional). The db file path. Default: `./var/job.db`.
- `enable-job-taggers`: Type bool (Optional). Enable automatic job taggers for
  application and job class detection. Requires to provide tagger rules. Default:
  `false`.
- `validate`: Type bool (Optional). Validate all input JSON documents against
  JSON schema. Default: `false`.
- `session-max-age`: Type string (Optional). Specifies for how long a session
  shall be valid as a string parsable by time.ParseDuration(). If 0 or empty, the
  session/token does not expire! Default `168h`.
- `https-cert-file` and `https-key-file`: Type string (Optional). If both those
  options are not empty, use HTTPS using those certificates. Default: No HTTPS.
- `redirect-http-to`: Type string (Optional). If not the empty string and `addr`
  does not end in ":80", redirect every request incoming at port 80 to that url.
- `stop-jobs-exceeding-walltime`: Type int (Optional). If not zero,
  automatically mark jobs as stopped running X seconds longer than their walltime.
  Only applies if walltime is set for job. Default `0`.
- `short-running-jobs-duration`: Type int (Optional). Do not show running jobs
  shorter than X seconds. Default `300`.
- `emission-constant`: Type integer (Optional). Energy Mix CO2 Emission Constant
  [g/kWh]. If entered, UI displays estimated CO2 emission for job based on jobs'
  total Energy.
- `enable-resampling`: Type object (Optional). If configured, will enable
  dynamic downsampling of metric data using the configured values.
  - `minimum-points`: Type integer. TODO
  - `resolutions`: Type array [integer]. Array of resampling target resolutions,
    in seconds; Example: [600,300,60].
  - `trigger`: Type integer. Trigger next zoom level at less than this many
    visible datapoints.
- `machine-state-dir`: Type string (Optional). Where to store MachineState
  files. TODO: Explain in more detail!
- `api-subjects`: Type object (Optional). NATS subjects configuration for
  subscribing to job and node events. Default: No NATS API.
  - `subject-job-event`: Type string. NATS subject for job events (start_job, stop_job).
  - `subject-node-state`: Type string. NATS subject for node state updates.

### Section `nats`

Section is optional.

- `address`: Type string. Address of the NATS server (e.g., `nats://localhost:4222`).
- `username`: Type string (Optional). Username for NATS authentication.
- `password`: Type string (Optional). Password for NATS authentication (optional).
- `creds-file-path`: Type string (Optional). Path to NATS credentials file for
  authentication (optional).

### Section `cron`

Section must exist.

- `commit-job-worker`: Type string. Frequency of commit job worker. Default: `2m`
- `duration-worker`: Type string. Frequency of duration worker. Default: `5m`
- `footprint-worker`: Type string. Frequency of footprint. Default: `10m`

### Section `archive`

Section is optional. If section is not provided, the default is `kind` set to
`file` with `path` set to `./var/job-archive`.

- `kind`: Type string (required). Set archive backend. Supported values: `file`,
  `s3`, `sqlite`.
- `path`: Type string (Optional). Path to the job-archive. Default: `./var/job-archive`.
- `compression`: Type integer (Optional). Setup automatic compression for jobs
  older than number of days.
- `retention`: Type object (Optional). Enable retention policy for archive and
  database.
  - `policy`: Type string (required). Retention policy. Possible values none,
    delete, move.
  - `include-db`: Type bool (Optional). Also remove jobs from database. Default:
    `true`.
  - `age`: Type integer (Optional). Act on jobs with startTime older than age
    (in days).
    Default: 7 days.
  - `location`: Type string (Optional). The target directory for retention. Only
    applicable
    for retention policy move. Only applies for move policy.

### Section `auth`

Section must exist.

- `jwts`: Type object (required). For JWT Authentication.
  - `max-age`: Type string (required). Configure how long a token is valid. As
    string parsable by time.ParseDuration().
  - `cookie-name`: Type string (Optional). Cookie that should be checked for a
    JWT token.
  - `vaidate-user`: Type bool (Optional). Deny login for users not in database
    (but defined in JWT). Overwrite roles in JWT with database roles.
  - `trusted-issuer`: Type string (Optional). Issuer that should be accepted when
    validating external JWTs.
  - `sync-user-on-login`: Type bool (Optional). Add non-existent user to DB at
    login attempt with values provided in JWT.
  - `update-user-on-login`: Type bool (Optional). Update existent user in DB at
    login attempt with values provided in JWT. Currently only the person name is
    updated.
- `ldap`: Type object (Optional). For LDAP Authentication and user
  synchronisation. Default `nil`.
  - `url`: Type string (required). URL of LDAP directory server.
  - `user-base`: Type string (required). Base DN of user tree root.
  - `search-dn`: Type string (required). DN for authenticating LDAP admin
    account with general read rights.
  - `user-bind`: Type string (required). Expression used to authenticate users
    via LDAP bind. Must contain `uid={username}`.
  - `user-filter`: Type string (required). Filter to extract users for syncing.
  - `username-attr`: Type string (Optional). Attribute with full user name.
    Defaults to `gecos` if not provided.
  - `sync-interval`: Type string (Optional). Interval used for syncing local
    user table with LDAP directory. Parsed using time.ParseDuration.
  - `sync-del-old-users`: Type bool (Optional). Delete obsolete users in database.
  - `sync-user-on-login`: Type bool (Optional). Add non-existent user to DB at
    login attempt if user exists in LDAP directory.
- `oidc`: Type object (Optional). For OpenID Connect Authentication. Default `nil`.
  - `provider`: Type string (required). OpenID Connect provider URL.
  - `sync-user-on-login`: Type bool. Add non-existent user to DB at login attempt
    with values provided.
  - `update-user-on-login`: Type bool. Update existent user in DB at login attempt
    with values provided. Currently only the person name is updated.

### Section `metric-store`

Section must exist.

- `retention-in-memory`: Type string (required). Keep the metrics within memory
  for given time interval. Retention for X hours, then the metrics would be freed.
  Buffers that are still used by running jobs will be kept.
- `memory-cap`: Type integer (required). If memory used exceeds value in GB,
  buffers still used by long running jobs will be freed.
- `num-workers`: Type integer (Optional). Number of concurrent workers for
  checkpoint and archive operations. Default: If not set defaults to
  `min(runtime.NumCPU()/2+1, 10)`
- `checkpoints`: Type object (required). Configuration for checkpointing the
  metrics buffers
  - `file-format`: Type string (Optional). Format to use for checkpoint files.
    Can be JSON or Avro. Default: Avro.
  - `interval`: Type string (required). Interval at which the metrics should be
    checkpointed. Expression must be parsable by `time.ParseDuration()`. Usually
    the unit is hours. E.g. `12h`.
  - `directory`: Type string (Optional). Path in which the checkpoints should be
    placed. Default: `./var/checkpoints`.
- `cleanup`: Type object (Optional). Configuration for the cleanup process. If
  not set the `mode` is `delete` with `interval` set to the `retention-in-memory`
  interval.
  - `mode`: Type string (Optional). The mode for cleanup. Can be `delete` or
    `archive`. Default: `delete`.
  - `interval`: Type string (Optional). Interval at which the cleanup runs.
  - `directory`: Type string (required if mode is `archive`). Directory where to
    put the archive
    files.
- `nats-subscriptions`: Type array (Optional). List of NATS subjects the metric
  store should subscribe to. Items are of type object with the following
  attributes:
  - `subscribe-to`: Type string (required). NATS subject to subscribe to.
  - `cluster-tag`: Type string (Optional). Allow lines without a cluster tag,
    use this as default.

### Section `ui`

The `ui` section specifies defaults for the web user interface. The defaults
which metrics to show in different views can be overwritten per cluster or
subcluster.

- `job-list`: Type object (Optional). Job list defaults. Applies to user and
  jobs views.
  - `use-paging`: Type bool (Optional). If classic paging is used instead of
    continuous scrolling by default.
  - `show-footprint`: Type bool (Optional). If footprint bars are shown as first
    column by default.
- `node-list`: Type object (Optional). Node list defaults. Applies to node list
  view.
  - `use-paging`: Type bool (Optional). If classic paging is used instead of
    continuous scrolling by default.
- `job-view`: Type object (Optional). Job view defaults.
  - `show-polar-plot`: Type bool (Optional). If the job metric footprints polar
    plot is shown by default.
  - `show-footprint`: Type bool (Optional). If the annotated job metric
    footprint bars are shown by default.
  - `show-roofline`: Type bool (Optional). If the job roofline plot is shown by
    default.
  - `show-stat-table`: Type bool (Optional). If the job metric statistics table
    is shown by default.
- `metric-config`: Type object (Optional). Global initial metric selections for
  primary views of all clusters.
  - `job-list-metrics`: Type array [string] (Optional). Initial metrics shown
    for new users in job lists (User and jobs view).
  - `job-view-plot-metrics`: Type array [string] (Optional). Initial metrics
    shown for new users as job view metric plots.
  - `job-view-table-metrics`: Type array [string] (Optional). Initial metrics
    shown for new users in job view statistics table.
  - `clusters`: Type array of objects (Optional). Overrides for global defaults
    by cluster and subcluster.
    - `name`: Type string (required). The name of the cluster.
    - `job-list-metrics`: Type array [string] (Optional). Initial metrics shown
      for new users in job lists (User and jobs view) for this cluster.
    - `job-view-plot-metrics`: Type array [string] (Optional). Initial metrics
      shown for new users as job view timeplots for this cluster.
    - `job-view-table-metrics`: Type array [string] (Optional). Initial metrics
      shown for new users in job view statistics table for this cluster.
    - `sub-clusters`: Type array of objects (Optional). The array of overrides
      per subcluster.
      - `name`: Type string (required). The name of the subcluster.
      - `job-list-metrics`: Type array [string] (Optional). Initial metrics
        shown for new users in job lists (User and jobs view) for subcluster.
      - `job-view-plot-metrics`: Type array [string] (Optional). Initial metrics
        shown for new users as job view timeplots for subcluster.
      - `job-view-table-metrics`: Type array [string] (Optional). Initial
        metrics shown for new users in job view statistics table for subcluster.
- `plot-configuration`: Type object (Optional). Initial settings for plot render
  options.
  - `color-background`: Type bool (Optional). If the metric plot backgrounds are
    initially colored by threshold limits.
  - `plots-per-row`: Type integer (Optional). How many plots are initially
    rendered per row. Applies to job, single node, and analysis views.
  - `line-width`: Type integer (Optional). Initial thickness of rendered
    plotlines. Applies to metric plot, job compare plot and roofline.
  - `color-scheme`: Type array [string] (Optional). Initial colorScheme to be
    used for metric plots.
