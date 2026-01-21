---
title: grepCCLog.pl
description: >
  Analyze ClusterCockpit Log Files for Running Jobs
categories: [cc-backend]
tags: [Backend, Tools]
weight: 5
---

The `grepCCLog.pl` script analyzes ClusterCockpit log files to identify jobs that were started but not yet archived on a specific day. This is useful for troubleshooting and monitoring job lifecycle.

## Purpose

Parses ClusterCockpit log files to:
- Identify jobs that started on a specific day
- Detect jobs that have not been archived
- Generate statistics per user
- Report jobs that may be stuck or still running

## Usage

```bash
./grepCCLog.pl <logfile> <day>
```

### Arguments

```txt
<logfile>
```

_Function:_ Path to ClusterCockpit log file

_Example:_ `/var/log/clustercockpit/cc-backend.log`

---

```txt
<day>
```

_Function:_ Day of month to analyze (numeric)

_Example:_ `15` (for October 15th)

## Output

The script produces:

1. **List of Non-Archived Jobs**: Details for each job that started but hasn't been archived
2. **Per-User Summary**: Count of non-archived jobs per user
3. **Total Statistics**: Overall count of started vs. non-archived jobs

### Example Output

```txt
======
jobID:  12345 User:  alice
======
======
jobID:  12346 User:  bob
======
alice => 1
bob => 1
Not stopped: 2 of 10
```

## Log Format Requirements

The script expects log entries in the following format:

### Job Start Entry

```txt
Oct 15 ... new job (id: 123): cluster=woody, jobId=12345, user=alice, ...
```

### Job Archive Entry

```txt
Oct 15 ... archiving job... (dbid: 123): cluster=woody, jobId=12345, user=alice, ...
```

## Limitations

- Hard-coded for cluster name `woody`
- Hard-coded for month `Oct`
- Requires specific log message format
- Day must match exactly

## Customization

To adapt for your environment, modify the script:

```perl
# Line 19: Change cluster name
if ( $cluster eq 'your-cluster-name' && $day eq $Tday  ) {

# Line 35: Change cluster name for archive matching
if ( $cluster eq 'your-cluster-name' ) {

# Lines 12 & 28: Update month pattern
if ( /Oct ([0-9]+) .../ ) {
# Change 'Oct' to your desired month
```

## Use Cases

- **Debugging**: Identify jobs that failed to archive properly
- **Monitoring**: Track running jobs for a specific day
- **Troubleshooting**: Find stuck jobs in the system
- **Auditing**: Verify job lifecycle completion

## Example Workflow

```bash
# Analyze today's jobs (e.g., October 15)
./grepCCLog.pl /var/log/cc-backend.log 15

# Find jobs started on the 20th
./grepCCLog.pl /var/log/cc-backend.log 20

# Check specific log file
./grepCCLog.pl /path/to/old-logs/cc-backend-2024-10.log 15
```

## Technical Details

The script:
1. Opens specified log file
2. Parses log entries with regex patterns
3. Tracks started jobs in hash table
4. Tracks archived jobs in separate hash table
5. Compares to find jobs without archive entry
6. Aggregates statistics per user
7. Outputs results

Jobs are matched by database ID (`id:` field) between start and archive entries.
