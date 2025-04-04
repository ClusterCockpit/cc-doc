---
title: Nodes
description: >
  Node Based Metric Information of one Cluster
categories: [cc-backend]
tags: [Frontend, Admin]
weight: 12
---

## Node Overview

{{< figure src="../../figures/nodesview_table.png" alt="Nodes View" width="100%" class="ccfigure mw-xl"
    caption="Nodes View. This example shows the last two hours of the 'clock' metric of eight nodes. Node 'f0147' of the 'main' partition has an average below the configured 'alert' threshold, and is colored in red."
>}}

The node overview is always called in respect to one specified cluster. It displays the current state of *all* nodes in that cluster in respect to *one* selected metric, rendered in form of [metric plots]({{< ref "plots#metric-plots" >}} "Metric Plots"), and *independent* of job meta data, i.e. without consideration for job start and end timestamps.

{{< alert >}}*Please note:* The X-Axis of all plots rendered in this view are relative to the latest data point received from the collector daemon, and thus, the time displayed reaches *backward* as indicated by negative X-axis labels.{{< /alert >}}

### Overview Selection Bar

{{< figure src="../../figures/nodesview_navbar.png" alt="Nodes View" width="100%" class="ccfigure mw-xl">}}

Selections regarding the display, and update, of the plots rendered in the node table can be performed here:

* *Find Node:*: Filter the node table by hostname. Partial queries are possible.
* *Displayed Timerange:* Select the timeframe to be rendered in the node table
  * `Custom`: Select timestamp `from` and `to` in which the data should be fetched. It is possible to select date and time.
  * `15 Minutes, 30 Minutes, 1 Hour, 2 Hours, 4 Hours, 12 Hours, 24 Hours`
* *Metric:*: Select the metric to be fetched for *all* nodes. If no data can be fetched, messages are displayed per node.
* *(Periodic) Reload:* Force reload of fresh data from the backend or set a periodic reload in specified intervals
  * `30 Seconds, 60 Seconds, 120 Seconds, 5 Minutes`

### Node Table

Nodes (hosts) are ordered alphanumerically in this table, rendering the selected metric in the selected timeframe.

Each heading links to the singular [node view]({{< ref "node" >}} "Node View") of the respective host.

## Node List

{{< figure src="../../figures/nodelist_plotline.png" alt="Nodes List Data" width="100%" class="ccfigure mw-xl"
    caption="Nodes View."
>}}

The node list view is also always called in respect to one specified cluster, and optionally, subCluster. It displays the current state of *all* nodes in that cluster (or subCluster) in respect to a *selectable* number, and order, of metrics. Plots are rendered in form of [metric plots]({{< ref "plots#metric-plots" >}} "Metric Plots"), and are *independent* of job meta data, i.e. without consideration for job start and end timestamps.

{{< alert >}}*Please note:* The X-Axis of all plots rendered in this view are relative to the latest data point received from the collector daemon, and thus, the time displayed reaches *backward* as indicated by negative X-axis labels.{{< /alert >}}

The always visible "Node Info"-Card displays the following information. "List"-Bottons will lead to according views with preset filters.

|Field|Example|Description|Destination|
|-----|-------|-----------|----|
|Card Header|`Node a0421 Alex A40`|Hostname and Cluster|[Node View]({{< ref "node" >}} "Node View")|
|Status Indicator|`Status Exclusive`|Indicates the host state via keywords, see below|-|
|Activity|`2 Jobs`|Number of Jobs currently running on host|[Job List]({{< ref "joblist" >}} "Job List")|
|Users|`2 Users`|Number and IDs of users currently running jobs|[User Table]({{< ref "users" >}} "User Table")|
|Projects|`1 Project`|Number and IDs of projects currently running jobs|[Project Table]({{< ref "projects" >}} "Project Table")|

In order to give an idea of the currentnode state, the following indicators are possible:

|Node Status|Type|Description|
|-----|-------|------|
|Exclusive|Job-Info|One *exclusive* job is currently running, utilizing all of the nodes' hardware|
|Shared|Job-Info|One or more *shared* jobs are currently running, utilizing allocated amounts of the nodes' hardware|
|Allocated|Fallback|If more jobs than one are running, but all jobs are marked as 'exclusive', this fallback is used|
|Idle|Job-Info|No currently active jobs|
|Warning|Warning|At least one of the selected metrics does not return data successfully. Can hint to configuration problems.|
|Unhealthy|Warning|None of the selected metrics return data successfully. Node could be offline or misconfigured.|

{{< alert >}}*Please note:* All "Warning States" are estimated on the basis of returned metric data from the metric data repository. **No** actual hardware health information is queried or handled in any way or form.{{< /alert >}}

### List Selection Bar

{{< figure src="../../figures/nodelist_header.png" alt="Nodes List Header" width="100%" class="ccfigure mw-xl"
    caption="Nodes List Header Options. "
>}}

The selection header allows for configuration of the displayed data in terms of selected metrics or timerange.

|Field|Example|Description|
|-----|-------|-----------|----|
|Metrics|`4 Selected`|Menu for and Number of Metrics currently selected|
|Resolution|`600`|Resolution of the metric plots rendered for each node|
|Find Node(s)|`a0421`|Filter for hostnames|
|Range|`Last 12hrs`|Time range to be displayed as X-Axis|
|Refresh|`60 Seconds`|Enable automatic refresh of metric plots|

|Field|Example|Description|Destination|
|-----|-------|-----------|----|
|Job Id|`123456`|The JobId of the job assigned by the scheduling daemon. The icon on the right allows for easy copy to clipboard.|[Job View]({{< ref "job" >}} "Job View")|

### Extended Legend

{{< figure src="../../figures/nodelist_extendedlegend.png" alt="Extended Legend" width="100%" class="ccfigure mw-xxs"
    caption="Nodes List Extended Legend. Usernames and Job-IDs are shown in addition to the Resource-ID for shared resources."
>}}

For nodes with multiple jobs running on them, accelerator metrics are extended by the username and the job-id currently utilizing this hardware ID. This is based on the ID information sent during job-start to cc-backend (Database `resources`-column).
