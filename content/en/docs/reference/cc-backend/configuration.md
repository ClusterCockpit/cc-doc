---
title: Configuration
description: >
  ClusterCockpit Configuration Option References
categories: [cc-backend]
tags: [Backend]
weight: 2
---

CC-Backend requires a JSON configuration file that specifies the cluster systems to be used. The schema of the configuration is described at the [schema documentation]({{< ref "config-schema" >}} "Configuration Schema").

To override the default, specify the location of a JSON configuration file with the `-config <file path>` command line option.

## Configuration Options

* `addr`: Type string.  Address where the http (or https) server will listen on (for example: 'localhost:80'). Default `:8080`.
* `apiAllowedIPs`: Type array [string].  Addresses from which the secured API endpoints (/users and other auth related endpoints)  can be reached
* `user`: Type string. Drop root permissions once .env was read and the port was taken. Only applicable if using privileged port.
* `group`: Type string.  Drop root permissions once .env was read and the port was taken. Only applicable if using privileged port.
* `disable-authentication`: Type bool.  Disable authentication (for everything: API, Web-UI, ...). Default `false`.
* `embed-static-files`: Type bool. If all files in `web/frontend/public` should be served from within the binary itself (they are embedded) or not. Default `true`.
* `static-files`: Type string. Folder where static assets can be found, if `embed-static-files` is `false`. No default.
* `db-driver`: Type string. 'sqlite3' or 'mysql' (mysql will work for mariadb as well). Default `sqlite3`.
* `db`: Type string. For sqlite3 a filename, for mysql a DSN in [this format](https://github.com/go-sql-driver/mysql#dsn-data-source-name), *without query parameters*. Default: `./var/job.db`.
* `job-archive`: Type object.
  * `kind`: Type string. At them moment only file is supported as value.
  * `path`: Type string. Path to the job-archive. Default: `./var/job-archive`.
  * `compression`: Type integer. Setup automatic compression for jobs older than number of days.
  * `retention`: Type object.
    * `policy`: Type string (required). Retention policy. Possible values none, delete, move.
    * `includeDB`: Type bool. Also remove jobs from database.
    * `age`: Type integer. Act on jobs with startTime older than age (in days).
    * `location`: Type string. The target directory for retention. Only applicable for retention policy move.
* `disable-archive`: Type bool. Keep all metric data in the metric data repositories, do not write to the job-archive. Default `false`.
* `validate`: Type bool. Validate all input json documents against json schema.
* `ldap`: Type object. For LDAP Authentication and user synchronisation. Default `nil`.
  * `url`: Type string (required). URL of LDAP directory server.
  * `user_base`: Type string (required). Base DN of user tree root.
  * `search_dn`: Type string (required). DN for authenticating LDAP admin account with general read rights.
  * `user_bind`: Type string (required). Expression used to authenticate users via LDAP bind. Must contain `uid={username}`.
  * `user_filter`: Type string (required). Filter to extract users for syncing.
  * `username_attr`: Type string. Attribute with full user name. Defaults to `gecos` if not provided.
  * `sync_interval`: Type string. Interval used for syncing local user table with LDAP directory. Parsed using time.ParseDuration.
  * `sync_del_old_users`: Type bool. Delete obsolete users in database.
  * `syncUserOnLogin`: Type bool. Add non-existent user to DB at login attempt if user exists in Ldap directory.
* `jwts`: Type object (required). For JWT Authentication.
  * `max-age`: Type string (required). Configure how long a token is valid. As string parsable by time.ParseDuration().
  * `cookieName`: Type string. Cookie that should be checked for a JWT token.
  * `vaidateUser`: Type bool. Deny login for users not in database (but defined in JWT). Overwrite roles in JWT with database roles.
  * `trustedIssuer`: Type string. Issuer that should be accepted when validating external JWTs.
  * `syncUserOnLogin`: Type bool. Add non-existent user to DB at login attempt with values provided in JWT.
  * `updateUserOnLogin`: Type bool. Update existent user in DB at login attempt with values provided in JWT. Currently only the person name is updated.
* `oidc`: Type object. Default `nil`.
  * `provider`: Type string.
  * `syncUserOnLogin`: Type bool. Add non-existent user to DB at login attempt with values provided in JWT.
  * `updateUserOnLogin`: Type bool. Update existent user in DB at login attempt with values provided in JWT. Currently only the person name is updated.
* `session-max-age`: Type string. Specifies for how long a session shall be valid  as a string parsable by time.ParseDuration(). If 0 or empty, the session/token does not expire! Default `168h`.
* `https-cert-file` and `https-key-file`: Type string. If both those options are not empty, use HTTPS using those certificates.
* `redirect-http-to`: Type string. If not the empty string and `addr` does not end in ":80", redirect every request incoming at port 80 to that url.
* `ui-defaults`: Type object. Default configuration for webinterface views. Most options can be overwritten by the user via the web interface. See [below]({{< ref "#ui-default-object-fields" >}}) for details.
* `enable-resampling`: Type object. If configured, will enable dynamic zoom in frontend metric plots using the configured values.
  * `resolutions`: Type array [integer]. Array of resampling target resolutions, in seconds; Example: [600,300,60].
  * `trigger`: Type integer. Trigger next zoom level at less than this many visible datapoints.
* `machine-state-dir`: Type string. Where to store MachineState files. TODO: Explain in more detail!
* `stop-jobs-exceeding-walltime`: Type int. If not zero, automatically mark jobs as stopped running X seconds longer than their walltime. Only applies if walltime is set for job. Default `0`.
* `short-running-jobs-duration`: Type int. Do not show running jobs shorter than X seconds. Default `300`.
* `emission-constant`: Type integer. Energy Mix CO2 Emission Constant [g/kWh]. If entered, displays estimated CO2 emission for job based on jobs' totalEnergy.
* `cron-frequency`: Type object. Defines frequency of cron job workers.
  * `duration-worker`: Type string. Default: `5m`
  * `footprint-worker`: Type string. Default: `10m`
* `clusters`: Type array [object] (required). Array of clusters.
  * `name`: Type string. The name of the cluster.
  * `metricDataRepository`: Type object.
    * `kind`: Type string. Can be one of [`cc-metric-store`, `influxdb`].
    * `url`: Type string.
    * `token`: Type string.
  * `filterRanges` Type object. This option controls the slider ranges for the UI controls of numNodes, duration, and startTime. Example:

```json
"filterRanges": {
               "numNodes": { "from": 1, "to": 64 },
               "duration": { "from": 0, "to": 86400 },
               "startTime": { "from": "2022-01-01T00:00:00Z", "to": null }
         }
```

## UI Default Object Fields

* `analysis_view_histogramMetrics`: Type array [string]. Metrics to show as job count histograms in analysis view. Default `["flops_any", "mem_bw", "mem_used"]`.
* `analysis_view_scatterPlotMetrics`: Type array of string array. Initial
scatter plot configuration in analysis view. Default `[["flops_any", "mem_bw"], ["flops_any", "cpu_load"], ["cpu_load", "mem_bw"]]`.
* `job_view_nodestats_selectedMetrics`: Type array [string]. Initial metrics shown in node statistics table of single job view. Default `["flops_any", "mem_bw", "mem_used"]`.
* `job_view_selectedMetrics`: Type array [string].  Default `["flops_any", "mem_bw", "mem_used"]`.
* `plot_general_colorBackground`: Type bool. Color plot background according to job average threshold limits. Default `true`.
* `plot_general_colorscheme`: Type array [string]. Initial color scheme. Default `"#00bfff", "#0000ff", "#ff00ff", "#ff0000", "#ff8000", "#ffff00", "#80ff00"`.
* `plot_general_lineWidth`: Type int. Initial linewidth. Default `3`.
* `plot_list_jobsPerPage`: Type int. Jobs shown per page in job lists. Default `50`.
* `plot_list_selectedMetrics`: Type array [string]. Initial metric plots shown in jobs lists. Default `"cpu_load", "ipc", "mem_used", "flops_any", "mem_bw"`.
* `plot_view_plotsPerRow`: Type int. Number of plots per row in single job view. Default `3`.
* `plot_view_showPolarplot`: Type bool. Option to toggle polar plot in single job view. Default `true`.
* `plot_view_showRoofline`: Type bool. Option to toggle roofline plot in single job view. Default `true`.
* `plot_view_showStatTable`: Type bool. Option to toggle the node statistic table in single job view. Default `true`.
* `system_view_selectedMetric`: Type string. Initial metric shown in system view. Default `cpu_load`.

Some of the `ui-defaults` values can be appended by `:<clustername>` in order to have different settings depending on the current cluster. Those are notably `job_view_nodestats_selectedMetrics`, `job_view_selectedMetrics` and `plot_list_selectedMetrics`.
