---
title: Unit Schema
description: ClusterCockpit Unit Schema Reference
categories: [cc-backend]
tags: [Backend]
weight: 5
---

The following schema in its raw form can be found in the [ClusterCockpit GitHub](https://github.com/ClusterCockpit/cc-backend/tree/master/pkg/schema/schemas) repository.

{{< alert title="Manual Updates">}}
  Changes to the original JSON schema found in the repository are not automatically rendered in this reference documentation.</br></br>
  **Last Update:** 04.12.2024
{{< /alert >}}

## Metric unit

- [1. Property `Metric unit > base`](#base)
- [2. Property `Metric unit > prefix`](#prefix)

**Title:** Metric unit

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** Format specification for job metric units

| Property             | Pattern | Type             | Deprecated | Definition | Title/Description |
| -------------------- | ------- | ---------------- | ---------- | ---------- | ----------------- |
| + [base](#base )     | No      | enum (of string) | No         | -          | Metric base unit  |
| - [prefix](#prefix ) | No      | enum (of string) | No         | -          | Unit prefix       |

## <a name="base"></a>1. Property `Metric unit > base`

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

## <a name="prefix"></a>2. Property `Metric unit > prefix`

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

----------------------------------------------------------------------------------------------------------------------------
Generated using [json-schema-for-humans](https://github.com/coveooss/json-schema-for-humans) on 2024-12-04 at 16:45:59 +0100
