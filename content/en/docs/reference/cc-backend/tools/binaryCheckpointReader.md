---
title: binaryCheckpointReader
description: >
  Metricstore Checkpoint Inspection Tool
categories: [cc-backend]
tags: [Backend, Tools]
weight: 5
---

{{< alert >}}
`binaryCheckpointReader` is part of the `cc-backend` repository and can be used to debug the content of binary checkpoint files.
{{< /alert >}}

The `binaryCheckpointReader` tool reads `.wal` or `.bin` checkpoint files produced
by the metricstore WAL/snapshot system and dumps their contents to a
human-readable `.txt` file. It is useful for debugging and inspecting checkpoint data.

## Build and Run

The tool is run directly with `go run` — no separate build step is needed:

```bash
go run ./tools/binaryCheckpointReader <file.wal|file.bin>
```

## Usage

```txt
go run ./tools/binaryCheckpointReader <file.wal|file.bin>
```

The tool accepts exactly one argument: the path to a `.wal` or `.bin` checkpoint file.

Output is written to a file with the same name as the input but with a `.txt`
extension. For example, `current.wal` produces `current.txt` in the same directory.

## Supported File Types

- **`.wal`** — Write-Ahead Log files produced by the binary WAL checkpoint writer.
  Each record contains a timestamp, metric name, selectors, and a float32 value.
- **`.bin`** — Binary snapshot files produced by the snapshot checkpoint system.
  These contain hierarchical metric data organized by scope level (node, socket, etc.).

## Output Format

### WAL files

```txt
=== WAL File Dump ===
File:        /path/to/current.wal
File Magic:  0xCC1DA701 (valid)

--- Record #1 ---
  Timestamp:   1700000000 (2023-11-14T22:13:20Z)
  Metric:      cpu_load
  Selectors:   [node01, cpu0]
  Value:       0.75

=== Total valid records: 42 ===
```

### Binary snapshot files

```txt
=== Binary Snapshot Dump ===
File:    /path/to/snapshot.bin
Magic:   0xCC5B0001 (valid)
From:    1700000000 (2023-11-14T22:13:20Z)
To:      1700003600 (2023-11-14T23:13:20Z)

Metrics (2):
  [cpu_load]
    Frequency:  60 s
    Start:      1700000000 (2023-11-14T22:13:20Z)
    Values (60):
      [22:13:20] 0.75 0.8 0.72 ...
```

## Checkpoint File Locations

By default, checkpoint files are stored under `./var/checkpoints/` organized by
cluster and host:

```
var/checkpoints/
└── <cluster>/
    └── <hostname>/
        ├── current.wal   (active WAL log)
        └── <timestamp>.bin  (periodic snapshots)
```

The checkpoint directory can be configured via the `checkpoints.directory` option
in the `metric-store` section of `config.json`.
