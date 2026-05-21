---
title: Configuration
description: ClusterCockpit Energy Manager Configuration Option References
categories: [cc-energy-manager]
tags: [Backend]
weight: 2
---

Configuration is provided as a JSON file. The default path is `./config.json` in the working directory; an alternative path can be specified with the `-config` flag.

The configuration has four required top-level sections: `receivers`, `sinks`, `controller`, and `clusters`.

## Receivers Section

A named map of receiver configurations. Each receiver defines a source from which `cc-energy-manager` ingests metric messages.

```json
"receivers": {
    "<name>": {
        "type": "nats",
        "address": "nats-server.example.org",
        "port": "4222",
        "subject": "metrics.subject"
    }
}
```

**Fields (NATS receiver):**

- `type` (string, required): Receiver type. Currently `"nats"`.
- `address` (string, required): Hostname or IP of the NATS server.
- `port` (string, required): Port of the NATS server.
- `subject` (string, required): NATS subject to subscribe to.

## Sinks Section

A named map of sink configurations. Each sink defines a destination for processed metric messages.

```json
"sinks": {
    "<name>": {
        "type": "stdout",
        "meta_as_tags": []
    }
}
```

**Fields (stdout sink):**

- `type` (string, required): Sink type. Examples: `"stdout"`, `"influxasync"`.
- `meta_as_tags` (array of strings, optional): Metadata fields to promote to tags.

## Controller Section

Configuration for the connection to `cc-node-controller`, which applies power limit changes on compute nodes.

```json
"controller": {
    "nats": {
        "url": "nats://nats-server.example.org:4222",
        "requestSubject": "cc-node-controller.%c.request"
    },
    "toposMaxAge": 86400
}
```

**Fields:**

- `nats` (object, required): NATS connection settings for `cc-node-controller`.
  - `url` (string, required): NATS server URL, e.g. `"nats://localhost:4222"`.
  - `requestSubject` (string, required): NATS subject for sending control commands. Use `%c` as a placeholder for the cluster name — it is substituted at runtime for each cluster (e.g. `"cc-node-controller.%c.request"` becomes `"cc-node-controller.fritz.request"` for cluster `fritz`).
- `toposMaxAge` (integer, optional): How long to cache node hardware topology data in seconds. Default: `86400` (1 day).

## Clusters Section

An array of cluster configurations. Each cluster defines which nodes to manage and how to optimize their power limits.

```json
"clusters": [
    {
        "name": "fritz",
        "powerBudgetTotal": 10000,
        "partitionRegex": "^energy_efficient$",
        "subclusters": [ ... ]
    }
]
```

**Cluster fields:**

- `name` (string, required): Cluster identifier. Must match the cluster name used in metric tags.
- `powerBudgetTotal` (number, required): Total power budget for this cluster in watts. Used for proportional budget distribution across device types.
- `partitionRegex` (string, required): Regular expression matched against the job's partition/queue name. Only jobs on matching partitions are managed.
- `subclusters` (array, required): List of subcluster configurations (see below).

### Subcluster Configuration

A subcluster groups nodes within a cluster that share the same hardware configuration.

```json
{
    "name": "main",
    "hostRegex": "^f\\d\\d\\d\\d$",
    "devicetypes": { ... }
}
```

**Fields:**

- `name` (string, required): Subcluster identifier.
- `hostRegex` (string, required): Regular expression matched against node hostnames to assign nodes to this subcluster.
- `devicetypes` (object, required): Map of device type name to device type configuration (see below). Supported keys: `"socket"`, `"nvidia_gpu"`, `"amd_gpu"`.

### Device Type Configuration

Each entry in `devicetypes` configures how `cc-energy-manager` optimizes a specific hardware device type.

```json
"socket": {
    "scope": "node",
    "aggregator": {
        "type": "last",
        "powerMetric": "cpu_energy",
        "performanceMetric": "ips",
        "deviceType": "socket"
    },
    "controlName": "rapl.pkg_power_limit1",
    "controlDefaultValue": 300,
    "intervalConverged": "10m",
    "intervalSearch": "2m",
    "powerBudgetWeight": 1,
    "optimizer": {
        "type": "gssng",
        "tolerance": 5,
        "borders": {
            "lower": 123,
            "upper": 800
        }
    }
}
```

**Fields:**

- `scope` (string, required): Optimization granularity. One of:
  - `"job"` — single optimizer shared across all devices of the job
  - `"node"` — one optimizer per node, applied to all devices on that node
  - `"device"` — independent optimizer per device on each node
- `aggregator` (object, required): Metric aggregation configuration.
  - `type` (string, required): Aggregation strategy: `"last"` (most recent value) or `"median"` (median over time window).
  - `powerMetric` (string, required): Name of the power metric to track (e.g. `"cpu_energy"`, `"acc_power"`).
  - `performanceMetric` (string, required): Name of the performance proxy metric (e.g. `"ips"` for instructions per second, `"kernels"` for CUDA kernel count).
  - `deviceType` (string, required): Device type from which to read metrics.
- `controlName` (string, required): RAPL or NVML control name used to set the power limit. Examples:
  - `"rapl.pkg_power_limit1"` — RAPL package power limit for CPU sockets
  - `"nvml.power_limit"` — NVML power limit for NVIDIA GPUs
- `controlDefaultValue` (number, required): Power limit in watts applied when no optimization is active (e.g. when a job ends).
- `intervalConverged` (string, required): How often to run optimization after convergence. Parsed as a Go duration string (e.g. `"10m"`, `"5m"`).
- `intervalSearch` (string, required): How often to run optimization during active search. Should be shorter than `intervalConverged` (e.g. `"2m"`).
- `powerBudgetWeight` (number, required): Relative weight for budget allocation when multiple device types share `powerBudgetTotal`. A device type with weight 2 receives twice the budget fraction of a device type with weight 1.
- `optimizer` (object, required): Optimizer algorithm configuration.
  - `type` (string, required): Algorithm type. `"gssng"` (Golden Section Search with Narrowing/Broadening, recommended) or `"gss"` (plain Golden Section Search).
  - `tolerance` (number, required): Convergence tolerance in watts. The optimizer considers itself converged when the search interval is smaller than this value.
  - `borders` (object, required): Power limit bounds.
    - `lower` (number, required): Minimum allowed power limit in watts.
    - `upper` (number, required): Maximum allowed power limit in watts.

## Complete Example

The following example configures two clusters: `fritz` (CPU-only nodes with socket-level optimization) and `alex` (GPU nodes with both GPU and CPU optimization).

```json
{
    "receivers": {
        "testnats": {
            "type": "nats",
            "address": "nats-server.example.org",
            "port": "4222",
            "subject": "subject"
        }
    },
    "sinks": {
        "testoutput": {
            "type": "stdout",
            "meta_as_tags": []
        }
    },
    "controller": {
        "nats": {
            "url": "nats://nats-server.example.org:4222",
            "requestSubject": "cc-node-controller.%c.request"
        },
        "toposMaxAge": 86400
    },
    "clusters": [
        {
            "name": "fritz",
            "powerBudgetTotal": 10000,
            "partitionRegex": "^energy_efficient$",
            "subclusters": [
                {
                    "name": "main",
                    "hostRegex": "^f\\d\\d\\d\\d$",
                    "devicetypes": {
                        "socket": {
                            "scope": "node",
                            "aggregator": {
                                "type": "last",
                                "powerMetric": "cpu_energy",
                                "performanceMetric": "ips",
                                "deviceType": "socket"
                            },
                            "controlName": "rapl.pkg_power_limit1",
                            "controlDefaultValue": 300,
                            "intervalConverged": "10m",
                            "intervalSearch": "2m",
                            "powerBudgetWeight": 1,
                            "optimizer": {
                                "type": "gssng",
                                "tolerance": 5,
                                "borders": {
                                    "lower": 123,
                                    "upper": 800
                                }
                            }
                        }
                    }
                }
            ]
        },
        {
            "name": "alex",
            "powerBudgetTotal": 20000,
            "partitionRegex": "^only_this_partition_please$",
            "subclusters": [
                {
                    "name": "a100",
                    "hostRegex": "^a\\d\\d\\d\\d$",
                    "devicetypes": {
                        "nvidia_gpu": {
                            "scope": "device",
                            "aggregator": {
                                "type": "last",
                                "powerMetric": "acc_power",
                                "performanceMetric": "kernels",
                                "deviceType": "nvidia_gpu"
                            },
                            "controlName": "nvml.power_limit",
                            "controlDefaultValue": 250,
                            "intervalConverged": "5m",
                            "intervalSearch": "2m",
                            "powerBudgetWeight": 2,
                            "optimizer": {
                                "type": "gssng",
                                "tolerance": 5,
                                "borders": {
                                    "lower": 123,
                                    "upper": 800
                                }
                            }
                        },
                        "socket": {
                            "scope": "job",
                            "aggregator": {
                                "type": "median",
                                "powerMetric": "cpu_energy",
                                "performanceMetric": "ips",
                                "deviceType": "nvidia_gpu"
                            },
                            "controlName": "rapl.pkg_power_limit1",
                            "controlDefaultValue": 100,
                            "intervalConverged": "5m",
                            "intervalSearch": "2m",
                            "powerBudgetWeight": 1,
                            "optimizer": {
                                "type": "gssng",
                                "tolerance": 5,
                                "borders": {
                                    "lower": 123,
                                    "upper": 800
                                }
                            }
                        }
                    }
                }
            ]
        }
    ]
}
```
