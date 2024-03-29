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
  **Last Update:** 02.02.2024
{{< /alert >}}

## Job metric data

- [1. [Required] Property Job metric data > unit](#unit)
  - [1.1. [Required] Property Job metric data > unit > base](#unit_base)
  - [1.2. [Optional] Property Job metric data > unit > prefix](#unit_prefix)
- [2. [Required] Property Job metric data > timestep](#timestep)
- [3. [Optional] Property Job metric data > thresholds](#thresholds)
  - [3.1. [Optional] Property Job metric data > thresholds > peak](#thresholds_peak)
  - [3.2. [Optional] Property Job metric data > thresholds > normal](#thresholds_normal)
  - [3.3. [Optional] Property Job metric data > thresholds > caution](#thresholds_caution)
  - [3.4. [Optional] Property Job metric data > thresholds > alert](#thresholds_alert)
- [4. [Optional] Property Job metric data > statisticsSeries](#statisticsSeries)
  - [4.1. [Optional] Property Job metric data > statisticsSeries > min](#statisticsSeries_min)
    - [4.1.1. Job metric data > statisticsSeries > min > min items](#autogenerated_heading_2)
  - [4.2. [Optional] Property Job metric data > statisticsSeries > max](#statisticsSeries_max)
    - [4.2.1. Job metric data > statisticsSeries > max > max items](#autogenerated_heading_3)
  - [4.3. [Optional] Property Job metric data > statisticsSeries > mean](#statisticsSeries_mean)
    - [4.3.1. Job metric data > statisticsSeries > mean > mean items](#autogenerated_heading_4)
  - [4.4. [Optional] Property Job metric data > statisticsSeries > percentiles](#statisticsSeries_percentiles)
    - [4.4.1. [Optional] Property Job metric data > statisticsSeries > percentiles > 10](#statisticsSeries_percentiles_10)
      - [4.4.1.1. Job metric data > statisticsSeries > percentiles > 10 > 10 items](#autogenerated_heading_5)
    - [4.4.2. [Optional] Property Job metric data > statisticsSeries > percentiles > 20](#statisticsSeries_percentiles_20)
      - [4.4.2.1. Job metric data > statisticsSeries > percentiles > 20 > 20 items](#autogenerated_heading_6)
    - [4.4.3. [Optional] Property Job metric data > statisticsSeries > percentiles > 30](#statisticsSeries_percentiles_30)
      - [4.4.3.1. Job metric data > statisticsSeries > percentiles > 30 > 30 items](#autogenerated_heading_7)
    - [4.4.4. [Optional] Property Job metric data > statisticsSeries > percentiles > 40](#statisticsSeries_percentiles_40)
      - [4.4.4.1. Job metric data > statisticsSeries > percentiles > 40 > 40 items](#autogenerated_heading_8)
    - [4.4.5. [Optional] Property Job metric data > statisticsSeries > percentiles > 50](#statisticsSeries_percentiles_50)
      - [4.4.5.1. Job metric data > statisticsSeries > percentiles > 50 > 50 items](#autogenerated_heading_9)
    - [4.4.6. [Optional] Property Job metric data > statisticsSeries > percentiles > 60](#statisticsSeries_percentiles_60)
      - [4.4.6.1. Job metric data > statisticsSeries > percentiles > 60 > 60 items](#autogenerated_heading_10)
    - [4.4.7. [Optional] Property Job metric data > statisticsSeries > percentiles > 70](#statisticsSeries_percentiles_70)
      - [4.4.7.1. Job metric data > statisticsSeries > percentiles > 70 > 70 items](#autogenerated_heading_11)
    - [4.4.8. [Optional] Property Job metric data > statisticsSeries > percentiles > 80](#statisticsSeries_percentiles_80)
      - [4.4.8.1. Job metric data > statisticsSeries > percentiles > 80 > 80 items](#autogenerated_heading_12)
    - [4.4.9. [Optional] Property Job metric data > statisticsSeries > percentiles > 90](#statisticsSeries_percentiles_90)
      - [4.4.9.1. Job metric data > statisticsSeries > percentiles > 90 > 90 items](#autogenerated_heading_13)
    - [4.4.10. [Optional] Property Job metric data > statisticsSeries > percentiles > 25](#statisticsSeries_percentiles_25)
      - [4.4.10.1. Job metric data > statisticsSeries > percentiles > 25 > 25 items](#autogenerated_heading_14)
    - [4.4.11. [Optional] Property Job metric data > statisticsSeries > percentiles > 75](#statisticsSeries_percentiles_75)
      - [4.4.11.1. Job metric data > statisticsSeries > percentiles > 75 > 75 items](#autogenerated_heading_15)
- [5. [Required] Property Job metric data > series](#series)
  - [5.1. Job metric data > series > series items](#autogenerated_heading_16)
    - [5.1.1. [Required] Property Job metric data > series > series items > hostname](#series_items_hostname)
    - [5.1.2. [Optional] Property Job metric data > series > series items > id](#series_items_id)
    - [5.1.3. [Required] Property Job metric data > series > series items > statistics](#series_items_statistics)
      - [5.1.3.1. [Required] Property Job metric data > series > series items > statistics > avg](#series_items_statistics_avg)
      - [5.1.3.2. [Required] Property Job metric data > series > series items > statistics > min](#series_items_statistics_min)
      - [5.1.3.3. [Required] Property Job metric data > series > series items > statistics > max](#series_items_statistics_max)
    - [5.1.4. [Required] Property Job metric data > series > series items > data](#series_items_data)
      - [5.1.4.1. At least one of the items must be](#autogenerated_heading_17)

**Title:** Job metric data

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

**Description:** Metric data of a HPC job

<details>
<summary>
<strong> <a name="unit"></a>1. [Required] Property Job metric data > unit</strong>  

</summary>
<blockquote>

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | Yes                                                                       |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | unit.schema.json                                                          |

**Description:** Metric unit

<details>
<summary>
<strong> <a name="unit_base"></a>1.1. [Required] Property Job metric data > unit > base</strong>  

</summary>
<blockquote>

|              |                    |
| ------------ | ------------------ |
| **Type**     | `enum (of string)` |
| **Required** | Yes                |

**Description:** Metric base unit

Must be one of:
* "B"
* "F"
* "B/s"
* "F/s"
* "CPI"
* "IPC"
* "Hz"
* "W"
* "°C"
* ""

</blockquote>
</details>

<details>
<summary>
<strong> <a name="unit_prefix"></a>1.2. [Optional] Property Job metric data > unit > prefix</strong>  

</summary>
<blockquote>

|              |                    |
| ------------ | ------------------ |
| **Type**     | `enum (of string)` |
| **Required** | No                 |

**Description:** Unit prefix

Must be one of:
* "K"
* "M"
* "G"
* "T"
* "P"
* "E"

</blockquote>
</details>

</blockquote>
</details>

<details>
<summary>
<strong> <a name="timestep"></a>2. [Required] Property Job metric data > timestep</strong>  

</summary>
<blockquote>

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

**Description:** Measurement interval in seconds

</blockquote>
</details>

<details>
<summary>
<strong> <a name="thresholds"></a>3. [Optional] Property Job metric data > thresholds</strong>  

</summary>
<blockquote>

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

**Description:** Metric thresholds for specific system

<details>
<summary>
<strong> <a name="thresholds_peak"></a>3.1. [Optional] Property Job metric data > thresholds > peak</strong>  

</summary>
<blockquote>

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |

</blockquote>
</details>

<details>
<summary>
<strong> <a name="thresholds_normal"></a>3.2. [Optional] Property Job metric data > thresholds > normal</strong>  

</summary>
<blockquote>

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |

</blockquote>
</details>

<details>
<summary>
<strong> <a name="thresholds_caution"></a>3.3. [Optional] Property Job metric data > thresholds > caution</strong>  

</summary>
<blockquote>

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |

</blockquote>
</details>

<details>
<summary>
<strong> <a name="thresholds_alert"></a>3.4. [Optional] Property Job metric data > thresholds > alert</strong>  

</summary>
<blockquote>

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |

</blockquote>
</details>

</blockquote>
</details>

<details>
<summary>
<strong> <a name="statisticsSeries"></a>4. [Optional] Property Job metric data > statisticsSeries</strong>  

</summary>
<blockquote>

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

**Description:** Statistics series across topology

<details>
<summary>
<strong> <a name="statisticsSeries_min"></a>4.1. [Optional] Property Job metric data > statisticsSeries > min</strong>  

</summary>
<blockquote>

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

#### <a name="autogenerated_heading_2"></a>4.1.1. Job metric data > statisticsSeries > min > min items

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |

| Restrictions |        |
| ------------ | ------ |
| **Minimum**  | &ge; 0 |

</blockquote>
</details>

<details>
<summary>
<strong> <a name="statisticsSeries_max"></a>4.2. [Optional] Property Job metric data > statisticsSeries > max</strong>  

</summary>
<blockquote>

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

#### <a name="autogenerated_heading_3"></a>4.2.1. Job metric data > statisticsSeries > max > max items

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |

| Restrictions |        |
| ------------ | ------ |
| **Minimum**  | &ge; 0 |

</blockquote>
</details>

<details>
<summary>
<strong> <a name="statisticsSeries_mean"></a>4.3. [Optional] Property Job metric data > statisticsSeries > mean</strong>  

</summary>
<blockquote>

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

#### <a name="autogenerated_heading_4"></a>4.3.1. Job metric data > statisticsSeries > mean > mean items

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |

| Restrictions |        |
| ------------ | ------ |
| **Minimum**  | &ge; 0 |

</blockquote>
</details>

<details>
<summary>
<strong> <a name="statisticsSeries_percentiles"></a>4.4. [Optional] Property Job metric data > statisticsSeries > percentiles</strong>  

</summary>
<blockquote>

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

<details>
<summary>
<strong> <a name="statisticsSeries_percentiles_10"></a>4.4.1. [Optional] Property Job metric data > statisticsSeries > percentiles > 10</strong>  

</summary>
<blockquote>

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

##### <a name="autogenerated_heading_5"></a>4.4.1.1. Job metric data > statisticsSeries > percentiles > 10 > 10 items

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |

| Restrictions |        |
| ------------ | ------ |
| **Minimum**  | &ge; 0 |

</blockquote>
</details>

<details>
<summary>
<strong> <a name="statisticsSeries_percentiles_20"></a>4.4.2. [Optional] Property Job metric data > statisticsSeries > percentiles > 20</strong>  

</summary>
<blockquote>

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

##### <a name="autogenerated_heading_6"></a>4.4.2.1. Job metric data > statisticsSeries > percentiles > 20 > 20 items

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |

| Restrictions |        |
| ------------ | ------ |
| **Minimum**  | &ge; 0 |

</blockquote>
</details>

<details>
<summary>
<strong> <a name="statisticsSeries_percentiles_30"></a>4.4.3. [Optional] Property Job metric data > statisticsSeries > percentiles > 30</strong>  

</summary>
<blockquote>

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

##### <a name="autogenerated_heading_7"></a>4.4.3.1. Job metric data > statisticsSeries > percentiles > 30 > 30 items

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |

| Restrictions |        |
| ------------ | ------ |
| **Minimum**  | &ge; 0 |

</blockquote>
</details>

<details>
<summary>
<strong> <a name="statisticsSeries_percentiles_40"></a>4.4.4. [Optional] Property Job metric data > statisticsSeries > percentiles > 40</strong>  

</summary>
<blockquote>

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

##### <a name="autogenerated_heading_8"></a>4.4.4.1. Job metric data > statisticsSeries > percentiles > 40 > 40 items

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |

| Restrictions |        |
| ------------ | ------ |
| **Minimum**  | &ge; 0 |

</blockquote>
</details>

<details>
<summary>
<strong> <a name="statisticsSeries_percentiles_50"></a>4.4.5. [Optional] Property Job metric data > statisticsSeries > percentiles > 50</strong>  

</summary>
<blockquote>

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

##### <a name="autogenerated_heading_9"></a>4.4.5.1. Job metric data > statisticsSeries > percentiles > 50 > 50 items

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |

| Restrictions |        |
| ------------ | ------ |
| **Minimum**  | &ge; 0 |

</blockquote>
</details>

<details>
<summary>
<strong> <a name="statisticsSeries_percentiles_60"></a>4.4.6. [Optional] Property Job metric data > statisticsSeries > percentiles > 60</strong>  

</summary>
<blockquote>

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

##### <a name="autogenerated_heading_10"></a>4.4.6.1. Job metric data > statisticsSeries > percentiles > 60 > 60 items

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |

| Restrictions |        |
| ------------ | ------ |
| **Minimum**  | &ge; 0 |

</blockquote>
</details>

<details>
<summary>
<strong> <a name="statisticsSeries_percentiles_70"></a>4.4.7. [Optional] Property Job metric data > statisticsSeries > percentiles > 70</strong>  

</summary>
<blockquote>

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

##### <a name="autogenerated_heading_11"></a>4.4.7.1. Job metric data > statisticsSeries > percentiles > 70 > 70 items

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |

| Restrictions |        |
| ------------ | ------ |
| **Minimum**  | &ge; 0 |

</blockquote>
</details>

<details>
<summary>
<strong> <a name="statisticsSeries_percentiles_80"></a>4.4.8. [Optional] Property Job metric data > statisticsSeries > percentiles > 80</strong>  

</summary>
<blockquote>

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

##### <a name="autogenerated_heading_12"></a>4.4.8.1. Job metric data > statisticsSeries > percentiles > 80 > 80 items

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |

| Restrictions |        |
| ------------ | ------ |
| **Minimum**  | &ge; 0 |

</blockquote>
</details>

<details>
<summary>
<strong> <a name="statisticsSeries_percentiles_90"></a>4.4.9. [Optional] Property Job metric data > statisticsSeries > percentiles > 90</strong>  

</summary>
<blockquote>

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

##### <a name="autogenerated_heading_13"></a>4.4.9.1. Job metric data > statisticsSeries > percentiles > 90 > 90 items

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |

| Restrictions |        |
| ------------ | ------ |
| **Minimum**  | &ge; 0 |

</blockquote>
</details>

<details>
<summary>
<strong> <a name="statisticsSeries_percentiles_25"></a>4.4.10. [Optional] Property Job metric data > statisticsSeries > percentiles > 25</strong>  

</summary>
<blockquote>

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

##### <a name="autogenerated_heading_14"></a>4.4.10.1. Job metric data > statisticsSeries > percentiles > 25 > 25 items

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |

| Restrictions |        |
| ------------ | ------ |
| **Minimum**  | &ge; 0 |

</blockquote>
</details>

<details>
<summary>
<strong> <a name="statisticsSeries_percentiles_75"></a>4.4.11. [Optional] Property Job metric data > statisticsSeries > percentiles > 75</strong>  

</summary>
<blockquote>

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

##### <a name="autogenerated_heading_15"></a>4.4.11.1. Job metric data > statisticsSeries > percentiles > 75 > 75 items

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |

| Restrictions |        |
| ------------ | ------ |
| **Minimum**  | &ge; 0 |

</blockquote>
</details>

</blockquote>
</details>

</blockquote>
</details>

<details>
<summary>
<strong> <a name="series"></a>5. [Required] Property Job metric data > series</strong>  

</summary>
<blockquote>

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

### <a name="autogenerated_heading_16"></a>5.1. Job metric data > series > series items

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

<details>
<summary>
<strong> <a name="series_items_hostname"></a>5.1.1. [Required] Property Job metric data > series > series items > hostname</strong>  

</summary>
<blockquote>

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

</blockquote>
</details>

<details>
<summary>
<strong> <a name="series_items_id"></a>5.1.2. [Optional] Property Job metric data > series > series items > id</strong>  

</summary>
<blockquote>

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

</blockquote>
</details>

<details>
<summary>
<strong> <a name="series_items_statistics"></a>5.1.3. [Required] Property Job metric data > series > series items > statistics</strong>  

</summary>
<blockquote>

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | Yes                                                                       |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

**Description:** Statistics across time dimension

<details>
<summary>
<strong> <a name="series_items_statistics_avg"></a>5.1.3.1. [Required] Property Job metric data > series > series items > statistics > avg</strong>  

</summary>
<blockquote>

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | Yes      |

**Description:** Series average

| Restrictions |        |
| ------------ | ------ |
| **Minimum**  | &ge; 0 |

</blockquote>
</details>

<details>
<summary>
<strong> <a name="series_items_statistics_min"></a>5.1.3.2. [Required] Property Job metric data > series > series items > statistics > min</strong>  

</summary>
<blockquote>

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | Yes      |

**Description:** Series minimum

| Restrictions |        |
| ------------ | ------ |
| **Minimum**  | &ge; 0 |

</blockquote>
</details>

<details>
<summary>
<strong> <a name="series_items_statistics_max"></a>5.1.3.3. [Required] Property Job metric data > series > series items > statistics > max</strong>  

</summary>
<blockquote>

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | Yes      |

**Description:** Series maximum

| Restrictions |        |
| ------------ | ------ |
| **Minimum**  | &ge; 0 |

</blockquote>
</details>

</blockquote>
</details>

<details>
<summary>
<strong> <a name="series_items_data"></a>5.1.4. [Required] Property Job metric data > series > series items > data</strong>  

</summary>
<blockquote>

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

##### <a name="autogenerated_heading_17"></a>5.1.4.1. At least one of the items must be

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |

| Restrictions |        |
| ------------ | ------ |
| **Minimum**  | &ge; 0 |

</blockquote>
</details>

</blockquote>
</details>

----------------------------------------------------------------------------------------------------------------------------
Generated using [json-schema-for-humans](https://github.com/coveooss/json-schema-for-humans) on 2024-02-02 at 14:36:54 +0100