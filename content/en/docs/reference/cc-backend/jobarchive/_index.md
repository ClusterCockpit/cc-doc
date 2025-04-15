---
title: Job Archive Handbook
description: All you need to know about the ClusterCockpit Job Archive
categories: [cc-backend]
tags: [Admin, Developer]
weight: 5
---

The job archive specifies an exchange format for job meta and performance metric
data. It consists of two parts:

* a [Json file format](https://github.com/ClusterCockpit/cc-backend/tree/master/pkg/schema/schemas)
* a Directory hierarchy specification

By using an open, portable and simple specification based on files it is
possible to exchange job performance data for research and analysis purposes as
well as use it as a robust way for archiving job performance data to disk.

### Specification

To manage the number of directories within a single directory a tree approach is
used splitting the integer job ID. The job id is split in junks of 1000 each.
Usually 2 layers of directories is sufficient but the concept can be used for an
arbitrary number of layers.

For a 2 layer schema this can be achieved with (code example in Perl):

``` perl
$level1 = $jobID/1000;
$level2 = $jobID%1000;
$dstPath = sprintf("%s/%s/%d/%03d", $trunk, $destdir, $level1, $level2);
```

### Example

For the job ID 1034871 the directory path is `./1034/871/`.

## Json file format

### Overview

Every cluster must be configured in a `cluster.json` file.

The job data consists of two files:

* `meta.json`: Contains job meta information and job statistics.
* `data.json`: Contains complete job data with time series

The description of the json format specification is available as [[json
schema|https://json-schema.org/]] format file. The latest version of the json
schema is part of the `cc-backend` source tree. For external reference it is
also available in a separate repository.

### Specification `cluster.json`

The json schema specification in its raw format is available at the
[GitHub repository](https://github.com/ClusterCockpit/cc-backend/tree/master/pkg/schema/schemas/cluster.schema.json). A variant rendered for better readability is found in the [references]({{< ref "cluster-schema" >}} "Cluster Schema Reference").

### Specification `meta.json`

The json schema specification in its raw format is available at the
[GitHub repository](https://github.com/ClusterCockpit/cc-backend/tree/master/pkg/schema/schemas/job-meta.schema.json). A variant rendered for better readability is found in the [references]({{< ref "job-meta-schema" >}} "Job Metadata Schema Reference").

### Specification `data.json`

The json schema specification in its raw format is available at the
[GitHub repository](https://github.com/ClusterCockpit/cc-backend/tree/master/pkg/schema/schemas/job-data.schema.json). A variant rendered for better readability is found in the [references]({{< ref "job-metric-data-schema" >}} "Job Metadata Schema Reference").

Metric time series data is stored for a fixed time step. The time step is set
per metric. If no value is available for a metric time series data timestamp
`null` is entered.
