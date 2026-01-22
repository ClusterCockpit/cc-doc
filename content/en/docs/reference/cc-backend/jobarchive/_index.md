---
title: Job Archive Handbook
description: All you need to know about the ClusterCockpit Job Archive
categories: [cc-backend]
tags: [Admin, Developer]
weight: 5
---

The job archive specifies an exchange format for job meta and performance metric
data. It consists of two parts:

- a [Json file format](https://github.com/ClusterCockpit/cc-backend/tree/master/pkg/schema/schemas)
- a Directory hierarchy / Key specification

By using an open, portable and simple specification based on JSON objects it is
possible to exchange job performance data for research and analysis purposes as
well as use it as a robust way for archiving job performance data.

The current release supports new SQLite and S3 object store based job archive
backends. Those are still experimental and for production we still recommend to
use the proven file based job archive. One major disadvantage of the file based
job archive backend is that for large job counts it will consume a lot of
inodes.

## Trying the new job-archive backends

We provide the tool `archive-manager` that allows to convert between different
job-archive formats. This allows to convert your existing file-based job-archive
into either a SQLite or S3 variant. Please be aware that for large archives this
may take a long time. You can find details about how to use this tool in the
[archive-manager reference
documentation](/docs/reference/cc-backend/tools/archive-manager).

## Specification for file path / key

To manage the number of directories within a single directory a tree approach is
used splitting the integer job ID. The job id is split in junks of 1000 each.
Usually 2 layers of directories is sufficient but the concept can be used for an
arbitrary number of layers.

For a 2 layer schema this can be achieved with (code example in Perl):

```perl
$level1 = $jobID/1000;
$level2 = $jobID%1000;
$dstPath = sprintf("%s/%s/%d/%03d", $trunk, $destdir, $level1, $level2);
```

While for the SQLite and S3 object store based backend the systematic to
introduce layers is obsolete we kept it to keep the naming consistent. This
means what is the path in case of the file based backend is used as a object key
and column value there.

### Example

For the job ID 1034871 on cluster `large` with start time `1768978339` the key
is `./large/1034/871/1768978339`.

## Create a Job archive from scratch

In case you place the job-archive in the `./var` folder create the folder with:

```bash
mkdir -p ./var/job-archive
```

The job-archive is versioned, the current version is documented in the Release
Notes. Currently you have to create the version file manually when initializing the
job-archive:

```bash
echo 3 > ./var/job-archive/version.txt
```

### Directory layout

ClusterCockpit supports multiple clusters, for each cluster you need to create a
directory named after the cluster and a `cluster.json` file specifying the metric
list and hardware partitions within the clusters. Hardware partitions are
subsets of a cluster with homogeneous hardware (CPU type, memory capacity, GPUs)
that are called subclusters in ClusterCockpit.

For above configuration the job archive directory hierarchy looks like the
following:

```text
./var/job-archive/
     version.txt
     fritz/
        cluster.json
     alex/
        cluster.json
     woody/
        cluster.json
```

{{< alert title="Note" >}}
The `cluster.json` files currently have to be provided and maintained by the administrator!
{{< /alert >}}

You find help how-to create a `cluster.json` file in the [How to create a
cluster.json file](/docs/how-to-guides/clusterconfig/) guide.

## Json file format

### Overview

Every cluster must be configured in a `cluster.json` file.

The job data consists of two files:

- `meta.json`: Contains job meta information and job statistics.
- `data.json`: Contains complete job data with time series

The description of the json format specification is available as [[json
schema|https://json-schema.org/]] format file. The latest version of the json
schema is part of the `cc-backend` source tree. For external reference it is
also available in a separate repository.

### Specification `cluster.json`

The json schema specification in its raw format is available at the
[cc-lib GitHub repository](https://raw.githubusercontent.com/ClusterCockpit/cc-lib/refs/heads/main/schema/schemas/cluster.schema.json).
A variant rendered for better readability is found in the [references]({{< ref
"cluster-schema" >}} "Cluster Schema Reference").

### Specification `meta.json`

The json schema specification in its raw format is available at the
[cc-lib GitHub repository](https://raw.githubusercontent.com/ClusterCockpit/cc-lib/refs/heads/main/schema/schemas/job-meta.schema.json).
A variant rendered for better readability is found in the [references]({{< ref
"job-meta-schema" >}} "Job Metadata Schema Reference").

### Specification `data.json`

The json schema specification in its raw format is available at the
[cc-lib GitHub repository](https://raw.githubusercontent.com/ClusterCockpit/cc-lib/refs/heads/main/schema/schemas/job-data.schema.json).
A variant rendered for better readability is found in the [references]({{< ref
"job-metric-data-schema" >}} "Job Metadata Schema Reference").

Metric time series data is stored for a fixed time step. The time step is set
per metric. If no value is available for a metric time series data timestamp
`null` is entered.
