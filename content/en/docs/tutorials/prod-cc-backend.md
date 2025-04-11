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
- enable re-sampling of timeseries metric data for long jobs
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

The `cluster.json` file contains two top level parts: the metric configuration
and the subcluster list.
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

### `cluster.json`: Subcluster configuration

## Environment variables

Secrets are provided in terms of environment variables. The only two required
secrets are `JWT_PUBLIC_KEY` and `JWT_PRIVATE_KEY` used for signing generated
JWT tokens and validate JWT authentication.

Please refer to the
[environment reference]({{< ref "docs/reference/cc-backend/environment" >}})
for details.
