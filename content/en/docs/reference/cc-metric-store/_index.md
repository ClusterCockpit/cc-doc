---
title: cc-metric-store
description: ClusterCockpit Metric Store References
categories: [cc-metric-store]
tags: [Backend]
weight: 2
---

{{% pageinfo %}}
Reference information regarding the ClusterCockpit component "cc-metric-store" ([GitHub Repo](https://github.com/ClusterCockpit/cc-metric-store "See GitHub")).
{{% /pageinfo %}}

## Query Requests

The metric store provides a flexible API for querying time-series metric data with support for hierarchical selectors, aggregation, and scope transformation.

### APIQueryRequest

The main request structure for batch metric queries.

```go
type APIQueryRequest struct {
    Cluster     string     `json:"cluster"`
    Queries     []APIQuery `json:"queries"`
    ForAllNodes []string   `json:"for-all-nodes"`
    From        int64      `json:"from"`
    To          int64      `json:"to"`
    WithStats   bool       `json:"with-stats"`
    WithData    bool       `json:"with-data"`
    WithPadding bool       `json:"with-padding"`
}
```

**Fields:**

- `Cluster` (string): The cluster name to query
- `Queries` ([]APIQuery): List of individual metric queries (see below)
- `ForAllNodes` ([]string): Alternative to explicit queries - automatically generates queries for all specified metrics across all nodes in the cluster
- `From` (int64): Start timestamp (Unix epoch seconds)
- `To` (int64): End timestamp (Unix epoch seconds)
- `WithStats` (bool): Include computed statistics (avg, min, max) in response
- `WithData` (bool): Include raw time-series data in response
- `WithPadding` (bool): Pad data arrays with NaN values to align with requested time range

**Query Modes:**

1. **Explicit Queries**: Specify individual queries via the `Queries` field for fine-grained control
2. **Batch Mode**: Use `ForAllNodes` to automatically query all specified metrics for all nodes in the cluster

**Validation:**

- `From` must be less than `To` (returns `ErrInvalidTimeRange` otherwise)
- `Cluster` is required when using `ForAllNodes` (returns `ErrEmptyCluster` otherwise)

### APIQuery

Represents a single metric query with optional hierarchical selectors.

```go
type APIQuery struct {
    Type        *string      `json:"type,omitempty"`
    SubType     *string      `json:"subtype,omitempty"`
    Metric      string       `json:"metric"`
    Hostname    string       `json:"host"`
    Resolution  int64        `json:"resolution"`
    TypeIds     []string     `json:"type-ids,omitempty"`
    SubTypeIds  []string     `json:"subtype-ids,omitempty"`
    ScaleFactor schema.Float `json:"scale-by,omitempty"`
    Aggregate   bool         `json:"aggreg"`
}
```

**Fields:**

- `Metric` (string, required): The metric name to query (e.g., "cpu_load", "mem_used")
- `Hostname` (string, required): The node hostname to query
- `Type` (*string, optional): First level of hierarchy (e.g., "hwthread", "core", "socket", "accelerator", "memorydomain")
- `TypeIds` ([]string, optional): IDs for the Type level (e.g., ["0", "1", "2"] for cores 0-2)
- `SubType` (*string, optional): Second level of hierarchy (for nested selectors)
- `SubTypeIds` ([]string, optional): IDs for the SubType level
- `Resolution` (int64): Data resolution in seconds (0 = native resolution)
- `ScaleFactor` (float, optional): Multiply all data points by this factor (for unit conversion)
- `Aggregate` (bool): If true, aggregate data from multiple TypeIds/SubTypeIds; if false, return separate results for each

**Hierarchical Selection:**

The query system supports hierarchical data selection:

```
Cluster → Hostname → Type+TypeIds → SubType+SubTypeIds
```

**Examples:**

```json
// Query node-level CPU load
{
  "metric": "cpu_load",
  "host": "node001",
  "resolution": 60
}

// Query per-core CPU load (non-aggregated)
{
  "metric": "cpu_load",
  "host": "node001",
  "type": "core",
  "type-ids": ["0", "1", "2", "3"],
  "aggreg": false,
  "resolution": 60
}

// Query aggregated socket memory bandwidth
{
  "metric": "mem_bw",
  "host": "node001",
  "type": "socket",
  "type-ids": ["0", "1"],
  "aggreg": true,
  "resolution": 60
}

// Query GPU metrics
{
  "metric": "gpu_power",
  "host": "node001",
  "type": "accelerator",
  "type-ids": ["0", "1", "2", "3"],
  "aggreg": false,
  "resolution": 60
}
```

### APIQueryResponse

The response structure containing query results.

```go
type APIQueryResponse struct {
    Queries []APIQuery        `json:"queries,omitempty"`
    Results [][]APIMetricData `json:"results"`
}
```

**Fields:**

- `Queries` ([]APIQuery, optional): Echo of the queries executed (populated when using `ForAllNodes`)
- `Results` ([][]APIMetricData): 2D array of results where:
  - Outer array: One element per query
  - Inner array: One element per selector (e.g., multiple cores/sockets when `Aggregate=false`)

### APIMetricData

Represents the response data for a single metric query.

```go
type APIMetricData struct {
    Error      *string           `json:"error,omitempty"`
    Data       schema.FloatArray `json:"data,omitempty"`
    From       int64             `json:"from"`
    To         int64             `json:"to"`
    Resolution int64             `json:"resolution"`
    Avg        schema.Float      `json:"avg"`
    Min        schema.Float      `json:"min"`
    Max        schema.Float      `json:"max"`
}
```

**Fields:**

- `Data` ([]float): Time-series data points (omitted if `WithData=false`)
- `From` (int64): Actual start timestamp of returned data
- `To` (int64): Actual end timestamp of returned data
- `Resolution` (int64): Actual resolution of returned data in seconds
- `Avg` (float): Average value (only if `WithStats=true`)
- `Min` (float): Minimum value (only if `WithStats=true`)
- `Max` (float): Maximum value (only if `WithStats=true`)
- `Error` (*string, optional): Error message if query failed

**Notes:**

- NaN values in data are ignored during statistics computation
- If all values are NaN, statistics will be NaN
- Missing hosts or metrics result in empty results (not errors) for graceful frontend handling

## Metric Scopes

Metrics are collected at different granularities (native scope):

- **HWThread**: Per hardware thread
- **Core**: Per CPU core
- **Socket**: Per CPU socket
- **MemoryDomain**: Per memory domain (NUMA)
- **Accelerator**: Per GPU/accelerator
- **Node**: Per compute node

### Scope Transformation

The query system automatically transforms between native metric scope and requested scope:

- **Aggregation** (native scope ≥ requested scope): Finer-grained data is aggregated to coarser granularity
  - Example: HWThread → Core → Socket → Node
- **Rejection** (native scope < requested scope): Cannot increase granularity - returns error
- **Special Cases**: Accelerator metrics are independent of CPU hierarchy

**Transformation Rules:**

| Native Scope | Requested Scope | Result |
|--------------|-----------------|--------|
| HWThread | HWThread | Direct query |
| HWThread | Core | Aggregate HWThreads per core |
| HWThread | Socket | Aggregate HWThreads per socket |
| HWThread | Node | Aggregate all HWThreads |
| Core | Core | Direct query |
| Core | Socket | Aggregate cores per socket |
| Core | Node | Aggregate all cores |
| Socket | Socket | Direct query |
| Socket | Node | Aggregate all sockets |
| Node | Node | Direct query |
| Accelerator | Accelerator | Direct query |
| Accelerator | Node | Aggregate all accelerators |

## Error Handling

The API uses a hybrid error model:

1. **Request-level errors**: Returned as HTTP errors
   - `ErrInvalidTimeRange`: `From` ≥ `To`
   - `ErrEmptyCluster`: Missing cluster name with `ForAllNodes`
   - Uninitialized metric store

2. **Query-level errors**: Stored in `APIMetricData.Error` field
   - Individual query failures don't fail the entire request
   - Missing hosts/metrics are logged as warnings but return empty results

3. **Partial errors**: When some queries succeed and others fail
   - Successful data is returned
   - Error messages are collected and returned as a combined error

## Complete Example

```json
{
  "cluster": "fritz",
  "from": 1609459200,
  "to": 1609462800,
  "with-stats": true,
  "with-data": true,
  "queries": [
    {
      "metric": "cpu_load",
      "host": "node001",
      "resolution": 60
    },
    {
      "metric": "mem_used",
      "host": "node001",
      "type": "socket",
      "type-ids": ["0", "1"],
      "aggreg": false,
      "resolution": 60
    }
  ]
}
```

**Response:**

```json
{
  "results": [
    [
      {
        "data": [0.5, 0.6, 0.7, ...],
        "from": 1609459200,
        "to": 1609462800,
        "resolution": 60,
        "avg": 0.6,
        "min": 0.5,
        "max": 0.7
      }
    ],
    [
      {
        "data": [1024.0, 1536.0, 2048.0, ...],
        "from": 1609459200,
        "to": 1609462800,
        "resolution": 60,
        "avg": 1536.0,
        "min": 1024.0,
        "max": 2048.0
      },
      {
        "data": [2048.0, 2560.0, 3072.0, ...],
        "from": 1609459200,
        "to": 1609462800,
        "resolution": 60,
        "avg": 2560.0,
        "min": 2048.0,
        "max": 3072.0
      }
    ]
  ]
}
```
