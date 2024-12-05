---
title: Nodes
description: >
  Node Based Metric Information of one Cluster
categories: [cc-backend]
tags: [Frontend, Admin]
weight: 12
---

{{< figure src="../../figures/nodesview_table.png" alt="Nodes View" width="100%" class="ccfigure mw-xl"
    caption="Nodes View. This example shows the last two hours of the 'clock' metric of eight nodes. Node 'f0147' of the 'main' partition has an average below the configured 'alert' threshold, and is colored in red."
>}}

The nodes view, or systems view, is always called in respect to one specified cluster. It displays the current state of *all* nodes in that cluster in respect to *one* selected metric, rendered in form of [metric plots]({{< ref "plots#metric-plots" >}} "Metric Plots"), and *independent* of job meta data, i.e. without consideration for job start and end timestamps.

{{< alert >}}*Please note:* The X-Axis of all plots rendered in this view are relative to the latest data point received from the collector daemon, and thus, the time displayed reaches *backward* as indicated by negative X-axis labels.{{< /alert >}}

### Selection Bar

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
