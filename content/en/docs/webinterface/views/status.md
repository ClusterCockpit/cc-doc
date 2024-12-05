---
title: Status
description: >
  Hardware Usage Information
categories: [cc-backend]
tags: [Frontend, Admin]
weight: 16
---

The status view is always called in respect to one specified cluster. It displays the current state of utilization of the respective clusters resources, as well as user and project top lists and distribution histograms of the allocated resources per job.

{{< alert >}}*Please note:* By default, the periodic reload function is set to `2 Minutes`.{{< /alert >}}

## Utilization Information

{{< figure src="../../figures/status_subcluster.png" alt="Subluster Urilization in Status view" width="100%" class="ccfigure mw-xl">}}

For each subluster, utilization is displayed in two parts rendered in one row.

### Gauges

Simple gauge representation of the current utilization of available resources

|Field|Description|Note|
|-----|-----------|----|
|Allocated Nodes|Number of nodes currently allocated in respect to maximum available|-|
|Flop Rate (Any)|Currently achieved flop rate in respect to theoretical maximum|Floprate calculated  as `f_any = (f_double x 2) + f_single`|
|MemBW Rate|Currently achieved memory bandwidth in respect to technical maximum|-|

### Roofline

A [roofline plot]({{< ref "plots#roofline-plot" >}} "Roofline Plot") representing the utilization of available resources as the relation between computation and memory for each currently allocated, running job at the time of the latest data retrieval. Therefore, no time information is represented (all dots in blue, representing one job each).

## Top Users and Projects

{{< figure src="../../figures/status_piecharts.png" alt="Subluster Urilization in Status view" width="100%" class="ccfigure mw-xl">}}

The ten most active users or projects are rendered in a combination of pie chart and tabular legend. By default, the top ten users or projects with the most allocated, running jobs are listed.

The selection can be changed directly in the tables header at `Number of ...`, and can be changed to

* Jobs (Default)
* Nodes
* Cores
* Accelerators

The selection is saved for each user and cluster, and will select the last chosen type of list as default the next time this view is rendered.

Hovering over one of the pie chart fractions will display a legend featuring the identifier and value of the selected parameter.

"User Names" and "Project Codes" are rendered as links, leading to [user job lists]({{< ref "userjobs" >}} "User Job List") or [project job lists]({{< ref "joblist" >}} "Project Jobs") with preset filters for cluster, entity ID, and `state == running`.

{{< alert >}}*Please note:* The legend colors are fixed by their position, and *not* by their respective identifier. This means that the orange fraction will always be the largest fraction, even if the contributing user or project changes.{{< /alert >}}

## Statistic Histograms

Several [histograms]({{< ref "plots#histograms" >}} "Histograms") depicting the utilization of the clusters resources, based on all currently running jobs are rendered here:

* Duration Distribution
* Number of Nodes Distribution
* Number of Cores Distribution
* Number of Accelerators Distribution

Additional Histograms showing specified footprint metrics across all systems can be selected via the "Select histograms" menu next to the refresher tool.

{{< alert >}}*Please note:* Metric statistics available here for selection are configured. All metrics, for which the `footprint` flag is set in the respective metrics' configuration will be shown.{{< /alert >}}