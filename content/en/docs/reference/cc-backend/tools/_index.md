---
title: Tools
description: >
  Command-line tools for ClusterCockpit maintenance and administration
categories: [cc-backend]
tags: [Backend, Tools]
weight: 10
---

This section documents the command-line tools included with ClusterCockpit for various maintenance, migration, and administrative tasks.

## Available Tools

### Archive Management

- **[archive-manager](archive-manager)**: Comprehensive job archive management, validation, cleaning, and import/export
- **[archive-migration](archive-migration)**: Migrate job archives between schema versions

### Security & Authentication

- **[gen-keypair](gen-keypair)**: Generate Ed25519 keypairs for JWT signing and validation
- **[convert-pem-pubkey](convert-pem-pubkey)**: Convert external Ed25519 PEM keys to ClusterCockpit format

### Diagnostics

- **[grepCCLog.pl](grepcclog)**: Analyze log files to identify non-archived jobs

## Building Tools

All Go-based tools follow the same build pattern:

```bash
cd tools/<tool-name>
go build
```

## Common Features

Most tools support:
- Configurable logging levels (`-loglevel`)
- Timestamped log output (`-logdate`)
- Configuration file specification (`-config`)
