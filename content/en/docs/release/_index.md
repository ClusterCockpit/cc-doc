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
  data to multiple time-series backends or to forward all metric-data to
  `cc-backend`. We also dropped support for the Prometheus metric data base.
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
- **Switch to more flexible .env handling**: In previous releases the
  environment variables must be provided in an `.env` file which has to exist. We
  switched to the [godotenv](https://github.com/joho/godotenv) package, which is
  more flexible about where and how to provide the environment variables.

### New experimental features

- **Automatic Job taggers**: It is possible to automatically detect application
  types and classify pathological jobs and tag jobs accordingly. The tagger
  rules are specified in rules.
- **Alternative job-archive backends**: As alternatives to the file-based job
  archives there exist now an **SQLite** and **S3** compatible object store backends.

## What you need to do

You need to:

- Adapt your central `config.json` to the new [configuration
  option]({{< ref "ccb-configuration" >}}) systematic.
- Revise all of your `cluster.json` files in the job archive to reflect the
  [current options](/docs/how-to-guides/clusterconfig/).
- Migrate your job database to version 10 (see [Database
  migration](/docs/how-to-guides/database-migration/)).
- Migrate your job archive to version 3 (see [Job Archive
  migration](/docs/how-to-guides/archive-migration/)).
- Transfer the checkpoints from the external `cc-metric-store` instance to the
  `cc-backend` `./var/checkpoints` directory

## Configuration changes

GitHub Repository with [complete configuration examples](https://github.com/ClusterCockpit/cc-examples/tree/main/nhr%40fau).
All configuration options are now checked against a JSON schema.
The required options are significantly reduced.

## Transfer `cc-metric-store` checkpoints

## Known issues

- Currently energy footprint metrics of type energy are ignored for calculating
  total energy.
- With energy footprint metrics of type power the unit is ignored and it is
  assumed the metric has the unit Watt.
