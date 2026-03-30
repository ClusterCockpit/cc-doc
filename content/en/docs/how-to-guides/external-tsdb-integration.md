---
title: How to ingest metrics from external time series databases
description: Integrate Prometheus and InfluxDB data into cc-metric-store using adapter scripts and proxy approaches
categories: [cc-metric-store]
tags: [Admin, Developer]
weight: 20
---

## Overview

Many HPC sites already operate Prometheus or InfluxDB for general infrastructure
monitoring. When adopting ClusterCockpit, you may want to reuse existing metric
data rather than immediately deploying
[cc-metric-collector]({{< ref "../reference/cc-metric-collector" >}}) on every
node. This guide shows how to bridge data from external time series databases
into cc-metric-store.

cc-metric-store accepts metric data through two ingestion paths:

1. **REST API** (`POST /api/write/`) — uses
   [InfluxDB line protocol]({{< ref "../explanation/lineProtocol" >}}) format,
   authenticated with JWT (Ed25519)
2. **NATS messaging** — see
   [NATS configuration]({{< ref "../reference/cc-metric-store/ccms-configuration#nats-section" >}})

This guide focuses on the REST API path since it requires no additional
infrastructure beyond HTTP connectivity.

{{< alert title="Important" >}}
cc-metric-store only stores metrics that are listed in its
[`metrics` configuration section]({{< ref "../reference/cc-metric-store/ccms-configuration" >}}).
Any metric name sent via `/api/write/` that is not configured will be silently
dropped. Plan your metric name mapping carefully before deploying.
{{< /alert >}}

## Architecture

The general approach is: query the external TSDB, transform results into
ClusterCockpit's InfluxDB line protocol format, and POST them to cc-metric-store.

```mermaid
flowchart LR
  subgraph External ["External TSDB"]
    prom["Prometheus"]
    influx["InfluxDB"]
  end

  subgraph Adapter ["Adapter Layer"]
    script["Sync Script\n(cron-based)"]
  end

  subgraph CC ["ClusterCockpit"]
    ccms[("cc-metric-store\n/api/write/")]
    ccbe["cc-backend"]
  end

  prom -->|"HTTP API query"| script
  influx -->|"HTTP API query"| script
  script -->|"InfluxDB line protocol\n+ JWT auth"| ccms
  ccms <--> ccbe
```

### Approach Comparison

| Approach | Source | Mechanism | Latency | Complexity |
|---|---|---|---|---|
| Cron-based sync script | Prometheus or InfluxDB | Periodic query + POST | ~60s | Low |
| Prometheus remote_write proxy | Prometheus | Continuous push | ~seconds | Medium |
| Telegraf HTTP output | InfluxDB | Telegraf pipeline | ~seconds | Medium |

For most HPC sites, the **cron-based sync script** is recommended. It is the
simplest to deploy and maintain, and 60-second latency is perfectly adequate for
monitoring dashboards.

## Prerequisites

- Running cc-metric-store instance with HTTP API enabled
- Valid JWT token (Ed25519-signed) — see
  [JWT generation guide]({{< ref "../how-to-guides/generateJWT" >}})
- Python 3.6+ with the `requests` library (`pip install requests`)
- Target metrics pre-configured in cc-metric-store's `config.json`
- Network access from the adapter host to both the source TSDB and cc-metric-store

## Metric Name Mapping

ClusterCockpit uses its own
[metric naming convention]({{< ref "../tutorials/prod-metric-list" >}}) which
differs from Prometheus and InfluxDB/Telegraf conventions. The adapter scripts
must translate between them.

The following table shows mappings for common node-level metrics:

| CC Metric | Prometheus Query | InfluxDB / Telegraf | Unit | Aggregation |
|---|---|---|---|---|
| `cpu_load` | `node_load1` | `system.load1` | - | avg |
| `cpu_user` | `100 * rate(node_cpu_seconds_total{mode="user"}[1m])` | `cpu.usage_user` | % | avg |
| `mem_used` | `(node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / (1024*1024)` | `mem.used / (1024*1024)` | MB | - |
| `net_bw` | `rate(node_network_receive_bytes_total[1m]) + rate(node_network_transmit_bytes_total[1m])` | `net.bytes_recv + net.bytes_sent` | bytes/s | sum |
| `cpu_power` | `node_rapl_package_joules_total` (rate) | `ipmi_sensors` (if available) | W | sum |

{{< alert color="warning" title="Limitation" >}}
HPC-specific metrics like `flops_any`, `mem_bw`, and `ipc` require hardware
performance counter access (e.g., via LIKWID). These are **not** available from
standard Prometheus node_exporter or Telegraf. This integration supplements but
does not replace
[cc-metric-collector]({{< ref "../reference/cc-metric-collector" >}}) for
hardware counter metrics.
{{< /alert >}}

## cc-metric-store Configuration

Each bridged metric must be listed in the `metrics` section of cc-metric-store's
`config.json`. The `frequency` must match the interval at which your sync script
runs (in seconds).

```json
{
  "metrics": {
    "cpu_load":  { "frequency": 60, "aggregation": "avg" },
    "cpu_user":  { "frequency": 60, "aggregation": "avg" },
    "mem_used":  { "frequency": 60, "aggregation": null },
    "net_bw":    { "frequency": 60, "aggregation": "sum" }
  }
}
```

If you already have metrics configured for cc-metric-collector with a different
frequency (e.g., 10s), do **not** change that. Instead, the sync script should
run at the same frequency as the already configured value. See the
[configuration reference]({{< ref "../reference/cc-metric-store/ccms-configuration" >}})
for details.

## Prometheus to cc-metric-store

### Cron-based Sync Script

The following Python script queries Prometheus for the latest metric values and
forwards them to cc-metric-store. Save it as `prom2ccms.py`:

```python
#!/usr/bin/env python3
"""Sync metrics from Prometheus to cc-metric-store."""

import sys
import time
import logging
import requests

# --- Configuration -----------------------------------------------------------

PROMETHEUS_URL = "http://prometheus.example.org:9090"
CCMS_URL       = "http://ccms.example.org:8080"
JWT_TOKEN      = "eyJ0eXAiOiJKV1QiLC..."  # Your Ed25519-signed JWT
CLUSTER_NAME   = "mycluster"

# Mapping: CC metric name -> (PromQL query, type, scale_factor)
# type is "node" for node-level metrics
METRIC_MAP = {
    "cpu_load": (
        'node_load1',
        "node", 1.0
    ),
    "cpu_user": (
        '100 * avg by(instance)(rate(node_cpu_seconds_total{mode="user"}[2m]))',
        "node", 1.0
    ),
    "mem_used": (
        '(node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / (1024*1024)',
        "node", 1.0
    ),
    "net_bw": (
        'sum by(instance)(rate(node_network_receive_bytes_total{device!="lo"}[2m])'
        ' + rate(node_network_transmit_bytes_total{device!="lo"}[2m]))',
        "node", 1.0
    ),
}

# --- End Configuration -------------------------------------------------------

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("prom2ccms")


def query_prometheus(promql: str) -> list:
    """Run an instant query against Prometheus and return result list."""
    resp = requests.get(
        f"{PROMETHEUS_URL}/api/v1/query",
        params={"query": promql},
        timeout=10,
    )
    resp.raise_for_status()
    data = resp.json()
    if data["status"] != "success":
        raise RuntimeError(f"Prometheus query failed: {data}")
    return data["data"]["result"]


def instance_to_hostname(instance: str) -> str:
    """Strip port from Prometheus instance label (e.g., 'node01:9100' -> 'node01')."""
    return instance.rsplit(":", 1)[0]


def build_line_protocol(metric_name: str, hostname: str, metric_type: str,
                        value: float, timestamp: int) -> str:
    """Build an InfluxDB line protocol string for cc-metric-store."""
    return (
        f"{metric_name},cluster={CLUSTER_NAME},hostname={hostname},"
        f"type={metric_type} value={value} {timestamp}"
    )


def push_to_ccms(lines: list):
    """POST metric lines to cc-metric-store /api/write/ endpoint."""
    if not lines:
        return
    payload = "\n".join(lines)
    resp = requests.post(
        f"{CCMS_URL}/api/write/",
        headers={"Authorization": f"Bearer {JWT_TOKEN}"},
        data=payload,
        timeout=10,
    )
    resp.raise_for_status()
    log.info("Pushed %d lines to cc-metric-store", len(lines))


def main():
    lines = []
    now = int(time.time())

    for cc_name, (promql, metric_type, scale) in METRIC_MAP.items():
        try:
            results = query_prometheus(promql)
        except Exception as e:
            log.error("Failed to query %s: %s", cc_name, e)
            continue

        for series in results:
            instance = series["metric"].get("instance", "")
            if not instance:
                continue
            hostname = instance_to_hostname(instance)
            value = float(series["value"][1]) * scale
            lines.append(
                build_line_protocol(cc_name, hostname, metric_type, value, now)
            )

    try:
        push_to_ccms(lines)
    except Exception as e:
        log.error("Failed to push to cc-metric-store: %s", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
```

Make the script executable and set up a cron job:

```bash
chmod +x /opt/monitoring/prom2ccms/prom2ccms.py

# Run every 60 seconds (matching cc-metric-store frequency)
# crontab -e
* * * * * /opt/monitoring/prom2ccms/prom2ccms.py >> /var/log/prom2ccms.log 2>&1
```

{{< alert title="Note" >}}
For rate-based Prometheus metrics (like `node_cpu_seconds_total`), the PromQL
query itself uses `rate()` or `irate()` so the returned value is already a
per-second rate. The script simply forwards the computed value.
{{< /alert >}}

### Advanced: Prometheus remote_write Proxy

For near-real-time forwarding, Prometheus can push metrics via its `remote_write`
feature to a small HTTP proxy that converts them to cc-metric-store format.

Add to your `prometheus.yml`:

```yaml
remote_write:
  - url: "http://adapter-host:9201/receive"
    write_relabel_configs:
      # Only forward metrics we care about
      - source_labels: [__name__]
        regex: "node_load1|node_cpu_seconds_total|node_memory_.*|node_network_.*"
        action: keep
```

The proxy receives Protobuf-encoded, Snappy-compressed payloads and must decode
them before converting. This requires additional Python packages:

```bash
pip install protobuf python-snappy
```

A skeleton implementation is available in the
[Prometheus remote write specification](https://prometheus.io/docs/concepts/remote_write_spec/).
The proxy must:

1. Decompress the Snappy-encoded request body
2. Decode the Protobuf `WriteRequest` message
3. Map metric names and labels to CC format
4. Batch-POST the resulting lines to `/api/write/`

{{< alert title="Note" >}}
The remote_write proxy is significantly more complex than the cron approach. It
requires a long-running service, additional dependencies, and handling Protobuf
schemas. For most HPC sites, the cron-based script above is recommended.
{{< /alert >}}

## InfluxDB to cc-metric-store

### Cron-based Sync Script

The following script queries InfluxDB v2 (Flux) for the latest metric values and
forwards them to cc-metric-store. Save it as `influx2ccms.py`:

```python
#!/usr/bin/env python3
"""Sync metrics from InfluxDB v2 to cc-metric-store."""

import sys
import time
import csv
import io
import logging
import requests

# --- Configuration -----------------------------------------------------------

INFLUXDB_URL   = "http://influxdb.example.org:8086"
INFLUXDB_ORG   = "myorg"
INFLUXDB_TOKEN = "your-influxdb-token"
INFLUXDB_BUCKET = "telegraf"

CCMS_URL    = "http://ccms.example.org:8080"
JWT_TOKEN   = "eyJ0eXAiOiJKV1QiLC..."  # Your Ed25519-signed JWT
CLUSTER_NAME = "mycluster"

# Mapping: CC metric name -> (Flux query returning _value and host columns)
METRIC_MAP = {
    "cpu_load": '''
        from(bucket: "{bucket}")
          |> range(start: -5m)
          |> filter(fn: (r) => r._measurement == "system" and r._field == "load1")
          |> last()
    ''',
    "cpu_user": '''
        from(bucket: "{bucket}")
          |> range(start: -5m)
          |> filter(fn: (r) => r._measurement == "cpu" and r._field == "usage_user" and r.cpu == "cpu-total")
          |> last()
    ''',
    "mem_used": '''
        from(bucket: "{bucket}")
          |> range(start: -5m)
          |> filter(fn: (r) => r._measurement == "mem" and r._field == "used")
          |> last()
          |> map(fn: (r) => ({{ r with _value: r._value / 1048576.0 }}))
    ''',
    "net_bw": '''
        from(bucket: "{bucket}")
          |> range(start: -5m)
          |> filter(fn: (r) => r._measurement == "net" and (r._field == "bytes_recv" or r._field == "bytes_sent"))
          |> derivative(unit: 1s, nonNegative: true)
          |> last()
          |> group(columns: ["host"])
          |> sum()
    ''',
}

# --- End Configuration -------------------------------------------------------

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("influx2ccms")


def query_influxdb(flux_query: str) -> list:
    """Execute a Flux query and return list of (host, value) tuples."""
    query = flux_query.format(bucket=INFLUXDB_BUCKET)
    resp = requests.post(
        f"{INFLUXDB_URL}/api/v2/query",
        headers={
            "Authorization": f"Token {INFLUXDB_TOKEN}",
            "Content-Type": "application/vnd.flux",
            "Accept": "text/csv",
        },
        params={"org": INFLUXDB_ORG},
        data=query,
        timeout=15,
    )
    resp.raise_for_status()

    results = []
    reader = csv.DictReader(io.StringIO(resp.text))
    for row in reader:
        host = row.get("host", "")
        value = row.get("_value", "")
        if host and value:
            try:
                results.append((host, float(value)))
            except ValueError:
                continue
    return results


def push_to_ccms(lines: list):
    """POST metric lines to cc-metric-store /api/write/ endpoint."""
    if not lines:
        return
    payload = "\n".join(lines)
    resp = requests.post(
        f"{CCMS_URL}/api/write/",
        headers={"Authorization": f"Bearer {JWT_TOKEN}"},
        data=payload,
        timeout=10,
    )
    resp.raise_for_status()
    log.info("Pushed %d lines to cc-metric-store", len(lines))


def main():
    lines = []
    now = int(time.time())

    for cc_name, flux_query in METRIC_MAP.items():
        try:
            results = query_influxdb(flux_query)
        except Exception as e:
            log.error("Failed to query %s: %s", cc_name, e)
            continue

        for hostname, value in results:
            lines.append(
                f"{cc_name},cluster={CLUSTER_NAME},hostname={hostname},"
                f"type=node value={value} {now}"
            )

    try:
        push_to_ccms(lines)
    except Exception as e:
        log.error("Failed to push to cc-metric-store: %s", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
```

Deploy the same way as the Prometheus script:

```bash
chmod +x /opt/monitoring/influx2ccms/influx2ccms.py

# Run every 60 seconds
* * * * * /opt/monitoring/influx2ccms/influx2ccms.py >> /var/log/influx2ccms.log 2>&1
```

### Alternative: Telegraf HTTP Output

If you already run [Telegraf](https://docs.influxdata.com/telegraf/) and prefer
not to maintain a separate script, Telegraf can POST directly to cc-metric-store
using the `outputs.http` plugin:

```toml
[[outputs.http]]
  url = "http://ccms.example.org:8080/api/write/"
  method = "POST"
  data_format = "influx"
  [outputs.http.headers]
    Authorization = "Bearer eyJ0eXAiOiJKV1QiLC..."

# Rename tags to match CC expectations
[[processors.rename]]
  [[processors.rename.replace]]
    tag = "host"
    dest = "hostname"

# Add required cluster and type tags
[[processors.override]]
  [processors.override.tags]
    cluster = "mycluster"
    type = "node"

# Only forward metrics we care about
[[processors.filter]]
  namepass = ["system", "cpu", "mem", "net"]
```

{{< alert color="warning" title="Caveat" >}}
Telegraf's native tag structure may not match cc-metric-store's expected format
exactly. The `processors.rename` and `processors.override` plugins help, but
metric *names* (measurement + field) still differ from CC conventions. For full
control over the mapping, the Python script approach is more transparent.
{{< /alert >}}

## Deployment as a Systemd Service

For higher reliability than cron (with restart-on-failure and journald logging),
deploy the sync script as a systemd timer or a looping service.

**Systemd service** (`/etc/systemd/system/prom2ccms.service`):

```ini
[Unit]
Description=Prometheus to cc-metric-store Sync
After=network.target

[Service]
Type=oneshot
User=monitoring
ExecStart=/opt/monitoring/prom2ccms/prom2ccms.py
```

**Systemd timer** (`/etc/systemd/system/prom2ccms.timer`):

```ini
[Unit]
Description=Run prom2ccms every 60 seconds

[Timer]
OnBootSec=30s
OnUnitActiveSec=60s
AccuracySec=5s

[Install]
WantedBy=timers.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now prom2ccms.timer

# Check status
systemctl list-timers prom2ccms.timer
journalctl -u prom2ccms.service -f
```

## Testing and Validation

### 1. Test the Write Endpoint Manually

Verify cc-metric-store accepts writes with a simple curl command:

```bash
JWT="eyJ0eXAiOiJKV1QiLC..."

curl -X POST "http://ccms.example.org:8080/api/write/" \
  -H "Authorization: Bearer $JWT" \
  -d "cpu_load,cluster=mycluster,hostname=testnode,type=node value=1.5 $(date +%s)"
```

A `200 OK` response with no body confirms success.

### 2. Query the Data Back

Verify the metric was stored:

```bash
curl -X GET "http://ccms.example.org:8080/api/query/" \
  -H "Authorization: Bearer $JWT" \
  -d '{
    "cluster": "mycluster",
    "from": '"$(($(date +%s) - 300))"',
    "to": '"$(date +%s)"',
    "queries": [{"metric": "cpu_load", "hostname": "testnode"}]
  }'
```

### 3. Check cc-backend

Open the cc-backend web interface and navigate to the node view. Metrics from
external sources should appear alongside natively collected ones.

### 4. Check Logs

Monitor cc-metric-store logs for warnings about unknown or dropped metrics:

```bash
journalctl -u cc-metric-store -f | grep -i "unknown\|drop\|error"
```

## Troubleshooting

| Symptom | Cause | Solution |
|---|---|---|
| Metrics not appearing in cc-backend | Metric name not in cc-metric-store `metrics` config | Add the metric to the `metrics` section and restart cc-metric-store |
| `401 Unauthorized` from `/api/write/` | Invalid or expired JWT token | Regenerate JWT with the correct Ed25519 private key |
| Data gaps or irregular intervals | Cron interval does not match configured `frequency` | Align cron/timer schedule with the `frequency` value in cc-metric-store config |
| Hostname mismatch (no data for known nodes) | Prometheus `instance` label includes port, or InfluxDB uses different host naming | Adjust hostname extraction in the adapter script to match cc-backend's `cluster.json` |
| Wrong values after aggregation | `aggregation` set to `sum` instead of `avg` or vice versa | Check the `aggregation` field in cc-metric-store config matches the metric semantics |
| Script runs but pushes 0 lines | Source TSDB returns empty results | Verify the source query works independently (e.g., test PromQL in Prometheus UI) |

## See Also

- [JWT Token Generation]({{< ref "../how-to-guides/generateJWT" >}})
- [cc-metric-store Configuration]({{< ref "../reference/cc-metric-store/ccms-configuration" >}})
- [cc-metric-store REST API]({{< ref "../reference/cc-metric-store/ccms-rest-api" >}})
- [InfluxDB Line Protocol]({{< ref "../explanation/lineProtocol" >}})
- [Hierarchical Metric Collection]({{< ref "../how-to-guides/hierarchical-collection" >}})
- [Decide on Metric List]({{< ref "../tutorials/prod-metric-list" >}})
- [Cluster Configuration]({{< ref "../how-to-guides/clusterConfig" >}})
- [CC Line Protocol Specification](https://github.com/ClusterCockpit/cc-specifications/blob/master/interfaces/lineprotocol/README.md)
