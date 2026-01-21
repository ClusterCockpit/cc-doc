---
title: archive-manager
description: >
  Job Archive Management Tool
categories: [cc-backend]
tags: [Backend, Tools]
weight: 1
---

The `archive-manager` tool provides comprehensive management and maintenance capabilities for ClusterCockpit job archives. It supports validation, cleaning, importing between different archive backends, and general archive operations.

## Build

```bash
cd tools/archive-manager
go build
```

## Command-Line Options

---

```txt
-s <path>
```

_Function:_ Specify the source job archive path.

_Default:_ `./var/job-archive`

_Example:_ `-s /data/job-archive`

---

```txt
-config <path>
```

_Function:_ Specify alternative path to `config.json`.

_Default:_ `./config.json`

_Example:_ `-config /etc/clustercockpit/config.json`

---

```txt
-validate
```

_Function:_ Validate a job archive against the JSON schema.

---

```txt
-remove-cluster <cluster>
```

_Function:_ Remove specified cluster from archive and database.

_Example:_ `-remove-cluster oldcluster`

---

```txt
-remove-before <date>
```

_Function:_ Remove all jobs with start time before the specified date.

_Format:_ `2006-Jan-04`

_Example:_ `-remove-before 2023-Jan-01`

---

```txt
-remove-after <date>
```

_Function:_ Remove all jobs with start time after the specified date.

_Format:_ `2006-Jan-04`

_Example:_ `-remove-after 2024-Dec-31`

---

```txt
-import
```

_Function:_ Import jobs from source archive to destination archive.

_Note:_ Requires `-src-config` and `-dst-config` options.

---

```txt
-src-config <json>
```

_Function:_ Source archive backend configuration in JSON format.

_Example:_ `-src-config '{"kind":"file","path":"./archive"}'`

---

```txt
-dst-config <json>
```

_Function:_ Destination archive backend configuration in JSON format.

_Example:_ `-dst-config '{"kind":"sqlite","dbPath":"./archive.db"}'`

---

```txt
-loglevel <level>
```

_Function:_ Sets the logging level.

_Arguments:_ `debug | info | warn | err | fatal | crit`

_Default:_ `info`

_Example:_ `-loglevel debug`

---

```txt
-logdate
```

_Function:_ Set this flag to add date and time to log messages.

## Usage Examples

### Validate Archive

```bash
./archive-manager -s /data/job-archive -validate
```

### Clean Old Jobs

```bash
# Remove jobs older than January 1, 2023
./archive-manager -s /data/job-archive -remove-before 2023-Jan-01
```

### Import Between Archives

```bash
# Import from file-based archive to SQLite archive
./archive-manager -import \
  -src-config '{"kind":"file","path":"./old-archive"}' \
  -dst-config '{"kind":"sqlite","dbPath":"./new-archive.db"}'
```

### Archive Information

```bash
# Display archive statistics
./archive-manager -s /data/job-archive
```

## Features

- **Validation**: Verify job archive integrity against JSON schemas
- **Cleaning**: Remove jobs by date range or cluster
- **Import/Export**: Transfer jobs between different archive backend types
- **Statistics**: Display archive information and job counts
- **Progress Tracking**: Real-time progress reporting for long operations
