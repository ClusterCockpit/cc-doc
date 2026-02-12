---
title: Filters
description: >
  Webinterface Filter Options
categories: [cc-backend]
tags: [Frontend, General]
weight: 4
---

{{< figure src="../figures/filterbutton.png" alt="Filter Button" width="100%" class="ccfigure mw-xs"
    caption="Filter Button as displayed in Job List Views"
>}}

The ClusterCockpit filter component is used for reducing the number of jobs, either for direct display in job list views, or to specifiy the data-source for collecting information displayed in user or project tables, as well as the analysis view.

## Filter Options

{{< figure src="../figures/multiplefilter.png" alt="Multiple Active Filters" width="100%" class="ccfigure mw-sm"
    caption="Three active filters have reduced the total job count considerably"
>}}

Multiple filters can be easily combined by selecting more than one option of the available filters.

By clicking on the respective filter pill, colored in blue, and located right of the filter component, one can directly access the respective filters' menu for editing, or removing, the filter.

At the moment, the following filters are implemented:

### Cluster/Partition

{{< figure src="../figures/filter_cluster.png" alt="Cluster Filter" width="100%" class="ccfigure mw-xxs">}}

Select a configured cluster, or a specified partition of a given cluster, and display only jobs started on that cluster (and partition).

*Options:* All cluster names, and nested partition names, configured in `config.json`

*Default:* Any Cluster (Any Partition)

### Job States

{{< figure src="../figures/filter_state.png" alt="Job State Filter" width="100%" class="ccfigure mw-xxs">}}

Select one or more job states, and display only jobs matching the selected criteria. Additionally, filters for resource sharing as well as processing type can be selected. Combinations *are possible*, for example: `Only Running, Shared, Batch Processed Jobs`.

A note on sharing option nomenclature: Select options are chosen to be "Human Readable", while the strings used in the backend database column `job.shared` differ as follows:

|Option Name|Database String|
|---|---|
|All|No Filter Applied|
|Exclusive|`none`|
|Shared|`multi_user`|
|Multitask|`single_user`|

* *State Options:* `Pending, Running, Completed, Failed, Timeout, Deadline, Preempted, Suspended, Cancelled, Out_of_memory, Boot_fail, Node_fail`
* *Sharing Options:* `All, Exclusive, Shared, Multitask`
* *Processing Options:* `All, Interactive, Batch Processed`

*Default:* All states, all sharing types, all processing types

{{< alert >}}**BETA Warning:** *Currently, processing type filters depend simply on `meta_data.jobName == 'interactive'`!* If interactive jobs are permitted on your site, but use a different naminig scheme or a different method to differentiate them from batch processed jobs, please contact or support mail adress.{{< /alert >}}

### Start Time

{{< figure src="../figures/filter_starttime.png" alt="Starttime Filter" width="100%" class="ccfigure mw-xs">}}

Select the timeframe in which jobs were started, and display only jobs matching the selected criteria.

*Options:* Free selection of date `dd.mm.YYYY` and time `hh:mm` for `from` and `to` limits.

*Default:* All Starttimes

*Preset:* Jobs started one month ago until `$now`

### Duration

{{< figure src="../figures/filter_duration.png" alt="Duration Filter" width="100%" class="ccfigure mw-xxs">}}

Select the duration of jobs, and display only jobs matching the selected criteria.

*Options:* Duration less than `hh:mm`, duration more than `hh:mm`, duration between two duration selections. Only **one** of the three options can be used at a time.

*Default:* All Durations

### Tags

{{< figure src="../figures/filter_tags.png" alt="Tags Filter" width="100%" class="ccfigure mw-xs">}}

Select one or more job tags, and display only jobs tagged with the selected tags.

*Options:* All available tags. It is possible to search within the list of tags.

*Default:* No selection

### Resources

{{< figure src="../figures/filter_resources.png" alt="Resources Filter" width="100%" class="ccfigure mw-xs">}}

Select a named node or specify an amount of used resources, and display only jobs matching the selected criteria.

*Options:*

* Named node free text field: Enter a hostname here to only return jobs which were ran on this node. Select the desired match logic (Defaults to "Equal", i.e. exact match).
* Range selectors: Select a range of allocated job resources ranging from the minimal to the maximum configured resource count of all clusters. If the [cluster filter]({{< ref "#clusterpartition" >}} "Cluster Filter") is set, the ranges are limited to the respective resources' configuration. Available resources are:
  * Nodes
  * HWThreads
  * Accelerators (if available)

*Default:* No named node, full resource ranges of all configured clusters

### Energy

Specify total consumed energy, and display only jobs matching the selected range.

*Options:* "Total Job Energy" in kWh.

*Default:* No selection

{{< alert >}}*Please note:* Consumed energy will be written during archiving *after* a job has finished. Thus, this filter only works on jobs which are not marked as `running`.{{< /alert >}}

### Statistics

{{< figure src="../figures/filter_statistics.png" alt="Statistics Filter" width="100%" class="ccfigure mw-xxs">}}

Specify ranges of metric statistics, and display only jobs matching the selected criteria.

{{< alert >}}*Please note:* Metric statistics listed here for selection are configured. All metrics, for which the `footprint` flag is set in the respective metrics' configuration will be available here.{{< /alert >}}

*Example Options:*

* FLOPs (Avg.): Select Range `From-To` by dragging the slider or entering values directly.
* Memory Bandwith (Avg.): Select Range `From-To` by dragging the slider or entering values directly.
* Load (Avg.): Select Range `From-To` by dragging the slider or entering values directly.
* Memory Used (Max.): Select Range `From-To` by dragging the slider or entering values directly.

*Default:* Full metric statistics ranges as configured

### Start Time Quick Selections

{{< alert >}}*Please note:* Not available in all views!{{< /alert >}}

Quickly select a preconfigured range of job start times. Will display as named [start time filter]({{< ref "#starttime" >}} "Starttime Filter").

When the returned URL is copied and shared, and the named filter value will transfer over.

*Options:* `Last 6 hours, Last 24 hours, Last 7 Days, Last 30 Days`

*Default:* No selection
