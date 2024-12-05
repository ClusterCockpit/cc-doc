---
title: Job Archive Metadata Schema
description: ClusterCockpit Job Archive Metadata Schema Reference
categories: [cc-backend]
tags: [Backend, Archive]
weight: 6
---

The following schema in its raw form can be found in the [ClusterCockpit GitHub](https://github.com/ClusterCockpit/cc-backend/tree/master/pkg/schema/schemas) repository.

{{< alert title="Manual Updates">}}
  Changes to the original JSON schema found in the repository are not automatically rendered in this reference documentation.</br></br>
  **Last Update:** 04.12.2024
{{< /alert >}}

# Job meta data

- [1. Property `Job meta data > jobId`](#jobId)
- [2. Property `Job meta data > user`](#user)
- [3. Property `Job meta data > project`](#project)
- [4. Property `Job meta data > cluster`](#cluster)
- [5. Property `Job meta data > subCluster`](#subCluster)
- [6. Property `Job meta data > partition`](#partition)
- [7. Property `Job meta data > arrayJobId`](#arrayJobId)
- [8. Property `Job meta data > numNodes`](#numNodes)
- [9. Property `Job meta data > numHwthreads`](#numHwthreads)
- [10. Property `Job meta data > numAcc`](#numAcc)
- [11. Property `Job meta data > exclusive`](#exclusive)
- [12. Property `Job meta data > monitoringStatus`](#monitoringStatus)
- [13. Property `Job meta data > smt`](#smt)
- [14. Property `Job meta data > walltime`](#walltime)
- [15. Property `Job meta data > jobState`](#jobState)
- [16. Property `Job meta data > startTime`](#startTime)
- [17. Property `Job meta data > duration`](#duration)
- [18. Property `Job meta data > resources`](#resources)
  - [18.1. Job meta data > resources > resources items](#resources_items)
    - [18.1.1. Property `Job meta data > resources > resources items > hostname`](#resources_items_hostname)
    - [18.1.2. Property `Job meta data > resources > resources items > hwthreads`](#resources_items_hwthreads)
      - [18.1.2.1. Job meta data > resources > resources items > hwthreads > hwthreads items](#resources_items_hwthreads_items)
    - [18.1.3. Property `Job meta data > resources > resources items > accelerators`](#resources_items_accelerators)
      - [18.1.3.1. Job meta data > resources > resources items > accelerators > accelerators items](#resources_items_accelerators_items)
    - [18.1.4. Property `Job meta data > resources > resources items > configuration`](#resources_items_configuration)
- [19. Property `Job meta data > metaData`](#metaData)
  - [19.1. Property `Job meta data > metaData > jobScript`](#metaData_jobScript)
  - [19.2. Property `Job meta data > metaData > jobName`](#metaData_jobName)
  - [19.3. Property `Job meta data > metaData > slurmInfo`](#metaData_slurmInfo)
- [20. Property `Job meta data > tags`](#tags)
  - [20.1. Job meta data > tags > tags items](#tags_items)
    - [20.1.1. Property `Job meta data > tags > tags items > name`](#tags_items_name)
    - [20.1.2. Property `Job meta data > tags > tags items > type`](#tags_items_type)
- [21. Property `Job meta data > statistics`](#statistics)
  - [21.1. Property `Job meta data > statistics > mem_used`](#statistics_mem_used)
  - [21.2. Property `Job meta data > statistics > cpu_load`](#statistics_cpu_load)
  - [21.3. Property `Job meta data > statistics > flops_any`](#statistics_flops_any)
  - [21.4. Property `Job meta data > statistics > mem_bw`](#statistics_mem_bw)
  - [21.5. Property `Job meta data > statistics > net_bw`](#statistics_net_bw)
  - [21.6. Property `Job meta data > statistics > file_bw`](#statistics_file_bw)
  - [21.7. Property `Job meta data > statistics > ipc`](#statistics_ipc)
  - [21.8. Property `Job meta data > statistics > cpu_user`](#statistics_cpu_user)
  - [21.9. Property `Job meta data > statistics > flops_dp`](#statistics_flops_dp)
  - [21.10. Property `Job meta data > statistics > flops_sp`](#statistics_flops_sp)
  - [21.11. Property `Job meta data > statistics > rapl_power`](#statistics_rapl_power)
  - [21.12. Property `Job meta data > statistics > acc_used`](#statistics_acc_used)
  - [21.13. Property `Job meta data > statistics > acc_mem_used`](#statistics_acc_mem_used)
  - [21.14. Property `Job meta data > statistics > acc_power`](#statistics_acc_power)
  - [21.15. Property `Job meta data > statistics > clock`](#statistics_clock)
  - [21.16. Property `Job meta data > statistics > eth_read_bw`](#statistics_eth_read_bw)
  - [21.17. Property `Job meta data > statistics > eth_write_bw`](#statistics_eth_write_bw)
  - [21.18. Property `Job meta data > statistics > ic_rcv_packets`](#statistics_ic_rcv_packets)
  - [21.19. Property `Job meta data > statistics > ic_send_packets`](#statistics_ic_send_packets)
  - [21.20. Property `Job meta data > statistics > ic_read_bw`](#statistics_ic_read_bw)
  - [21.21. Property `Job meta data > statistics > ic_write_bw`](#statistics_ic_write_bw)
  - [21.22. Property `Job meta data > statistics > filesystems`](#statistics_filesystems)
    - [21.22.1. Job meta data > statistics > filesystems > filesystems items](#statistics_filesystems_items)
      - [21.22.1.1. Property `Job meta data > statistics > filesystems > filesystems items > name`](#statistics_filesystems_items_name)
      - [21.22.1.2. Property `Job meta data > statistics > filesystems > filesystems items > type`](#statistics_filesystems_items_type)
      - [21.22.1.3. Property `Job meta data > statistics > filesystems > filesystems items > read_bw`](#statistics_filesystems_items_read_bw)
      - [21.22.1.4. Property `Job meta data > statistics > filesystems > filesystems items > write_bw`](#statistics_filesystems_items_write_bw)
      - [21.22.1.5. Property `Job meta data > statistics > filesystems > filesystems items > read_req`](#statistics_filesystems_items_read_req)
      - [21.22.1.6. Property `Job meta data > statistics > filesystems > filesystems items > write_req`](#statistics_filesystems_items_write_req)
      - [21.22.1.7. Property `Job meta data > statistics > filesystems > filesystems items > inodes`](#statistics_filesystems_items_inodes)
      - [21.22.1.8. Property `Job meta data > statistics > filesystems > filesystems items > accesses`](#statistics_filesystems_items_accesses)
      - [21.22.1.9. Property `Job meta data > statistics > filesystems > filesystems items > fsync`](#statistics_filesystems_items_fsync)
      - [21.22.1.10. Property `Job meta data > statistics > filesystems > filesystems items > create`](#statistics_filesystems_items_create)
      - [21.22.1.11. Property `Job meta data > statistics > filesystems > filesystems items > open`](#statistics_filesystems_items_open)
      - [21.22.1.12. Property `Job meta data > statistics > filesystems > filesystems items > close`](#statistics_filesystems_items_close)
      - [21.22.1.13. Property `Job meta data > statistics > filesystems > filesystems items > seek`](#statistics_filesystems_items_seek)

**Title:** Job meta data

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** Meta data information of a HPC job

| Property                                 | Pattern | Type             | Deprecated | Definition | Title/Description                                                                                                                                |
| ---------------------------------------- | ------- | ---------------- | ---------- | ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| + [jobId](#jobId )                       | No      | integer          | No         | -          | The unique identifier of a job                                                                                                                   |
| + [user](#user )                         | No      | string           | No         | -          | The unique identifier of a user                                                                                                                  |
| + [project](#project )                   | No      | string           | No         | -          | The unique identifier of a project                                                                                                               |
| + [cluster](#cluster )                   | No      | string           | No         | -          | The unique identifier of a cluster                                                                                                               |
| + [subCluster](#subCluster )             | No      | string           | No         | -          | The unique identifier of a sub cluster                                                                                                           |
| - [partition](#partition )               | No      | string           | No         | -          | The Slurm partition to which the job was submitted                                                                                               |
| - [arrayJobId](#arrayJobId )             | No      | integer          | No         | -          | The unique identifier of an array job                                                                                                            |
| + [numNodes](#numNodes )                 | No      | integer          | No         | -          | Number of nodes used                                                                                                                             |
| - [numHwthreads](#numHwthreads )         | No      | integer          | No         | -          | Number of HWThreads used                                                                                                                         |
| - [numAcc](#numAcc )                     | No      | integer          | No         | -          | Number of accelerators used                                                                                                                      |
| + [exclusive](#exclusive )               | No      | integer          | No         | -          | Specifies how nodes are shared. 0 - Shared among multiple jobs of multiple users, 1 - Job exclusive, 2 - Shared among multiple jobs of same user |
| - [monitoringStatus](#monitoringStatus ) | No      | integer          | No         | -          | State of monitoring system during job run                                                                                                        |
| - [smt](#smt )                           | No      | integer          | No         | -          | SMT threads used by job                                                                                                                          |
| - [walltime](#walltime )                 | No      | integer          | No         | -          | Requested walltime of job in seconds                                                                                                             |
| + [jobState](#jobState )                 | No      | enum (of string) | No         | -          | Final state of job                                                                                                                               |
| + [startTime](#startTime )               | No      | integer          | No         | -          | Start epoch time stamp in seconds                                                                                                                |
| + [duration](#duration )                 | No      | integer          | No         | -          | Duration of job in seconds                                                                                                                       |
| + [resources](#resources )               | No      | array of object  | No         | -          | Resources used by job                                                                                                                            |
| - [metaData](#metaData )                 | No      | object           | No         | -          | Additional information about the job                                                                                                             |
| - [tags](#tags )                         | No      | array of object  | No         | -          | List of tags                                                                                                                                     |
| + [statistics](#statistics )             | No      | object           | No         | -          | Job statistic data                                                                                                                               |

## <a name="jobId"></a>1. Property `Job meta data > jobId`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

**Description:** The unique identifier of a job

## <a name="user"></a>2. Property `Job meta data > user`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** The unique identifier of a user

## <a name="project"></a>3. Property `Job meta data > project`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** The unique identifier of a project

## <a name="cluster"></a>4. Property `Job meta data > cluster`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** The unique identifier of a cluster

## <a name="subCluster"></a>5. Property `Job meta data > subCluster`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** The unique identifier of a sub cluster

## <a name="partition"></a>6. Property `Job meta data > partition`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** The Slurm partition to which the job was submitted

## <a name="arrayJobId"></a>7. Property `Job meta data > arrayJobId`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

**Description:** The unique identifier of an array job

## <a name="numNodes"></a>8. Property `Job meta data > numNodes`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

**Description:** Number of nodes used

| Restrictions |        |
| ------------ | ------ |
| **Minimum**  | &gt; 0 |

## <a name="numHwthreads"></a>9. Property `Job meta data > numHwthreads`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

**Description:** Number of HWThreads used

| Restrictions |        |
| ------------ | ------ |
| **Minimum**  | &gt; 0 |

## <a name="numAcc"></a>10. Property `Job meta data > numAcc`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

**Description:** Number of accelerators used

| Restrictions |        |
| ------------ | ------ |
| **Minimum**  | &gt; 0 |

## <a name="exclusive"></a>11. Property `Job meta data > exclusive`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

**Description:** Specifies how nodes are shared. 0 - Shared among multiple jobs of multiple users, 1 - Job exclusive, 2 - Shared among multiple jobs of same user

| Restrictions |        |
| ------------ | ------ |
| **Minimum**  | &ge; 0 |
| **Maximum**  | &le; 2 |

## <a name="monitoringStatus"></a>12. Property `Job meta data > monitoringStatus`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

**Description:** State of monitoring system during job run

## <a name="smt"></a>13. Property `Job meta data > smt`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

**Description:** SMT threads used by job

## <a name="walltime"></a>14. Property `Job meta data > walltime`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

**Description:** Requested walltime of job in seconds

| Restrictions |        |
| ------------ | ------ |
| **Minimum**  | &gt; 0 |

## <a name="jobState"></a>15. Property `Job meta data > jobState`

|              |                    |
| ------------ | ------------------ |
| **Type**     | `enum (of string)` |
| **Required** | Yes                |

**Description:** Final state of job

Must be one of:
* "completed"
* "failed"
* "cancelled"
* "stopped"
* "out_of_memory"
* "timeout"

## <a name="startTime"></a>16. Property `Job meta data > startTime`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

**Description:** Start epoch time stamp in seconds

| Restrictions |        |
| ------------ | ------ |
| **Minimum**  | &gt; 0 |

## <a name="duration"></a>17. Property `Job meta data > duration`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

**Description:** Duration of job in seconds

| Restrictions |        |
| ------------ | ------ |
| **Minimum**  | &gt; 0 |

## <a name="resources"></a>18. Property `Job meta data > resources`

|              |                   |
| ------------ | ----------------- |
| **Type**     | `array of object` |
| **Required** | Yes               |

**Description:** Resources used by job

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be     | Description |
| ----------------------------------- | ----------- |
| [resources items](#resources_items) | -           |

### <a name="resources_items"></a>18.1. Job meta data > resources > resources items

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

| Property                                           | Pattern | Type             | Deprecated | Definition | Title/Description                     |
| -------------------------------------------------- | ------- | ---------------- | ---------- | ---------- | ------------------------------------- |
| + [hostname](#resources_items_hostname )           | No      | string           | No         | -          | -                                     |
| - [hwthreads](#resources_items_hwthreads )         | No      | array of integer | No         | -          | List of OS processor ids              |
| - [accelerators](#resources_items_accelerators )   | No      | array of string  | No         | -          | List of of accelerator device ids     |
| - [configuration](#resources_items_configuration ) | No      | string           | No         | -          | The configuration options of the node |

#### <a name="resources_items_hostname"></a>18.1.1. Property `Job meta data > resources > resources items > hostname`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

#### <a name="resources_items_hwthreads"></a>18.1.2. Property `Job meta data > resources > resources items > hwthreads`

|              |                    |
| ------------ | ------------------ |
| **Type**     | `array of integer` |
| **Required** | No                 |

**Description:** List of OS processor ids

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be                     | Description |
| --------------------------------------------------- | ----------- |
| [hwthreads items](#resources_items_hwthreads_items) | -           |

##### <a name="resources_items_hwthreads_items"></a>18.1.2.1. Job meta data > resources > resources items > hwthreads > hwthreads items

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

#### <a name="resources_items_accelerators"></a>18.1.3. Property `Job meta data > resources > resources items > accelerators`

|              |                   |
| ------------ | ----------------- |
| **Type**     | `array of string` |
| **Required** | No                |

**Description:** List of of accelerator device ids

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be                           | Description |
| --------------------------------------------------------- | ----------- |
| [accelerators items](#resources_items_accelerators_items) | -           |

##### <a name="resources_items_accelerators_items"></a>18.1.3.1. Job meta data > resources > resources items > accelerators > accelerators items

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

#### <a name="resources_items_configuration"></a>18.1.4. Property `Job meta data > resources > resources items > configuration`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** The configuration options of the node

## <a name="metaData"></a>19. Property `Job meta data > metaData`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** Additional information about the job

| Property                            | Pattern | Type   | Deprecated | Definition | Title/Description                                   |
| ----------------------------------- | ------- | ------ | ---------- | ---------- | --------------------------------------------------- |
| - [jobScript](#metaData_jobScript ) | No      | string | No         | -          | The batch script of the job                         |
| - [jobName](#metaData_jobName )     | No      | string | No         | -          | Slurm Job name                                      |
| - [slurmInfo](#metaData_slurmInfo ) | No      | string | No         | -          | Additional slurm infos as show by scontrol show job |

### <a name="metaData_jobScript"></a>19.1. Property `Job meta data > metaData > jobScript`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** The batch script of the job

### <a name="metaData_jobName"></a>19.2. Property `Job meta data > metaData > jobName`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** Slurm Job name

### <a name="metaData_slurmInfo"></a>19.3. Property `Job meta data > metaData > slurmInfo`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** Additional slurm infos as show by scontrol show job

## <a name="tags"></a>20. Property `Job meta data > tags`

|              |                   |
| ------------ | ----------------- |
| **Type**     | `array of object` |
| **Required** | No                |

**Description:** List of tags

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | True               |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be | Description |
| ------------------------------- | ----------- |
| [tags items](#tags_items)       | -           |

### <a name="tags_items"></a>20.1. Job meta data > tags > tags items

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

| Property                    | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| + [name](#tags_items_name ) | No      | string | No         | -          | -                 |
| + [type](#tags_items_type ) | No      | string | No         | -          | -                 |

#### <a name="tags_items_name"></a>20.1.1. Property `Job meta data > tags > tags items > name`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

#### <a name="tags_items_type"></a>20.1.2. Property `Job meta data > tags > tags items > type`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

## <a name="statistics"></a>21. Property `Job meta data > statistics`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | Yes              |
| **Additional properties** | Any type allowed |

**Description:** Job statistic data

| Property                                          | Pattern | Type            | Deprecated | Definition                                     | Title/Description                                    |
| ------------------------------------------------- | ------- | --------------- | ---------- | ---------------------------------------------- | ---------------------------------------------------- |
| + [mem_used](#statistics_mem_used )               | No      | object          | No         | In embedfs://job-metric-statistics.schema.json | Memory capacity used (required)                      |
| + [cpu_load](#statistics_cpu_load )               | No      | object          | No         | In embedfs://job-metric-statistics.schema.json | CPU requested core utilization (load 1m) (required)  |
| + [flops_any](#statistics_flops_any )             | No      | object          | No         | In embedfs://job-metric-statistics.schema.json | Total flop rate with DP flops scaled up (required)   |
| + [mem_bw](#statistics_mem_bw )                   | No      | object          | No         | In embedfs://job-metric-statistics.schema.json | Main memory bandwidth (required)                     |
| - [net_bw](#statistics_net_bw )                   | No      | object          | No         | In embedfs://job-metric-statistics.schema.json | Total fast interconnect network bandwidth (required) |
| - [file_bw](#statistics_file_bw )                 | No      | object          | No         | In embedfs://job-metric-statistics.schema.json | Total file IO bandwidth (required)                   |
| - [ipc](#statistics_ipc )                         | No      | object          | No         | In embedfs://job-metric-statistics.schema.json | Instructions executed per cycle                      |
| + [cpu_user](#statistics_cpu_user )               | No      | object          | No         | In embedfs://job-metric-statistics.schema.json | CPU user active core utilization                     |
| - [flops_dp](#statistics_flops_dp )               | No      | object          | No         | In embedfs://job-metric-statistics.schema.json | Double precision flop rate                           |
| - [flops_sp](#statistics_flops_sp )               | No      | object          | No         | In embedfs://job-metric-statistics.schema.json | Single precision flops rate                          |
| - [rapl_power](#statistics_rapl_power )           | No      | object          | No         | In embedfs://job-metric-statistics.schema.json | CPU power consumption                                |
| - [acc_used](#statistics_acc_used )               | No      | object          | No         | In embedfs://job-metric-statistics.schema.json | GPU utilization                                      |
| - [acc_mem_used](#statistics_acc_mem_used )       | No      | object          | No         | In embedfs://job-metric-statistics.schema.json | GPU memory capacity used                             |
| - [acc_power](#statistics_acc_power )             | No      | object          | No         | In embedfs://job-metric-statistics.schema.json | GPU power consumption                                |
| - [clock](#statistics_clock )                     | No      | object          | No         | In embedfs://job-metric-statistics.schema.json | Average core frequency                               |
| - [eth_read_bw](#statistics_eth_read_bw )         | No      | object          | No         | In embedfs://job-metric-statistics.schema.json | Ethernet read bandwidth                              |
| - [eth_write_bw](#statistics_eth_write_bw )       | No      | object          | No         | In embedfs://job-metric-statistics.schema.json | Ethernet write bandwidth                             |
| - [ic_rcv_packets](#statistics_ic_rcv_packets )   | No      | object          | No         | In embedfs://job-metric-statistics.schema.json | Network interconnect read packets                    |
| - [ic_send_packets](#statistics_ic_send_packets ) | No      | object          | No         | In embedfs://job-metric-statistics.schema.json | Network interconnect send packet                     |
| - [ic_read_bw](#statistics_ic_read_bw )           | No      | object          | No         | In embedfs://job-metric-statistics.schema.json | Network interconnect read bandwidth                  |
| - [ic_write_bw](#statistics_ic_write_bw )         | No      | object          | No         | In embedfs://job-metric-statistics.schema.json | Network interconnect write bandwidth                 |
| - [filesystems](#statistics_filesystems )         | No      | array of object | No         | -                                              | Array of filesystems                                 |

### <a name="statistics_mem_used"></a>21.1. Property `Job meta data > statistics > mem_used`

|                           |                                             |
| ------------------------- | ------------------------------------------- |
| **Type**                  | `object`                                    |
| **Required**              | Yes                                         |
| **Additional properties** | Any type allowed                            |
| **Defined in**            | embedfs://job-metric-statistics.schema.json |

**Description:** Memory capacity used (required)

### <a name="statistics_cpu_load"></a>21.2. Property `Job meta data > statistics > cpu_load`

|                           |                                             |
| ------------------------- | ------------------------------------------- |
| **Type**                  | `object`                                    |
| **Required**              | Yes                                         |
| **Additional properties** | Any type allowed                            |
| **Defined in**            | embedfs://job-metric-statistics.schema.json |

**Description:** CPU requested core utilization (load 1m) (required)

### <a name="statistics_flops_any"></a>21.3. Property `Job meta data > statistics > flops_any`

|                           |                                             |
| ------------------------- | ------------------------------------------- |
| **Type**                  | `object`                                    |
| **Required**              | Yes                                         |
| **Additional properties** | Any type allowed                            |
| **Defined in**            | embedfs://job-metric-statistics.schema.json |

**Description:** Total flop rate with DP flops scaled up (required)

### <a name="statistics_mem_bw"></a>21.4. Property `Job meta data > statistics > mem_bw`

|                           |                                             |
| ------------------------- | ------------------------------------------- |
| **Type**                  | `object`                                    |
| **Required**              | Yes                                         |
| **Additional properties** | Any type allowed                            |
| **Defined in**            | embedfs://job-metric-statistics.schema.json |

**Description:** Main memory bandwidth (required)

### <a name="statistics_net_bw"></a>21.5. Property `Job meta data > statistics > net_bw`

|                           |                                             |
| ------------------------- | ------------------------------------------- |
| **Type**                  | `object`                                    |
| **Required**              | No                                          |
| **Additional properties** | Any type allowed                            |
| **Defined in**            | embedfs://job-metric-statistics.schema.json |

**Description:** Total fast interconnect network bandwidth (required)

### <a name="statistics_file_bw"></a>21.6. Property `Job meta data > statistics > file_bw`

|                           |                                             |
| ------------------------- | ------------------------------------------- |
| **Type**                  | `object`                                    |
| **Required**              | No                                          |
| **Additional properties** | Any type allowed                            |
| **Defined in**            | embedfs://job-metric-statistics.schema.json |

**Description:** Total file IO bandwidth (required)

### <a name="statistics_ipc"></a>21.7. Property `Job meta data > statistics > ipc`

|                           |                                             |
| ------------------------- | ------------------------------------------- |
| **Type**                  | `object`                                    |
| **Required**              | No                                          |
| **Additional properties** | Any type allowed                            |
| **Defined in**            | embedfs://job-metric-statistics.schema.json |

**Description:** Instructions executed per cycle

### <a name="statistics_cpu_user"></a>21.8. Property `Job meta data > statistics > cpu_user`

|                           |                                             |
| ------------------------- | ------------------------------------------- |
| **Type**                  | `object`                                    |
| **Required**              | Yes                                         |
| **Additional properties** | Any type allowed                            |
| **Defined in**            | embedfs://job-metric-statistics.schema.json |

**Description:** CPU user active core utilization

### <a name="statistics_flops_dp"></a>21.9. Property `Job meta data > statistics > flops_dp`

|                           |                                             |
| ------------------------- | ------------------------------------------- |
| **Type**                  | `object`                                    |
| **Required**              | No                                          |
| **Additional properties** | Any type allowed                            |
| **Defined in**            | embedfs://job-metric-statistics.schema.json |

**Description:** Double precision flop rate

### <a name="statistics_flops_sp"></a>21.10. Property `Job meta data > statistics > flops_sp`

|                           |                                             |
| ------------------------- | ------------------------------------------- |
| **Type**                  | `object`                                    |
| **Required**              | No                                          |
| **Additional properties** | Any type allowed                            |
| **Defined in**            | embedfs://job-metric-statistics.schema.json |

**Description:** Single precision flops rate

### <a name="statistics_rapl_power"></a>21.11. Property `Job meta data > statistics > rapl_power`

|                           |                                             |
| ------------------------- | ------------------------------------------- |
| **Type**                  | `object`                                    |
| **Required**              | No                                          |
| **Additional properties** | Any type allowed                            |
| **Defined in**            | embedfs://job-metric-statistics.schema.json |

**Description:** CPU power consumption

### <a name="statistics_acc_used"></a>21.12. Property `Job meta data > statistics > acc_used`

|                           |                                             |
| ------------------------- | ------------------------------------------- |
| **Type**                  | `object`                                    |
| **Required**              | No                                          |
| **Additional properties** | Any type allowed                            |
| **Defined in**            | embedfs://job-metric-statistics.schema.json |

**Description:** GPU utilization

### <a name="statistics_acc_mem_used"></a>21.13. Property `Job meta data > statistics > acc_mem_used`

|                           |                                             |
| ------------------------- | ------------------------------------------- |
| **Type**                  | `object`                                    |
| **Required**              | No                                          |
| **Additional properties** | Any type allowed                            |
| **Defined in**            | embedfs://job-metric-statistics.schema.json |

**Description:** GPU memory capacity used

### <a name="statistics_acc_power"></a>21.14. Property `Job meta data > statistics > acc_power`

|                           |                                             |
| ------------------------- | ------------------------------------------- |
| **Type**                  | `object`                                    |
| **Required**              | No                                          |
| **Additional properties** | Any type allowed                            |
| **Defined in**            | embedfs://job-metric-statistics.schema.json |

**Description:** GPU power consumption

### <a name="statistics_clock"></a>21.15. Property `Job meta data > statistics > clock`

|                           |                                             |
| ------------------------- | ------------------------------------------- |
| **Type**                  | `object`                                    |
| **Required**              | No                                          |
| **Additional properties** | Any type allowed                            |
| **Defined in**            | embedfs://job-metric-statistics.schema.json |

**Description:** Average core frequency

### <a name="statistics_eth_read_bw"></a>21.16. Property `Job meta data > statistics > eth_read_bw`

|                           |                                             |
| ------------------------- | ------------------------------------------- |
| **Type**                  | `object`                                    |
| **Required**              | No                                          |
| **Additional properties** | Any type allowed                            |
| **Defined in**            | embedfs://job-metric-statistics.schema.json |

**Description:** Ethernet read bandwidth

### <a name="statistics_eth_write_bw"></a>21.17. Property `Job meta data > statistics > eth_write_bw`

|                           |                                             |
| ------------------------- | ------------------------------------------- |
| **Type**                  | `object`                                    |
| **Required**              | No                                          |
| **Additional properties** | Any type allowed                            |
| **Defined in**            | embedfs://job-metric-statistics.schema.json |

**Description:** Ethernet write bandwidth

### <a name="statistics_ic_rcv_packets"></a>21.18. Property `Job meta data > statistics > ic_rcv_packets`

|                           |                                             |
| ------------------------- | ------------------------------------------- |
| **Type**                  | `object`                                    |
| **Required**              | No                                          |
| **Additional properties** | Any type allowed                            |
| **Defined in**            | embedfs://job-metric-statistics.schema.json |

**Description:** Network interconnect read packets

### <a name="statistics_ic_send_packets"></a>21.19. Property `Job meta data > statistics > ic_send_packets`

|                           |                                             |
| ------------------------- | ------------------------------------------- |
| **Type**                  | `object`                                    |
| **Required**              | No                                          |
| **Additional properties** | Any type allowed                            |
| **Defined in**            | embedfs://job-metric-statistics.schema.json |

**Description:** Network interconnect send packet

### <a name="statistics_ic_read_bw"></a>21.20. Property `Job meta data > statistics > ic_read_bw`

|                           |                                             |
| ------------------------- | ------------------------------------------- |
| **Type**                  | `object`                                    |
| **Required**              | No                                          |
| **Additional properties** | Any type allowed                            |
| **Defined in**            | embedfs://job-metric-statistics.schema.json |

**Description:** Network interconnect read bandwidth

### <a name="statistics_ic_write_bw"></a>21.21. Property `Job meta data > statistics > ic_write_bw`

|                           |                                             |
| ------------------------- | ------------------------------------------- |
| **Type**                  | `object`                                    |
| **Required**              | No                                          |
| **Additional properties** | Any type allowed                            |
| **Defined in**            | embedfs://job-metric-statistics.schema.json |

**Description:** Network interconnect write bandwidth

### <a name="statistics_filesystems"></a>21.22. Property `Job meta data > statistics > filesystems`

|              |                   |
| ------------ | ----------------- |
| **Type**     | `array of object` |
| **Required** | No                |

**Description:** Array of filesystems

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | 1                  |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be                    | Description |
| -------------------------------------------------- | ----------- |
| [filesystems items](#statistics_filesystems_items) | -           |

#### <a name="statistics_filesystems_items"></a>21.22.1. Job meta data > statistics > filesystems > filesystems items

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

| Property                                                | Pattern | Type             | Deprecated | Definition                                     | Title/Description           |
| ------------------------------------------------------- | ------- | ---------------- | ---------- | ---------------------------------------------- | --------------------------- |
| + [name](#statistics_filesystems_items_name )           | No      | string           | No         | -                                              | -                           |
| + [type](#statistics_filesystems_items_type )           | No      | enum (of string) | No         | -                                              | -                           |
| + [read_bw](#statistics_filesystems_items_read_bw )     | No      | object           | No         | In embedfs://job-metric-statistics.schema.json | File system read bandwidth  |
| + [write_bw](#statistics_filesystems_items_write_bw )   | No      | object           | No         | In embedfs://job-metric-statistics.schema.json | File system write bandwidth |
| - [read_req](#statistics_filesystems_items_read_req )   | No      | object           | No         | In embedfs://job-metric-statistics.schema.json | File system read requests   |
| - [write_req](#statistics_filesystems_items_write_req ) | No      | object           | No         | In embedfs://job-metric-statistics.schema.json | File system write requests  |
| - [inodes](#statistics_filesystems_items_inodes )       | No      | object           | No         | In embedfs://job-metric-statistics.schema.json | File system write requests  |
| - [accesses](#statistics_filesystems_items_accesses )   | No      | object           | No         | In embedfs://job-metric-statistics.schema.json | File system open and close  |
| - [fsync](#statistics_filesystems_items_fsync )         | No      | object           | No         | In embedfs://job-metric-statistics.schema.json | File system fsync           |
| - [create](#statistics_filesystems_items_create )       | No      | object           | No         | In embedfs://job-metric-statistics.schema.json | File system create          |
| - [open](#statistics_filesystems_items_open )           | No      | object           | No         | In embedfs://job-metric-statistics.schema.json | File system open            |
| - [close](#statistics_filesystems_items_close )         | No      | object           | No         | In embedfs://job-metric-statistics.schema.json | File system close           |
| - [seek](#statistics_filesystems_items_seek )           | No      | object           | No         | In embedfs://job-metric-statistics.schema.json | File system seek            |

##### <a name="statistics_filesystems_items_name"></a>21.22.1.1. Property `Job meta data > statistics > filesystems > filesystems items > name`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

##### <a name="statistics_filesystems_items_type"></a>21.22.1.2. Property `Job meta data > statistics > filesystems > filesystems items > type`

|              |                    |
| ------------ | ------------------ |
| **Type**     | `enum (of string)` |
| **Required** | Yes                |

Must be one of:
* "nfs"
* "lustre"
* "gpfs"
* "nvme"
* "ssd"
* "hdd"
* "beegfs"

##### <a name="statistics_filesystems_items_read_bw"></a>21.22.1.3. Property `Job meta data > statistics > filesystems > filesystems items > read_bw`

|                           |                                             |
| ------------------------- | ------------------------------------------- |
| **Type**                  | `object`                                    |
| **Required**              | Yes                                         |
| **Additional properties** | Any type allowed                            |
| **Defined in**            | embedfs://job-metric-statistics.schema.json |

**Description:** File system read bandwidth

##### <a name="statistics_filesystems_items_write_bw"></a>21.22.1.4. Property `Job meta data > statistics > filesystems > filesystems items > write_bw`

|                           |                                             |
| ------------------------- | ------------------------------------------- |
| **Type**                  | `object`                                    |
| **Required**              | Yes                                         |
| **Additional properties** | Any type allowed                            |
| **Defined in**            | embedfs://job-metric-statistics.schema.json |

**Description:** File system write bandwidth

##### <a name="statistics_filesystems_items_read_req"></a>21.22.1.5. Property `Job meta data > statistics > filesystems > filesystems items > read_req`

|                           |                                             |
| ------------------------- | ------------------------------------------- |
| **Type**                  | `object`                                    |
| **Required**              | No                                          |
| **Additional properties** | Any type allowed                            |
| **Defined in**            | embedfs://job-metric-statistics.schema.json |

**Description:** File system read requests

##### <a name="statistics_filesystems_items_write_req"></a>21.22.1.6. Property `Job meta data > statistics > filesystems > filesystems items > write_req`

|                           |                                             |
| ------------------------- | ------------------------------------------- |
| **Type**                  | `object`                                    |
| **Required**              | No                                          |
| **Additional properties** | Any type allowed                            |
| **Defined in**            | embedfs://job-metric-statistics.schema.json |

**Description:** File system write requests

##### <a name="statistics_filesystems_items_inodes"></a>21.22.1.7. Property `Job meta data > statistics > filesystems > filesystems items > inodes`

|                           |                                             |
| ------------------------- | ------------------------------------------- |
| **Type**                  | `object`                                    |
| **Required**              | No                                          |
| **Additional properties** | Any type allowed                            |
| **Defined in**            | embedfs://job-metric-statistics.schema.json |

**Description:** File system write requests

##### <a name="statistics_filesystems_items_accesses"></a>21.22.1.8. Property `Job meta data > statistics > filesystems > filesystems items > accesses`

|                           |                                             |
| ------------------------- | ------------------------------------------- |
| **Type**                  | `object`                                    |
| **Required**              | No                                          |
| **Additional properties** | Any type allowed                            |
| **Defined in**            | embedfs://job-metric-statistics.schema.json |

**Description:** File system open and close

##### <a name="statistics_filesystems_items_fsync"></a>21.22.1.9. Property `Job meta data > statistics > filesystems > filesystems items > fsync`

|                           |                                             |
| ------------------------- | ------------------------------------------- |
| **Type**                  | `object`                                    |
| **Required**              | No                                          |
| **Additional properties** | Any type allowed                            |
| **Defined in**            | embedfs://job-metric-statistics.schema.json |

**Description:** File system fsync

##### <a name="statistics_filesystems_items_create"></a>21.22.1.10. Property `Job meta data > statistics > filesystems > filesystems items > create`

|                           |                                             |
| ------------------------- | ------------------------------------------- |
| **Type**                  | `object`                                    |
| **Required**              | No                                          |
| **Additional properties** | Any type allowed                            |
| **Defined in**            | embedfs://job-metric-statistics.schema.json |

**Description:** File system create

##### <a name="statistics_filesystems_items_open"></a>21.22.1.11. Property `Job meta data > statistics > filesystems > filesystems items > open`

|                           |                                             |
| ------------------------- | ------------------------------------------- |
| **Type**                  | `object`                                    |
| **Required**              | No                                          |
| **Additional properties** | Any type allowed                            |
| **Defined in**            | embedfs://job-metric-statistics.schema.json |

**Description:** File system open

##### <a name="statistics_filesystems_items_close"></a>21.22.1.12. Property `Job meta data > statistics > filesystems > filesystems items > close`

|                           |                                             |
| ------------------------- | ------------------------------------------- |
| **Type**                  | `object`                                    |
| **Required**              | No                                          |
| **Additional properties** | Any type allowed                            |
| **Defined in**            | embedfs://job-metric-statistics.schema.json |

**Description:** File system close

##### <a name="statistics_filesystems_items_seek"></a>21.22.1.13. Property `Job meta data > statistics > filesystems > filesystems items > seek`

|                           |                                             |
| ------------------------- | ------------------------------------------- |
| **Type**                  | `object`                                    |
| **Required**              | No                                          |
| **Additional properties** | Any type allowed                            |
| **Defined in**            | embedfs://job-metric-statistics.schema.json |

**Description:** File system seek

----------------------------------------------------------------------------------------------------------------------------
Generated using [json-schema-for-humans](https://github.com/coveooss/json-schema-for-humans) on 2024-12-04 at 16:45:59 +0100
