---
title: How to set up hierarchical metric collection
description: Configure multiple cc-metric-collector instances to receive metrics from compute nodes and forward them to the backend
categories: [cc-metric-collector]
tags: [Collector, HPC, Deployment]
weight: 15
---

## Overview

In large HPC clusters, it's often impractical or undesirable to have every
compute node connect directly to the central database. A hierarchical collection
setup allows you to:

- **Reduce database connections**: Instead of hundreds of nodes connecting
  directly, use aggregation nodes as intermediaries
- **Improve network efficiency**: Aggregate metrics at rack or partition level
  before forwarding
- **Add processing layers**: Filter, transform, or enrich metrics at
  intermediate collection points
- **Increase resilience**: Buffer metrics during temporary database outages

This guide shows how to configure multiple cc-metric-collector instances where
compute nodes send metrics to aggregation nodes, which then forward them to the
backend database.

## Architecture

```mermaid
flowchart TD
  subgraph Rack1 ["Rack 1 - Compute Nodes"]
    direction LR
    node1["Node 1<br/>cc-metric-collector"]
    node2["Node 2<br/>cc-metric-collector"]
    node3["Node 3<br/>cc-metric-collector"]
  end

  subgraph Rack2 ["Rack 2 - Compute Nodes"]
    direction LR
    node4["Node 4<br/>cc-metric-collector"]
    node5["Node 5<br/>cc-metric-collector"]
    node6["Node 6<br/>cc-metric-collector"]
  end

  subgraph Aggregator ["Aggregation Node"]
    ccrecv["cc-metric-collector<br/>(with receivers)"]
  end

  subgraph Backend ["Backend Server"]
    ccms[("cc-metric-store")]
    ccweb["cc-backend<br/>(Web Frontend)"]
  end
  
  node1 --> ccrecv
  node2 --> ccrecv
  node3 --> ccrecv
  node4 --> ccrecv
  node5 --> ccrecv
  node6 --> ccrecv
  
  ccrecv --> ccms
  ccms <--> ccweb
```

### Components

1. **Compute Node Collectors**: Run on each compute node, collect local metrics, forward to aggregation node
2. **Aggregation Node**: Receives metrics from multiple compute nodes, optionally processes them, forwards to cc-metric-store
3. **cc-metric-store**: In-memory time-series database for metric storage and retrieval
4. **cc-backend**: Web frontend that queries cc-metric-store and visualizes metrics

## Configuration

### Step 1: Configure Compute Nodes

Compute nodes collect local metrics and send them to the aggregation node using a network sink (NATS or HTTP).

#### Using NATS (Recommended)

NATS provides better performance, reliability, and built-in clustering support.

**config.json**:

```json
{
  "sinks-file": "/etc/cc-metric-collector/sinks.json",
  "collectors-file": "/etc/cc-metric-collector/collectors.json",
  "receivers-file": "/etc/cc-metric-collector/receivers.json",
  "router-file": "/etc/cc-metric-collector/router.json",
  "main": {
    "interval": "10s",
    "duration": "1s"
  }
}
```

**sinks.json**:

```json
{
  "nats_aggregator": {
    "type": "nats",
    "host": "aggregator.example.org",
    "port": "4222",
    "subject": "metrics.rack1"
  }
}
```

**collectors.json** (enable metrics you need):

```json
{
  "cpustat": {},
  "memstat": {},
  "diskstat": {},
  "netstat": {},
  "loadavg": {},
  "tempstat": {}
}
```

**router.json** (add identifying tags):

```json
{
  "interval_timestamp": true,
  "process_messages": {
    "manipulate_messages": [
      {
        "add_base_tags": {
          "cluster": "mycluster",
          "rack": "rack1"
        }
      }
    ]
  }
}
```

**receivers.json** (empty for compute nodes):

```json
{}
```

#### Using HTTP

HTTP is simpler but less efficient for high-frequency metrics.

**sinks.json** (HTTP alternative):

```json
{
  "http_aggregator": {
    "type": "http",
    "host": "aggregator.example.org",
    "port": "8080",
    "path": "/api/write",
    "idle_connection_timeout": "5s",
    "timeout": "3s"
  }
}
```

### Step 2: Configure Aggregation Node

The aggregation node receives metrics from compute nodes via receivers and forwards them to the backend database.

**config.json**:

```json
{
  "sinks-file": "/etc/cc-metric-collector/sinks.json",
  "collectors-file": "/etc/cc-metric-collector/collectors.json",
  "receivers-file": "/etc/cc-metric-collector/receivers.json",
  "router-file": "/etc/cc-metric-collector/router.json",
  "main": {
    "interval": "10s",
    "duration": "1s"
  }
}
```

**receivers.json** (receive from compute nodes):

```json
{
  "nats_rack1": {
    "type": "nats",
    "address": "localhost",
    "port": "4222",
    "subject": "metrics.rack1"
  },
  "nats_rack2": {
    "type": "nats",
    "address": "localhost",
    "port": "4222",
    "subject": "metrics.rack2"
  }
}
```

**sinks.json** (forward to cc-metric-store):

```json
{
  "metricstore": {
    "type": "http",
    "host": "backend.example.org",
    "port": "8082",
    "path": "/api/write",
    "idle_connection_timeout": "5s",
    "timeout": "5s",
    "jwt": "eyJ0eXAiOiJKV1QiLCJhbGciOiJFZERTQSJ9.eyJ1c2VyIjoiYWRtaW4iLCJyb2xlcyI6WyJST0xFX0FETUlOIiwiUk9MRV9VU0VSIl19.d-3_3FZTsadPjDbVXKrQr4jNiQV-B_1-uaL_lW8d8gGb-TSAG9KdMg"
  }
}
```

**Note**: The `jwt` token must be signed with the private key corresponding to the public key configured in cc-metric-store. See [JWT generation guide]({{< ref "../how-to-guides/generateJWT.md" >}}) for details.

**collectors.json** (optionally collect local metrics):

```json
{
  "cpustat": {},
  "memstat": {},
  "loadavg": {}
}
```

**router.json** (optionally process metrics):

```json
{
  "interval_timestamp": false,
  "num_cache_intervals": 0,
  "process_messages": {
    "manipulate_messages": [
      {
        "add_base_tags": {
          "datacenter": "dc1"
        }
      }
    ]
  }
}
```

### Step 3: Set Up cc-metric-store

The backend server needs cc-metric-store to receive and store metrics from the aggregation node.

**config.json** (`/etc/cc-metric-store/config.json`):

```json
{
  "metrics": {
    "cpu_user": {
      "frequency": 10,
      "aggregation": "avg"
    },
    "cpu_system": {
      "frequency": 10,
      "aggregation": "avg"
    },
    "mem_used": {
      "frequency": 10,
      "aggregation": null
    },
    "mem_total": {
      "frequency": 10,
      "aggregation": null
    },
    "net_bw": {
      "frequency": 10,
      "aggregation": "sum"
    },
    "flops_any": {
      "frequency": 10,
      "aggregation": "sum"
    },
    "mem_bw": {
      "frequency": 10,
      "aggregation": "sum"
    }
  },
  "http-api": {
    "address": "0.0.0.0:8082"
  },
  "jwt-public-key": "kzfYrYy+TzpanWZHJ5qSdMj5uKUWgq74BWhQG6copP0=",
  "retention-in-memory": "48h",
  "checkpoints": {
    "interval": "12h",
    "directory": "/var/lib/cc-metric-store/checkpoints",
    "restore": "48h"
  },
  "archive": {
    "interval": "24h",
    "directory": "/var/lib/cc-metric-store/archive"
  }
}
```

**Important configuration notes**:

- **metrics**: Must list ALL metrics you want to store. Only configured metrics are accepted.
- **frequency**: Must match the collection interval from cc-metric-collector (in seconds)
- **aggregation**: `"sum"` for resource metrics (bandwidth, FLOPS), `"avg"` for diagnostic metrics (CPU %), `null` for node-only metrics
- **jwt-public-key**: Must correspond to the private key used to sign JWT tokens in the aggregation node sink configuration
- **retention-in-memory**: How long to keep metrics in memory (should cover typical job durations)

**Install cc-metric-store**:

```bash
# Download binary
wget https://github.com/ClusterCockpit/cc-metric-store/releases/latest/download/cc-metric-store

# Install
sudo mkdir -p /opt/monitoring/cc-metric-store
sudo mv cc-metric-store /opt/monitoring/cc-metric-store/
sudo chmod +x /opt/monitoring/cc-metric-store/cc-metric-store

# Create directories
sudo mkdir -p /var/lib/cc-metric-store/checkpoints
sudo mkdir -p /var/lib/cc-metric-store/archive
sudo mkdir -p /etc/cc-metric-store
```

**Create systemd service** (`/etc/systemd/system/cc-metric-store.service`):

```ini
[Unit]
Description=ClusterCockpit Metric Store
After=network.target

[Service]
Type=simple
User=cc-metricstore
Group=cc-metricstore
WorkingDirectory=/opt/monitoring/cc-metric-store
ExecStart=/opt/monitoring/cc-metric-store/cc-metric-store -config /etc/cc-metric-store/config.json
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Start cc-metric-store**:

```bash
# Create user
sudo useradd -r -s /bin/false cc-metricstore
sudo chown -R cc-metricstore:cc-metricstore /var/lib/cc-metric-store

# Start service
sudo systemctl daemon-reload
sudo systemctl start cc-metric-store
sudo systemctl enable cc-metric-store

# Check status
sudo systemctl status cc-metric-store
```

### Step 4: Set Up NATS Server

The aggregation node needs a NATS server to receive metrics from compute nodes.

**Install NATS**:

```bash
# Using Docker
docker run -d --name nats -p 4222:4222 nats:latest

# Using package manager (example for Ubuntu/Debian)
curl -L https://github.com/nats-io/nats-server/releases/download/v2.10.5/nats-server-v2.10.5-linux-amd64.zip -o nats-server.zip
unzip nats-server.zip
sudo mv nats-server-v2.10.5-linux-amd64/nats-server /usr/local/bin/
```

**NATS Configuration** (`/etc/nats/nats-server.conf`):

```
listen: 0.0.0.0:4222
max_payload: 10MB
max_connections: 1000

# Optional: Enable authentication
authorization {
  user: collector
  password: secure_password
}

# Optional: Enable clustering for HA
cluster {
  name: metrics-cluster
  listen: 0.0.0.0:6222
}
```

**Start NATS**:

```bash
# Systemd
sudo systemctl start nats
sudo systemctl enable nats

# Or directly
nats-server -c /etc/nats/nats-server.conf
```

## Advanced Configurations

### Multiple Aggregation Levels

For very large clusters, you can create multiple aggregation levels:

```mermaid
flowchart TD
  subgraph Compute ["Compute Nodes"]
    node1["Node 1-100"]
  end

  subgraph Rack ["Rack Aggregators"]
    agg1["Aggregator<br/>Rack 1-10"]
  end

  subgraph Cluster ["Cluster Aggregator"]
    agg_main["Main Aggregator"]
  end

  subgraph Backend ["Backend"]
    ccms[("cc-metric-store")]
  end
  
  node1 --> agg1
  agg1 --> agg_main
  agg_main --> ccms
```

**Rack-level aggregator sinks.json**:

```json
{
  "cluster_aggregator": {
    "type": "nats",
    "host": "main-aggregator.example.org",
    "port": "4222",
    "subject": "metrics.cluster"
  }
}
```

**Cluster-level aggregator receivers.json**:

```json
{
  "all_racks": {
    "type": "nats",
    "address": "localhost",
    "port": "4222",
    "subject": "metrics.cluster"
  }
}
```

### Load Balancing with Multiple Aggregators

Use NATS queue groups to distribute load across multiple aggregation nodes:

**Compute node sinks.json**:

```json
{
  "nats_aggregator": {
    "type": "nats",
    "host": "nats-cluster.example.org",
    "port": "4222",
    "subject": "metrics.loadbalanced"
  }
}
```

**Aggregator 1 and 2 receivers.json** (identical configuration):

```json
{
  "nats_with_queue": {
    "type": "nats",
    "address": "localhost",
    "port": "4222",
    "subject": "metrics.loadbalanced",
    "queue_group": "aggregators"
  }
}
```

With `queue_group` configured, NATS automatically distributes messages across all aggregators in the group.

### Filtering at Aggregation Level

Reduce cc-metric-store load by filtering metrics at the aggregation node:

**Aggregator router.json**:

```json
{
  "interval_timestamp": false,
  "process_messages": {
    "manipulate_messages": [
      {
        "drop_by_name": ["cpu_idle", "cpu_guest", "cpu_guest_nice"]
      },
      {
        "drop_by": "value == 0 && match('temp_', name)"
      },
      {
        "add_base_tags": {
          "aggregated": "true"
        }
      }
    ]
  }
}
```

### Metric Transformation

Aggregate or transform metrics before forwarding:

**Aggregator router.json**:

```json
{
  "interval_timestamp": false,
  "num_cache_intervals": 1,
  "interval_aggregates": [
    {
      "name": "rack_avg_temp",
      "if": "name == 'temp_package_id_0'",
      "function": "avg(values)",
      "tags": {
        "type": "rack",
        "rack": "<copy>"
      },
      "meta": {
        "unit": "degC",
        "source": "aggregated"
      }
    }
  ]
}
```

### High Availability Setup

Use multiple NATS servers in cluster mode:

**NATS server 1 config**:

```
cluster {
  name: metrics-cluster
  listen: 0.0.0.0:6222
  routes: [
    nats://nats2.example.org:6222
    nats://nats3.example.org:6222
  ]
}
```

**Compute node sinks.json** (with failover):

```json
{
  "nats_ha": {
    "type": "nats",
    "host": "nats1.example.org,nats2.example.org,nats3.example.org",
    "port": "4222",
    "subject": "metrics.rack1"
  }
}
```

## Deployment

### 1. Install cc-metric-collector

On all nodes (compute and aggregation):

```bash
# Download binary
wget https://github.com/ClusterCockpit/cc-metric-collector/releases/latest/download/cc-metric-collector

# Install
sudo mkdir -p /opt/monitoring/cc-metric-collector
sudo mv cc-metric-collector /opt/monitoring/cc-metric-collector/
sudo chmod +x /opt/monitoring/cc-metric-collector/cc-metric-collector
```

### 2. Deploy Configuration Files

**Compute nodes**:

```bash
sudo mkdir -p /etc/cc-metric-collector
sudo cp config.json /etc/cc-metric-collector/
sudo cp sinks.json /etc/cc-metric-collector/
sudo cp collectors.json /etc/cc-metric-collector/
sudo cp receivers.json /etc/cc-metric-collector/
sudo cp router.json /etc/cc-metric-collector/
```

**Aggregation node**:

```bash
sudo mkdir -p /etc/cc-metric-collector
# Deploy aggregator-specific configs
sudo cp aggregator-config.json /etc/cc-metric-collector/config.json
sudo cp aggregator-sinks.json /etc/cc-metric-collector/sinks.json
sudo cp aggregator-receivers.json /etc/cc-metric-collector/receivers.json
# etc...
```

### 3. Create Systemd Service

**On all nodes** (`/etc/systemd/system/cc-metric-collector.service`):

```ini
[Unit]
Description=ClusterCockpit Metric Collector
After=network.target

[Service]
Type=simple
User=cc-collector
Group=cc-collector
ExecStart=/opt/monitoring/cc-metric-collector/cc-metric-collector -config /etc/cc-metric-collector/config.json
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 4. Start Services

**Order of startup**:

1. Start cc-metric-store on backend server
2. Start NATS server on aggregation node
3. Start cc-metric-collector on aggregation node
4. Start cc-metric-collector on compute nodes

```bash
# On backend server
sudo systemctl start cc-metric-store

# On aggregation node
sudo systemctl start nats
sudo systemctl start cc-metric-collector

# On compute nodes
sudo systemctl start cc-metric-collector

# Enable on boot (on all nodes)
sudo systemctl enable cc-metric-store  # backend only
sudo systemctl enable nats              # aggregator only
sudo systemctl enable cc-metric-collector
```

## Testing and Validation

### Test Compute Node → Aggregator

**On compute node**, run once to verify metrics are collected:

```bash
cc-metric-collector -config /etc/cc-metric-collector/config.json -once
```

**On aggregation node**, check NATS for incoming metrics:

```bash
# Subscribe to see messages
nats sub 'metrics.>'
```

### Test Aggregator → cc-metric-store

**On aggregation node**, verify metrics are forwarded:

```bash
# Check logs
journalctl -u cc-metric-collector -f
```

**On backend server**, verify cc-metric-store is receiving data:

```bash
# Check cc-metric-store logs
journalctl -u cc-metric-store -f

# Query metrics via REST API (requires valid JWT token)
curl -H "Authorization: Bearer $JWT_TOKEN" \
  "http://backend.example.org:8082/api/query?cluster=mycluster&from=$(date -d '5 minutes ago' +%s)&to=$(date +%s)"
```

### Validate End-to-End

**Check cc-backend** to see if metrics appear for all nodes:

1. Open cc-backend web interface
2. Navigate to node view
3. Verify metrics are displayed for compute nodes
4. Check that tags (cluster, rack, etc.) are present

## Monitoring and Troubleshooting

### Check Collection Pipeline

```bash
# Compute node: metrics are being sent
journalctl -u cc-metric-collector -n 100 | grep -i "sent\|error"

# Aggregator: metrics are being received
journalctl -u cc-metric-collector -n 100 | grep -i "received\|error"

# NATS: check connections
nats server info
nats server list
```

### Common Issues

**Metrics not appearing in cc-metric-store**:

1. Check compute node → NATS connection
2. Verify NATS → aggregator reception
3. Check aggregator → cc-metric-store sink (verify JWT token is valid)
4. Verify metrics are configured in cc-metric-store's config.json
5. Examine router filters (may be dropping metrics)

**High latency**:

1. Reduce metric collection interval on compute nodes
2. Increase batch size in aggregator sinks
3. Add more aggregation nodes with load balancing
4. Check network bandwidth between tiers

**Memory growth on aggregator**:

1. Reduce `num_cache_intervals` in router
2. Check sink write performance
3. Verify cc-metric-store is accepting writes
4. Monitor NATS queue depth

**Memory growth on cc-metric-store**:

1. Reduce `retention-in-memory` setting
2. Increase checkpoint frequency
3. Verify archive cleanup is working

**Connection failures**:

1. Verify firewall rules allow NATS port (4222)
2. Check NATS server is running and accessible
3. Test network connectivity: `telnet aggregator.example.org 4222`
4. Review NATS server logs: `journalctl -u nats -f`

### Performance Tuning

**Compute nodes** (reduce overhead):

```json
{
  "main": {
    "interval": "30s",
    "duration": "1s"
  }
}
```

**Aggregator** (increase throughput):

```json
{
  "metricstore": {
    "type": "http",
    "host": "backend.example.org",
    "port": "8082",
    "path": "/api/write",
    "timeout": "10s",
    "idle_connection_timeout": "10s"
  }
}
```

**NATS server** (handle more connections):

```
max_connections: 10000
max_payload: 10MB
write_deadline: "10s"
```

## Security Considerations

### NATS Authentication

**NATS server config**:

```
authorization {
  users = [
    {
      user: "collector"
      password: "$2a$11$..."  # bcrypt hash
    }
  ]
}
```

**Compute node sinks.json**:

```json
{
  "nats_aggregator": {
    "type": "nats",
    "host": "aggregator.example.org",
    "port": "4222",
    "subject": "metrics.rack1",
    "username": "collector",
    "password": "secure_password"
  }
}
```

### TLS Encryption

**NATS server config**:

```
tls {
  cert_file: "/etc/nats/certs/server-cert.pem"
  key_file: "/etc/nats/certs/server-key.pem"
  ca_file: "/etc/nats/certs/ca.pem"
  verify: true
}
```

**Compute node sinks.json**:

```json
{
  "nats_aggregator": {
    "type": "nats",
    "host": "aggregator.example.org",
    "port": "4222",
    "subject": "metrics.rack1",
    "ssl": true,
    "ssl_cert": "/etc/cc-metric-collector/certs/client-cert.pem",
    "ssl_key": "/etc/cc-metric-collector/certs/client-key.pem"
  }
}
```

### Firewall Rules

**On aggregation node**:

```bash
# Allow NATS from compute network
sudo firewall-cmd --permanent --add-rich-rule='rule family="ipv4" source address="10.0.0.0/8" port protocol="tcp" port="4222" accept'

sudo firewall-cmd --reload
```

**On backend server**:

```bash
# Allow HTTP from aggregation node to cc-metric-store
sudo firewall-cmd --permanent --add-rich-rule='rule family="ipv4" source address="aggregator.example.org" port protocol="tcp" port="8082" accept'

sudo firewall-cmd --reload
```

## Alternative: Using NATS for cc-metric-store

Instead of HTTP, you can also use NATS to send metrics from the aggregation node to cc-metric-store.

**Aggregation node sinks.json**:

```json
{
  "nats_metricstore": {
    "type": "nats",
    "host": "backend.example.org",
    "port": "4222",
    "subject": "metrics.store"
  }
}
```

**cc-metric-store config.json** (add NATS section):

```json
{
  "metrics": { ... },
  "nats": {
    "address": "nats://0.0.0.0:4222",
    "subscriptions": [
      {
        "subscribe-to": "metrics.store",
        "cluster-tag": "mycluster"
      }
    ]
  },
  "http-api": { ... },
  "jwt-public-key": "...",
  "retention-in-memory": "48h",
  "checkpoints": { ... },
  "archive": { ... }
}
```

**Benefits of NATS**:
- Better performance for high-frequency metrics
- Built-in message buffering
- No need for JWT tokens in sink configuration
- Easier to scale with multiple aggregators

**Trade-offs**:
- Requires running NATS server on backend
- More complex infrastructure

## See Also

- [cc-metric-collector Configuration Reference]({{< ref "../reference/cc-metric-collector/ccmc-configuration.md" >}})
- [Router Configuration]({{< ref "../reference/cc-metric-collector/router.md" >}})
- [Metric Collectors]({{< ref "../reference/cc-metric-collector/collectors" >}})
- [cc-metric-store Configuration]({{< ref "../reference/cc-metric-store/ccms-configuration.md" >}})
- [JWT Token Generation]({{< ref "../how-to-guides/generateJWT.md" >}})
- [NATS Documentation](https://docs.nats.io/)
