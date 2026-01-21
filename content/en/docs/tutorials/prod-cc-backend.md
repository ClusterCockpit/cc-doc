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

```bash
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
- enable re-sampling of time-series metric data for long jobs
- Enable NATS for job and metric store APIs
- Set metric in memory retention to 48h
- Set upper memory capping for internal metric store to 100GB
- Enable archiving of metric data
- Using S3 as job archive backend. Note: The file based archive in
  `./var/job-archive` is the default.

Not included below but set by the default settings:

- Use compression for metric data files in job archive
- Allow access to the REST API from all IPs

```json
{
  "main": {
    "addr": "0.0.0.0:443",
    "https-cert-file": "/etc/letsencrypt/live/url/fullchain.pem",
    "https-key-file": "/etc/letsencrypt/live/url/privkey.pem",
    "user": "clustercockpit",
    "group": "clustercockpit",
    "short-running-jobs-duration": 300,
    "enable-job-taggers": true,
    "resampling": {
      "minimum-points": 600,
      "trigger": 180,
      "resolutions": [240, 60]
    },
    "api-subjects": {
      "subject-job-event": "cc.job.event",
      "subject-node-state": "cc.node.state"
    }
  },
  "nats": {
    "address": "nats://x.x.x.x:4222",
    "username": "root",
    "password": "root"
  },
  "auth": {
    "jwts": {
      "max-age": "2000h"
    },
    "ldap": {
      "url": "ldaps://hpcldap.rrze.uni-erlangen.de",
      "user_base": "ou=people,ou=hpc,dc=rz,dc=uni,dc=de",
      "search_dn": "cn=hpcmonitoring,ou=roadm,ou=profile,ou=hpc,dc=rz,dc=uni,dc=de",
      "user_bind": "uid={username},ou=people,ou=hpc,dc=rrze,dc=uni,dc=de",
      "user_filter": "(&(objectclass=posixAccount))",
      "sync_interval": "24h"
    }
  },
  "cron": {
    "commit-job-worker": "1m",
    "duration-worker": "5m",
    "footprint-worker": "10m"
  },
  "archive": {
    "kind": "s3",
    "endpoint": "http://x.x.x.x",
    "bucket": "jobarchive",
    "access-key": "xx",
    "secret-key": "xx",
    "retention": {
      "policy": "move",
      "age": 365,
      "location": "./var/archive"
    }
  },
  "metric-store": {
    "memory-cap": 100,
    "retention-in-memory": "48h",
    "cleanup": {
      "mode": "archive",
      "directory": "./var/archive"
    },
    "nats-subscriptions": [
      {
        "subscribe-to": "hpc-nats",
        "cluster-tag": "fritz"
      },
      {
        "subscribe-to": "hpc-nats",
        "cluster-tag": "alex"
      }
    ]
  },
  "ui-file": "ui-config.json"
}
```

Further reading:

- [Configuration reference]({{< ref "docs/reference/cc-backend/configuration" >}})
- [Authentication Handbook]({{< ref "docs/reference/cc-backend/authentication" >}})
- [Job-Archive Handbook]({{< ref "docs/reference/cc-backend/jobarchive" >}})

## Environment variables

Secrets are provided in terms of environment variables. The only two required
secrets are `JWT_PUBLIC_KEY` and `JWT_PRIVATE_KEY` used for signing generated
JWT tokens and validate JWT authentication.

Please refer to the
[environment reference]({{< ref "docs/reference/cc-backend/environment" >}})
for details.
