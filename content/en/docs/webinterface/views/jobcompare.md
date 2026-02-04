---
title: Job Comparison
description: >
  Compare Job Metric Statistics
categories: [cc-backend]
tags: [Frontend, User, Manager, Support, Admin]
weight: 4
---

{{< figure src="../../figures/compare_list.png" alt="Job List With Compare Switch" width="100%" class="ccfigure mw-xl"
    caption="Job list with compare switch. In this example, filters return 145 jobs, while no job is selected manually."
>}}

Accessible from the general job list as well as the user view job lists, the job compare view allows for the comparison of metric statistics in a pseudo-time-dependent manner.

The "Compare Jobs" button is located in the upper right corner of the job list views. Jobs for comparison are either selected by

1) ... a combination of filters resulting in a dataset of _500 jobs or less_.
2) ... manual job selection by checking the box in the job info card.

If too many jobs are returned by the current filter selection, the button will be disabled.

If jobs are directly selected from the current job list, the button will display the current count, as well as an additional "Reset" button, which will empty the list of selected jobs, if pressed.

Manual job selection will also work if the current job list has more than 500 returned jobs, while the subsequent job compare view will ignore all additional filters, and only show selected jobs. Returning to the job list also returns with the last used filters.

{{< alert >}}This allows manual job selection between pages, but also manual job selection between different filter combinations!{{< /alert >}}

## Fixed Compare Elements

{{< figure src="../../figures/compare_top.png" alt="Job Compare Options and Resource Compare" width="100%" class="ccfigure mw-xl"
    caption="Job compare view top elements. The count of 145 jobs remains after switching to this view. The resource plot shows jobs sorted by their startTime, and all jobs have allocated accelerators (red data line)."
>}}

The compare view features a reduced header:

* Sorting is disabled, as jobs are _always_ sorted by `startTime` in ascending order.
* The filter component is removed and only shows the total number of compared jobs.
* The refresh component is also removed.

The "Metric Selection" is active and can be used to add additional metric comparison plots to the view, if desired.

"Return to List" closes the compare view and restores the former job list view.

The resource [compare plot]({{< ref "plots#comparogram" >}}) is always shown at the first position. It features a semi-logarithmic view of allocated job resources in a pseudeo-time-dependent manner, as all jobs are sorted by actual start time. The data is colored as follows:

* Black: Nodes - will always be at least `1` (Note: Also for shared jobs!)
* Blue: Hardware Threads ( ~ Cores)
* Red: Accelerators - Can be zero! If so, no line is rendered.

The legend includes further information, such as:

* Job-ID
* Cluster (and subCluster) on which the job ran
* Runtimeof the job

## Selectable Compare Elements

{{< figure src="../../figures/compare_down.png" alt="Job Compare Metric Plot and Table" width="100%" class="ccfigure mw-xl"
    caption="Job compare view metric plot and table. 'Clock' metric statistics are plotted for every job sorted by their startTime. All information is also shown as sortable table at the bottom of the compare view."
>}}

Below the first plot, the individual metric [compare plots]({{< ref "plots#comparogram" >}}) are rendered. For each job, the `Min/Max/Avg` of the respective metric is plotted in a banded manner.

Zooming is possible, and will be synchronized to all other rendered plots, including the resource comparison.

{{< alert >}}**Please Note:** Due to spacing reasons, not all jobIDs can be rendered as tick-marks if the total count of compared jobs is high!{{< /alert >}}

Below the plots, all information is again rendered as a single table consisting of the following columns:

* JobID
* Start Time
* Duration
* Cluster
* Resources (Nodes, Threads , Accs)
* For each Metric: Minimum, Maximum, Average

It is possible to filter for specific jobIDs or parts thereof, all other columns are sortable.

Clicking on a JobID will lead to the respective [Job View]({{< ref "job" >}} "Job View").
