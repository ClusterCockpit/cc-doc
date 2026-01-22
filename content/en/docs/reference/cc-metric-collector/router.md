---
title: Metric Router
description: Routing and processing metrics in cc-metric-collector
categories: [cc-metric-collector]
tags: [Collector, Router]
weight: 5
---

## Overview

The metric router sits between collectors/receivers and sinks, enabling metric processing such as:

- Adding and removing tags
- Filtering and dropping metrics
- Renaming metrics
- Aggregating metrics across an interval
- Normalizing units
- Setting common timestamps

## Basic Configuration

**File**: `router.json`

**Minimal configuration**:
```json
{
  "interval_timestamp": false,
  "num_cache_intervals": 0
}
```

**Typical configuration**:
```json
{
  "add_tags": [
    {
      "key": "cluster",
      "value": "mycluster",
      "if": "*"
    }
  ],
  "interval_timestamp": true,
  "num_cache_intervals": 0
}
```

## Configuration Options

### Core Settings

| Option                | Type    | Default      | Description                                                                              |
| --------------------- | ------- | ------------ | ---------------------------------------------------------------------------------------- |
| `interval_timestamp`  | bool    | `false`      | Use common timestamp (interval start) for all metrics in an interval                     |
| `num_cache_intervals` | int     | `0`          | Number of past intervals to cache (0 disables cache, required for interval aggregates)   |
| `hostname_tag`        | string  | `"hostname"` | Tag name for hostname (added to locally created metrics)                                 |
| `max_forward`         | int     | `50`         | Max metrics to read from a channel at once (must be > 1)                                 |

### The `interval_timestamp` Option

Collectors' `Read()` functions are not called simultaneously, so metrics within an interval can have different timestamps. 

**When `true`**: All metrics in an interval get a common timestamp (the interval start time)
**When `false`**: Each metric keeps its original collection timestamp

**Use case**: Enable this to simplify time-series alignment in your database.

### The `num_cache_intervals` Option

Controls metric caching for interval aggregations.

| Value | Behavior                                                       |
| ----- | -------------------------------------------------------------- |
| `0`   | Cache disabled (no aggregations possible)                      |
| `1`   | Cache last interval only (minimal memory, basic aggregations)  |
| `2+`  | Cache multiple intervals (for complex time-based aggregations) |

**Note**: Required to be > 0 for `interval_aggregates` to work.

### The `hostname_tag` Option

By default, the router tags locally created metrics with the hostname.

**Default tag name**: `hostname`

**Custom tag name**:
```json
{
  "hostname_tag": "node"
}
```

### The `max_forward` Option

Performance tuning for metric processing.

**How it works**: When the router receives a metric, it tries to read up to `max_forward` additional metrics from the same channel before processing.

**Default**: `50`

**Must be**: Greater than `1`

## Metric Processing

### Modern Configuration (Recommended)

Use the `process_messages` section with the [message processor](https://github.com/ClusterCockpit/cc-lib/blob/main/messageProcessor/README.md):

```json
{
  "process_messages": {
    "manipulate_messages": [
      {
        "add_base_tags": {
          "cluster": "mycluster",
          "partition": "compute"
        }
      },
      {
        "drop_by_name": ["cpu_idle", "mem_cached"]
      },
      {
        "rename_by": {
          "clock_mhz": "clock"
        }
      }
    ]
  }
}
```

### Legacy Configuration (Deprecated)

The following options are **deprecated** but still supported for backward compatibility. They are automatically converted to `process_messages` format.

#### Adding Tags

**Deprecated syntax**:
```json
{
  "add_tags": [
    {
      "key": "cluster",
      "value": "mycluster",
      "if": "*"
    },
    {
      "key": "type",
      "value": "socket",
      "if": "name == 'temp_package_id_0'"
    }
  ]
}
```

**Modern equivalent**:
```json
{
  "process_messages": {
    "manipulate_messages": [
      {
        "add_base_tags": {
          "cluster": "mycluster"
        }
      },
      {
        "add_tags_by": {
          "type": "socket"
        },
        "if": "name == 'temp_package_id_0'"
      }
    ]
  }
}
```

#### Deleting Tags

**Deprecated syntax**:
```json
{
  "delete_tags": [
    {
      "key": "unit",
      "if": "*"
    }
  ]
}
```

**Never delete these tags**: `hostname`, `type`, `type-id`

#### Dropping Metrics

**By name (deprecated)**:
```json
{
  "drop_metrics": [
    "not_interesting_metric",
    "debug_metric"
  ]
}
```

**By condition (deprecated)**:
```json
{
  "drop_metrics_if": [
    "match('temp_core_%d+', name)",
    "match('cpu', type) && type-id == 0"
  ]
}
```

**Modern equivalent**:
```json
{
  "process_messages": {
    "manipulate_messages": [
      {
        "drop_by_name": ["not_interesting_metric", "debug_metric"]
      },
      {
        "drop_by": "match('temp_core_%d+', name)"
      }
    ]
  }
}
```

#### Renaming Metrics

**Deprecated syntax**:
```json
{
  "rename_metrics": {
    "old_name": "new_name",
    "clock_mhz": "clock"
  }
}
```

**Modern equivalent**:
```json
{
  "process_messages": {
    "manipulate_messages": [
      {
        "rename_by": {
          "old_name": "new_name",
          "clock_mhz": "clock"
        }
      }
    ]
  }
}
```

**Use case**: Standardize metric names across different systems or collectors.

#### Normalizing Units

**Deprecated syntax**:
```json
{
  "normalize_units": true
}
```

**Effect**: Normalizes unit names (e.g., `byte`, `Byte`, `B`, `bytes` → consistent format)

#### Changing Unit Prefixes

**Deprecated syntax**:
```json
{
  "change_unit_prefix": {
    "mem_used": "G",
    "mem_total": "G"
  }
}
```

**Use case**: Convert memory metrics from kB (as reported by `/proc/meminfo`) to GB for better readability.

## Interval Aggregates (Experimental)

**Requires**: `num_cache_intervals` > 0

Derive new metrics by aggregating metrics from the current interval.

### Configuration

```json
{
  "num_cache_intervals": 1,
  "interval_aggregates": [
    {
      "name": "temp_cores_avg",
      "if": "match('temp_core_%d+', metric.Name())",
      "function": "avg(values)",
      "tags": {
        "type": "node"
      },
      "meta": {
        "group": "IPMI",
        "unit": "degC",
        "source": "TempCollector"
      }
    }
  ]
}
```

### Parameters

| Field      | Type   | Description                                                                   |
| ---------- | ------ | ----------------------------------------------------------------------------- |
| `name`     | string | Name of the new derived metric                                               |
| `if`       | string | Condition to select which metrics to aggregate                               |
| `function` | string | Aggregation function (e.g., `avg(values)`, `sum(values)`, `max(values)`)     |
| `tags`     | object | Tags to add to the derived metric                                            |
| `meta`     | object | Metadata for the derived metric (use `"<copy>"` to copy from source metrics) |

### Available Functions

| Function          | Description                           |
| ----------------- | ------------------------------------- |
| `avg(values)`     | Average of all matching metrics       |
| `sum(values)`     | Sum of all matching metrics           |
| `min(values)`     | Minimum value                         |
| `max(values)`     | Maximum value                         |
| `count(values)`   | Number of matching metrics            |

### Complex Example

Calculate `mem_used` from multiple memory metrics:

```json
{
  "interval_aggregates": [
    {
      "name": "mem_used",
      "if": "source == 'MemstatCollector'",
      "function": "sum(mem_total) - (sum(mem_free) + sum(mem_buffers) + sum(mem_cached))",
      "tags": {
        "type": "node"
      },
      "meta": {
        "group": "<copy>",
        "unit": "<copy>",
        "source": "<copy>"
      }
    }
  ]
}
```

### Dropping Source Metrics

If you only want the aggregated metric, drop the source metrics:

```json
{
  "drop_metrics_if": [
    "match('temp_core_%d+', metric.Name())"
  ],
  "interval_aggregates": [
    {
      "name": "temp_cores_avg",
      "if": "match('temp_core_%d+', metric.Name())",
      "function": "avg(values)",
      "tags": {
        "type": "node"
      },
      "meta": {
        "group": "IPMI",
        "unit": "degC"
      }
    }
  ]
}
```

## Processing Order

The router processes metrics in a specific order:

1. Add `hostname_tag` (if sent by collectors or cache)
2. Change timestamp to interval timestamp (if `interval_timestamp == true`)
3. Check if metric should be dropped (`drop_metrics`, `drop_metrics_if`)
4. Add tags (`add_tags`)
5. Delete tags (`del_tags`)
6. Rename metric (`rename_metrics`) and store old name in meta as `oldname`
7. Add tags again (to support conditions using new name)
8. Delete tags again (to support conditions using new name)
9. Normalize units (if `normalize_units == true`)
10. Convert unit prefix (`change_unit_prefix`)
11. Send to sinks
12. Move to cache (if `num_cache_intervals > 0`)

**Legend**:
- Operations apply to metrics from collectors (c)
- Operations apply to metrics from receivers (r)
- Operations apply to both (c,r)

## Complete Example

```json
{
  "interval_timestamp": true,
  "num_cache_intervals": 1,
  "hostname_tag": "hostname",
  "max_forward": 50,
  "process_messages": {
    "manipulate_messages": [
      {
        "add_base_tags": {
          "cluster": "production",
          "datacenter": "dc1"
        }
      },
      {
        "drop_by_name": ["cpu_idle", "cpu_guest", "cpu_guest_nice"]
      },
      {
        "rename_by": {
          "clock_mhz": "clock"
        }
      },
      {
        "add_tags_by": {
          "high_temp": "true"
        },
        "if": "name == 'temp_package_id_0' && value > 70"
      }
    ]
  },
  "interval_aggregates": [
    {
      "name": "temp_avg",
      "if": "match('temp_core_%d+', name)",
      "function": "avg(values)",
      "tags": {
        "type": "node"
      },
      "meta": {
        "group": "Temperature",
        "unit": "degC",
        "source": "TempCollector"
      }
    }
  ]
}
```

## Performance Considerations

- **Caching**: Only enable if you need interval aggregates (memory overhead)
- **Complex conditions**: Evaluated for every metric (CPU overhead)
- **Aggregations**: Evaluated at the start of each interval (CPU overhead)
- **max_forward**: Higher values can improve throughput but increase latency

## See Also

- [Message Processor Documentation](https://github.com/ClusterCockpit/cc-lib/blob/main/messageProcessor/README.md)
- [Collectors](../collectors/)
- [Configuration](../configuration/)
