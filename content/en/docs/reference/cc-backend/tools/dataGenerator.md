---
title: "Metric Generator Script"
draft: false
weight: 5
summary: "Documentation for the HPC metric load generator, covering REST/NATS transport modes and Internal/External modes."
tags: ["API", "NATS", "Backend", "Tools"]
categories: [cc-backend]
---

## Overview

The Metric Generator is a bash script designed to simulate high-frequency metric data for the `alex` and `fritz` clusters. It is primarily used for  testing the connection to cc-metric-store and put dummy data into it. This can either be your separately hoster cc-metric-store (which is what we call external mode) or your integrated cc-metric-store into cc-backend (which is what we call internal cc-metric-store).

The script supports two transport mechanisms:
1.  **REST API** (via `curl`)
2.  **NATS Messaging** (via `nats-cli`)

It also supports two deployment scopes to handle different URL structures and authentication methods:
1.  **Internal** (Integrated cc-metric-store into cc-backend)
2.  **External** (Self-hosted separate cc-metric-store)

---

## Configuration

The script behavior is controlled by variables defined at the top of the file. 

### Main Operation Flags

| Variable           | Options                     | Description                                                                                                    |
| :----------------- | :-------------------------- | :------------------------------------------------------------------------------------------------------------- |
| `TRANSPORT_MODE`   | `"REST"` / `"NATS"`         | **REST**: Sends HTTP POST requests.<br>**NATS**: Publishes to a NATS subject.                                  |
| `CONNECTION_SCOPE` | `"INTERNAL"` / `"EXTERNAL"` | **INTERNAL**: To use integrated cc-metric-store.<br>**EXTERNAL**: To use self-hosted separate cc-metric-store. |
| `API_USER`         | String (e.g., `"demo"`)     | The username used to generate the JWT when in **INTERNAL** mode.                                               |

### Network Settings

| Variable          | Description                                                  | Required Mode |
| :---------------- | :----------------------------------------------------------- | :------------ |
| `SERVICE_ADDRESS` | Base URL of the API (e.g., `http://localhost:8080`).         | **REST**      |
| `NATS_SERVER`     | NATS connection string (e.g., `nats://0.0.0.0:4222`).        | **NATS**      |
| `NATS_SUBJECT`    | The subject topic to publish messages to (e.g., `hpc-nats`). | **NATS**      |
| `JWT_STATIC`      | A hardcoded Bearer token used for authentication.            | **EXTERNAL**  |

---

## Logic & Behavior

### Connection Scopes (REST Mode)

The script automatically adjusts the target URL and Authentication method based on the `CONNECTION_SCOPE`.

| Feature            | Scope: `INTERNAL`                                     | Scope: `EXTERNAL`                      |
| :----------------- | :---------------------------------------------------- | :------------------------------------- |
| **Target URL**     | `{SERVICE_ADDRESS}/metricstore/api/write`             | `{SERVICE_ADDRESS}/api/write`          |
| **Authentication** | **Dynamic**: Executes `./cc-backend -jwt "$API_USER"` | **Static**: Uses `JWT_STATIC` variable |

### Transport Modes

* **REST**: The script writes a batch of metrics to a temporary file and uses `curl` to POST the file binary to the configured URL.
* **NATS**: The script writes a batch of metrics to a temporary file and pipes (`|`) the content directly to the `nats pub` command.

---

## Data Specifications

The script generates InfluxDB/Line Protocol formatted text. It iterates through varying hardware hierarchies for two clusters: **Alex** and **Fritz**.

### 1. Metric Dimensions (Tags)
Every data point includes the following tags:
* `cluster`: `alex` or `fritz`
* `hostname`: A random host from the predefined host lists.
* `type`: The hardware level (see below).
* `type-id`: The specific index or ID of the hardware component.

### 2. Hierarchy Levels

| Hierarchy Type | ID Format   | Count                         | Notes                 |
| :------------- | :---------- | :---------------------------- | :-------------------- |
| `hwthread`     | Integer     | 0..127 (Alex) / 0..71 (Fritz) | Highest volume metric |
| `accelerator`  | PCI Address | 8 per node                    | Alex Only             |
| `memoryDomain` | Integer     | 0..7                          | Alex Only             |
| `socket`       | Integer     | 0..1                          | All Clusters          |
| `node`         | N/A         | 1 per host                    | All Clusters          |

### 3. Metric Fields

**Standard Metrics** (hwthread, socket, accelerator, memoryDomain):
> `cpu_load`, `cpu_user`, `flops_any`, `cpu_irq`, `cpu_system`, `ipc`, `cpu_idle`, `cpu_iowait`, `core_power`, `clock`

**Node Metrics** (node):
> `cpu_irq`, `cpu_load`, `mem_cached`, `net_bytes_in`, `cpu_user`, `cpu_idle`, `nfs4_read`, `mem_used`, `nfs4_write`, `nfs4_total`, `ib_xmit`, `ib_xmit_pkts`, `net_bytes_out`, `cpu_iowait`, `ib_recv`, `cpu_system`, `ib_recv_pkts`

---

## Usage Examples

### 1. Run for Internal CCMS
Set the variables inside the script:
```bash
TRANSPORT_MODE="REST"
CONNECTION_SCOPE="INTERNAL"
```

**Effect:** Generates a new token using `cc-backend` and posts to `/metricstore/api/write`.

### 2. Run for External CCMS
Set the variables inside the script:

```bash
TRANSPORT_MODE="REST"
CONNECTION_SCOPE="EXTERNAL"
```

**Effect:** Uses the static JWT and posts to `/api/write`.

### 3. Run as NATS Publisher
Set the variables inside the script:

```bash
TRANSPORT_MODE="NATS"
```

**Effect:** Pipes data directly to the NATS server on `hpc-nats`.