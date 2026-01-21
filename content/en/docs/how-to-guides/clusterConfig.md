---
title: How to create a `cluster.json` file
description: >
  How to initially create a cluster configuration
categories: [cc-backend]
tags: [Admin]
---

## Overview

Every cluster is configured using a dedicated `cluster.json` file, that is part
of the job archive. You can find the JSON schema for it
[here](https://github.com/ClusterCockpit/cc-lib/blob/main/schema/schemas/cluster.schema.json).
This file provides information about the homogeneous hardware partitions within
the cluster including the node topology and the metric list. A real production
configuration is provided as part of
[cc-examples](https://github.com/ClusterCockpit/cc-examples/tree/main/nhr%40fau/job-archive).

## `cluster.json`: Basics

The `cluster.json` file contains three top level parts: the name of the cluster,
the metric configuration, and the subcluster list.
You find the latest `cluster.json` schema
[here](https://github.com/ClusterCockpit/cc-lib/blob/main/schema/schemas/cluster.schema.json).
Basic layout of `cluster.json` files:

```json
{
  "name": "fritz",
  "metricConfig": [
    {
      "name": "cpu_load",
      ...
    },
    {
      "name": "mem_used",
      ...
    }
  ],
  "subClusters": [
    {
      "name": "main",
      ...
    },
    {
      "name": "spr",
      ...
    }
  ]
}
```

### `cluster.json`: Metric configuration

There is one metric list per cluster. You can find a list of recommended metrics
and their naming [here]({{< ref "/docs/tutorials/prod-metric-list" >}}).
Example for a metric list entry with only the required attributes:

```json
"metricConfig": [
    {
        "name": "flops_sp",
        "unit": {
            "base": "Flops/s",
            "prefix": "G"
        },
        "scope": "hwthread",
        "timestep": 60,
        "aggregation": "sum",
        "peak": 5600,
        "normal": 1000,
        "caution": 200,
        "alert": 50
    }
]
```

Explanation of required attributes:

- `name`: The metric name.
- `unit`: The metrics unit. Base can be: `B` (for bytes), `F` (for flops),
  `B/s`, `F/s`, `Flops` (for floating point operations), `Flops/s` (for FLOP rate),
  `CPI` (for cycles per instruction), `IPC` (for instructions per cycle),
  `Hz`, `W` (for Watts), `°C`, or empty string for no unit. Prefix can
  be: `K`, `M`, `G`, `T`, `P`, or `E`.
- `scope`: The native metric measurement resolution. Can be `node`, `socket`,
  `memoryDomain`, `core`, `hwthread`, or `accelerator`.
- `timestep`: The measurement frequency in seconds
- `aggregation`: How the metric is aggregated with in node topology. Can be one
  of `sum`, `avg`, or empty string for no aggregation
  (node level metrics).
- Metric thresholds. If threshold applies for larger or smaller values depends
  on optional attribute `lowerIsBetter` (default false).
  - `peak`: The maximum possible metric value
  - `normal`: A common metric value level
  - `caution`: Metric value requires attention
  - `alert`: Metric value requiring immediate attention

Optional attributes:

- `footprint`: Is this a job footprint metric. Set to how the footprint is
  aggregated: Can `avg`, `min`, or `max`. Footprint metrics are shown in the
  footprint UI component and job view polar plot.
- `energy`: Should the metric be used to calculate the job energy. Can be
  `power` (metric has unit Watts) or `energy` (metric has unit Joules).
- `lowerIsBetter`: Is lower better. Influences frontend UI and evaluation of
  metric thresholds. Default is `false`.
- `restrict`: Whether to restrict visibility of this metric to non-user roles
  (admin, support, manager). Default is `false`. When set to `true`, regular
  users cannot view this metric.
- `subClusters` (Type: array of objects): Overwrites for specific subClusters. The metrics per default
  are valid for all subClusters. It is possible to overwrite or remove metrics for
  specific subClusters. If a metric is overwritten for a subClusters all
  attributes have to be set, partial overwrites are not supported. Example for a
  metric overwrite:

```json
{
    "name": "mem_used",
    "unit": {
        "base": "B",
        "prefix": "G"
    },
    "scope": "node",
    "aggregation": "sum",
    "footprint": "max",
    "timestep": 60,
    "lowerIsBetter": true,
    "peak": 256,
    "normal": 128,
    "caution": 200,
    "alert": 240,
    "subClusters": [
        {
            "name": "spr1tb",
            "footprint": "max",
            "peak": 1024,
            "normal": 512,
            "caution": 900,
            "alert": 1000
        },
        {
            "name": "spr2tb",
            "footprint": "max",
            "peak": 2048,
            "normal": 1024,
            "caution": 1800,
            "alert": 2000
        }
    ]
},
```

This metric characterizes the memory capacity used by a job. Aggregation for a
job is the sum of all node values. As footprint the largest allocated memory
capacity is used. For this configuration lower is better is set, which results
in jobs with more than the metric thresholds are marked. There exist two
subClusters with 1TB and 2TB memory capacity compared to the default 256GB.

Example for removing metrics for a subcluster:

```json
{
  "name": "vectorization_ratio",
  "unit": {
    "base": ""
  },
  "scope": "hwthread",
  "aggregation": "avg",
  "timestep": 60,
  "peak": 100,
  "normal": 60,
  "caution": 40,
  "alert": 10,
  "subClusters": [
    {
      "name": "icelake",
      "remove": true
    }
  ]
}
```

### `cluster.json`: subcluster configuration

SubClusters in ClusterCockpit are subsets of a cluster with homogeneous
hardware. The subCluster part specifies the node topology, a list of nodes that
are part of a subClusters, and the node capabilities that are used to draw the
roofline diagrams.

#### Topology Structure

The `topology` section defines the hardware topology using nested arrays that map
relationships between hardware threads, cores, sockets, memory domains, and dies:

- `node`: Flat list of all hardware thread IDs on the node
- `socket`: Hardware threads grouped by physical CPU socket (2D array)
- `memoryDomain`: Hardware threads grouped by NUMA domain (2D array)
- `die`: Optional grouping by CPU die within sockets (2D array). This is used for
  multi-die processors where each socket contains multiple dies. If not applicable,
  use an empty array `[]`
- `core`: Hardware threads grouped by physical core (2D array)
- `accelerators`: Optional list of attached accelerators (GPUs, FPGAs, etc.)

The resource ID for CPU cores is the OS processor ID. For GPUs we recommend using
the PCI-E address as resource ID.

Here is an example:

```json
{
  "name": "icelake",
  "nodes": "w22[01-35],w23[01-35],w24[01-20],w25[01-20]",
  "processorType": "Intel Xeon Gold 6326",
  "socketsPerNode": 2,
  "coresPerSocket": 16,
  "threadsPerCore": 1,
  "flopRateScalar": {
    "unit": {
      "base": "F/s",
      "prefix": "G"
    },
    "value": 432
  },
  "flopRateSimd": {
    "unit": {
      "base": "F/s",
      "prefix": "G"
    },
    "value": 9216
  },
  "memoryBandwidth": {
    "unit": {
      "base": "B/s",
      "prefix": "G"
    },
    "value": 350
  },
  "topology": {
    "node": [
      0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
      21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38,
      39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56,
      57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71
    ],
    "socket": [
      [
        0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
        20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35
      ],
      [
        36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53,
        54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71
      ]
    ],
    "memoryDomain": [
      [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17],
      [18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35],
      [36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53],
      [54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71]
    ],
    "die": [],
    "core": [
      [0],
      [1],
      [2],
      [3],
      [4],
      [5],
      [6],
      [7],
      [8],
      [9],
      [10],
      [11],
      [12],
      [13],
      [14],
      [15],
      [16],
      [17],
      [18],
      [19],
      [20],
      [21],
      [22],
      [23],
      [24],
      [25],
      [26],
      [27],
      [28],
      [29],
      [30],
      [31],
      [32],
      [33],
      [34],
      [35],
      [36],
      [37],
      [38],
      [39],
      [40],
      [41],
      [42],
      [43],
      [44],
      [45],
      [46],
      [47],
      [48],
      [49],
      [50],
      [51],
      [52],
      [53],
      [54],
      [55],
      [56],
      [57],
      [58],
      [59],
      [60],
      [61],
      [62],
      [63],
      [64],
      [65],
      [66],
      [67],
      [68],
      [69],
      [70],
      [71]
    ]
  }
}
```

Since it is tedious to write this by hand, we provide a
[Perl script](https://raw.githubusercontent.com/ClusterCockpit/cc-backend/refs/heads/master/configs/generate-subcluster.pl)
as part of `cc-backend` that generates a subCluster template. This script only
works if the `LIKWID` tools are installed and in the PATH. You also need the
`LIKWID` library for cc-metric-store. You find instructions on how to install
`LIKWID` [here](https://github.com/RRZE-HPC/likwid/wiki/Build).

#### Example: SubCluster with GPU Accelerators

Here is an example for a subCluster with GPU accelerators:

```json
{
  "name": "a100m80",
  "nodes": "a[0531-0537],a[0631-0633],a0731,a[0831-0833],a[0931-0934]",
  "processorType": "AMD Milan",
  "socketsPerNode": 2,
  "coresPerSocket": 64,
  "threadsPerCore": 1,
  "flopRateScalar": {
    "unit": {
      "base": "F/s",
      "prefix": "G"
    },
    "value": 432
  },
  "flopRateSimd": {
    "unit": {
      "base": "F/s",
      "prefix": "G"
    },
    "value": 9216
  },
  "memoryBandwidth": {
    "unit": {
      "base": "B/s",
      "prefix": "G"
    },
    "value": 400
  },
  "topology": {
    "node": [
      0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
      21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38,
      39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56,
      57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74,
      75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92,
      93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108,
      109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123,
      124, 125, 126, 127
    ],
    "socket": [
      [
        0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
        20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37,
        38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55,
        56, 57, 58, 59, 60, 61, 62, 63
      ],
      [
        64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81,
        82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99,
        100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113,
        114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127
      ]
    ],
    "memoryDomain": [
      [
        0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
        20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37,
        38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55,
        56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73,
        74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91,
        92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107,
        108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121,
        122, 123, 124, 125, 126, 127
      ]
    ],
    "core": [
      [0],
      [1],
      [2],
      [3],
      [4],
      [5],
      [6],
      [7],
      [8],
      [9],
      [10],
      [11],
      [12],
      [13],
      [14],
      [15],
      [16],
      [17],
      [18],
      [19],
      [20],
      [21],
      [22],
      [23],
      [24],
      [25],
      [26],
      [27],
      [28],
      [29],
      [30],
      [31],
      [32],
      [33],
      [34],
      [35],
      [36],
      [37],
      [38],
      [39],
      [40],
      [41],
      [42],
      [43],
      [44],
      [45],
      [46],
      [47],
      [48],
      [49],
      [50],
      [51],
      [52],
      [53],
      [54],
      [55],
      [56],
      [57],
      [58],
      [59],
      [60],
      [61],
      [62],
      [63],
      [64],
      [65],
      [66],
      [67],
      [68],
      [69],
      [70],
      [71],
      [73],
      [74],
      [75],
      [76],
      [77],
      [78],
      [79],
      [80],
      [81],
      [82],
      [83],
      [84],
      [85],
      [86],
      [87],
      [88],
      [89],
      [90],
      [91],
      [92],
      [93],
      [94],
      [95],
      [96],
      [97],
      [98],
      [99],
      [100],
      [101],
      [102],
      [103],
      [104],
      [105],
      [106],
      [107],
      [108],
      [109],
      [110],
      [111],
      [112],
      [113],
      [114],
      [115],
      [116],
      [117],
      [118],
      [119],
      [120],
      [121],
      [122],
      [123],
      [124],
      [125],
      [126],
      [127]
    ],
    "accelerators": [
      {
        "id": "00000000:0E:00.0",
        "type": "Nvidia GPU",
        "model": "A100"
      },
      {
        "id": "00000000:13:00.0",
        "type": "Nvidia GPU",
        "model": "A100"
      },
      {
        "id": "00000000:49:00.0",
        "type": "Nvidia GPU",
        "model": "A100"
      },
      {
        "id": "00000000:4F:00.0",
        "type": "Nvidia GPU",
        "model": "A100"
      },
      {
        "id": "00000000:90:00.0",
        "type": "Nvidia GPU",
        "model": "A100"
      },
      {
        "id": "00000000:96:00.0",
        "type": "Nvidia GPU",
        "model": "A100"
      },
      {
        "id": "00000000:CC:00.0",
        "type": "Nvidia GPU",
        "model": "A100"
      },
      {
        "id": "00000000:D1:00.0",
        "type": "Nvidia GPU",
        "model": "A100"
      }
    ]
  }
}
```

**Important**: Each accelerator requires three fields:

- `id`: Unique identifier (PCI-E address recommended, e.g., "00000000:0E:00.0")
- `type`: Type of accelerator. Valid values are: `"Nvidia GPU"`, `"AMD GPU"`, `"Intel GPU"`
- `model`: Specific model name (e.g., "A100", "MI100")

You must ensure that the metric collector as well as the Slurm adapter also uses
the same identifier format (PCI-E address) as the accelerator resource ID for
consistency.
