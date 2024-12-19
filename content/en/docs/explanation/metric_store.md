---
title: Metric Store
description: >
  An architectural view of the CC Metric Store and working of its background workers.
categories: [cc-metric-store]
tags: [Developer, General]
---

## Introduction

**CCMS (Cluster Cockpit Metric Store)** is a simple in-memory time series
database. It stores the data about the nodes in your cluster for a specific
interval of days. Data about your nodes can be collected with various
instrumentation tools like RAPL, LIKWID, PAPI etc. Instrumentation tools can
collect data like memory bandwidth, flops, clock frequency, CPU usage etc. After
a specified number of days, the data from the in-memory database will be written
to disk, archived and released from the in-memory database. In this
documentation, we will explain in-detail working of the CCMS components and the
outline of the documentation is as follows:

- Present the structure of the metric store.
- Explain background workers.

Let us get started with the very basic understanding of how CCMS is structured
and how it manages data over time.

General tree structure can be as follows:

```txt
root
|-----cluster
| |------node -> [node-metrics]
| |  |--components -> [node-level-metrics]
| |  |--components -> [node-level-metrics]
| |
| |------node -> [node-metrics]
|   |--components -> [node-level-metrics]
|   |--components -> [node-level-metrics]
|
|-----cluster
 |-----node -> [node-metrics]
 | |--components -> [node-level-metrics]
 | |--components -> [node-level-metrics]
 |
 |-----node -> [node-metrics]
  |--components -> [node-level-metrics]
  |--components -> [node-level-metrics]
```

A simple tree representation with example:

```txt
root
|-----alex
| |------a903 -> [mem_cached,cpu_idle,nfs4_read]
| |  |--hwthread01 -> [cpu_load,cpu_user,flops_any]
| |  |--accelerator01 -> [mem_bw,mem_used,flops_any]
| |
| |------a322 -> [mem_cached,cpu_idle,nfs4_read]
|   |--hwthread42 -> [cpu_load,cpu_user,flops_any]
|   |--accelerator05 -> [mem_bw,mem_used,flops_any]
|
|-----fritz
 |-----f104 -> [mem_cached,cpu_idle,nfs4_read]
 | |--hwthread35 -> [cpu_load,cpu_user,flops_any]
 | |--socket02 -> [cpu_load,cpu_user,flops_any]
 |
 |-----f576 -> [mem_cached,cpu_idle,nfs4_read]
  |--hwthread47 -> [cpu_load,cpu_user,flops_any]
  |--cpu01 -> [cpu_load,cpu_user,flops_any]
```

Example tree structure of CCMS containing 2 clusters 'alex' and 'fritz' that
contains each of its own nodes and each node contains its components. Each node
and its component contains metrics. a903 is an example of a node and hwthread01
& accelerator01 is a node-level component. Each node will have its own metrics
as well as node-level components will also have their own metrics i.e.
node-level-metrics.

![](https://pad.nhr.fau.de/uploads/854adf04-9198-44dd-ae99-2218628cd2f0.png)

## Internal data structures used in cc-metric-store

A representation of the Level and Buffer data structure with the buffer chain.

![](https://pad.nhr.fau.de/uploads/dd5c123c-2f8c-4d7a-b566-55e058d803fc.png)

From our previous example, we move from a simplistic view to a more realistic
view. Each buffer for the given metric holds up to BUFFER_CAP elements in its
data array. Usually the BUFFER_CAP is 512 elements, so for float64 elements, the
buffer size is 4KB, which is also the size of the page in general. Below you can
find all the data structures and its associated member variables. In our example,
the start time in buffer is exactly 512 epoch seconds apart. Older buffers are
pushed to the previous of the new buffer. This creates a chain of buffers for
every level.

Data structure used to hold the data in memory:

- MemoryStore

```go
MemoryStore struct {
    // Parses and stores the metrics from config.json
    Metrics HashMap[string][MetricConfig]

    // Initial root level.
    root    Level
}
```

- Level

```go
// From our example, alex, fritz, a903, a322, hwthreads01 are all of Level data stucture.
Level struct {
    // Stores the metrics for the level.
    // From our example, mem_cached, flops_any are of Buffer data structure.
    metrics  []*buffer

    // Stores
    children HashMap[string][*Level]
}
```

- Buffer

```go
buffer struct {
    // Pointer to previous buffer
    prev      *buffer

    // Pointer to next buffer
    next      *buffer

    // Array of floats to store

    // Interval in seconds at which measurements will arive.
    frequency int64

    // Buffer's start time stored in epoch seconds
    start     int

    // If true, this buffer will be skipped for file checkpointing
    archived  bool

    closed    bool
}
```

- MetricConfig

```go
MetricConfig struct {
    // Interval in seconds at which measurements will arive.
    // frequency of 60 means the the timestep/resolution is 60 seconds.
    Frequency     int

    // Can be 'sum', 'avg' or null. Describes how to aggregate metrics from the same timestep over the hierarchy.
    Aggregation   String

    // Private, used internally...
    Offset        int
}
```

## Background workers

Background workers are separate threads spawned for each background task like:

- Data retention -> This background worker uses `retention-on-memory` parameter
  in the `config.json` and sets a looping interval for the user-given time. It
  ticks until the given interval is reached and then releases all the Buffers in
  CCMS which are less than the user-given time.

  ![](https://pad.nhr.fau.de/uploads/9fe3abca-ed77-4bda-861a-856e07196947.png)

In this example, we assume that we insert data continuously in CCMS with
retention period of 48 hrs. So the background worker will always check with an
interval of retention-period/2. In the example, it is necessary to check every
24 hrs so that the CCMS can retain data of 48 hrs overall. Once it reaches 72
hrs, background worker releases the first 24 hours of data from the in-memory
database.

- Data check pointing -> This background worker uses `interval` from
  the `checkpoints` parameter in the `config.json` and sets a looping interval for
  the user-given time. It ticks until the given interval is reached and creates
  local backups of the data from the CCMS to the disk. The check pointed files can
  be found at the user-defined `directory` sub-parameter from the `checkpoints`
  parameter in the `config.json` file. Check pointing does not mean removing the
  data from the in-memory database. The data from the memory will only be released
  until retention period is reached.
- Data archiving -> This background worker uses `interval` from the `archive`
  parameter in the `config.json` and sets a looping interval for the user-given
  time. It ticks until the given interval is reached and zips all the checkpointed
  files which are before the user-given time in the `interval` sub-parameter. Once
  the checkpointed files are zipped, they are deleted from the checkpointing
  directory.
- Graceful shutdown handler -> This is a special background worker that detects
  system or keyboard interrupts like Ctrl+C or Ctrl+Z. In case of an interrupt, it
  is essential to save the data from the in-memory database. There can be a case
  when the CCMS contains data just in the memory and it has not been checkpointed.
  So this background worker scans for the Buffers that have not been checkpointed
  and writes them to the checkpoint files before shutting down the CCMS.

## Reusing the buffers in cc-metric-store

This section explain how CCMS handles the buffer re usability once the buffers
are released by the retention background worker.

![](https://pad.nhr.fau.de/uploads/46ea5b35-4d19-4c71-8117-392e79e4dfec.png)

In this example, we extend the previous example and assume that the retention
background worker releases every last buffer from each level i.e. node and
node-level metrics. Each buffer that is about to be unlinked from the buffer
chain will not be freed from memory, but instead will be unlinked and stored in
the memory pool as shown. This allow buffer reusability whenever the buffers
reaches the BUFFER_CAP limit and each metric requests new buffers.
