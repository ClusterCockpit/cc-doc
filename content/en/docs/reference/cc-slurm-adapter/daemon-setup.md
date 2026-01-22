---
title: Daemon Setup
description: Setting up cc-slurm-adapter as a daemon
categories: [cc-slurm-adapter]
tags: [Adapter, Setup]
weight: 3
---

The daemon mode is **required** for cc-slurm-adapter to function. This page describes how to set up the daemon using systemd.

## 1. Copy Binary and Configuration

Copy the binary and create a configuration file:

```bash
sudo mkdir -p /opt/cc-slurm-adapter
sudo cp cc-slurm-adapter /opt/cc-slurm-adapter/
sudo cp config.json /opt/cc-slurm-adapter/
```

**Security**: The config file contains sensitive credentials (JWT, NATS). Set appropriate permissions:

```bash
sudo chmod 600 /opt/cc-slurm-adapter/config.json
```

## 2. Create System User

```bash
sudo useradd -r -s /bin/false cc-slurm-adapter
sudo chown -R cc-slurm-adapter:slurm /opt/cc-slurm-adapter
```

## 3. Grant Slurm Permissions

The adapter user needs permission to query Slurm:

```bash
sacctmgr add user cc-slurm-adapter Account=root AdminLevel=operator
```

**Critical**: If permissions are not set and Slurm is restricted, **NO JOBS WILL BE REPORTED**.

## 4. Install systemd Service

Create `/etc/systemd/system/cc-slurm-adapter.service`:

```ini
[Unit]
Description=cc-slurm-adapter
Wants=network.target
After=network.target

[Service]
User=cc-slurm-adapter
Group=slurm
ExecStart=/opt/cc-slurm-adapter/cc-slurm-adapter -daemon -config /opt/cc-slurm-adapter/config.json
WorkingDirectory=/opt/cc-slurm-adapter/
RuntimeDirectory=cc-slurm-adapter
RuntimeDirectoryMode=0750
Restart=on-failure
RestartSec=15s

[Install]
WantedBy=multi-user.target
```

**Notes**:

- `RuntimeDirectory` creates `/run/cc-slurm-adapter` for PID and socket files
- `Group=slurm` allows Prolog/Epilog (running as slurm user) to access the socket
- `RuntimeDirectoryMode=0750` enables group access

## 5. Enable and Start Service

```bash
sudo systemctl daemon-reload
sudo systemctl enable cc-slurm-adapter
sudo systemctl start cc-slurm-adapter
```

## Verification

Check that the service is running:

```bash
sudo systemctl status cc-slurm-adapter
```

You should see output indicating the service is active and running.
