---
title: Job Data Schema
description: ClusterCockpit Job Data Schema Reference
categories: [cc-backend]
tags: [Backend]
weight: 3
---

The following schema in its raw form can be found in the [ClusterCockpit GitHub](https://github.com/ClusterCockpit/cc-backend/tree/master/pkg/schema/schemas) repository.

{{< alert title="Manual Updates">}}
  Changes to the original JSON schema found in the repository are not automatically rendered in this reference documentation.</br></br>
  **Last Update:** 04.12.2024
{{< /alert >}}

## Job metric data list

- [1. Property `Job metric data list > mem_used`](#mem_used)
  - [1.1. Property `Job metric data list > mem_used > node`](#mem_used_node)
- [2. Property `Job metric data list > flops_any`](#flops_any)
  - [2.1. Property `Job metric data list > flops_any > node`](#flops_any_node)
  - [2.2. Property `Job metric data list > flops_any > socket`](#flops_any_socket)
  - [2.3. Property `Job metric data list > flops_any > memoryDomain`](#flops_any_memoryDomain)
  - [2.4. Property `Job metric data list > flops_any > core`](#flops_any_core)
  - [2.5. Property `Job metric data list > flops_any > hwthread`](#flops_any_hwthread)
- [3. Property `Job metric data list > mem_bw`](#mem_bw)
  - [3.1. Property `Job metric data list > mem_bw > node`](#mem_bw_node)
  - [3.2. Property `Job metric data list > mem_bw > socket`](#mem_bw_socket)
  - [3.3. Property `Job metric data list > mem_bw > memoryDomain`](#mem_bw_memoryDomain)
- [4. Property `Job metric data list > net_bw`](#net_bw)
  - [4.1. Property `Job metric data list > net_bw > node`](#net_bw_node)
- [5. Property `Job metric data list > ipc`](#ipc)
  - [5.1. Property `Job metric data list > ipc > node`](#ipc_node)
  - [5.2. Property `Job metric data list > ipc > socket`](#ipc_socket)
  - [5.3. Property `Job metric data list > ipc > memoryDomain`](#ipc_memoryDomain)
  - [5.4. Property `Job metric data list > ipc > core`](#ipc_core)
  - [5.5. Property `Job metric data list > ipc > hwthread`](#ipc_hwthread)
- [6. Property `Job metric data list > cpu_user`](#cpu_user)
  - [6.1. Property `Job metric data list > cpu_user > node`](#cpu_user_node)
  - [6.2. Property `Job metric data list > cpu_user > socket`](#cpu_user_socket)
  - [6.3. Property `Job metric data list > cpu_user > memoryDomain`](#cpu_user_memoryDomain)
  - [6.4. Property `Job metric data list > cpu_user > core`](#cpu_user_core)
  - [6.5. Property `Job metric data list > cpu_user > hwthread`](#cpu_user_hwthread)
- [7. Property `Job metric data list > cpu_load`](#cpu_load)
  - [7.1. Property `Job metric data list > cpu_load > node`](#cpu_load_node)
- [8. Property `Job metric data list > flops_dp`](#flops_dp)
  - [8.1. Property `Job metric data list > flops_dp > node`](#flops_dp_node)
  - [8.2. Property `Job metric data list > flops_dp > socket`](#flops_dp_socket)
  - [8.3. Property `Job metric data list > flops_dp > memoryDomain`](#flops_dp_memoryDomain)
  - [8.4. Property `Job metric data list > flops_dp > core`](#flops_dp_core)
  - [8.5. Property `Job metric data list > flops_dp > hwthread`](#flops_dp_hwthread)
- [9. Property `Job metric data list > flops_sp`](#flops_sp)
  - [9.1. Property `Job metric data list > flops_sp > node`](#flops_sp_node)
  - [9.2. Property `Job metric data list > flops_sp > socket`](#flops_sp_socket)
  - [9.3. Property `Job metric data list > flops_sp > memoryDomain`](#flops_sp_memoryDomain)
  - [9.4. Property `Job metric data list > flops_sp > core`](#flops_sp_core)
  - [9.5. Property `Job metric data list > flops_sp > hwthread`](#flops_sp_hwthread)
- [10. Property `Job metric data list > vectorization_ratio`](#vectorization_ratio)
  - [10.1. Property `Job metric data list > vectorization_ratio > node`](#vectorization_ratio_node)
  - [10.2. Property `Job metric data list > vectorization_ratio > socket`](#vectorization_ratio_socket)
  - [10.3. Property `Job metric data list > vectorization_ratio > memoryDomain`](#vectorization_ratio_memoryDomain)
  - [10.4. Property `Job metric data list > vectorization_ratio > core`](#vectorization_ratio_core)
  - [10.5. Property `Job metric data list > vectorization_ratio > hwthread`](#vectorization_ratio_hwthread)
- [11. Property `Job metric data list > cpu_power`](#cpu_power)
  - [11.1. Property `Job metric data list > cpu_power > node`](#cpu_power_node)
  - [11.2. Property `Job metric data list > cpu_power > socket`](#cpu_power_socket)
- [12. Property `Job metric data list > mem_power`](#mem_power)
  - [12.1. Property `Job metric data list > mem_power > node`](#mem_power_node)
  - [12.2. Property `Job metric data list > mem_power > socket`](#mem_power_socket)
- [13. Property `Job metric data list > acc_utilization`](#acc_utilization)
  - [13.1. Property `Job metric data list > acc_utilization > accelerator`](#acc_utilization_accelerator)
- [14. Property `Job metric data list > acc_mem_used`](#acc_mem_used)
  - [14.1. Property `Job metric data list > acc_mem_used > accelerator`](#acc_mem_used_accelerator)
- [15. Property `Job metric data list > acc_power`](#acc_power)
  - [15.1. Property `Job metric data list > acc_power > accelerator`](#acc_power_accelerator)
- [16. Property `Job metric data list > clock`](#clock)
  - [16.1. Property `Job metric data list > clock > node`](#clock_node)
  - [16.2. Property `Job metric data list > clock > socket`](#clock_socket)
  - [16.3. Property `Job metric data list > clock > memoryDomain`](#clock_memoryDomain)
  - [16.4. Property `Job metric data list > clock > core`](#clock_core)
  - [16.5. Property `Job metric data list > clock > hwthread`](#clock_hwthread)
- [17. Property `Job metric data list > eth_read_bw`](#eth_read_bw)
  - [17.1. Property `Job metric data list > eth_read_bw > node`](#eth_read_bw_node)
- [18. Property `Job metric data list > eth_write_bw`](#eth_write_bw)
  - [18.1. Property `Job metric data list > eth_write_bw > node`](#eth_write_bw_node)
- [19. Property `Job metric data list > filesystems`](#filesystems)
  - [19.1. Job metric data list > filesystems > filesystems items](#filesystems_items)
    - [19.1.1. Property `Job metric data list > filesystems > filesystems items > name`](#filesystems_items_name)
    - [19.1.2. Property `Job metric data list > filesystems > filesystems items > type`](#filesystems_items_type)
    - [19.1.3. Property `Job metric data list > filesystems > filesystems items > read_bw`](#filesystems_items_read_bw)
      - [19.1.3.1. Property `Job metric data list > filesystems > filesystems items > read_bw > node`](#filesystems_items_read_bw_node)
    - [19.1.4. Property `Job metric data list > filesystems > filesystems items > write_bw`](#filesystems_items_write_bw)
      - [19.1.4.1. Property `Job metric data list > filesystems > filesystems items > write_bw > node`](#filesystems_items_write_bw_node)
    - [19.1.5. Property `Job metric data list > filesystems > filesystems items > read_req`](#filesystems_items_read_req)
      - [19.1.5.1. Property `Job metric data list > filesystems > filesystems items > read_req > node`](#filesystems_items_read_req_node)
    - [19.1.6. Property `Job metric data list > filesystems > filesystems items > write_req`](#filesystems_items_write_req)
      - [19.1.6.1. Property `Job metric data list > filesystems > filesystems items > write_req > node`](#filesystems_items_write_req_node)
    - [19.1.7. Property `Job metric data list > filesystems > filesystems items > inodes`](#filesystems_items_inodes)
      - [19.1.7.1. Property `Job metric data list > filesystems > filesystems items > inodes > node`](#filesystems_items_inodes_node)
    - [19.1.8. Property `Job metric data list > filesystems > filesystems items > accesses`](#filesystems_items_accesses)
      - [19.1.8.1. Property `Job metric data list > filesystems > filesystems items > accesses > node`](#filesystems_items_accesses_node)
    - [19.1.9. Property `Job metric data list > filesystems > filesystems items > fsync`](#filesystems_items_fsync)
      - [19.1.9.1. Property `Job metric data list > filesystems > filesystems items > fsync > node`](#filesystems_items_fsync_node)
    - [19.1.10. Property `Job metric data list > filesystems > filesystems items > create`](#filesystems_items_create)
      - [19.1.10.1. Property `Job metric data list > filesystems > filesystems items > create > node`](#filesystems_items_create_node)
    - [19.1.11. Property `Job metric data list > filesystems > filesystems items > open`](#filesystems_items_open)
      - [19.1.11.1. Property `Job metric data list > filesystems > filesystems items > open > node`](#filesystems_items_open_node)
    - [19.1.12. Property `Job metric data list > filesystems > filesystems items > close`](#filesystems_items_close)
      - [19.1.12.1. Property `Job metric data list > filesystems > filesystems items > close > node`](#filesystems_items_close_node)
    - [19.1.13. Property `Job metric data list > filesystems > filesystems items > seek`](#filesystems_items_seek)
      - [19.1.13.1. Property `Job metric data list > filesystems > filesystems items > seek > node`](#filesystems_items_seek_node)

**Title:** Job metric data list

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** Collection of metric data of a HPC job

| Property                                       | Pattern | Type            | Deprecated | Definition | Title/Description                                           |
| ---------------------------------------------- | ------- | --------------- | ---------- | ---------- | ----------------------------------------------------------- |
| + [mem_used](#mem_used )                       | No      | object          | No         | -          | Memory capacity used                                        |
| + [flops_any](#flops_any )                     | No      | object          | No         | -          | Total flop rate with DP flops scaled up                     |
| + [mem_bw](#mem_bw )                           | No      | object          | No         | -          | Main memory bandwidth                                       |
| + [net_bw](#net_bw )                           | No      | object          | No         | -          | Total fast interconnect network bandwidth                   |
| - [ipc](#ipc )                                 | No      | object          | No         | -          | Instructions executed per cycle                             |
| + [cpu_user](#cpu_user )                       | No      | object          | No         | -          | CPU user active core utilization                            |
| + [cpu_load](#cpu_load )                       | No      | object          | No         | -          | CPU requested core utilization (load 1m)                    |
| - [flops_dp](#flops_dp )                       | No      | object          | No         | -          | Double precision flop rate                                  |
| - [flops_sp](#flops_sp )                       | No      | object          | No         | -          | Single precision flops rate                                 |
| - [vectorization_ratio](#vectorization_ratio ) | No      | object          | No         | -          | Fraction of arithmetic instructions using SIMD instructions |
| - [cpu_power](#cpu_power )                     | No      | object          | No         | -          | CPU power consumption                                       |
| - [mem_power](#mem_power )                     | No      | object          | No         | -          | Memory power consumption                                    |
| - [acc_utilization](#acc_utilization )         | No      | object          | No         | -          | GPU utilization                                             |
| - [acc_mem_used](#acc_mem_used )               | No      | object          | No         | -          | GPU memory capacity used                                    |
| - [acc_power](#acc_power )                     | No      | object          | No         | -          | GPU power consumption                                       |
| - [clock](#clock )                             | No      | object          | No         | -          | Average core frequency                                      |
| - [eth_read_bw](#eth_read_bw )                 | No      | object          | No         | -          | Ethernet read bandwidth                                     |
| - [eth_write_bw](#eth_write_bw )               | No      | object          | No         | -          | Ethernet write bandwidth                                    |
| + [filesystems](#filesystems )                 | No      | array of object | No         | -          | Array of filesystems                                        |

## <a name="mem_used"></a>1. Property `Job metric data list > mem_used`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | Yes              |
| **Additional properties** | Any type allowed |

**Description:** Memory capacity used

| Property                  | Pattern | Type   | Deprecated | Definition                               | Title/Description                                                                                             |
| ------------------------- | ------- | ------ | ---------- | ---------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| + [node](#mem_used_node ) | No      | object | No         | In embedfs://job-metric-data.schema.json | 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️ |

### <a name="mem_used_node"></a>1.1. Property `Job metric data list > mem_used > node`

|                           |                                       |
| ------------------------- | ------------------------------------- |
| **Type**                  | `object`                              |
| **Required**              | Yes                                   |
| **Additional properties** | Any type allowed                      |
| **Defined in**            | embedfs://job-metric-data.schema.json |

**Description:** 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️

## <a name="flops_any"></a>2. Property `Job metric data list > flops_any`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | Yes              |
| **Additional properties** | Any type allowed |

**Description:** Total flop rate with DP flops scaled up

| Property                                   | Pattern | Type   | Deprecated | Definition                               | Title/Description                                                                                             |
| ------------------------------------------ | ------- | ------ | ---------- | ---------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| - [node](#flops_any_node )                 | No      | object | No         | In embedfs://job-metric-data.schema.json | 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️ |
| - [socket](#flops_any_socket )             | No      | object | No         | In embedfs://job-metric-data.schema.json | 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️ |
| - [memoryDomain](#flops_any_memoryDomain ) | No      | object | No         | In embedfs://job-metric-data.schema.json | 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️ |
| - [core](#flops_any_core )                 | No      | object | No         | In embedfs://job-metric-data.schema.json | 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️ |
| - [hwthread](#flops_any_hwthread )         | No      | object | No         | In embedfs://job-metric-data.schema.json | 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️ |

### <a name="flops_any_node"></a>2.1. Property `Job metric data list > flops_any > node`

|                           |                                       |
| ------------------------- | ------------------------------------- |
| **Type**                  | `object`                              |
| **Required**              | No                                    |
| **Additional properties** | Any type allowed                      |
| **Defined in**            | embedfs://job-metric-data.schema.json |

**Description:** 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️

### <a name="flops_any_socket"></a>2.2. Property `Job metric data list > flops_any > socket`

|                           |                                       |
| ------------------------- | ------------------------------------- |
| **Type**                  | `object`                              |
| **Required**              | No                                    |
| **Additional properties** | Any type allowed                      |
| **Defined in**            | embedfs://job-metric-data.schema.json |

**Description:** 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️

### <a name="flops_any_memoryDomain"></a>2.3. Property `Job metric data list > flops_any > memoryDomain`

|                           |                                       |
| ------------------------- | ------------------------------------- |
| **Type**                  | `object`                              |
| **Required**              | No                                    |
| **Additional properties** | Any type allowed                      |
| **Defined in**            | embedfs://job-metric-data.schema.json |

**Description:** 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️

### <a name="flops_any_core"></a>2.4. Property `Job metric data list > flops_any > core`

|                           |                                       |
| ------------------------- | ------------------------------------- |
| **Type**                  | `object`                              |
| **Required**              | No                                    |
| **Additional properties** | Any type allowed                      |
| **Defined in**            | embedfs://job-metric-data.schema.json |

**Description:** 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️

### <a name="flops_any_hwthread"></a>2.5. Property `Job metric data list > flops_any > hwthread`

|                           |                                       |
| ------------------------- | ------------------------------------- |
| **Type**                  | `object`                              |
| **Required**              | No                                    |
| **Additional properties** | Any type allowed                      |
| **Defined in**            | embedfs://job-metric-data.schema.json |

**Description:** 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️

## <a name="mem_bw"></a>3. Property `Job metric data list > mem_bw`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | Yes              |
| **Additional properties** | Any type allowed |

**Description:** Main memory bandwidth

| Property                                | Pattern | Type   | Deprecated | Definition                               | Title/Description                                                                                             |
| --------------------------------------- | ------- | ------ | ---------- | ---------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| - [node](#mem_bw_node )                 | No      | object | No         | In embedfs://job-metric-data.schema.json | 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️ |
| - [socket](#mem_bw_socket )             | No      | object | No         | In embedfs://job-metric-data.schema.json | 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️ |
| - [memoryDomain](#mem_bw_memoryDomain ) | No      | object | No         | In embedfs://job-metric-data.schema.json | 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️ |

### <a name="mem_bw_node"></a>3.1. Property `Job metric data list > mem_bw > node`

|                           |                                       |
| ------------------------- | ------------------------------------- |
| **Type**                  | `object`                              |
| **Required**              | No                                    |
| **Additional properties** | Any type allowed                      |
| **Defined in**            | embedfs://job-metric-data.schema.json |

**Description:** 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️

### <a name="mem_bw_socket"></a>3.2. Property `Job metric data list > mem_bw > socket`

|                           |                                       |
| ------------------------- | ------------------------------------- |
| **Type**                  | `object`                              |
| **Required**              | No                                    |
| **Additional properties** | Any type allowed                      |
| **Defined in**            | embedfs://job-metric-data.schema.json |

**Description:** 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️

### <a name="mem_bw_memoryDomain"></a>3.3. Property `Job metric data list > mem_bw > memoryDomain`

|                           |                                       |
| ------------------------- | ------------------------------------- |
| **Type**                  | `object`                              |
| **Required**              | No                                    |
| **Additional properties** | Any type allowed                      |
| **Defined in**            | embedfs://job-metric-data.schema.json |

**Description:** 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️

## <a name="net_bw"></a>4. Property `Job metric data list > net_bw`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | Yes              |
| **Additional properties** | Any type allowed |

**Description:** Total fast interconnect network bandwidth

| Property                | Pattern | Type   | Deprecated | Definition                               | Title/Description                                                                                             |
| ----------------------- | ------- | ------ | ---------- | ---------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| + [node](#net_bw_node ) | No      | object | No         | In embedfs://job-metric-data.schema.json | 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️ |

### <a name="net_bw_node"></a>4.1. Property `Job metric data list > net_bw > node`

|                           |                                       |
| ------------------------- | ------------------------------------- |
| **Type**                  | `object`                              |
| **Required**              | Yes                                   |
| **Additional properties** | Any type allowed                      |
| **Defined in**            | embedfs://job-metric-data.schema.json |

**Description:** 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️

## <a name="ipc"></a>5. Property `Job metric data list > ipc`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** Instructions executed per cycle

| Property                             | Pattern | Type   | Deprecated | Definition                               | Title/Description                                                                                             |
| ------------------------------------ | ------- | ------ | ---------- | ---------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| - [node](#ipc_node )                 | No      | object | No         | In embedfs://job-metric-data.schema.json | 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️ |
| - [socket](#ipc_socket )             | No      | object | No         | In embedfs://job-metric-data.schema.json | 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️ |
| - [memoryDomain](#ipc_memoryDomain ) | No      | object | No         | In embedfs://job-metric-data.schema.json | 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️ |
| - [core](#ipc_core )                 | No      | object | No         | In embedfs://job-metric-data.schema.json | 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️ |
| - [hwthread](#ipc_hwthread )         | No      | object | No         | In embedfs://job-metric-data.schema.json | 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️ |

### <a name="ipc_node"></a>5.1. Property `Job metric data list > ipc > node`

|                           |                                       |
| ------------------------- | ------------------------------------- |
| **Type**                  | `object`                              |
| **Required**              | No                                    |
| **Additional properties** | Any type allowed                      |
| **Defined in**            | embedfs://job-metric-data.schema.json |

**Description:** 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️

### <a name="ipc_socket"></a>5.2. Property `Job metric data list > ipc > socket`

|                           |                                       |
| ------------------------- | ------------------------------------- |
| **Type**                  | `object`                              |
| **Required**              | No                                    |
| **Additional properties** | Any type allowed                      |
| **Defined in**            | embedfs://job-metric-data.schema.json |

**Description:** 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️

### <a name="ipc_memoryDomain"></a>5.3. Property `Job metric data list > ipc > memoryDomain`

|                           |                                       |
| ------------------------- | ------------------------------------- |
| **Type**                  | `object`                              |
| **Required**              | No                                    |
| **Additional properties** | Any type allowed                      |
| **Defined in**            | embedfs://job-metric-data.schema.json |

**Description:** 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️

### <a name="ipc_core"></a>5.4. Property `Job metric data list > ipc > core`

|                           |                                       |
| ------------------------- | ------------------------------------- |
| **Type**                  | `object`                              |
| **Required**              | No                                    |
| **Additional properties** | Any type allowed                      |
| **Defined in**            | embedfs://job-metric-data.schema.json |

**Description:** 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️

### <a name="ipc_hwthread"></a>5.5. Property `Job metric data list > ipc > hwthread`

|                           |                                       |
| ------------------------- | ------------------------------------- |
| **Type**                  | `object`                              |
| **Required**              | No                                    |
| **Additional properties** | Any type allowed                      |
| **Defined in**            | embedfs://job-metric-data.schema.json |

**Description:** 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️

## <a name="cpu_user"></a>6. Property `Job metric data list > cpu_user`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | Yes              |
| **Additional properties** | Any type allowed |

**Description:** CPU user active core utilization

| Property                                  | Pattern | Type   | Deprecated | Definition                               | Title/Description                                                                                             |
| ----------------------------------------- | ------- | ------ | ---------- | ---------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| - [node](#cpu_user_node )                 | No      | object | No         | In embedfs://job-metric-data.schema.json | 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️ |
| - [socket](#cpu_user_socket )             | No      | object | No         | In embedfs://job-metric-data.schema.json | 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️ |
| - [memoryDomain](#cpu_user_memoryDomain ) | No      | object | No         | In embedfs://job-metric-data.schema.json | 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️ |
| - [core](#cpu_user_core )                 | No      | object | No         | In embedfs://job-metric-data.schema.json | 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️ |
| - [hwthread](#cpu_user_hwthread )         | No      | object | No         | In embedfs://job-metric-data.schema.json | 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️ |

### <a name="cpu_user_node"></a>6.1. Property `Job metric data list > cpu_user > node`

|                           |                                       |
| ------------------------- | ------------------------------------- |
| **Type**                  | `object`                              |
| **Required**              | No                                    |
| **Additional properties** | Any type allowed                      |
| **Defined in**            | embedfs://job-metric-data.schema.json |

**Description:** 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️

### <a name="cpu_user_socket"></a>6.2. Property `Job metric data list > cpu_user > socket`

|                           |                                       |
| ------------------------- | ------------------------------------- |
| **Type**                  | `object`                              |
| **Required**              | No                                    |
| **Additional properties** | Any type allowed                      |
| **Defined in**            | embedfs://job-metric-data.schema.json |

**Description:** 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️

### <a name="cpu_user_memoryDomain"></a>6.3. Property `Job metric data list > cpu_user > memoryDomain`

|                           |                                       |
| ------------------------- | ------------------------------------- |
| **Type**                  | `object`                              |
| **Required**              | No                                    |
| **Additional properties** | Any type allowed                      |
| **Defined in**            | embedfs://job-metric-data.schema.json |

**Description:** 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️

### <a name="cpu_user_core"></a>6.4. Property `Job metric data list > cpu_user > core`

|                           |                                       |
| ------------------------- | ------------------------------------- |
| **Type**                  | `object`                              |
| **Required**              | No                                    |
| **Additional properties** | Any type allowed                      |
| **Defined in**            | embedfs://job-metric-data.schema.json |

**Description:** 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️

### <a name="cpu_user_hwthread"></a>6.5. Property `Job metric data list > cpu_user > hwthread`

|                           |                                       |
| ------------------------- | ------------------------------------- |
| **Type**                  | `object`                              |
| **Required**              | No                                    |
| **Additional properties** | Any type allowed                      |
| **Defined in**            | embedfs://job-metric-data.schema.json |

**Description:** 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️

## <a name="cpu_load"></a>7. Property `Job metric data list > cpu_load`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | Yes              |
| **Additional properties** | Any type allowed |

**Description:** CPU requested core utilization (load 1m)

| Property                  | Pattern | Type   | Deprecated | Definition                               | Title/Description                                                                                             |
| ------------------------- | ------- | ------ | ---------- | ---------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| + [node](#cpu_load_node ) | No      | object | No         | In embedfs://job-metric-data.schema.json | 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️ |

### <a name="cpu_load_node"></a>7.1. Property `Job metric data list > cpu_load > node`

|                           |                                       |
| ------------------------- | ------------------------------------- |
| **Type**                  | `object`                              |
| **Required**              | Yes                                   |
| **Additional properties** | Any type allowed                      |
| **Defined in**            | embedfs://job-metric-data.schema.json |

**Description:** 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️

## <a name="flops_dp"></a>8. Property `Job metric data list > flops_dp`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** Double precision flop rate

| Property                                  | Pattern | Type   | Deprecated | Definition                               | Title/Description                                                                                             |
| ----------------------------------------- | ------- | ------ | ---------- | ---------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| - [node](#flops_dp_node )                 | No      | object | No         | In embedfs://job-metric-data.schema.json | 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️ |
| - [socket](#flops_dp_socket )             | No      | object | No         | In embedfs://job-metric-data.schema.json | 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️ |
| - [memoryDomain](#flops_dp_memoryDomain ) | No      | object | No         | In embedfs://job-metric-data.schema.json | 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️ |
| - [core](#flops_dp_core )                 | No      | object | No         | In embedfs://job-metric-data.schema.json | 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️ |
| - [hwthread](#flops_dp_hwthread )         | No      | object | No         | In embedfs://job-metric-data.schema.json | 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️ |

### <a name="flops_dp_node"></a>8.1. Property `Job metric data list > flops_dp > node`

|                           |                                       |
| ------------------------- | ------------------------------------- |
| **Type**                  | `object`                              |
| **Required**              | No                                    |
| **Additional properties** | Any type allowed                      |
| **Defined in**            | embedfs://job-metric-data.schema.json |

**Description:** 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️

### <a name="flops_dp_socket"></a>8.2. Property `Job metric data list > flops_dp > socket`

|                           |                                       |
| ------------------------- | ------------------------------------- |
| **Type**                  | `object`                              |
| **Required**              | No                                    |
| **Additional properties** | Any type allowed                      |
| **Defined in**            | embedfs://job-metric-data.schema.json |

**Description:** 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️

### <a name="flops_dp_memoryDomain"></a>8.3. Property `Job metric data list > flops_dp > memoryDomain`

|                           |                                       |
| ------------------------- | ------------------------------------- |
| **Type**                  | `object`                              |
| **Required**              | No                                    |
| **Additional properties** | Any type allowed                      |
| **Defined in**            | embedfs://job-metric-data.schema.json |

**Description:** 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️

### <a name="flops_dp_core"></a>8.4. Property `Job metric data list > flops_dp > core`

|                           |                                       |
| ------------------------- | ------------------------------------- |
| **Type**                  | `object`                              |
| **Required**              | No                                    |
| **Additional properties** | Any type allowed                      |
| **Defined in**            | embedfs://job-metric-data.schema.json |

**Description:** 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️

### <a name="flops_dp_hwthread"></a>8.5. Property `Job metric data list > flops_dp > hwthread`

|                           |                                       |
| ------------------------- | ------------------------------------- |
| **Type**                  | `object`                              |
| **Required**              | No                                    |
| **Additional properties** | Any type allowed                      |
| **Defined in**            | embedfs://job-metric-data.schema.json |

**Description:** 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️

## <a name="flops_sp"></a>9. Property `Job metric data list > flops_sp`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** Single precision flops rate

| Property                                  | Pattern | Type   | Deprecated | Definition                               | Title/Description                                                                                             |
| ----------------------------------------- | ------- | ------ | ---------- | ---------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| - [node](#flops_sp_node )                 | No      | object | No         | In embedfs://job-metric-data.schema.json | 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️ |
| - [socket](#flops_sp_socket )             | No      | object | No         | In embedfs://job-metric-data.schema.json | 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️ |
| - [memoryDomain](#flops_sp_memoryDomain ) | No      | object | No         | In embedfs://job-metric-data.schema.json | 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️ |
| - [core](#flops_sp_core )                 | No      | object | No         | In embedfs://job-metric-data.schema.json | 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️ |
| - [hwthread](#flops_sp_hwthread )         | No      | object | No         | In embedfs://job-metric-data.schema.json | 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️ |

### <a name="flops_sp_node"></a>9.1. Property `Job metric data list > flops_sp > node`

|                           |                                       |
| ------------------------- | ------------------------------------- |
| **Type**                  | `object`                              |
| **Required**              | No                                    |
| **Additional properties** | Any type allowed                      |
| **Defined in**            | embedfs://job-metric-data.schema.json |

**Description:** 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️

### <a name="flops_sp_socket"></a>9.2. Property `Job metric data list > flops_sp > socket`

|                           |                                       |
| ------------------------- | ------------------------------------- |
| **Type**                  | `object`                              |
| **Required**              | No                                    |
| **Additional properties** | Any type allowed                      |
| **Defined in**            | embedfs://job-metric-data.schema.json |

**Description:** 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️

### <a name="flops_sp_memoryDomain"></a>9.3. Property `Job metric data list > flops_sp > memoryDomain`

|                           |                                       |
| ------------------------- | ------------------------------------- |
| **Type**                  | `object`                              |
| **Required**              | No                                    |
| **Additional properties** | Any type allowed                      |
| **Defined in**            | embedfs://job-metric-data.schema.json |

**Description:** 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️

### <a name="flops_sp_core"></a>9.4. Property `Job metric data list > flops_sp > core`

|                           |                                       |
| ------------------------- | ------------------------------------- |
| **Type**                  | `object`                              |
| **Required**              | No                                    |
| **Additional properties** | Any type allowed                      |
| **Defined in**            | embedfs://job-metric-data.schema.json |

**Description:** 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️

### <a name="flops_sp_hwthread"></a>9.5. Property `Job metric data list > flops_sp > hwthread`

|                           |                                       |
| ------------------------- | ------------------------------------- |
| **Type**                  | `object`                              |
| **Required**              | No                                    |
| **Additional properties** | Any type allowed                      |
| **Defined in**            | embedfs://job-metric-data.schema.json |

**Description:** 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️

## <a name="vectorization_ratio"></a>10. Property `Job metric data list > vectorization_ratio`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** Fraction of arithmetic instructions using SIMD instructions

| Property                                             | Pattern | Type   | Deprecated | Definition                               | Title/Description                                                                                             |
| ---------------------------------------------------- | ------- | ------ | ---------- | ---------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| - [node](#vectorization_ratio_node )                 | No      | object | No         | In embedfs://job-metric-data.schema.json | 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️ |
| - [socket](#vectorization_ratio_socket )             | No      | object | No         | In embedfs://job-metric-data.schema.json | 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️ |
| - [memoryDomain](#vectorization_ratio_memoryDomain ) | No      | object | No         | In embedfs://job-metric-data.schema.json | 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️ |
| - [core](#vectorization_ratio_core )                 | No      | object | No         | In embedfs://job-metric-data.schema.json | 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️ |
| - [hwthread](#vectorization_ratio_hwthread )         | No      | object | No         | In embedfs://job-metric-data.schema.json | 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️ |

### <a name="vectorization_ratio_node"></a>10.1. Property `Job metric data list > vectorization_ratio > node`

|                           |                                       |
| ------------------------- | ------------------------------------- |
| **Type**                  | `object`                              |
| **Required**              | No                                    |
| **Additional properties** | Any type allowed                      |
| **Defined in**            | embedfs://job-metric-data.schema.json |

**Description:** 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️

### <a name="vectorization_ratio_socket"></a>10.2. Property `Job metric data list > vectorization_ratio > socket`

|                           |                                       |
| ------------------------- | ------------------------------------- |
| **Type**                  | `object`                              |
| **Required**              | No                                    |
| **Additional properties** | Any type allowed                      |
| **Defined in**            | embedfs://job-metric-data.schema.json |

**Description:** 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️

### <a name="vectorization_ratio_memoryDomain"></a>10.3. Property `Job metric data list > vectorization_ratio > memoryDomain`

|                           |                                       |
| ------------------------- | ------------------------------------- |
| **Type**                  | `object`                              |
| **Required**              | No                                    |
| **Additional properties** | Any type allowed                      |
| **Defined in**            | embedfs://job-metric-data.schema.json |

**Description:** 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️

### <a name="vectorization_ratio_core"></a>10.4. Property `Job metric data list > vectorization_ratio > core`

|                           |                                       |
| ------------------------- | ------------------------------------- |
| **Type**                  | `object`                              |
| **Required**              | No                                    |
| **Additional properties** | Any type allowed                      |
| **Defined in**            | embedfs://job-metric-data.schema.json |

**Description:** 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️

### <a name="vectorization_ratio_hwthread"></a>10.5. Property `Job metric data list > vectorization_ratio > hwthread`

|                           |                                       |
| ------------------------- | ------------------------------------- |
| **Type**                  | `object`                              |
| **Required**              | No                                    |
| **Additional properties** | Any type allowed                      |
| **Defined in**            | embedfs://job-metric-data.schema.json |

**Description:** 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️

## <a name="cpu_power"></a>11. Property `Job metric data list > cpu_power`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** CPU power consumption

| Property                       | Pattern | Type   | Deprecated | Definition                               | Title/Description                                                                                             |
| ------------------------------ | ------- | ------ | ---------- | ---------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| - [node](#cpu_power_node )     | No      | object | No         | In embedfs://job-metric-data.schema.json | 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️ |
| - [socket](#cpu_power_socket ) | No      | object | No         | In embedfs://job-metric-data.schema.json | 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️ |

### <a name="cpu_power_node"></a>11.1. Property `Job metric data list > cpu_power > node`

|                           |                                       |
| ------------------------- | ------------------------------------- |
| **Type**                  | `object`                              |
| **Required**              | No                                    |
| **Additional properties** | Any type allowed                      |
| **Defined in**            | embedfs://job-metric-data.schema.json |

**Description:** 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️

### <a name="cpu_power_socket"></a>11.2. Property `Job metric data list > cpu_power > socket`

|                           |                                       |
| ------------------------- | ------------------------------------- |
| **Type**                  | `object`                              |
| **Required**              | No                                    |
| **Additional properties** | Any type allowed                      |
| **Defined in**            | embedfs://job-metric-data.schema.json |

**Description:** 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️

## <a name="mem_power"></a>12. Property `Job metric data list > mem_power`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** Memory power consumption

| Property                       | Pattern | Type   | Deprecated | Definition                               | Title/Description                                                                                             |
| ------------------------------ | ------- | ------ | ---------- | ---------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| - [node](#mem_power_node )     | No      | object | No         | In embedfs://job-metric-data.schema.json | 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️ |
| - [socket](#mem_power_socket ) | No      | object | No         | In embedfs://job-metric-data.schema.json | 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️ |

### <a name="mem_power_node"></a>12.1. Property `Job metric data list > mem_power > node`

|                           |                                       |
| ------------------------- | ------------------------------------- |
| **Type**                  | `object`                              |
| **Required**              | No                                    |
| **Additional properties** | Any type allowed                      |
| **Defined in**            | embedfs://job-metric-data.schema.json |

**Description:** 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️

### <a name="mem_power_socket"></a>12.2. Property `Job metric data list > mem_power > socket`

|                           |                                       |
| ------------------------- | ------------------------------------- |
| **Type**                  | `object`                              |
| **Required**              | No                                    |
| **Additional properties** | Any type allowed                      |
| **Defined in**            | embedfs://job-metric-data.schema.json |

**Description:** 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️

## <a name="acc_utilization"></a>13. Property `Job metric data list > acc_utilization`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** GPU utilization

| Property                                       | Pattern | Type   | Deprecated | Definition                               | Title/Description                                                                                             |
| ---------------------------------------------- | ------- | ------ | ---------- | ---------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| + [accelerator](#acc_utilization_accelerator ) | No      | object | No         | In embedfs://job-metric-data.schema.json | 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️ |

### <a name="acc_utilization_accelerator"></a>13.1. Property `Job metric data list > acc_utilization > accelerator`

|                           |                                       |
| ------------------------- | ------------------------------------- |
| **Type**                  | `object`                              |
| **Required**              | Yes                                   |
| **Additional properties** | Any type allowed                      |
| **Defined in**            | embedfs://job-metric-data.schema.json |

**Description:** 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️

## <a name="acc_mem_used"></a>14. Property `Job metric data list > acc_mem_used`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** GPU memory capacity used

| Property                                    | Pattern | Type   | Deprecated | Definition                               | Title/Description                                                                                             |
| ------------------------------------------- | ------- | ------ | ---------- | ---------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| + [accelerator](#acc_mem_used_accelerator ) | No      | object | No         | In embedfs://job-metric-data.schema.json | 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️ |

### <a name="acc_mem_used_accelerator"></a>14.1. Property `Job metric data list > acc_mem_used > accelerator`

|                           |                                       |
| ------------------------- | ------------------------------------- |
| **Type**                  | `object`                              |
| **Required**              | Yes                                   |
| **Additional properties** | Any type allowed                      |
| **Defined in**            | embedfs://job-metric-data.schema.json |

**Description:** 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️

## <a name="acc_power"></a>15. Property `Job metric data list > acc_power`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** GPU power consumption

| Property                                 | Pattern | Type   | Deprecated | Definition                               | Title/Description                                                                                             |
| ---------------------------------------- | ------- | ------ | ---------- | ---------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| + [accelerator](#acc_power_accelerator ) | No      | object | No         | In embedfs://job-metric-data.schema.json | 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️ |

### <a name="acc_power_accelerator"></a>15.1. Property `Job metric data list > acc_power > accelerator`

|                           |                                       |
| ------------------------- | ------------------------------------- |
| **Type**                  | `object`                              |
| **Required**              | Yes                                   |
| **Additional properties** | Any type allowed                      |
| **Defined in**            | embedfs://job-metric-data.schema.json |

**Description:** 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️

## <a name="clock"></a>16. Property `Job metric data list > clock`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** Average core frequency

| Property                               | Pattern | Type   | Deprecated | Definition                               | Title/Description                                                                                             |
| -------------------------------------- | ------- | ------ | ---------- | ---------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| - [node](#clock_node )                 | No      | object | No         | In embedfs://job-metric-data.schema.json | 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️ |
| - [socket](#clock_socket )             | No      | object | No         | In embedfs://job-metric-data.schema.json | 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️ |
| - [memoryDomain](#clock_memoryDomain ) | No      | object | No         | In embedfs://job-metric-data.schema.json | 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️ |
| - [core](#clock_core )                 | No      | object | No         | In embedfs://job-metric-data.schema.json | 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️ |
| - [hwthread](#clock_hwthread )         | No      | object | No         | In embedfs://job-metric-data.schema.json | 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️ |

### <a name="clock_node"></a>16.1. Property `Job metric data list > clock > node`

|                           |                                       |
| ------------------------- | ------------------------------------- |
| **Type**                  | `object`                              |
| **Required**              | No                                    |
| **Additional properties** | Any type allowed                      |
| **Defined in**            | embedfs://job-metric-data.schema.json |

**Description:** 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️

### <a name="clock_socket"></a>16.2. Property `Job metric data list > clock > socket`

|                           |                                       |
| ------------------------- | ------------------------------------- |
| **Type**                  | `object`                              |
| **Required**              | No                                    |
| **Additional properties** | Any type allowed                      |
| **Defined in**            | embedfs://job-metric-data.schema.json |

**Description:** 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️

### <a name="clock_memoryDomain"></a>16.3. Property `Job metric data list > clock > memoryDomain`

|                           |                                       |
| ------------------------- | ------------------------------------- |
| **Type**                  | `object`                              |
| **Required**              | No                                    |
| **Additional properties** | Any type allowed                      |
| **Defined in**            | embedfs://job-metric-data.schema.json |

**Description:** 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️

### <a name="clock_core"></a>16.4. Property `Job metric data list > clock > core`

|                           |                                       |
| ------------------------- | ------------------------------------- |
| **Type**                  | `object`                              |
| **Required**              | No                                    |
| **Additional properties** | Any type allowed                      |
| **Defined in**            | embedfs://job-metric-data.schema.json |

**Description:** 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️

### <a name="clock_hwthread"></a>16.5. Property `Job metric data list > clock > hwthread`

|                           |                                       |
| ------------------------- | ------------------------------------- |
| **Type**                  | `object`                              |
| **Required**              | No                                    |
| **Additional properties** | Any type allowed                      |
| **Defined in**            | embedfs://job-metric-data.schema.json |

**Description:** 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️

## <a name="eth_read_bw"></a>17. Property `Job metric data list > eth_read_bw`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** Ethernet read bandwidth

| Property                     | Pattern | Type   | Deprecated | Definition                               | Title/Description                                                                                             |
| ---------------------------- | ------- | ------ | ---------- | ---------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| + [node](#eth_read_bw_node ) | No      | object | No         | In embedfs://job-metric-data.schema.json | 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️ |

### <a name="eth_read_bw_node"></a>17.1. Property `Job metric data list > eth_read_bw > node`

|                           |                                       |
| ------------------------- | ------------------------------------- |
| **Type**                  | `object`                              |
| **Required**              | Yes                                   |
| **Additional properties** | Any type allowed                      |
| **Defined in**            | embedfs://job-metric-data.schema.json |

**Description:** 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️

## <a name="eth_write_bw"></a>18. Property `Job metric data list > eth_write_bw`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** Ethernet write bandwidth

| Property                      | Pattern | Type   | Deprecated | Definition                               | Title/Description                                                                                             |
| ----------------------------- | ------- | ------ | ---------- | ---------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| + [node](#eth_write_bw_node ) | No      | object | No         | In embedfs://job-metric-data.schema.json | 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️ |

### <a name="eth_write_bw_node"></a>18.1. Property `Job metric data list > eth_write_bw > node`

|                           |                                       |
| ------------------------- | ------------------------------------- |
| **Type**                  | `object`                              |
| **Required**              | Yes                                   |
| **Additional properties** | Any type allowed                      |
| **Defined in**            | embedfs://job-metric-data.schema.json |

**Description:** 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️

## <a name="filesystems"></a>19. Property `Job metric data list > filesystems`

|              |                   |
| ------------ | ----------------- |
| **Type**     | `array of object` |
| **Required** | Yes               |

**Description:** Array of filesystems

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | 1                  |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be         | Description |
| --------------------------------------- | ----------- |
| [filesystems items](#filesystems_items) | -           |

### <a name="filesystems_items"></a>19.1. Job metric data list > filesystems > filesystems items

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

| Property                                     | Pattern | Type             | Deprecated | Definition | Title/Description           |
| -------------------------------------------- | ------- | ---------------- | ---------- | ---------- | --------------------------- |
| + [name](#filesystems_items_name )           | No      | string           | No         | -          | -                           |
| + [type](#filesystems_items_type )           | No      | enum (of string) | No         | -          | -                           |
| + [read_bw](#filesystems_items_read_bw )     | No      | object           | No         | -          | File system read bandwidth  |
| + [write_bw](#filesystems_items_write_bw )   | No      | object           | No         | -          | File system write bandwidth |
| - [read_req](#filesystems_items_read_req )   | No      | object           | No         | -          | File system read requests   |
| - [write_req](#filesystems_items_write_req ) | No      | object           | No         | -          | File system write requests  |
| - [inodes](#filesystems_items_inodes )       | No      | object           | No         | -          | File system write requests  |
| - [accesses](#filesystems_items_accesses )   | No      | object           | No         | -          | File system open and close  |
| - [fsync](#filesystems_items_fsync )         | No      | object           | No         | -          | File system fsync           |
| - [create](#filesystems_items_create )       | No      | object           | No         | -          | File system create          |
| - [open](#filesystems_items_open )           | No      | object           | No         | -          | File system open            |
| - [close](#filesystems_items_close )         | No      | object           | No         | -          | File system close           |
| - [seek](#filesystems_items_seek )           | No      | object           | No         | -          | File system seek            |

#### <a name="filesystems_items_name"></a>19.1.1. Property `Job metric data list > filesystems > filesystems items > name`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

#### <a name="filesystems_items_type"></a>19.1.2. Property `Job metric data list > filesystems > filesystems items > type`

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

#### <a name="filesystems_items_read_bw"></a>19.1.3. Property `Job metric data list > filesystems > filesystems items > read_bw`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | Yes              |
| **Additional properties** | Any type allowed |

**Description:** File system read bandwidth

| Property                                   | Pattern | Type   | Deprecated | Definition                               | Title/Description                                                                                             |
| ------------------------------------------ | ------- | ------ | ---------- | ---------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| + [node](#filesystems_items_read_bw_node ) | No      | object | No         | In embedfs://job-metric-data.schema.json | 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️ |

##### <a name="filesystems_items_read_bw_node"></a>19.1.3.1. Property `Job metric data list > filesystems > filesystems items > read_bw > node`

|                           |                                       |
| ------------------------- | ------------------------------------- |
| **Type**                  | `object`                              |
| **Required**              | Yes                                   |
| **Additional properties** | Any type allowed                      |
| **Defined in**            | embedfs://job-metric-data.schema.json |

**Description:** 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️

#### <a name="filesystems_items_write_bw"></a>19.1.4. Property `Job metric data list > filesystems > filesystems items > write_bw`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | Yes              |
| **Additional properties** | Any type allowed |

**Description:** File system write bandwidth

| Property                                    | Pattern | Type   | Deprecated | Definition                               | Title/Description                                                                                             |
| ------------------------------------------- | ------- | ------ | ---------- | ---------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| + [node](#filesystems_items_write_bw_node ) | No      | object | No         | In embedfs://job-metric-data.schema.json | 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️ |

##### <a name="filesystems_items_write_bw_node"></a>19.1.4.1. Property `Job metric data list > filesystems > filesystems items > write_bw > node`

|                           |                                       |
| ------------------------- | ------------------------------------- |
| **Type**                  | `object`                              |
| **Required**              | Yes                                   |
| **Additional properties** | Any type allowed                      |
| **Defined in**            | embedfs://job-metric-data.schema.json |

**Description:** 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️

#### <a name="filesystems_items_read_req"></a>19.1.5. Property `Job metric data list > filesystems > filesystems items > read_req`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** File system read requests

| Property                                    | Pattern | Type   | Deprecated | Definition                               | Title/Description                                                                                             |
| ------------------------------------------- | ------- | ------ | ---------- | ---------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| + [node](#filesystems_items_read_req_node ) | No      | object | No         | In embedfs://job-metric-data.schema.json | 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️ |

##### <a name="filesystems_items_read_req_node"></a>19.1.5.1. Property `Job metric data list > filesystems > filesystems items > read_req > node`

|                           |                                       |
| ------------------------- | ------------------------------------- |
| **Type**                  | `object`                              |
| **Required**              | Yes                                   |
| **Additional properties** | Any type allowed                      |
| **Defined in**            | embedfs://job-metric-data.schema.json |

**Description:** 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️

#### <a name="filesystems_items_write_req"></a>19.1.6. Property `Job metric data list > filesystems > filesystems items > write_req`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** File system write requests

| Property                                     | Pattern | Type   | Deprecated | Definition                               | Title/Description                                                                                             |
| -------------------------------------------- | ------- | ------ | ---------- | ---------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| + [node](#filesystems_items_write_req_node ) | No      | object | No         | In embedfs://job-metric-data.schema.json | 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️ |

##### <a name="filesystems_items_write_req_node"></a>19.1.6.1. Property `Job metric data list > filesystems > filesystems items > write_req > node`

|                           |                                       |
| ------------------------- | ------------------------------------- |
| **Type**                  | `object`                              |
| **Required**              | Yes                                   |
| **Additional properties** | Any type allowed                      |
| **Defined in**            | embedfs://job-metric-data.schema.json |

**Description:** 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️

#### <a name="filesystems_items_inodes"></a>19.1.7. Property `Job metric data list > filesystems > filesystems items > inodes`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** File system write requests

| Property                                  | Pattern | Type   | Deprecated | Definition                               | Title/Description                                                                                             |
| ----------------------------------------- | ------- | ------ | ---------- | ---------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| + [node](#filesystems_items_inodes_node ) | No      | object | No         | In embedfs://job-metric-data.schema.json | 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️ |

##### <a name="filesystems_items_inodes_node"></a>19.1.7.1. Property `Job metric data list > filesystems > filesystems items > inodes > node`

|                           |                                       |
| ------------------------- | ------------------------------------- |
| **Type**                  | `object`                              |
| **Required**              | Yes                                   |
| **Additional properties** | Any type allowed                      |
| **Defined in**            | embedfs://job-metric-data.schema.json |

**Description:** 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️

#### <a name="filesystems_items_accesses"></a>19.1.8. Property `Job metric data list > filesystems > filesystems items > accesses`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** File system open and close

| Property                                    | Pattern | Type   | Deprecated | Definition                               | Title/Description                                                                                             |
| ------------------------------------------- | ------- | ------ | ---------- | ---------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| + [node](#filesystems_items_accesses_node ) | No      | object | No         | In embedfs://job-metric-data.schema.json | 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️ |

##### <a name="filesystems_items_accesses_node"></a>19.1.8.1. Property `Job metric data list > filesystems > filesystems items > accesses > node`

|                           |                                       |
| ------------------------- | ------------------------------------- |
| **Type**                  | `object`                              |
| **Required**              | Yes                                   |
| **Additional properties** | Any type allowed                      |
| **Defined in**            | embedfs://job-metric-data.schema.json |

**Description:** 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️

#### <a name="filesystems_items_fsync"></a>19.1.9. Property `Job metric data list > filesystems > filesystems items > fsync`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** File system fsync

| Property                                 | Pattern | Type   | Deprecated | Definition                               | Title/Description                                                                                             |
| ---------------------------------------- | ------- | ------ | ---------- | ---------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| + [node](#filesystems_items_fsync_node ) | No      | object | No         | In embedfs://job-metric-data.schema.json | 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️ |

##### <a name="filesystems_items_fsync_node"></a>19.1.9.1. Property `Job metric data list > filesystems > filesystems items > fsync > node`

|                           |                                       |
| ------------------------- | ------------------------------------- |
| **Type**                  | `object`                              |
| **Required**              | Yes                                   |
| **Additional properties** | Any type allowed                      |
| **Defined in**            | embedfs://job-metric-data.schema.json |

**Description:** 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️

#### <a name="filesystems_items_create"></a>19.1.10. Property `Job metric data list > filesystems > filesystems items > create`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** File system create

| Property                                  | Pattern | Type   | Deprecated | Definition                               | Title/Description                                                                                             |
| ----------------------------------------- | ------- | ------ | ---------- | ---------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| + [node](#filesystems_items_create_node ) | No      | object | No         | In embedfs://job-metric-data.schema.json | 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️ |

##### <a name="filesystems_items_create_node"></a>19.1.10.1. Property `Job metric data list > filesystems > filesystems items > create > node`

|                           |                                       |
| ------------------------- | ------------------------------------- |
| **Type**                  | `object`                              |
| **Required**              | Yes                                   |
| **Additional properties** | Any type allowed                      |
| **Defined in**            | embedfs://job-metric-data.schema.json |

**Description:** 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️

#### <a name="filesystems_items_open"></a>19.1.11. Property `Job metric data list > filesystems > filesystems items > open`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** File system open

| Property                                | Pattern | Type   | Deprecated | Definition                               | Title/Description                                                                                             |
| --------------------------------------- | ------- | ------ | ---------- | ---------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| + [node](#filesystems_items_open_node ) | No      | object | No         | In embedfs://job-metric-data.schema.json | 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️ |

##### <a name="filesystems_items_open_node"></a>19.1.11.1. Property `Job metric data list > filesystems > filesystems items > open > node`

|                           |                                       |
| ------------------------- | ------------------------------------- |
| **Type**                  | `object`                              |
| **Required**              | Yes                                   |
| **Additional properties** | Any type allowed                      |
| **Defined in**            | embedfs://job-metric-data.schema.json |

**Description:** 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️

#### <a name="filesystems_items_close"></a>19.1.12. Property `Job metric data list > filesystems > filesystems items > close`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** File system close

| Property                                 | Pattern | Type   | Deprecated | Definition                               | Title/Description                                                                                             |
| ---------------------------------------- | ------- | ------ | ---------- | ---------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| + [node](#filesystems_items_close_node ) | No      | object | No         | In embedfs://job-metric-data.schema.json | 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️ |

##### <a name="filesystems_items_close_node"></a>19.1.12.1. Property `Job metric data list > filesystems > filesystems items > close > node`

|                           |                                       |
| ------------------------- | ------------------------------------- |
| **Type**                  | `object`                              |
| **Required**              | Yes                                   |
| **Additional properties** | Any type allowed                      |
| **Defined in**            | embedfs://job-metric-data.schema.json |

**Description:** 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️

#### <a name="filesystems_items_seek"></a>19.1.13. Property `Job metric data list > filesystems > filesystems items > seek`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** File system seek

| Property                                | Pattern | Type   | Deprecated | Definition                               | Title/Description                                                                                             |
| --------------------------------------- | ------- | ------ | ---------- | ---------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| + [node](#filesystems_items_seek_node ) | No      | object | No         | In embedfs://job-metric-data.schema.json | 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️ |

##### <a name="filesystems_items_seek_node"></a>19.1.13.1. Property `Job metric data list > filesystems > filesystems items > seek > node`

|                           |                                       |
| ------------------------- | ------------------------------------- |
| **Type**                  | `object`                              |
| **Required**              | Yes                                   |
| **Additional properties** | Any type allowed                      |
| **Defined in**            | embedfs://job-metric-data.schema.json |

**Description:** 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️

----------------------------------------------------------------------------------------------------------------------------
Generated using [json-schema-for-humans](https://github.com/coveooss/json-schema-for-humans) on 2024-12-04 at 16:45:59 +0100
