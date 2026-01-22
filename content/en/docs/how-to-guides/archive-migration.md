---
title: Job archive migrations
weight: 200
description: Job archive migrations
categories: [cc-backend]
tags: [Admin]
---

## Introduction

In general, an upgrade is nothing more than a replacement of the binary file.
All the necessary files, except the database file, the configuration file and
the job archive, are embedded in the binary file. It is recommended to use a
directory where the file names of the binary files are named with a version
indicator. This can be, for example, the date or the Unix epoch time. A symbolic
link points to the version to be used. This makes it easier to switch to earlier
versions.

{{< alert color="warning" >}}
**IMPORTANT NOTE**</br>
It is recommended to make a backup copy of the job-archive before each update.
{{< /alert >}}

## Migrating the job archive

{{< alert title="Notice" >}}
Don't forget to also migrate archive jobs in case you use an archive retention
policy!. Archive migration is only supported from the previous archive version.
{{< /alert >}}

Job archive migration requires a separate tool (`archive-migration`), which is
part of the cc-backend source tree (build with `go build ./tools/archive-migration`)
and is also provided as part of the releases.

Migration is supported only between two successive releases.
You find details how to use the `archive-migration` tool in its [reference
documentation](/docs/reference/cc-backend/tools/archive-migration/)

The `cluster.json` files in `job-archive-new` must be checked for errors, especially
whether the aggregation attribute is set correctly for all metrics.

Migration takes a few hours for large job archives (several hundred
GB). A versioned job archive contains a version.txt file in the root directory
of the job archive. This file contains the version as an unsigned integer.
