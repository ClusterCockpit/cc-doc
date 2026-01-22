---
title: Installation
description: Installing and building cc-slurm-adapter
categories: [cc-slurm-adapter]
tags: [Adapter, Installation]
weight: 1
---

## Prerequisites

- Go 1.24.0 or higher
- Slurm with slurmdbd configured
- cc-backend instance with API access
- Access to the slurmctld node

## Building from Source

### Requirements

```
go 1.24.0+
```

### Dependencies

Key dependencies (managed via `go.mod`):

- `github.com/ClusterCockpit/cc-lib` - ClusterCockpit common library
- `github.com/nats-io/nats.go` - NATS client

### Compilation

```bash
make
```

This creates the `cc-slurm-adapter` binary.

### Build Commands

```bash
# Build binary
make

# Format code
make format

# Clean build artifacts
make clean
```
