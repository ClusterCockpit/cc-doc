---
title: NATS messaging
description: NATS message broker infrastructure
categories: [cc-backend, cc-metric-store, cc-metric-collector]
tags: [Developer, Admin]
---

## Introduction

[NATS](https://docs.nats.io/) is a powerful messaging solution supporting many
paradigms. Since it is itself implemented in Golang it provides excellent
support for Golang based applications. Currently NATS is offered in most
ClusterCockpit applications as an alternative to the default REST API.
We plan to make NATS the default way to communicate within the ClusterCockpit
framework in the future.

Advantages for us to use NATS:

- Scalable and low overhead messaging infrastructure
- Flexible configuration free setup of message sources and consumers
- Builtin zero trust JWT-based authentication system
- Simple message filtering based on hierarchical subject names
- Multicast and message queue support

## NATS API

When `api-subjects` is configured in the `main` section of `config.json`,
cc-backend subscribes to the specified NATS subjects for job events and node
state updates. This replaces the REST API endpoints for `start_job` and
`stop_job` -- those REST endpoints are automatically disabled when NATS subjects
are configured.

### Message Format

All NATS messages use [InfluxDB line protocol](https://docs.influxdata.com/influxdb/v2.0/reference/syntax/line-protocol/)
format:

```
measurement,tag1=value1,tag2=value2 field1=value1 timestamp
```

### Job Events

Job start/stop events use the `job` measurement with a `function` tag:

**Start a job:**

```
job,function=start_job event="{\"jobId\":1001,\"user\":\"testuser\",\"cluster\":\"fritz\",\"subCluster\":\"spr\",\"partition\":\"normal\",\"project\":\"myproject\",\"numNodes\":2,\"numHwthreads\":128,\"numAcc\":0,\"exclusive\":1,\"walltime\":86400,\"resources\":[{\"hostname\":\"node01\"},{\"hostname\":\"node02\"}],\"startTime\":1234567890}" 1234567890000000000
```

**Stop a job:**

```
job,function=stop_job event="{\"jobId\":1001,\"cluster\":\"fritz\",\"stopTime\":1234569000,\"state\":\"completed\"}" 1234569000000000000
```

The JSON payload in the `event` field follows the `schema.Job` structure for
start events and the `StopJobAPIRequest` structure for stop events.

### Node State Events

Node state updates use the `nodestate` measurement:

```
nodestate event="{\"cluster\":\"fritz\",\"nodes\":[{\"hostname\":\"node01\",\"states\":[\"idle\"],\"cpusAllocated\":0,\"memoryAllocated\":0,\"gpusAllocated\":0,\"jobsRunning\":0},{\"hostname\":\"node02\",\"states\":[\"allocated\"],\"cpusAllocated\":128,\"memoryAllocated\":256000,\"gpusAllocated\":4,\"jobsRunning\":1}]}" 1234567890000000000
```

Each node entry in the `nodes` array supports the following fields:

| Field             | Type     | Description                                         |
|-------------------|----------|-----------------------------------------------------|
| `hostname`        | string   | Node hostname                                       |
| `states`          | []string | Scheduler state strings (allocated, idle, down, mixed, reserved) |
| `cpusAllocated`   | integer  | Number of allocated CPUs                             |
| `memoryAllocated` | integer  | Allocated memory in MB                               |
| `gpusAllocated`   | integer  | Number of allocated GPUs                             |
| `jobsRunning`     | integer  | Number of running jobs                               |

### Configuration

To enable the NATS API, configure both the `nats` and `api-subjects` sections:

```json
{
  "main": {
    "api-subjects": {
      "subject-job-event": "cc.job.event",
      "subject-node-state": "cc.node.state"
    }
  },
  "nats": {
    "address": "nats://localhost:4222",
    "username": "root",
    "password": "root"
  }
}
```

## Authentication

NATS provides a sophisticated [authentication scheme](https://docs.nats.io/running-a-nats-service/configuration/securing_nats/auth_intro/jwt) based on JWT tokens and NKeys.
It provides the [nsc tool](https://docs.nats.io/using-nats/nats-tools/nsc) to
create and manage tokens supporting fine grained authentication and
authorization control.
