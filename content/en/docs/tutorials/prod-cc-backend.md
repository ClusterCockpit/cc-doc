---
title: Setup of cc-backend
weight: 40
description: How to configure and deploy cc-backend
categories: [cc-backend]
tags: [Admin]
---

## Introduction

`cc-backend` is the main hub within the ClusterCockpit framework. Its
configuration consists of the general part in `config.json` and the cluster
configurations in `cluster.json` files, that are part of the
[job archive]({{< ref "docs/reference/cc-backend/jobarchive" >}}).
The job archive is a long-term persistent storage for all job meta and metric data.
The job meta data including job statistics as well as the user data are stored
in a SQL database. Secrets as passwords and tokens are provided as environment
variables. Environment variables can be initialized using a `.env` file residing
in the same directory as `cc-backend`. If using an `.env` file environment
variables that are already set take precedence.

{{< alert title="Note (cc-backend before v1.5.0)" >}}
For versions before v1.5.0 the `.env` file was the only option to set
environment variables, and they could not be set by other means!
{{< /alert >}}

## Configuration

`cc-backend` provides a command line switch to generate an initial template for
all required configuration files apart from the job archive:

``` bash
./cc-backend -init
```

This will create the `./var` folder, generate initial version of the
`config.json` and `.env` files, and initialize a sqlite database file.

### `config.json`

Below is a production configuration enabling the following functionality:

- Use HTTPS only
- Mark jobs as short job if smaller than 5m
- Enable authentication and user syncing via an LDAP directory
- Enable to initiate a user session via an JWT token, e.g. by an IDM portal
- Drop permission after privileged ports are taken
- Use compression for metric data files in job archive
- Allow access to the REST API from all IPs
- enable re-sampling of time-series metric data for long jobs
- Configure three clusters using one local `cc-metric-store`
- Use a sqlite database (this is the default)

``` json
{
    "addr":            "0.0.0.0:443",
    "short-running-jobs-duration": 300,
    "ldap": {
        "url":        "ldaps://hpcldap.rrze.uni-erlangen.de",
        "user_base":   "ou=people,ou=hpc,dc=rrze,dc=uni-erlangen,dc=de",
        "search_dn":   "cn=hpcmonitoring,ou=roadm,ou=profile,ou=hpc,dc=rrze,dc=uni-erlangen,dc=de",
        "user_bind":   "uid={username},ou=people,ou=hpc,dc=rrze,dc=uni-erlangen,dc=de",
        "user_filter": "(&(objectclass=posixAccount))",
        "sync_interval": "24h"
    },
    "jwts": {
        "syncUserOnLogin": true,
        "updateUserOnLogin":true,
        "validateUser": false,
        "trustedIssuer": "https://portal.hpc.fau.de/",
        "max-age": "168h"
    },
    "https-cert-file": "/etc/letsencrypt/live/monitoring.nhr.fau.de/fullchain.pem",
    "https-key-file":  "/etc/letsencrypt/live/monitoring.nhr.fau.de/privkey.pem",
    "user":            "clustercockpit",
    "group":           "clustercockpit",
    "archive": {
        "kind": "file",
        "path": "./var/job-archive",
        "compression": 7,
        "retention": {
            "policy": "none"
        }
    },
    "apiAllowedIPs": [
      "*"
    ],
    "enable-resampling": {
              "trigger": 30,
              "resolutions": [
                        600,
                        300,
                        120,
                         60
                ]
    },
    "emission-constant": 317,
    "clusters": [
        {
            "name": "fritz",
            "metricDataRepository": {
                "kind": "cc-metric-store",
                "url": "http://localhost:8082",
                "token": "XYZ"
            },
            "filterRanges": {
                "numNodes": { "from": 1, "to": 64 },
                "duration": { "from": 0, "to": 86400 },
                "startTime": { "from": "2022-01-01T00:00:00Z", "to": null }
            }
        },
        {
            "name": "alex",
            "metricDataRepository": {
                "kind": "cc-metric-store",
                "url": "http://localhost:8082",
                "token": "XYZ"
            },
            "filterRanges": {
                "numNodes": { "from": 1, "to": 64 },
                "duration": { "from": 0, "to": 86400 },
                "startTime": { "from": "2022-01-01T00:00:00Z", "to": null }
            }
        },
        {
            "name": "woody",
            "metricDataRepository": {
                "kind": "cc-metric-store",
                "url": "http://localhost:8082",
                "token": "XYZ"
            },
            "filterRanges": {
                "numNodes": { "from": 1, "to": 1 },
                "duration": { "from": 0, "to": 172800 },
                "startTime": { "from": "2020-01-01T00:00:00Z", "to": null }
            }
        }
    ]
}
```

The cluster names have to match the clusters configured in the job-archive. The
filter ranges in the cluster configuration affect the filter UI limits in
frontend views and should reflect your typical job properties.

Further reading:

- [Configuration reference]({{< ref "docs/reference/cc-backend/configuration" >}})
- [Authentication Handbook]({{< ref "docs/reference/cc-backend/authentication" >}})

## Job archive

In case you place the job-archive in the `./var` folder create the folder with:

``` bash
mkdir -p ./var/job-archive
```

The job-archive is versioned, the current version is documented in the Release
Notes. Currently you have to create the version file manually when initializing the
job-archive:

``` bash
echo 2 > ./var/job-archive/version.txt
```

### Directory layout

ClusterCockpit supports multiple clusters, for each cluster you need to create a
directory named after the cluster and a `cluster.json` file specifying the metric
list and hardware partitions within the clusters. Hardware partitions are
subsets of a cluster with homogeneous hardware (CPU type, memory capacity, GPUs)
that are called subclusters in ClusterCockpit.

For above configuration the job archive directory hierarchy looks like the
following:

``` text
./var/job-archive/
     version.txt
     fritz/
        cluster.json
     alex/
        cluster.json
     woody/
        cluster.json
```

### `cluster.json`: Basics

The `cluster.json` file contains three top level parts: the name of the cluster,
the metric configuration, and the subcluster list.
You find the latest `cluster.json` schema
[here](https://github.com/ClusterCockpit/cc-backend/blob/master/pkg/schema/schemas/cluster.schema.json).
Basic layout of `cluster.json` files:

``` json
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

- `name`: The metric name. This must match the metric name in `cc-metric-store`!
- `unit`:  The metrics unit. Base can be: `B` (for bytes), `F`  (for flops),
`B/s`, `F/s`, `CPI` (for cycles per instruction), `IPC` (for instructions per
cycle), `Hz`, `W` (for Watts), `°C`, or empty string for no unit.   Prefix can
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
metric thresholds.
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
           21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40,
           41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60,
           61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71
        ],
        "socket": [
            [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
             20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35 ],
            [ 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53,
             54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71 ]
        ],
        "memoryDomain": [
            [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17 ],
            [ 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35 ],
            [ 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53 ],
            [ 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71 ]
        ],
        "core": [
            [ 0 ], [ 1 ], [ 2 ], [ 3 ], [ 4 ], [ 5 ], [ 6 ], [ 7 ], [ 8 ], [ 9 ], [ 10 ],
           [ 11 ], [ 12 ], [ 13 ], [ 14 ], [ 15 ], [ 16 ], [ 17 ], [ 18 ], [ 19 ], [ 20 ],
           [ 21 ], [ 22 ], [ 23 ], [ 24 ], [ 25 ], [ 26 ], [ 27 ], [ 28 ], [ 29 ], [ 30 ],
           [ 31 ], [ 32 ], [ 33 ], [ 34 ], [ 35 ], [ 36 ], [ 37 ], [ 38 ], [ 39 ], [ 40 ],
           [ 41 ], [ 42 ], [ 43 ], [ 44 ], [ 45 ], [ 46 ], [ 47 ], [ 48 ], [ 49 ], [ 50 ],
           [ 51 ], [ 52 ], [ 53 ], [ 54 ], [ 55 ], [ 56 ], [ 57 ], [ 58 ], [ 59 ], [ 60 ],
           [ 61 ], [ 62 ], [ 63 ], [ 64 ], [ 65 ], [ 66 ], [ 67 ], [ 68 ], [ 69 ], [ 70 ], [ 71 ]
        ]
    }
}
```

Since it is tedious to write this by hand, we provide a
[Perl script](https://github.com/ClusterCockpit/cc-backend/blob/master/configs/generate-subcluster.pl)
as part of `cc-backend` that generates a subCluster template. This script only
works if the `LIKWID` tools are installed and in the PATH. You also need the
`LIKWID` library for cc-metric-store. You find instructions on how to install
`LIKWID` [here](https://github.com/RRZE-HPC/likwid/wiki/Build).

The resource ID for cores is the OS processor ID. For GPUs we recommend to use
the PCI-E address as resource ID.

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
         21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40,
         41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60,
         61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80,
         81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100,
        101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116,
        117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127
        ],
        "socket": [
            [
               0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
              21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40,
              41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60,
              61, 62, 63
            ],
            [
              64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80,
              81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100,
             101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116,
             117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127
            ]
        ],
        "memoryDomain": [
            [
              0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
             21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40,
             41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60,
             61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80,
             81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100,
            101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116,
            117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127
            ]
        ],
        "core": [
            [ 0 ], [ 1 ], [ 2 ], [ 3 ], [ 4 ], [ 5 ], [ 6 ], [ 7 ], [ 8 ], [ 9 ], [ 10 ], [ 11 ],
            [ 12 ], [ 13 ], [ 14 ], [ 15 ], [ 16 ], [ 17 ], [ 18 ], [ 19 ], [ 20 ], [ 21 ], [ 22 ],
            [ 23 ], [ 24 ], [ 25 ], [ 26 ], [ 27 ], [ 28 ], [ 29 ], [ 30 ], [ 31 ], [ 32 ], [ 33 ],
            [ 34 ], [ 35 ], [ 36 ], [ 37 ], [ 38 ], [ 39 ], [ 40 ], [ 41 ], [ 42 ], [ 43 ], [ 44 ],
            [ 45 ], [ 46 ], [ 47 ], [ 48 ], [ 49 ], [ 50 ], [ 51 ], [ 52 ], [ 53 ], [ 54 ], [ 55 ],
            [ 56 ], [ 57 ], [ 58 ], [ 59 ], [ 60 ], [ 61 ], [ 62 ], [ 63 ], [ 64 ], [ 65 ], [ 66 ],
            [ 67 ], [ 68 ], [ 69 ], [ 70 ], [ 71 ], [ 73 ], [ 74 ], [ 75 ], [ 76 ], [ 77 ], [ 78 ],
            [ 79 ], [ 80 ], [ 81 ], [ 82 ], [ 83 ], [ 84 ], [ 85 ], [ 86 ], [ 87 ], [ 88 ], [ 89 ],
            [ 90 ], [ 91 ], [ 92 ], [ 93 ], [ 94 ], [ 95 ], [ 96 ], [ 97 ], [ 98 ], [ 99 ], [ 100 ],
           [ 101 ], [ 102 ], [ 103 ], [ 104 ], [ 105 ], [ 106 ], [ 107 ], [ 108 ], [ 109 ], [ 110 ],
           [ 111 ], [ 112 ], [ 113 ], [ 114 ], [ 115 ], [ 116 ], [ 117 ], [ 118 ], [ 119 ], [ 120 ],
           [ 121 ], [ 122 ], [ 123 ], [ 124 ], [ 125 ], [ 126 ], [ 127 ]
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

You have to ensure that the metric collector also uses the PCI-E address as a
resource ID.

## Environment variables

Secrets are provided in terms of environment variables. The only two required
secrets are `JWT_PUBLIC_KEY` and `JWT_PRIVATE_KEY` used for signing generated
JWT tokens and validate JWT authentication.

Please refer to the
[environment reference]({{< ref "docs/reference/cc-backend/environment" >}})
for details.
