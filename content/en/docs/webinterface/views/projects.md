---
title: Projects
description: >
  Table of All Projects Running Jobs on the Clusters
categories: [cc-backend]
tags: [Frontend, Support, Admin]
weight: 9
---

{{< figure src="../../figures/projecttable.png" alt="User Table" width="100%" class="ccfigure mw-lg"
    caption="Project Table, sorted by 'Total Jobs' in descending order. In addition, active filters reduce the underlying data to jobs with less than six hours runtime, started on the CPU exclusive cluster."
>}}

This view lists all projects (usergroups) which are, and were, active on the configured clusters. Information about the total number of jobs, walltimes and calculation usages are shown.

It is possible to filter the list by project name using the equally named prompt, which also accepts partial queries.

The [filter component]({{< ref "filters" >}} "Filter") allows limitation of the returned projects based on job parameters like start timestamp or memory usage.

The table can be sorted by clicking the respective icon next to the column headers.

{{< alert >}}*Please Note:* By default, a "Last 30 Days" filter is activated by default when opening this view.{{< /alert >}}

{{< alert >}}*Managers Only:* For users with `manager` authority, this view will be titled 'Managed Projects' in the navigation bar. Managers will only be able to see colected data of managed projects.{{< /alert >}}

### Details

|Column|Description|Note|
|-----|-----------|----|
|Project Name|The project (usergoup) jobs are associated with|Links to a [job list]({{< ref "joblist" >}} "Project Job List") with preset filter returning only jobs of this project|
|Total Jobs|Project total of all started Jobs||
|Total Walltime|Project total requested walltime||
|Total Core Hours|Project total of all used core hours used||
|Total Accelerator Hours|Project total of all used accelerator hours |*Please Note*: This column is always shown, and will return `0` for clusters without installed accelerators|
