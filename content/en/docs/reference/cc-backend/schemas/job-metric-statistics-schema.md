---
title: Job Statistics Schema
description: ClusterCockpit Job Statistics Schema Reference
categories: [cc-backend]
tags: [Backend]
weight: 4
---

The following schema in its raw form can be found in the [ClusterCockpit GitHub](https://github.com/ClusterCockpit/cc-backend/tree/master/pkg/schema/schemas) repository.

{{< alert title="Manual Updates">}}
  Changes to the original JSON schema found in the repository are not automatically rendered in this reference documentation.</br></br>
  **Last Update:** 04.12.2024
{{< /alert >}}

## Job statistics

- [1. Property `Job statistics > unit`](#unit)
- [2. Property `Job statistics > avg`](#avg)
- [3. Property `Job statistics > min`](#min)
- [4. Property `Job statistics > max`](#max)

**Title:** Job statistics

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** Format specification for job metric statistics

| Property         | Pattern | Type   | Deprecated | Definition                    | Title/Description  |
| ---------------- | ------- | ------ | ---------- | ----------------------------- | ------------------ |
| + [unit](#unit ) | No      | object | No         | In embedfs://unit.schema.json | Metric unit        |
| + [avg](#avg )   | No      | number | No         | -                             | Job metric average |
| + [min](#min )   | No      | number | No         | -                             | Job metric minimum |
| + [max](#max )   | No      | number | No         | -                             | Job metric maximum |

## <a name="unit"></a>1. Property `Job statistics > unit`

|                           |                            |
| ------------------------- | -------------------------- |
| **Type**                  | `object`                   |
| **Required**              | Yes                        |
| **Additional properties** | Any type allowed           |
| **Defined in**            | embedfs://unit.schema.json |

**Description:** Metric unit

## <a name="avg"></a>2. Property `Job statistics > avg`

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | Yes      |

**Description:** Job metric average

| Restrictions |        |
| ------------ | ------ |
| **Minimum**  | &ge; 0 |

## <a name="min"></a>3. Property `Job statistics > min`

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | Yes      |

**Description:** Job metric minimum

| Restrictions |        |
| ------------ | ------ |
| **Minimum**  | &ge; 0 |

## <a name="max"></a>4. Property `Job statistics > max`

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | Yes      |

**Description:** Job metric maximum

| Restrictions |        |
| ------------ | ------ |
| **Minimum**  | &ge; 0 |

----------------------------------------------------------------------------------------------------------------------------
Generated using [json-schema-for-humans](https://github.com/coveooss/json-schema-for-humans) on 2024-12-04 at 16:45:59 +0100
