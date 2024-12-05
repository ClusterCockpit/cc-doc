---
title: Cluster Schema
description: ClusterCockpit Cluster Schema Reference
categories: [cc-backend]
tags: [Backend]
weight: 2
---

The following schema in its raw form can be found in the [ClusterCockpit GitHub](https://github.com/ClusterCockpit/cc-backend/tree/master/pkg/schema/schemas) repository.

{{< alert title="Manual Updates">}}
  Changes to the original JSON schema found in the repository are not automatically rendered in this reference documentation.</br></br>
  **Last Update:** 04.12.2024
{{< /alert >}}

## HPC cluster description

- [1. Property `HPC cluster description > name`](#name)
- [2. Property `HPC cluster description > metricConfig`](#metricConfig)
  - [2.1. HPC cluster description > metricConfig > metricConfig items](#metricConfig_items)
    - [2.1.1. Property `HPC cluster description > metricConfig > metricConfig items > name`](#metricConfig_items_name)
    - [2.1.2. Property `HPC cluster description > metricConfig > metricConfig items > unit`](#metricConfig_items_unit)
    - [2.1.3. Property `HPC cluster description > metricConfig > metricConfig items > scope`](#metricConfig_items_scope)
    - [2.1.4. Property `HPC cluster description > metricConfig > metricConfig items > timestep`](#metricConfig_items_timestep)
    - [2.1.5. Property `HPC cluster description > metricConfig > metricConfig items > aggregation`](#metricConfig_items_aggregation)
    - [2.1.6. Property `HPC cluster description > metricConfig > metricConfig items > footprint`](#metricConfig_items_footprint)
    - [2.1.7. Property `HPC cluster description > metricConfig > metricConfig items > energy`](#metricConfig_items_energy)
    - [2.1.8. Property `HPC cluster description > metricConfig > metricConfig items > lowerIsBetter`](#metricConfig_items_lowerIsBetter)
    - [2.1.9. Property `HPC cluster description > metricConfig > metricConfig items > peak`](#metricConfig_items_peak)
    - [2.1.10. Property `HPC cluster description > metricConfig > metricConfig items > normal`](#metricConfig_items_normal)
    - [2.1.11. Property `HPC cluster description > metricConfig > metricConfig items > caution`](#metricConfig_items_caution)
    - [2.1.12. Property `HPC cluster description > metricConfig > metricConfig items > alert`](#metricConfig_items_alert)
    - [2.1.13. Property `HPC cluster description > metricConfig > metricConfig items > subClusters`](#metricConfig_items_subClusters)
      - [2.1.13.1. HPC cluster description > metricConfig > metricConfig items > subClusters > subClusters items](#metricConfig_items_subClusters_items)
        - [2.1.13.1.1. Property `HPC cluster description > metricConfig > metricConfig items > subClusters > subClusters items > name`](#metricConfig_items_subClusters_items_name)
        - [2.1.13.1.2. Property `HPC cluster description > metricConfig > metricConfig items > subClusters > subClusters items > footprint`](#metricConfig_items_subClusters_items_footprint)
        - [2.1.13.1.3. Property `HPC cluster description > metricConfig > metricConfig items > subClusters > subClusters items > energy`](#metricConfig_items_subClusters_items_energy)
        - [2.1.13.1.4. Property `HPC cluster description > metricConfig > metricConfig items > subClusters > subClusters items > lowerIsBetter`](#metricConfig_items_subClusters_items_lowerIsBetter)
        - [2.1.13.1.5. Property `HPC cluster description > metricConfig > metricConfig items > subClusters > subClusters items > peak`](#metricConfig_items_subClusters_items_peak)
        - [2.1.13.1.6. Property `HPC cluster description > metricConfig > metricConfig items > subClusters > subClusters items > normal`](#metricConfig_items_subClusters_items_normal)
        - [2.1.13.1.7. Property `HPC cluster description > metricConfig > metricConfig items > subClusters > subClusters items > caution`](#metricConfig_items_subClusters_items_caution)
        - [2.1.13.1.8. Property `HPC cluster description > metricConfig > metricConfig items > subClusters > subClusters items > alert`](#metricConfig_items_subClusters_items_alert)
        - [2.1.13.1.9. Property `HPC cluster description > metricConfig > metricConfig items > subClusters > subClusters items > remove`](#metricConfig_items_subClusters_items_remove)
- [3. Property `HPC cluster description > subClusters`](#subClusters)
  - [3.1. HPC cluster description > subClusters > subClusters items](#subClusters_items)
    - [3.1.1. Property `HPC cluster description > subClusters > subClusters items > name`](#subClusters_items_name)
    - [3.1.2. Property `HPC cluster description > subClusters > subClusters items > processorType`](#subClusters_items_processorType)
    - [3.1.3. Property `HPC cluster description > subClusters > subClusters items > socketsPerNode`](#subClusters_items_socketsPerNode)
    - [3.1.4. Property `HPC cluster description > subClusters > subClusters items > coresPerSocket`](#subClusters_items_coresPerSocket)
    - [3.1.5. Property `HPC cluster description > subClusters > subClusters items > threadsPerCore`](#subClusters_items_threadsPerCore)
    - [3.1.6. Property `HPC cluster description > subClusters > subClusters items > flopRateScalar`](#subClusters_items_flopRateScalar)
      - [3.1.6.1. Property `HPC cluster description > subClusters > subClusters items > flopRateScalar > unit`](#subClusters_items_flopRateScalar_unit)
      - [3.1.6.2. Property `HPC cluster description > subClusters > subClusters items > flopRateScalar > value`](#subClusters_items_flopRateScalar_value)
    - [3.1.7. Property `HPC cluster description > subClusters > subClusters items > flopRateSimd`](#subClusters_items_flopRateSimd)
      - [3.1.7.1. Property `HPC cluster description > subClusters > subClusters items > flopRateSimd > unit`](#subClusters_items_flopRateSimd_unit)
      - [3.1.7.2. Property `HPC cluster description > subClusters > subClusters items > flopRateSimd > value`](#subClusters_items_flopRateSimd_value)
    - [3.1.8. Property `HPC cluster description > subClusters > subClusters items > memoryBandwidth`](#subClusters_items_memoryBandwidth)
      - [3.1.8.1. Property `HPC cluster description > subClusters > subClusters items > memoryBandwidth > unit`](#subClusters_items_memoryBandwidth_unit)
      - [3.1.8.2. Property `HPC cluster description > subClusters > subClusters items > memoryBandwidth > value`](#subClusters_items_memoryBandwidth_value)
    - [3.1.9. Property `HPC cluster description > subClusters > subClusters items > nodes`](#subClusters_items_nodes)
    - [3.1.10. Property `HPC cluster description > subClusters > subClusters items > topology`](#subClusters_items_topology)
      - [3.1.10.1. Property `HPC cluster description > subClusters > subClusters items > topology > node`](#subClusters_items_topology_node)
        - [3.1.10.1.1. HPC cluster description > subClusters > subClusters items > topology > node > node items](#subClusters_items_topology_node_items)
      - [3.1.10.2. Property `HPC cluster description > subClusters > subClusters items > topology > socket`](#subClusters_items_topology_socket)
        - [3.1.10.2.1. HPC cluster description > subClusters > subClusters items > topology > socket > socket items](#subClusters_items_topology_socket_items)
          - [3.1.10.2.1.1. HPC cluster description > subClusters > subClusters items > topology > socket > socket items > socket items items](#subClusters_items_topology_socket_items_items)
      - [3.1.10.3. Property `HPC cluster description > subClusters > subClusters items > topology > memoryDomain`](#subClusters_items_topology_memoryDomain)
        - [3.1.10.3.1. HPC cluster description > subClusters > subClusters items > topology > memoryDomain > memoryDomain items](#subClusters_items_topology_memoryDomain_items)
          - [3.1.10.3.1.1. HPC cluster description > subClusters > subClusters items > topology > memoryDomain > memoryDomain items > memoryDomain items items](#subClusters_items_topology_memoryDomain_items_items)
      - [3.1.10.4. Property `HPC cluster description > subClusters > subClusters items > topology > die`](#subClusters_items_topology_die)
        - [3.1.10.4.1. HPC cluster description > subClusters > subClusters items > topology > die > die items](#subClusters_items_topology_die_items)
          - [3.1.10.4.1.1. HPC cluster description > subClusters > subClusters items > topology > die > die items > die items items](#subClusters_items_topology_die_items_items)
      - [3.1.10.5. Property `HPC cluster description > subClusters > subClusters items > topology > core`](#subClusters_items_topology_core)
        - [3.1.10.5.1. HPC cluster description > subClusters > subClusters items > topology > core > core items](#subClusters_items_topology_core_items)
          - [3.1.10.5.1.1. HPC cluster description > subClusters > subClusters items > topology > core > core items > core items items](#subClusters_items_topology_core_items_items)
      - [3.1.10.6. Property `HPC cluster description > subClusters > subClusters items > topology > accelerators`](#subClusters_items_topology_accelerators)
        - [3.1.10.6.1. HPC cluster description > subClusters > subClusters items > topology > accelerators > accelerators items](#subClusters_items_topology_accelerators_items)
          - [3.1.10.6.1.1. Property `HPC cluster description > subClusters > subClusters items > topology > accelerators > accelerators items > id`](#subClusters_items_topology_accelerators_items_id)
          - [3.1.10.6.1.2. Property `HPC cluster description > subClusters > subClusters items > topology > accelerators > accelerators items > type`](#subClusters_items_topology_accelerators_items_type)
          - [3.1.10.6.1.3. Property `HPC cluster description > subClusters > subClusters items > topology > accelerators > accelerators items > model`](#subClusters_items_topology_accelerators_items_model)

**Title:** HPC cluster description

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** Meta data information of a HPC cluster

| Property                         | Pattern | Type            | Deprecated | Definition | Title/Description                    |
| -------------------------------- | ------- | --------------- | ---------- | ---------- | ------------------------------------ |
| + [name](#name )                 | No      | string          | No         | -          | The unique identifier of a cluster   |
| + [metricConfig](#metricConfig ) | No      | array of object | No         | -          | Metric specifications                |
| + [subClusters](#subClusters )   | No      | array of object | No         | -          | Array of cluster hardware partitions |

## <a name="name"></a>1. Property `HPC cluster description > name`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** The unique identifier of a cluster

## <a name="metricConfig"></a>2. Property `HPC cluster description > metricConfig`

|              |                   |
| ------------ | ----------------- |
| **Type**     | `array of object` |
| **Required** | Yes               |

**Description:** Metric specifications

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | 1                  |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be           | Description |
| ----------------------------------------- | ----------- |
| [metricConfig items](#metricConfig_items) | -           |

### <a name="metricConfig_items"></a>2.1. HPC cluster description > metricConfig > metricConfig items

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

| Property                                              | Pattern | Type             | Deprecated | Definition                    | Title/Description                                                           |
| ----------------------------------------------------- | ------- | ---------------- | ---------- | ----------------------------- | --------------------------------------------------------------------------- |
| + [name](#metricConfig_items_name )                   | No      | string           | No         | -                             | Metric name                                                                 |
| + [unit](#metricConfig_items_unit )                   | No      | object           | No         | In embedfs://unit.schema.json | Metric unit                                                                 |
| + [scope](#metricConfig_items_scope )                 | No      | string           | No         | -                             | Native measurement resolution                                               |
| + [timestep](#metricConfig_items_timestep )           | No      | integer          | No         | -                             | Frequency of timeseries points                                              |
| + [aggregation](#metricConfig_items_aggregation )     | No      | enum (of string) | No         | -                             | How the metric is aggregated                                                |
| - [footprint](#metricConfig_items_footprint )         | No      | enum (of string) | No         | -                             | Is it a footprint metric and what type                                      |
| - [energy](#metricConfig_items_energy )               | No      | enum (of string) | No         | -                             | Is it used to calculate job energy                                          |
| - [lowerIsBetter](#metricConfig_items_lowerIsBetter ) | No      | boolean          | No         | -                             | Is lower better.                                                            |
| + [peak](#metricConfig_items_peak )                   | No      | number           | No         | -                             | Metric peak threshold (Upper metric limit)                                  |
| + [normal](#metricConfig_items_normal )               | No      | number           | No         | -                             | Metric normal threshold                                                     |
| + [caution](#metricConfig_items_caution )             | No      | number           | No         | -                             | Metric caution threshold (Suspicious but does not require immediate action) |
| + [alert](#metricConfig_items_alert )                 | No      | number           | No         | -                             | Metric alert threshold (Requires immediate action)                          |
| - [subClusters](#metricConfig_items_subClusters )     | No      | array of object  | No         | -                             | Array of cluster hardware partition metric thresholds                       |

#### <a name="metricConfig_items_name"></a>2.1.1. Property `HPC cluster description > metricConfig > metricConfig items > name`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Metric name

#### <a name="metricConfig_items_unit"></a>2.1.2. Property `HPC cluster description > metricConfig > metricConfig items > unit`

|                           |                            |
| ------------------------- | -------------------------- |
| **Type**                  | `object`                   |
| **Required**              | Yes                        |
| **Additional properties** | Any type allowed           |
| **Defined in**            | embedfs://unit.schema.json |

**Description:** Metric unit

#### <a name="metricConfig_items_scope"></a>2.1.3. Property `HPC cluster description > metricConfig > metricConfig items > scope`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Native measurement resolution

#### <a name="metricConfig_items_timestep"></a>2.1.4. Property `HPC cluster description > metricConfig > metricConfig items > timestep`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

**Description:** Frequency of timeseries points

#### <a name="metricConfig_items_aggregation"></a>2.1.5. Property `HPC cluster description > metricConfig > metricConfig items > aggregation`

|              |                    |
| ------------ | ------------------ |
| **Type**     | `enum (of string)` |
| **Required** | Yes                |

**Description:** How the metric is aggregated

Must be one of:
* "sum"
* "avg"

#### <a name="metricConfig_items_footprint"></a>2.1.6. Property `HPC cluster description > metricConfig > metricConfig items > footprint`

|              |                    |
| ------------ | ------------------ |
| **Type**     | `enum (of string)` |
| **Required** | No                 |

**Description:** Is it a footprint metric and what type

Must be one of:
* "avg"
* "max"
* "min"

#### <a name="metricConfig_items_energy"></a>2.1.7. Property `HPC cluster description > metricConfig > metricConfig items > energy`

|              |                    |
| ------------ | ------------------ |
| **Type**     | `enum (of string)` |
| **Required** | No                 |

**Description:** Is it used to calculate job energy

Must be one of:
* "power"
* "energy"

#### <a name="metricConfig_items_lowerIsBetter"></a>2.1.8. Property `HPC cluster description > metricConfig > metricConfig items > lowerIsBetter`

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |

**Description:** Is lower better.

#### <a name="metricConfig_items_peak"></a>2.1.9. Property `HPC cluster description > metricConfig > metricConfig items > peak`

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | Yes      |

**Description:** Metric peak threshold (Upper metric limit)

#### <a name="metricConfig_items_normal"></a>2.1.10. Property `HPC cluster description > metricConfig > metricConfig items > normal`

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | Yes      |

**Description:** Metric normal threshold

#### <a name="metricConfig_items_caution"></a>2.1.11. Property `HPC cluster description > metricConfig > metricConfig items > caution`

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | Yes      |

**Description:** Metric caution threshold (Suspicious but does not require immediate action)

#### <a name="metricConfig_items_alert"></a>2.1.12. Property `HPC cluster description > metricConfig > metricConfig items > alert`

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | Yes      |

**Description:** Metric alert threshold (Requires immediate action)

#### <a name="metricConfig_items_subClusters"></a>2.1.13. Property `HPC cluster description > metricConfig > metricConfig items > subClusters`

|              |                   |
| ------------ | ----------------- |
| **Type**     | `array of object` |
| **Required** | No                |

**Description:** Array of cluster hardware partition metric thresholds

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be                            | Description |
| ---------------------------------------------------------- | ----------- |
| [subClusters items](#metricConfig_items_subClusters_items) | -           |

##### <a name="metricConfig_items_subClusters_items"></a>2.1.13.1. HPC cluster description > metricConfig > metricConfig items > subClusters > subClusters items

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

| Property                                                                | Pattern | Type             | Deprecated | Definition | Title/Description                                                |
| ----------------------------------------------------------------------- | ------- | ---------------- | ---------- | ---------- | ---------------------------------------------------------------- |
| + [name](#metricConfig_items_subClusters_items_name )                   | No      | string           | No         | -          | Hardware partition name                                          |
| - [footprint](#metricConfig_items_subClusters_items_footprint )         | No      | enum (of string) | No         | -          | Is it a footprint metric and what type. Overwrite global setting |
| - [energy](#metricConfig_items_subClusters_items_energy )               | No      | enum (of string) | No         | -          | Is it used to calculate job energy. Overwrite global             |
| - [lowerIsBetter](#metricConfig_items_subClusters_items_lowerIsBetter ) | No      | boolean          | No         | -          | Is lower better. Overwrite global                                |
| - [peak](#metricConfig_items_subClusters_items_peak )                   | No      | number           | No         | -          | -                                                                |
| - [normal](#metricConfig_items_subClusters_items_normal )               | No      | number           | No         | -          | -                                                                |
| - [caution](#metricConfig_items_subClusters_items_caution )             | No      | number           | No         | -          | -                                                                |
| - [alert](#metricConfig_items_subClusters_items_alert )                 | No      | number           | No         | -          | -                                                                |
| - [remove](#metricConfig_items_subClusters_items_remove )               | No      | boolean          | No         | -          | Remove this metric for this subcluster                           |

###### <a name="metricConfig_items_subClusters_items_name"></a>2.1.13.1.1. Property `HPC cluster description > metricConfig > metricConfig items > subClusters > subClusters items > name`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Hardware partition name

###### <a name="metricConfig_items_subClusters_items_footprint"></a>2.1.13.1.2. Property `HPC cluster description > metricConfig > metricConfig items > subClusters > subClusters items > footprint`

|              |                    |
| ------------ | ------------------ |
| **Type**     | `enum (of string)` |
| **Required** | No                 |

**Description:** Is it a footprint metric and what type. Overwrite global setting

Must be one of:
* "avg"
* "max"
* "min"

###### <a name="metricConfig_items_subClusters_items_energy"></a>2.1.13.1.3. Property `HPC cluster description > metricConfig > metricConfig items > subClusters > subClusters items > energy`

|              |                    |
| ------------ | ------------------ |
| **Type**     | `enum (of string)` |
| **Required** | No                 |

**Description:** Is it used to calculate job energy. Overwrite global

Must be one of:
* "power"
* "energy"

###### <a name="metricConfig_items_subClusters_items_lowerIsBetter"></a>2.1.13.1.4. Property `HPC cluster description > metricConfig > metricConfig items > subClusters > subClusters items > lowerIsBetter`

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |

**Description:** Is lower better. Overwrite global

###### <a name="metricConfig_items_subClusters_items_peak"></a>2.1.13.1.5. Property `HPC cluster description > metricConfig > metricConfig items > subClusters > subClusters items > peak`

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |

###### <a name="metricConfig_items_subClusters_items_normal"></a>2.1.13.1.6. Property `HPC cluster description > metricConfig > metricConfig items > subClusters > subClusters items > normal`

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |

###### <a name="metricConfig_items_subClusters_items_caution"></a>2.1.13.1.7. Property `HPC cluster description > metricConfig > metricConfig items > subClusters > subClusters items > caution`

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |

###### <a name="metricConfig_items_subClusters_items_alert"></a>2.1.13.1.8. Property `HPC cluster description > metricConfig > metricConfig items > subClusters > subClusters items > alert`

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |

###### <a name="metricConfig_items_subClusters_items_remove"></a>2.1.13.1.9. Property `HPC cluster description > metricConfig > metricConfig items > subClusters > subClusters items > remove`

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |

**Description:** Remove this metric for this subcluster

## <a name="subClusters"></a>3. Property `HPC cluster description > subClusters`

|              |                   |
| ------------ | ----------------- |
| **Type**     | `array of object` |
| **Required** | Yes               |

**Description:** Array of cluster hardware partitions

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | 1                  |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be         | Description |
| --------------------------------------- | ----------- |
| [subClusters items](#subClusters_items) | -           |

### <a name="subClusters_items"></a>3.1. HPC cluster description > subClusters > subClusters items

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

| Property                                                 | Pattern | Type    | Deprecated | Definition | Title/Description                                           |
| -------------------------------------------------------- | ------- | ------- | ---------- | ---------- | ----------------------------------------------------------- |
| + [name](#subClusters_items_name )                       | No      | string  | No         | -          | Hardware partition name                                     |
| + [processorType](#subClusters_items_processorType )     | No      | string  | No         | -          | Processor type                                              |
| + [socketsPerNode](#subClusters_items_socketsPerNode )   | No      | integer | No         | -          | Number of sockets per node                                  |
| + [coresPerSocket](#subClusters_items_coresPerSocket )   | No      | integer | No         | -          | Number of cores per socket                                  |
| + [threadsPerCore](#subClusters_items_threadsPerCore )   | No      | integer | No         | -          | Number of SMT threads per core                              |
| + [flopRateScalar](#subClusters_items_flopRateScalar )   | No      | object  | No         | -          | Theoretical node peak flop rate for scalar code in GFlops/s |
| + [flopRateSimd](#subClusters_items_flopRateSimd )       | No      | object  | No         | -          | Theoretical node peak flop rate for SIMD code in GFlops/s   |
| + [memoryBandwidth](#subClusters_items_memoryBandwidth ) | No      | object  | No         | -          | Theoretical node peak memory bandwidth in GB/s              |
| + [nodes](#subClusters_items_nodes )                     | No      | string  | No         | -          | Node list expression                                        |
| + [topology](#subClusters_items_topology )               | No      | object  | No         | -          | Node topology                                               |

#### <a name="subClusters_items_name"></a>3.1.1. Property `HPC cluster description > subClusters > subClusters items > name`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Hardware partition name

#### <a name="subClusters_items_processorType"></a>3.1.2. Property `HPC cluster description > subClusters > subClusters items > processorType`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Processor type

#### <a name="subClusters_items_socketsPerNode"></a>3.1.3. Property `HPC cluster description > subClusters > subClusters items > socketsPerNode`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

**Description:** Number of sockets per node

#### <a name="subClusters_items_coresPerSocket"></a>3.1.4. Property `HPC cluster description > subClusters > subClusters items > coresPerSocket`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

**Description:** Number of cores per socket

#### <a name="subClusters_items_threadsPerCore"></a>3.1.5. Property `HPC cluster description > subClusters > subClusters items > threadsPerCore`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

**Description:** Number of SMT threads per core

#### <a name="subClusters_items_flopRateScalar"></a>3.1.6. Property `HPC cluster description > subClusters > subClusters items > flopRateScalar`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | Yes              |
| **Additional properties** | Any type allowed |

**Description:** Theoretical node peak flop rate for scalar code in GFlops/s

| Property                                            | Pattern | Type   | Deprecated | Definition                    | Title/Description |
| --------------------------------------------------- | ------- | ------ | ---------- | ----------------------------- | ----------------- |
| - [unit](#subClusters_items_flopRateScalar_unit )   | No      | object | No         | In embedfs://unit.schema.json | Metric unit       |
| - [value](#subClusters_items_flopRateScalar_value ) | No      | number | No         | -                             | -                 |

##### <a name="subClusters_items_flopRateScalar_unit"></a>3.1.6.1. Property `HPC cluster description > subClusters > subClusters items > flopRateScalar > unit`

|                           |                            |
| ------------------------- | -------------------------- |
| **Type**                  | `object`                   |
| **Required**              | No                         |
| **Additional properties** | Any type allowed           |
| **Defined in**            | embedfs://unit.schema.json |

**Description:** Metric unit

##### <a name="subClusters_items_flopRateScalar_value"></a>3.1.6.2. Property `HPC cluster description > subClusters > subClusters items > flopRateScalar > value`

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |

#### <a name="subClusters_items_flopRateSimd"></a>3.1.7. Property `HPC cluster description > subClusters > subClusters items > flopRateSimd`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | Yes              |
| **Additional properties** | Any type allowed |

**Description:** Theoretical node peak flop rate for SIMD code in GFlops/s

| Property                                          | Pattern | Type   | Deprecated | Definition                    | Title/Description |
| ------------------------------------------------- | ------- | ------ | ---------- | ----------------------------- | ----------------- |
| - [unit](#subClusters_items_flopRateSimd_unit )   | No      | object | No         | In embedfs://unit.schema.json | Metric unit       |
| - [value](#subClusters_items_flopRateSimd_value ) | No      | number | No         | -                             | -                 |

##### <a name="subClusters_items_flopRateSimd_unit"></a>3.1.7.1. Property `HPC cluster description > subClusters > subClusters items > flopRateSimd > unit`

|                           |                            |
| ------------------------- | -------------------------- |
| **Type**                  | `object`                   |
| **Required**              | No                         |
| **Additional properties** | Any type allowed           |
| **Defined in**            | embedfs://unit.schema.json |

**Description:** Metric unit

##### <a name="subClusters_items_flopRateSimd_value"></a>3.1.7.2. Property `HPC cluster description > subClusters > subClusters items > flopRateSimd > value`

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |

#### <a name="subClusters_items_memoryBandwidth"></a>3.1.8. Property `HPC cluster description > subClusters > subClusters items > memoryBandwidth`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | Yes              |
| **Additional properties** | Any type allowed |

**Description:** Theoretical node peak memory bandwidth in GB/s

| Property                                             | Pattern | Type   | Deprecated | Definition                    | Title/Description |
| ---------------------------------------------------- | ------- | ------ | ---------- | ----------------------------- | ----------------- |
| - [unit](#subClusters_items_memoryBandwidth_unit )   | No      | object | No         | In embedfs://unit.schema.json | Metric unit       |
| - [value](#subClusters_items_memoryBandwidth_value ) | No      | number | No         | -                             | -                 |

##### <a name="subClusters_items_memoryBandwidth_unit"></a>3.1.8.1. Property `HPC cluster description > subClusters > subClusters items > memoryBandwidth > unit`

|                           |                            |
| ------------------------- | -------------------------- |
| **Type**                  | `object`                   |
| **Required**              | No                         |
| **Additional properties** | Any type allowed           |
| **Defined in**            | embedfs://unit.schema.json |

**Description:** Metric unit

##### <a name="subClusters_items_memoryBandwidth_value"></a>3.1.8.2. Property `HPC cluster description > subClusters > subClusters items > memoryBandwidth > value`

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |

#### <a name="subClusters_items_nodes"></a>3.1.9. Property `HPC cluster description > subClusters > subClusters items > nodes`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Node list expression

#### <a name="subClusters_items_topology"></a>3.1.10. Property `HPC cluster description > subClusters > subClusters items > topology`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | Yes              |
| **Additional properties** | Any type allowed |

**Description:** Node topology

| Property                                                    | Pattern | Type             | Deprecated | Definition | Title/Description               |
| ----------------------------------------------------------- | ------- | ---------------- | ---------- | ---------- | ------------------------------- |
| + [node](#subClusters_items_topology_node )                 | No      | array of integer | No         | -          | HwTread lists of node           |
| + [socket](#subClusters_items_topology_socket )             | No      | array of array   | No         | -          | HwTread lists of sockets        |
| + [memoryDomain](#subClusters_items_topology_memoryDomain ) | No      | array of array   | No         | -          | HwTread lists of memory domains |
| - [die](#subClusters_items_topology_die )                   | No      | array of array   | No         | -          | HwTread lists of dies           |
| - [core](#subClusters_items_topology_core )                 | No      | array of array   | No         | -          | HwTread lists of cores          |
| - [accelerators](#subClusters_items_topology_accelerators ) | No      | array of object  | No         | -          | List of of accelerator devices  |

##### <a name="subClusters_items_topology_node"></a>3.1.10.1. Property `HPC cluster description > subClusters > subClusters items > topology > node`

|              |                    |
| ------------ | ------------------ |
| **Type**     | `array of integer` |
| **Required** | Yes                |

**Description:** HwTread lists of node

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be                      | Description |
| ---------------------------------------------------- | ----------- |
| [node items](#subClusters_items_topology_node_items) | -           |

###### <a name="subClusters_items_topology_node_items"></a>3.1.10.1.1. HPC cluster description > subClusters > subClusters items > topology > node > node items

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

##### <a name="subClusters_items_topology_socket"></a>3.1.10.2. Property `HPC cluster description > subClusters > subClusters items > topology > socket`

|              |                  |
| ------------ | ---------------- |
| **Type**     | `array of array` |
| **Required** | Yes              |

**Description:** HwTread lists of sockets

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be                          | Description |
| -------------------------------------------------------- | ----------- |
| [socket items](#subClusters_items_topology_socket_items) | -           |

###### <a name="subClusters_items_topology_socket_items"></a>3.1.10.2.1. HPC cluster description > subClusters > subClusters items > topology > socket > socket items

|              |                    |
| ------------ | ------------------ |
| **Type**     | `array of integer` |
| **Required** | No                 |

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be                                      | Description |
| -------------------------------------------------------------------- | ----------- |
| [socket items items](#subClusters_items_topology_socket_items_items) | -           |

###### <a name="subClusters_items_topology_socket_items_items"></a>3.1.10.2.1.1. HPC cluster description > subClusters > subClusters items > topology > socket > socket items > socket items items

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

##### <a name="subClusters_items_topology_memoryDomain"></a>3.1.10.3. Property `HPC cluster description > subClusters > subClusters items > topology > memoryDomain`

|              |                  |
| ------------ | ---------------- |
| **Type**     | `array of array` |
| **Required** | Yes              |

**Description:** HwTread lists of memory domains

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be                                      | Description |
| -------------------------------------------------------------------- | ----------- |
| [memoryDomain items](#subClusters_items_topology_memoryDomain_items) | -           |

###### <a name="subClusters_items_topology_memoryDomain_items"></a>3.1.10.3.1. HPC cluster description > subClusters > subClusters items > topology > memoryDomain > memoryDomain items

|              |                    |
| ------------ | ------------------ |
| **Type**     | `array of integer` |
| **Required** | No                 |

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be                                                  | Description |
| -------------------------------------------------------------------------------- | ----------- |
| [memoryDomain items items](#subClusters_items_topology_memoryDomain_items_items) | -           |

###### <a name="subClusters_items_topology_memoryDomain_items_items"></a>3.1.10.3.1.1. HPC cluster description > subClusters > subClusters items > topology > memoryDomain > memoryDomain items > memoryDomain items items

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

##### <a name="subClusters_items_topology_die"></a>3.1.10.4. Property `HPC cluster description > subClusters > subClusters items > topology > die`

|              |                  |
| ------------ | ---------------- |
| **Type**     | `array of array` |
| **Required** | No               |

**Description:** HwTread lists of dies

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be                    | Description |
| -------------------------------------------------- | ----------- |
| [die items](#subClusters_items_topology_die_items) | -           |

###### <a name="subClusters_items_topology_die_items"></a>3.1.10.4.1. HPC cluster description > subClusters > subClusters items > topology > die > die items

|              |                    |
| ------------ | ------------------ |
| **Type**     | `array of integer` |
| **Required** | No                 |

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be                                | Description |
| -------------------------------------------------------------- | ----------- |
| [die items items](#subClusters_items_topology_die_items_items) | -           |

###### <a name="subClusters_items_topology_die_items_items"></a>3.1.10.4.1.1. HPC cluster description > subClusters > subClusters items > topology > die > die items > die items items

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

##### <a name="subClusters_items_topology_core"></a>3.1.10.5. Property `HPC cluster description > subClusters > subClusters items > topology > core`

|              |                  |
| ------------ | ---------------- |
| **Type**     | `array of array` |
| **Required** | No               |

**Description:** HwTread lists of cores

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be                      | Description |
| ---------------------------------------------------- | ----------- |
| [core items](#subClusters_items_topology_core_items) | -           |

###### <a name="subClusters_items_topology_core_items"></a>3.1.10.5.1. HPC cluster description > subClusters > subClusters items > topology > core > core items

|              |                    |
| ------------ | ------------------ |
| **Type**     | `array of integer` |
| **Required** | No                 |

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be                                  | Description |
| ---------------------------------------------------------------- | ----------- |
| [core items items](#subClusters_items_topology_core_items_items) | -           |

###### <a name="subClusters_items_topology_core_items_items"></a>3.1.10.5.1.1. HPC cluster description > subClusters > subClusters items > topology > core > core items > core items items

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

##### <a name="subClusters_items_topology_accelerators"></a>3.1.10.6. Property `HPC cluster description > subClusters > subClusters items > topology > accelerators`

|              |                   |
| ------------ | ----------------- |
| **Type**     | `array of object` |
| **Required** | No                |

**Description:** List of of accelerator devices

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be                                      | Description |
| -------------------------------------------------------------------- | ----------- |
| [accelerators items](#subClusters_items_topology_accelerators_items) | -           |

###### <a name="subClusters_items_topology_accelerators_items"></a>3.1.10.6.1. HPC cluster description > subClusters > subClusters items > topology > accelerators > accelerators items

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

| Property                                                         | Pattern | Type             | Deprecated | Definition | Title/Description     |
| ---------------------------------------------------------------- | ------- | ---------------- | ---------- | ---------- | --------------------- |
| + [id](#subClusters_items_topology_accelerators_items_id )       | No      | string           | No         | -          | The unique device id  |
| + [type](#subClusters_items_topology_accelerators_items_type )   | No      | enum (of string) | No         | -          | The accelerator type  |
| + [model](#subClusters_items_topology_accelerators_items_model ) | No      | string           | No         | -          | The accelerator model |

###### <a name="subClusters_items_topology_accelerators_items_id"></a>3.1.10.6.1.1. Property `HPC cluster description > subClusters > subClusters items > topology > accelerators > accelerators items > id`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** The unique device id

###### <a name="subClusters_items_topology_accelerators_items_type"></a>3.1.10.6.1.2. Property `HPC cluster description > subClusters > subClusters items > topology > accelerators > accelerators items > type`

|              |                    |
| ------------ | ------------------ |
| **Type**     | `enum (of string)` |
| **Required** | Yes                |

**Description:** The accelerator type

Must be one of:
* "Nvidia GPU"
* "AMD GPU"
* "Intel GPU"

###### <a name="subClusters_items_topology_accelerators_items_model"></a>3.1.10.6.1.3. Property `HPC cluster description > subClusters > subClusters items > topology > accelerators > accelerators items > model`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** The accelerator model

----------------------------------------------------------------------------------------------------------------------------
Generated using [json-schema-for-humans](https://github.com/coveooss/json-schema-for-humans) on 2024-12-04 at 16:45:59 +0100
