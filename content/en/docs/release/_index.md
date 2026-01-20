---
title: Release specific infos
description: Settings and issues specific to the current release
weight: 1
---

## Major changes

- **Metric store integration**: The previously external `cc-metric-store`
  component was integrated into `cc-backend`. In this process the configuration
  for the metric store was made much simpler. It is not possible to use an
  external time-series database. It is possible though to either send the metric
  data to multiple time-series backends or to forward all metric-data to `cc-backend`.
- **Drop support for MySQL/MariaDB**: We only support SQLite from now on. SQLite
  performance better and requires less administration.
- **New slurm adapter**: We provide now an official slurm batch job adapter with
  tighter slurm integration. The REST API should still work but was extended to
  also provide Slurm node and job states. The job and node-state API is offered
  as REST API or via NATS.
- **Revised configuration**: The structure of the configuration was unified and
  consolidated. It can now be distributed via multiple files. The UI
  configuration can be selectively configured. Defaults for the metric plots can
  be configured per cluster/subcluster.
- **Switch to more flexible .env handling**:

### New experimental features

- **Automatic Job taggers**: It is possible to automatically detect application
  types and classify pathological jobs and tag jobs accordingly. The tagger
  rules are specified in rules.
- **Alternative job-archive backends**: As alternatives to the file-based job
  archives there exist now an **SQLite** and **S3** compatible object store backends.

## What you need to do

You need to adapt your central `config.json` and all of your `cluster.json`
files in the job archive marking all footprint or energy metrics.

Here is an example how to mark a footprint metric:

```json
{
  "name": "fritz",
  "metricConfig": [
    {
      "name": "mem_used",
      "unit": {
        "base": "B",
        "prefix": "G"
      },
      "scope": "node",
      "aggregation": "sum",
      "footprint": "max",
      "timestep": 60,
      "peak": 256,
      "normal": 128,
      "caution": 200,
      "alert": 240,
      "lowerIsBetter": true,
      "subClusters": [
        {
          "name": "spr1tb",
          "peak": 1024,
          "normal": 512,
          "caution": 900,
          "footprint": "max",
          "lowerIsBetter": true,
          "alert": 1000
        },
        {
          "name": "spr2tb",
          "peak": 2048,
          "normal": 1024,
          "caution": 1800,
          "footprint": "max",
          "lowerIsBetter": true,
          "alert": 2000
        }
      ]
    }
  ]
}
```

In case the metrics has subcluster overwrites you currently have to also add the
attributes there. The new attribute `footprint` can have `avg`, `min`, or `max`
as value indicating what basic statistic over all nodes or cores of a job is
used for this metric. In above example the footprint is the maximum allocated
memory. Because this is (for us) a lower is better metric, this is marked
accordingly using the attribute `lowerIsBetter`.

To mark a metric to be used for calculating the total energy you need to add the
`energy` attribute.

Example for marking an energy footprint metric:

```json
{
  "name": "fritz",
  "metricConfig": [
    {
      "name": "cpu_power",
      "unit": {
        "base": "W"
      },
      "scope": "socket",
      "aggregation": "sum",
      "timestep": 60,
      "peak": 500,
      "normal": 250,
      "caution": 100,
      "alert": 50,
      "energy": "power"
    },
    {
      "name": "mem_power",
      "unit": {
        "base": "W"
      },
      "scope": "socket",
      "aggregation": "sum",
      "timestep": 60,
      "peak": 100,
      "normal": 50,
      "caution": 20,
      "alert": 10,
      "energy": "power"
    }
  ]
}
```

Again you need to add the attribute also to subcluster overwrite in case you
have some. The `energy` attribute can have `power` or `energy` as values. Power
indicates that this metric has Watt as unit and energy is used for metrics that
have Joules as unit. We are aware that we could also already get this
information from the existing metric configuration, but that's the way it is
currently implemented. Power metrics are converted to Joules using the average
job power and multiplying by the job duration. The total job power is then the
sum over all energy footprint metrics.

The web frontend can also show the CO2 footprint for a job. To enable this you
need to add a new top level configuration key `emission-constant` in g/kWh to the
`cc-backend` configuration:

```json
{
  "emission-constant": 317,
{
```

After you have marked all metrics you need to raise the job archive version
manually to 2 by editing `./var/job-archive/version.txt`

## Database migration

This release requires to migrate your database to version 10. Backup your
database before migration! Depending on your database size this may take a long
time. In our case with a database file size of 75GB it took more than 48
hours. Most of this time is spent on rebuilding the indices.

To migrate the database run the following command:

```sh
cc-backend -migrate-db
```

The migration creates

## Configuration changes

GitHub Repository with [complete configuration examples](https://github.com/ClusterCockpit/cc-examples/tree/main/nhr%40fau).
All configuration options are now checked against a JSON schema.
The required options are significantly reduced.

### Enable timeseries resampling

ClusterCockpit now supports resampling of time series data to a lower frequency.
This dramatically improves load times for very large or very long jobs and we
recommend to enable it. Resampling is supported for running as well as for
finished jobs. For running jobs this currently only works with the newest
version of `cc-metric-store`. Resampling support for the Prometheus time series
database will be added in the future.

To enable resampling you have to add the following toplevel configuration key:

```json
  "enable-resampling": {
    "trigger": 30,
    "resolutions": [
      600,
      300,
      120,
      60
    ]
  },
```

Trigger configures at which minimum number of points in every timeseries plot
window the next finer level is loaded. Resolutions defines the resolution steps
in seconds. The finest resolution must be the native resolution. In case you
have different native solutions in your metric configuration you should use the
finest. The implementation will fallback to the finest available resolution in
this case.

### Continuous scroll is default now

This release includes support for continuous scroll for job lists,
replacing the previous paging ui. Continuous scroll is now the default and you
can remove the `ui-defaults` block in case you added it just for enabling
continuous scroll. Every user can overwrite the scrolling option in his
configuration.

## Known issues

- Currently energy footprint metrics of type energy are ignored for calculating
  total energy.
- Resampling for running jobs only works with cc-metric-store
- With energy footprint metrics of type power the unit is ignored and it is
  assumed the metric has the unit Watt.
