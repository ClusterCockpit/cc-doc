---
title: Decide on metric list
weight: 10
description: Planning and naming the metrics
categories: [ClusterCockpit]
tags: [Admin]
---

## Introduction

To decide on a sensible and meaningful set of metrics is deciding factor for how
useful the monitoring will be. As part of a collaborative project several
academic HPC centers came up with a minimal set of metrics including their
naming. To use a consistent naming is crucial for establishing what metrics mean
and we urge you to adhere to the metric names suggested there. You can find this
list as part of the ClusterCockpit job data structure schemas.

## Required Metrics

### Flop throughput rate: `flops_any`

### Memory bandwidth: `mem_bw`

### Memory capacity used: `mem_used`

### Requested cpu core utilization: `cpu_load`

### Total fast network bandwidth: `net_bw`

### Total file IO bandwidth: `file_bw`

## Recommended CPU Metrics

### Instructions throughput in cycles: `ipc`

### User active CPU core utilization: `cpu_user`

### Double precision flop throughput rate: `flops_dp`

### Single precision flop throughput rate: `flops_sp`

### Average core frequency: `clock`

### CPU power consumption: `rapl_power`

## Recommended GPU Metrics

### GPU utilization: `acc_used`

### GPU memory capacity used: `acc_mem_used`

### GPU power consumption: `acc_power`

## Recommended node level metrics

### Ethernet read bandwidth: `eth_read_bw`

### Ethernet write bandwidth: `eth_write_bw`

### Fast network read bandwidth: `ic_read_bw`

### Fast network write bandwidth: `ic_write_bw`

## File system metrics

{{< alert color="warning" title="Warning" >}}
A file system metric tree is currently not yet supported in `cc-backend`
{{< /alert >}}

In the schema a tree of file system metrics is suggested. This allows to provide
a similar set of metrics for different file systems used in a cluster. The file
system type names suggested are:

- nfs
- lustre
- gpfs
- nvme
- ssd
- hdd
- beegfs

### File system read bandwidth: `read_bw`

### File system write bandwidth: `write_bw`

