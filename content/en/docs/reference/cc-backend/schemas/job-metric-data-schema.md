---
title: Job Archive Metrics Data Schema
description: ClusterCockpit Job Archive Metrics Data Schema Reference
categories: [cc-backend]
tags: [Backend, Archive]
weight: 7
---

The following schema in its raw form can be found in the [ClusterCockpit GitHub](https://github.com/ClusterCockpit/cc-backend/tree/master/pkg/schema/schemas) repository.

{{< alert title="Manual Updates">}}
  Changes to the original JSON schema found in the repository are not automatically rendered in this reference documentation.</br></br>
  **Last Update:** 04.12.2024
{{< /alert >}}

## Job metric data

- [1. Property `Job metric data > unit`](#unit)
- [2. Property `Job metric data > timestep`](#timestep)
- [3. Property `Job metric data > thresholds`](#thresholds)
  - [3.1. Property `Job metric data > thresholds > peak`](#thresholds_peak)
  - [3.2. Property `Job metric data > thresholds > normal`](#thresholds_normal)
  - [3.3. Property `Job metric data > thresholds > caution`](#thresholds_caution)
  - [3.4. Property `Job metric data > thresholds > alert`](#thresholds_alert)
- [4. Property `Job metric data > statisticsSeries`](#statisticsSeries)
  - [4.1. Property `Job metric data > statisticsSeries > min`](#statisticsSeries_min)
    - [4.1.1. Job metric data > statisticsSeries > min > min items](#statisticsSeries_min_items)
  - [4.2. Property `Job metric data > statisticsSeries > max`](#statisticsSeries_max)
    - [4.2.1. Job metric data > statisticsSeries > max > max items](#statisticsSeries_max_items)
  - [4.3. Property `Job metric data > statisticsSeries > mean`](#statisticsSeries_mean)
    - [4.3.1. Job metric data > statisticsSeries > mean > mean items](#statisticsSeries_mean_items)
  - [4.4. Property `Job metric data > statisticsSeries > percentiles`](#statisticsSeries_percentiles)
    - [4.4.1. Property `Job metric data > statisticsSeries > percentiles > 10`](#statisticsSeries_percentiles_10)
      - [4.4.1.1. Job metric data > statisticsSeries > percentiles > 10 > 10 items](#statisticsSeries_percentiles_10_items)
    - [4.4.2. Property `Job metric data > statisticsSeries > percentiles > 20`](#statisticsSeries_percentiles_20)
      - [4.4.2.1. Job metric data > statisticsSeries > percentiles > 20 > 20 items](#statisticsSeries_percentiles_20_items)
    - [4.4.3. Property `Job metric data > statisticsSeries > percentiles > 30`](#statisticsSeries_percentiles_30)
      - [4.4.3.1. Job metric data > statisticsSeries > percentiles > 30 > 30 items](#statisticsSeries_percentiles_30_items)
    - [4.4.4. Property `Job metric data > statisticsSeries > percentiles > 40`](#statisticsSeries_percentiles_40)
      - [4.4.4.1. Job metric data > statisticsSeries > percentiles > 40 > 40 items](#statisticsSeries_percentiles_40_items)
    - [4.4.5. Property `Job metric data > statisticsSeries > percentiles > 50`](#statisticsSeries_percentiles_50)
      - [4.4.5.1. Job metric data > statisticsSeries > percentiles > 50 > 50 items](#statisticsSeries_percentiles_50_items)
    - [4.4.6. Property `Job metric data > statisticsSeries > percentiles > 60`](#statisticsSeries_percentiles_60)
      - [4.4.6.1. Job metric data > statisticsSeries > percentiles > 60 > 60 items](#statisticsSeries_percentiles_60_items)
    - [4.4.7. Property `Job metric data > statisticsSeries > percentiles > 70`](#statisticsSeries_percentiles_70)
      - [4.4.7.1. Job metric data > statisticsSeries > percentiles > 70 > 70 items](#statisticsSeries_percentiles_70_items)
    - [4.4.8. Property `Job metric data > statisticsSeries > percentiles > 80`](#statisticsSeries_percentiles_80)
      - [4.4.8.1. Job metric data > statisticsSeries > percentiles > 80 > 80 items](#statisticsSeries_percentiles_80_items)
    - [4.4.9. Property `Job metric data > statisticsSeries > percentiles > 90`](#statisticsSeries_percentiles_90)
      - [4.4.9.1. Job metric data > statisticsSeries > percentiles > 90 > 90 items](#statisticsSeries_percentiles_90_items)
    - [4.4.10. Property `Job metric data > statisticsSeries > percentiles > 25`](#statisticsSeries_percentiles_25)
      - [4.4.10.1. Job metric data > statisticsSeries > percentiles > 25 > 25 items](#statisticsSeries_percentiles_25_items)
    - [4.4.11. Property `Job metric data > statisticsSeries > percentiles > 75`](#statisticsSeries_percentiles_75)
      - [4.4.11.1. Job metric data > statisticsSeries > percentiles > 75 > 75 items](#statisticsSeries_percentiles_75_items)
- [5. Property `Job metric data > series`](#series)
  - [5.1. Job metric data > series > series items](#series_items)
    - [5.1.1. Property `Job metric data > series > series items > hostname`](#series_items_hostname)
    - [5.1.2. Property `Job metric data > series > series items > id`](#series_items_id)
    - [5.1.3. Property `Job metric data > series > series items > statistics`](#series_items_statistics)
      - [5.1.3.1. Property `Job metric data > series > series items > statistics > avg`](#series_items_statistics_avg)
      - [5.1.3.2. Property `Job metric data > series > series items > statistics > min`](#series_items_statistics_min)
      - [5.1.3.3. Property `Job metric data > series > series items > statistics > max`](#series_items_statistics_max)
    - [5.1.4. Property `Job metric data > series > series items > data`](#series_items_data)
      - [5.1.4.1. At least one of the items must be](#autogenerated_heading_2)

**Title:** Job metric data

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** Metric data of a HPC job

| Property                                 | Pattern | Type            | Deprecated | Definition                    | Title/Description                     |
| ---------------------------------------- | ------- | --------------- | ---------- | ----------------------------- | ------------------------------------- |
| + [unit](#unit )                         | No      | object          | No         | In embedfs://unit.schema.json | Metric unit                           |
| + [timestep](#timestep )                 | No      | integer         | No         | -                             | Measurement interval in seconds       |
| - [thresholds](#thresholds )             | No      | object          | No         | -                             | Metric thresholds for specific system |
| - [statisticsSeries](#statisticsSeries ) | No      | object          | No         | -                             | Statistics series across topology     |
| + [series](#series )                     | No      | array of object | No         | -                             | -                                     |

## <a name="unit"></a>1. Property `Job metric data > unit`

|                           |                            |
| ------------------------- | -------------------------- |
| **Type**                  | `object`                   |
| **Required**              | Yes                        |
| **Additional properties** | Any type allowed           |
| **Defined in**            | embedfs://unit.schema.json |

**Description:** Metric unit

## <a name="timestep"></a>2. Property `Job metric data > timestep`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

**Description:** Measurement interval in seconds

## <a name="thresholds"></a>3. Property `Job metric data > thresholds`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** Metric thresholds for specific system

| Property                          | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [peak](#thresholds_peak )       | No      | number | No         | -          | -                 |
| - [normal](#thresholds_normal )   | No      | number | No         | -          | -                 |
| - [caution](#thresholds_caution ) | No      | number | No         | -          | -                 |
| - [alert](#thresholds_alert )     | No      | number | No         | -          | -                 |

### <a name="thresholds_peak"></a>3.1. Property `Job metric data > thresholds > peak`

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |

### <a name="thresholds_normal"></a>3.2. Property `Job metric data > thresholds > normal`

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |

### <a name="thresholds_caution"></a>3.3. Property `Job metric data > thresholds > caution`

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |

### <a name="thresholds_alert"></a>3.4. Property `Job metric data > thresholds > alert`

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |

## <a name="statisticsSeries"></a>4. Property `Job metric data > statisticsSeries`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** Statistics series across topology

| Property                                        | Pattern | Type            | Deprecated | Definition | Title/Description |
| ----------------------------------------------- | ------- | --------------- | ---------- | ---------- | ----------------- |
| - [min](#statisticsSeries_min )                 | No      | array of number | No         | -          | -                 |
| - [max](#statisticsSeries_max )                 | No      | array of number | No         | -          | -                 |
| - [mean](#statisticsSeries_mean )               | No      | array of number | No         | -          | -                 |
| - [percentiles](#statisticsSeries_percentiles ) | No      | object          | No         | -          | -                 |

### <a name="statisticsSeries_min"></a>4.1. Property `Job metric data > statisticsSeries > min`

|              |                   |
| ------------ | ----------------- |
| **Type**     | `array of number` |
| **Required** | No                |

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | 3                  |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be          | Description |
| ---------------------------------------- | ----------- |
| [min items](#statisticsSeries_min_items) | -           |

#### <a name="statisticsSeries_min_items"></a>4.1.1. Job metric data > statisticsSeries > min > min items

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |

| Restrictions |        |
| ------------ | ------ |
| **Minimum**  | &ge; 0 |

### <a name="statisticsSeries_max"></a>4.2. Property `Job metric data > statisticsSeries > max`

|              |                   |
| ------------ | ----------------- |
| **Type**     | `array of number` |
| **Required** | No                |

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | 3                  |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be          | Description |
| ---------------------------------------- | ----------- |
| [max items](#statisticsSeries_max_items) | -           |

#### <a name="statisticsSeries_max_items"></a>4.2.1. Job metric data > statisticsSeries > max > max items

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |

| Restrictions |        |
| ------------ | ------ |
| **Minimum**  | &ge; 0 |

### <a name="statisticsSeries_mean"></a>4.3. Property `Job metric data > statisticsSeries > mean`

|              |                   |
| ------------ | ----------------- |
| **Type**     | `array of number` |
| **Required** | No                |

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | 3                  |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be            | Description |
| ------------------------------------------ | ----------- |
| [mean items](#statisticsSeries_mean_items) | -           |

#### <a name="statisticsSeries_mean_items"></a>4.3.1. Job metric data > statisticsSeries > mean > mean items

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |

| Restrictions |        |
| ------------ | ------ |
| **Minimum**  | &ge; 0 |

### <a name="statisticsSeries_percentiles"></a>4.4. Property `Job metric data > statisticsSeries > percentiles`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

| Property                                  | Pattern | Type            | Deprecated | Definition | Title/Description |
| ----------------------------------------- | ------- | --------------- | ---------- | ---------- | ----------------- |
| - [10](#statisticsSeries_percentiles_10 ) | No      | array of number | No         | -          | -                 |
| - [20](#statisticsSeries_percentiles_20 ) | No      | array of number | No         | -          | -                 |
| - [30](#statisticsSeries_percentiles_30 ) | No      | array of number | No         | -          | -                 |
| - [40](#statisticsSeries_percentiles_40 ) | No      | array of number | No         | -          | -                 |
| - [50](#statisticsSeries_percentiles_50 ) | No      | array of number | No         | -          | -                 |
| - [60](#statisticsSeries_percentiles_60 ) | No      | array of number | No         | -          | -                 |
| - [70](#statisticsSeries_percentiles_70 ) | No      | array of number | No         | -          | -                 |
| - [80](#statisticsSeries_percentiles_80 ) | No      | array of number | No         | -          | -                 |
| - [90](#statisticsSeries_percentiles_90 ) | No      | array of number | No         | -          | -                 |
| - [25](#statisticsSeries_percentiles_25 ) | No      | array of number | No         | -          | -                 |
| - [75](#statisticsSeries_percentiles_75 ) | No      | array of number | No         | -          | -                 |

#### <a name="statisticsSeries_percentiles_10"></a>4.4.1. Property `Job metric data > statisticsSeries > percentiles > 10`

|              |                   |
| ------------ | ----------------- |
| **Type**     | `array of number` |
| **Required** | No                |

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | 3                  |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be                    | Description |
| -------------------------------------------------- | ----------- |
| [10 items](#statisticsSeries_percentiles_10_items) | -           |

##### <a name="statisticsSeries_percentiles_10_items"></a>4.4.1.1. Job metric data > statisticsSeries > percentiles > 10 > 10 items

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |

| Restrictions |        |
| ------------ | ------ |
| **Minimum**  | &ge; 0 |

#### <a name="statisticsSeries_percentiles_20"></a>4.4.2. Property `Job metric data > statisticsSeries > percentiles > 20`

|              |                   |
| ------------ | ----------------- |
| **Type**     | `array of number` |
| **Required** | No                |

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | 3                  |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be                    | Description |
| -------------------------------------------------- | ----------- |
| [20 items](#statisticsSeries_percentiles_20_items) | -           |

##### <a name="statisticsSeries_percentiles_20_items"></a>4.4.2.1. Job metric data > statisticsSeries > percentiles > 20 > 20 items

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |

| Restrictions |        |
| ------------ | ------ |
| **Minimum**  | &ge; 0 |

#### <a name="statisticsSeries_percentiles_30"></a>4.4.3. Property `Job metric data > statisticsSeries > percentiles > 30`

|              |                   |
| ------------ | ----------------- |
| **Type**     | `array of number` |
| **Required** | No                |

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | 3                  |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be                    | Description |
| -------------------------------------------------- | ----------- |
| [30 items](#statisticsSeries_percentiles_30_items) | -           |

##### <a name="statisticsSeries_percentiles_30_items"></a>4.4.3.1. Job metric data > statisticsSeries > percentiles > 30 > 30 items

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |

| Restrictions |        |
| ------------ | ------ |
| **Minimum**  | &ge; 0 |

#### <a name="statisticsSeries_percentiles_40"></a>4.4.4. Property `Job metric data > statisticsSeries > percentiles > 40`

|              |                   |
| ------------ | ----------------- |
| **Type**     | `array of number` |
| **Required** | No                |

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | 3                  |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be                    | Description |
| -------------------------------------------------- | ----------- |
| [40 items](#statisticsSeries_percentiles_40_items) | -           |

##### <a name="statisticsSeries_percentiles_40_items"></a>4.4.4.1. Job metric data > statisticsSeries > percentiles > 40 > 40 items

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |

| Restrictions |        |
| ------------ | ------ |
| **Minimum**  | &ge; 0 |

#### <a name="statisticsSeries_percentiles_50"></a>4.4.5. Property `Job metric data > statisticsSeries > percentiles > 50`

|              |                   |
| ------------ | ----------------- |
| **Type**     | `array of number` |
| **Required** | No                |

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | 3                  |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be                    | Description |
| -------------------------------------------------- | ----------- |
| [50 items](#statisticsSeries_percentiles_50_items) | -           |

##### <a name="statisticsSeries_percentiles_50_items"></a>4.4.5.1. Job metric data > statisticsSeries > percentiles > 50 > 50 items

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |

| Restrictions |        |
| ------------ | ------ |
| **Minimum**  | &ge; 0 |

#### <a name="statisticsSeries_percentiles_60"></a>4.4.6. Property `Job metric data > statisticsSeries > percentiles > 60`

|              |                   |
| ------------ | ----------------- |
| **Type**     | `array of number` |
| **Required** | No                |

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | 3                  |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be                    | Description |
| -------------------------------------------------- | ----------- |
| [60 items](#statisticsSeries_percentiles_60_items) | -           |

##### <a name="statisticsSeries_percentiles_60_items"></a>4.4.6.1. Job metric data > statisticsSeries > percentiles > 60 > 60 items

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |

| Restrictions |        |
| ------------ | ------ |
| **Minimum**  | &ge; 0 |

#### <a name="statisticsSeries_percentiles_70"></a>4.4.7. Property `Job metric data > statisticsSeries > percentiles > 70`

|              |                   |
| ------------ | ----------------- |
| **Type**     | `array of number` |
| **Required** | No                |

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | 3                  |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be                    | Description |
| -------------------------------------------------- | ----------- |
| [70 items](#statisticsSeries_percentiles_70_items) | -           |

##### <a name="statisticsSeries_percentiles_70_items"></a>4.4.7.1. Job metric data > statisticsSeries > percentiles > 70 > 70 items

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |

| Restrictions |        |
| ------------ | ------ |
| **Minimum**  | &ge; 0 |

#### <a name="statisticsSeries_percentiles_80"></a>4.4.8. Property `Job metric data > statisticsSeries > percentiles > 80`

|              |                   |
| ------------ | ----------------- |
| **Type**     | `array of number` |
| **Required** | No                |

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | 3                  |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be                    | Description |
| -------------------------------------------------- | ----------- |
| [80 items](#statisticsSeries_percentiles_80_items) | -           |

##### <a name="statisticsSeries_percentiles_80_items"></a>4.4.8.1. Job metric data > statisticsSeries > percentiles > 80 > 80 items

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |

| Restrictions |        |
| ------------ | ------ |
| **Minimum**  | &ge; 0 |

#### <a name="statisticsSeries_percentiles_90"></a>4.4.9. Property `Job metric data > statisticsSeries > percentiles > 90`

|              |                   |
| ------------ | ----------------- |
| **Type**     | `array of number` |
| **Required** | No                |

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | 3                  |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be                    | Description |
| -------------------------------------------------- | ----------- |
| [90 items](#statisticsSeries_percentiles_90_items) | -           |

##### <a name="statisticsSeries_percentiles_90_items"></a>4.4.9.1. Job metric data > statisticsSeries > percentiles > 90 > 90 items

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |

| Restrictions |        |
| ------------ | ------ |
| **Minimum**  | &ge; 0 |

#### <a name="statisticsSeries_percentiles_25"></a>4.4.10. Property `Job metric data > statisticsSeries > percentiles > 25`

|              |                   |
| ------------ | ----------------- |
| **Type**     | `array of number` |
| **Required** | No                |

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | 3                  |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be                    | Description |
| -------------------------------------------------- | ----------- |
| [25 items](#statisticsSeries_percentiles_25_items) | -           |

##### <a name="statisticsSeries_percentiles_25_items"></a>4.4.10.1. Job metric data > statisticsSeries > percentiles > 25 > 25 items

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |

| Restrictions |        |
| ------------ | ------ |
| **Minimum**  | &ge; 0 |

#### <a name="statisticsSeries_percentiles_75"></a>4.4.11. Property `Job metric data > statisticsSeries > percentiles > 75`

|              |                   |
| ------------ | ----------------- |
| **Type**     | `array of number` |
| **Required** | No                |

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | 3                  |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be                    | Description |
| -------------------------------------------------- | ----------- |
| [75 items](#statisticsSeries_percentiles_75_items) | -           |

##### <a name="statisticsSeries_percentiles_75_items"></a>4.4.11.1. Job metric data > statisticsSeries > percentiles > 75 > 75 items

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |

| Restrictions |        |
| ------------ | ------ |
| **Minimum**  | &ge; 0 |

## <a name="series"></a>5. Property `Job metric data > series`

|              |                   |
| ------------ | ----------------- |
| **Type**     | `array of object` |
| **Required** | Yes               |

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be | Description |
| ------------------------------- | ----------- |
| [series items](#series_items)   | -           |

### <a name="series_items"></a>5.1. Job metric data > series > series items

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

| Property                                  | Pattern | Type   | Deprecated | Definition | Title/Description                |
| ----------------------------------------- | ------- | ------ | ---------- | ---------- | -------------------------------- |
| + [hostname](#series_items_hostname )     | No      | string | No         | -          | -                                |
| - [id](#series_items_id )                 | No      | string | No         | -          | -                                |
| + [statistics](#series_items_statistics ) | No      | object | No         | -          | Statistics across time dimension |
| + [data](#series_items_data )             | No      | array  | No         | -          | -                                |

#### <a name="series_items_hostname"></a>5.1.1. Property `Job metric data > series > series items > hostname`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

#### <a name="series_items_id"></a>5.1.2. Property `Job metric data > series > series items > id`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

#### <a name="series_items_statistics"></a>5.1.3. Property `Job metric data > series > series items > statistics`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | Yes              |
| **Additional properties** | Any type allowed |

**Description:** Statistics across time dimension

| Property                               | Pattern | Type   | Deprecated | Definition | Title/Description |
| -------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| + [avg](#series_items_statistics_avg ) | No      | number | No         | -          | Series average    |
| + [min](#series_items_statistics_min ) | No      | number | No         | -          | Series minimum    |
| + [max](#series_items_statistics_max ) | No      | number | No         | -          | Series maximum    |

##### <a name="series_items_statistics_avg"></a>5.1.3.1. Property `Job metric data > series > series items > statistics > avg`

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | Yes      |

**Description:** Series average

| Restrictions |        |
| ------------ | ------ |
| **Minimum**  | &ge; 0 |

##### <a name="series_items_statistics_min"></a>5.1.3.2. Property `Job metric data > series > series items > statistics > min`

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | Yes      |

**Description:** Series minimum

| Restrictions |        |
| ------------ | ------ |
| **Minimum**  | &ge; 0 |

##### <a name="series_items_statistics_max"></a>5.1.3.3. Property `Job metric data > series > series items > statistics > max`

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | Yes      |

**Description:** Series maximum

| Restrictions |        |
| ------------ | ------ |
| **Minimum**  | &ge; 0 |

#### <a name="series_items_data"></a>5.1.4. Property `Job metric data > series > series items > data`

|              |         |
| ------------ | ------- |
| **Type**     | `array` |
| **Required** | Yes     |

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | 1                  |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

##### <a name="autogenerated_heading_2"></a>5.1.4.1. At least one of the items must be

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |

| Restrictions |        |
| ------------ | ------ |
| **Minimum**  | &ge; 0 |

----------------------------------------------------------------------------------------------------------------------------
Generated using [json-schema-for-humans](https://github.com/coveooss/json-schema-for-humans) on 2024-12-04 at 16:45:59 +0100
