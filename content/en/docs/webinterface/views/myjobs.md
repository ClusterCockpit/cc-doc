---
title: My Jobs
description: >
  All Jobs as Table of the Active User
categories: [cc-backend]
tags: [Frontend, User, Manager, Support, Admin]
weight: 1
---

{{< figure src="../../figures/userjobs.png" alt="User Job View" width="100%" class="ccfigure mw-xl"
    caption="Personal User Job View. Similar to the general job list view, this view expands it by user-specific meta data, as well as distributions histograms."
>}}

The "My Jobs" View is available to all users regardless of authority and displays the users personal jobs, i.e. jobs started by this users username on the cluster systems.

The view is a personal variant of the [user job view]({{< ref "userjobs" >}} "User Job View") and therefore also consists of three components: Basic Information about the users jobs, selectable statistic histograms of the jobs, and a generalized job list.

Users are able to change the sorting, select and reorder the rendered metrics, filter, and activate a periodic reload of the data.

## User Information and Basic Distributions

The top row always displays personal usage information, independent of the selected filters.

Additional histograms depicting the distribution of job duration and number of nodes occupied by the returned jobs *are* affected by the selected filters.

Information displayed:

* Username
* Total Jobs
* Short Jobs (as defined by the configuration, default: less than 300 second runtime)
* Total Walltime
* Total Core Hours

## Selectable Histograms

Histograms depicting the distribution of the selected jobs' statistics can be selected from the top navbar "Select Histograms" button. The displayed data is based on the jobs returned from active filters, and will be pulled from the database.

{{< alert >}}*Please note:* Metrics statistics listed here for selection are configured. All metrics, for which the `footprint` flag is set in the respective metrics' configuration will be available here.{{< /alert >}}

## Job List

The job list displays all jobs started by your username on the systems. Additional filters will always respect this limitation. For a detailed description of the job list component, see the [related documentation]({{< ref "joblist" >}} "Job List").
