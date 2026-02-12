---
title: Plan overall ClusterCockpit architecture
weight: 5
description: How to decide on communication and data flows
categories: [ClusterCockpit]
tags: [Admin]
---

## Introduction

When deploying ClusterCockpit in production, two key architectural decisions
need to be made:

1. **Transport mechanism**: How metrics flow from collectors to the metric store
   (REST API vs NATS)
2. **Metric store deployment**: Where the metric store runs (internal to
   cc-backend vs external standalone)

This guide helps you understand the trade-offs to make informed decisions based
on your cluster size, administrative capabilities, and requirements.

## Transport: REST API vs NATS

The cc-metric-collector can send metrics to cc-metric-store using either direct
HTTP REST API calls or via NATS messaging.

### REST API Transport

With REST transport, each collector node sends HTTP POST requests directly to
the metric store endpoint.

```
┌─────────────┐     HTTP POST      ┌──────────────────┐
│  Collector  │ ─────────────────► │  cc-metric-store │
│   (Node 1)  │                    │                  │
└─────────────┘                    │                  │
┌─────────────┐     HTTP POST      │                  │
│  Collector  │ ─────────────────► │                  │
│   (Node 2)  │                    └──────────────────┘
└─────────────┘
      ...
```

**Advantages:**

- Simple setup with no additional infrastructure
- Direct point-to-point communication
- Easy to debug and monitor
- Works well for smaller clusters (< 500 nodes)

**Disadvantages:**

- Each collector needs direct network access to metric store
- No buffering: if metric store is unavailable, metrics are lost
- Scales linearly with node count (many concurrent connections)
- Higher load on metric store during burst scenarios

### NATS Transport

With NATS, collectors publish metrics to a NATS server, and the metric store
subscribes to receive them.

```
┌─────────────┐                    ┌─────────────┐
│  Collector  │ ──► publish ──►    │             │
│   (Node 1)  │                    │             │
└─────────────┘                    │    NATS     │     subscribe     ┌──────────────────┐
┌─────────────┐                    │   Server    │ ◄───────────────► │  cc-metric-store │
│  Collector  │ ──► publish ──►    │             │                   └──────────────────┘
│   (Node 2)  │                    │             │
└─────────────┘                    └─────────────┘
      ...
```

**Advantages:**

- Decoupled architecture: collectors and metric store are independent
- Built-in buffering and message persistence (with JetStream)
- Better scalability for large clusters (1000+ nodes)
- Supports multiple subscribers (e.g., external metric store for redundancy)
- Collectors continue working even if metric store is temporarily down
- Lower connection overhead (single connection per collector to NATS)
- Integrated key management via NKeys (Ed25519-based authentication):
  - No need to generate and distribute JWT tokens to each collector
  - Centralized credential management in NATS server configuration
  - Support for accounts with fine-grained publish/subscribe permissions
  - Credential revocation without redeploying collectors
  - Simpler key rotation compared to JWT token redistribution

**Disadvantages:**

- Additional infrastructure component to deploy and maintain
- More complex initial setup and configuration
- Additional point of failure (NATS server)
- Requires NATS expertise for troubleshooting

### Recommendation

| Cluster Size  | Recommended Transport        |
| ------------- | ---------------------------- |
| < 200 nodes   | REST API                     |
| 200-500 nodes | Either (based on preference) |
| > 500 nodes   | NATS                         |

For large clusters or environments requiring high availability, NATS provides
better resilience and scalability. For smaller deployments or when minimizing
complexity is important, REST API is sufficient.

## Metric Store: Internal vs External

The cc-metric-store storage engine can run either integrated within cc-backend
(internal) or as a separate standalone service (external).

### Internal Metric Store

The metric store runs as part of the cc-backend process, sharing the same
configuration and lifecycle.

```
┌────────────────────────────────────────┐
│              cc-backend                │
│  ┌──────────────┐  ┌────────────────┐  │
│  │   Web UI &   │  │  metric-store  │  │
│  │   GraphQL    │  │    (internal)  │  │
│  └──────────────┘  └────────────────┘  │
└────────────────────────────────────────┘
         │                    ▲
         ▼                    │
    ┌─────────┐          ┌─────────┐
    │ Browser │          │Collector│
    └─────────┘          └─────────┘
```

**Advantages:**

- Single process to deploy and manage
- Unified configuration
- Simplified networking (metrics received on same endpoint)
- Lower resource overhead
- Easier initial setup

**Disadvantages:**

- Metric store restart requires cc-backend restart and the other way around
- A cc-backend restart can take very long since the metric store checkpoints
  have to loaded on startup
- Resource contention between web serving and metric ingestion
- No horizontal scaling of metric ingestion
- Single point of failure for entire system

### External Metric Store

The metric store runs as a separate process, communicating with cc-backend via
its REST API.

```
┌──────────────────┐         ┌──────────────────┐
│    cc-backend    │ ◄─────► │  cc-metric-store │
│   (Web UI/API)   │  query  │    (external)    │
└──────────────────┘         └──────────────────┘
         │                            ▲
         ▼                            │
    ┌─────────┐                  ┌─────────┐
    │ Browser │                  │Collector│
    └─────────┘                  └─────────┘
```

**Advantages:**

- Independent scaling and resource allocation
- Can restart metric store without affecting web interface and the other way
  around
- Enables redundancy with multiple metric store instances
- Better isolation for security and resource management
- Can run on dedicated hardware optimized for in-memory workloads

**Disadvantages:**

- Two processes to deploy and manage
- Separate configuration files
- Additional network communication between components
- More complex setup and monitoring

### Recommendation

| Scenario                           | Recommended Deployment       |
| ---------------------------------- | ---------------------------- |
| Development/Testing                | Internal                     |
| Small production (< 200 nodes)     | Internal                     |
| Medium production (200-1000 nodes) | Either                       |
| Large production (> 1000 nodes)    | External                     |
| Resource-constrained head node     | External (on dedicated host) |

## Security Considerations

### Network Exposure

| Component    | REST Transport                 | NATS Transport                              |
| ------------ | ------------------------------ | ------------------------------------------- |
| Metric Store | Exposed to all collector nodes | Only exposed to NATS server                 |
| NATS Server  | N/A                            | Exposed to all collectors and metric stores |
| cc-backend   | Exposed to users               | Exposed to users                            |

With NATS, the metric store can be isolated from the compute network, reducing
attack surface. The NATS server becomes the single point of ingress for metrics.
Another option to isolate the web backend from the compute network is to setup
[cc-metric-collector proxies]({{< ref hierarchical-collection >}}).

### Authentication

- **REST API**: Uses JWT tokens (Ed25519 signed). Each collector needs a valid
  token configured and distributed to it.
- **NATS**: Supports multiple authentication methods:
  - Username/password (simple, suitable for smaller deployments)
  - NKeys (Ed25519 key pairs managed centrally in NATS server)
  - Credential files (`.creds`) for decentralized authentication
  - Accounts for multi-tenancy with isolated namespaces

**NKeys Advantage**: With NATS NKeys, authentication keys are managed in the
NATS server configuration rather than distributed to each collector. This
simplifies credential management significantly:

- Add/remove collectors by editing NATS server config
- Revoke access instantly without touching collector nodes
- No JWT token expiration to manage
- Keys can be scoped to specific subjects (publish-only for collectors)

For both transports, ensure:

- Keys are properly generated and securely stored
- TLS is enabled for production deployments
- Network segmentation isolates monitoring traffic

### Privilege Separation

Both **cc-backend** and the external **cc-metric-store** support dropping
privileges after binding to privileged ports (via `user` and `group`
configuration). This limits the impact of potential vulnerabilities.

## Performance Considerations

### Memory Usage

The metric store keeps data in memory based on `retention-in-memory`. Memory
usage scales with:

- Number of nodes
- Number of metrics per node
- Number of hardware scopes (cores, sockets, accelerators)
- Retention duration
- Metric frequency

For a 1000-node cluster with 20 metrics at 60-second intervals and 48-hour
retention, expect approximately 10-20 GB of memory usage.
For larger setups and many core level metrics this can increase up to 100GB,
which must fit into main memory.

### CPU Usage

- **Internal**: Competes with cc-backend web serving
- **External**: Dedicated resources for metric processing

For clusters with high query load (many users viewing job details), external
deployment prevents metric ingestion from impacting user experience.

### Disk I/O

Checkpoints are written periodically. For large deployments:

- Use fast storage (SSD) for checkpoint directory
- Consider separate disks for checkpoints and archives
- Monitor disk space for archive growth

## Example Configurations

### Small Cluster (Internal + REST)

Single cc-backend with internal metric store, collectors using REST:

```json
// cc-backend config
{
  "metricstore": {
    "enabled": true,
    "checkpoints": {
      "interval": "12h",
      "directory": "./var/checkpoints"
    },
    "retention-in-memory": "48h"
  }
}
```

### Large Cluster (External + NATS)

Separate cc-metric-store with NATS transport:

```json
// cc-metric-store config
{
  "main": {
    "addr": "0.0.0.0:8080",
    "jwt-public-key": "..."
  },
  "nats": {
    "address": "nats://nats-server:4222",
    "username": "ccms",
    "password": "..."
  },
  "metric-store": {
    "retention-in-memory": "48h",
    "memory-cap": 80,
    "checkpoints": {
      "interval": "12h",
      "directory": "/data/checkpoints"
    },
    "cleanup": {
      "mode": "archive",
      "interval": "48h",
      "directory": "/data/archive"
    },
    "nats-subscriptions": [
      {
        "subscribe-to": "hpc-metrics",
        "cluster-tag": "mycluster"
      }
    ]
  }
}
```

## Decision Checklist

Use this checklist to guide your architecture decision:

- [ ] **Cluster size**: How many nodes need monitoring?
- [ ] **Availability requirements**: Is downtime acceptable?
- [ ] **Administrative capacity**: Can you manage additional services?
- [ ] **Network topology**: Can collectors reach the metric store directly?
- [ ] **Resource constraints**: Is the head node resource-limited?
- [ ] **Security requirements**: Do you need network isolation?
- [ ] **Growth plans**: Will the cluster expand significantly?

For most new deployments, starting with internal metric store and REST transport
is recommended. You can migrate to external deployment and/or NATS later as
needs evolve.
