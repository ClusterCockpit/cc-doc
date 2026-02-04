---
title: Users
description: >
  Table of All Users Running Jobs on the Clusters
categories: [cc-backend]
tags: [Frontend, Manager, Support, Admin]
weight: 7
---

{{< figure src="../../figures/usertable.png" alt="User Table" width="100%" class="ccfigure mw-lg"
    caption="User Table, sorted by 'Total Jobs' in descending order. In addition, active filters reduce the underlying data to jobs with more than one hour runtime, started on the GPU accelerated cluster."
>}}

This view lists all users which are, and were, active on the configured clusters. Information about the total number of jobs, walltimes and calculation usages are shown.

It is possible to filter the list by username using the equally named prompt, which also accepts partial queries.

The [filter component]({{< ref "filters" >}} "Filter") allows limitation of the returned users based on job parameters like start timestamp or memory usage.

The table can be sorted by clicking the respective icon next to the column headers.

{{< alert >}}*Please Note:* By default, a "Last 30 Days" filter is activated by default when opening this view.{{< /alert >}}

{{< alert >}}*Managers Only:* For users with `manager` authority, this view will be titled 'Managed Users' in the navigation bar. Managers will only be able to see other user accounts of the managed projects.{{< /alert >}}

### Details

|Column|Description|Note|
|-----|-----------|----|
|User Name|The user account jobs are associated with|Links to the users' [job list]({{< ref "userjobs" >}} "User Job List") with preset filter returning only jobs of this user and additional histograms|
|Name|The name of user||
|Total Jobs|Users' total of all started jobs||
|Short Jobs|Users' total of all jobs below short duration threshold||
|Total Cores|*Conditional, if running jobs*: Users' total of all cores allocated to currently running jobs||
|Total Accelerators|*Conditional, if running jobs*: Users' total of all accelerators allocated to currently running jobs||
|Total Walltime|Users' total requested walltime||
|Total Core Hours|Users' total of all used core hours||
|Total Accelerator Hours|Users' total of all used accelerator hours|*Please Note*: This column is always shown, and will return `0` for clusters without installed accelerators|
