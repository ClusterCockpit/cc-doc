---
title: Release specific infos
description: Settings and issues specific to the current release
weight: 1
---
## Enable continuous scroll

This release includes initial support for continuous scroll for job lists,
replacing the previous paging ui. Continuous scroll must be explicitly enabled
by setting the option `job_list_usePaging` to `false` in the configuration file.
Due to implementation details the `ui_defaults` can only be overwritten
specifying all options.
Find below a json snippet with continuous scroll enabled that you can copy-paste
to our `config.json`

``` json
 "ui-defaults": {
        "analysis_view_histogramMetrics":         ["flops_any", "mem_bw", "mem_used"],
        "analysis_view_scatterPlotMetrics":       [["flops_any", "mem_bw"], ["flops_any", "cpu_load"], ["cpu_load", "mem_bw"]],
        "job_view_nodestats_selectedMetrics":     ["flops_any", "mem_bw", "mem_used"],
        "job_view_polarPlotMetrics":              ["flops_any", "mem_bw", "mem_used"],
        "job_view_selectedMetrics":               ["flops_any", "mem_bw", "mem_used"],
        "job_view_showFootprint":                 true,
        "job_list_usePaging":                     false,
        "plot_general_colorBackground":           true,
        "plot_general_colorscheme":               ["#00bfff", "#0000ff", "#ff00ff", "#ff0000", "#ff8000", "#ffff00", "#80ff00"],
        "plot_general_lineWidth":                 3,
        "plot_list_jobsPerPage":                  10,
        "plot_list_selectedMetrics":              ["cpu_load", "mem_used", "flops_any", "mem_bw"],
        "plot_view_plotsPerRow":                  3,
        "plot_view_showPolarplot":                true,
        "plot_view_showRoofline":                 true,
        "plot_view_showStatTable":                true,
        "system_view_selectedMetric":             "cpu_load",
        "analysis_view_selectedTopEntity":        "user",
        "analysis_view_selectedTopCategory":      "totalWalltime",
        "status_view_selectedTopUserCategory":    "totalJobs",
        "status_view_selectedTopProjectCategory": "totalJobs"
    }
```
