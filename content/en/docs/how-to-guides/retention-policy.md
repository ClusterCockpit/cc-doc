---
title: Configure retention policies
linkTitle: Retention policies
weight: 6
description: Managing database and job archive size with retention policies
---

## Overview

Over time, the ClusterCockpit database and job archive can grow significantly,
especially in production environments with high job counts. Retention policies
help keep your storage at a manageable size by automatically removing or
archiving old jobs.

## Why use retention policies?

Without retention policies:

- The SQLite database file can grow to tens of gigabytes
- The job archive can reach terabytes in size
- Storage requirements increase indefinitely
- System performance may degrade

A typical multi-cluster setup over 5 years can accumulate:

- **75 GB** for the SQLite database
- **1.4 TB** for the job archive

Retention policies allow you to balance data retention needs with storage capacity.

## Retention policy options

ClusterCockpit supports three retention policies:

### None (default)

No automatic cleanup. Jobs are kept indefinitely.

```json
{
  "archive": {
    "kind": "file",
    "path": "./var/job-archive"
  }
}
```

### Delete

Permanently removes jobs older than the specified age from both the job archive
and the database.

**Use when:**

- Storage space is limited
- You don't need long-term job data
- You have external backups or data exports

**Configuration example:**

```json
{
  "archive": {
    "kind": "file",
    "path": "./var/job-archive",
    "retention": {
      "policy": "delete",
      "age": 365,
      "includeDB": true
    }
  }
}
```

This configuration will:

- Delete jobs older than 365 days
- Remove them from both the job archive and database
- Run automatically based on the cleanup interval

### Move

Moves old jobs to a separate location for long-term archival while removing them
from the active database.

**Use when:**

- You need to preserve historical data
- You want to reduce active database size
- You can store archived data on cheaper, slower storage

**Configuration example:**

```json
{
  "archive": {
    "kind": "file",
    "path": "./var/job-archive",
    "retention": {
      "policy": "move",
      "age": 365,
      "location": "/mnt/archive/old-jobs",
      "includeDB": true
    }
  }
}
```

This configuration will:

- Move jobs older than 365 days to `/mnt/archive/old-jobs`
- Remove them from the active database
- Preserve the data for potential future analysis

## Configuration parameters

### `archive.retention` section

| Parameter   | Type    | Required   | Default | Description                                              |
| ----------- | ------- | ---------- | ------- | -------------------------------------------------------- |
| `policy`    | string  | Yes        | -       | Retention policy: `none`, `delete`, or `move`            |
| `age`       | integer | No         | 7       | Age threshold in days. Jobs older than this are affected |
| `includeDB` | boolean | No         | true    | Also remove jobs from the database (not just archive)    |
| `location`  | string  | For `move` | -       | Target directory for moved jobs (only for `move` policy) |

## Complete configuration examples

### Example 1: One-year retention with deletion

Suitable for environments with limited storage:

```json
{
  "archive": {
    "kind": "file",
    "path": "./var/job-archive",
    "retention": {
      "policy": "delete",
      "age": 365,
      "includeDB": true
    }
  }
}
```

### Example 2: Two-tier archival system

Keep 6 months active, move older data to long-term storage:

```json
{
  "archive": {
    "kind": "file",
    "path": "./var/job-archive",
    "retention": {
      "policy": "move",
      "age": 180,
      "location": "/mnt/slow-storage/archive",
      "includeDB": true
    }
  }
}
```

### Example 3: S3 backend with retention

Using S3 object storage with one-year retention:

```json
{
  "archive": {
    "kind": "s3",
    "endpoint": "https://s3.example.com",
    "bucket": "clustercockpit-jobs",
    "access-key": "your-access-key",
    "secret-key": "your-secret-key",
    "retention": {
      "policy": "delete",
      "age": 365,
      "includeDB": true
    }
  }
}
```

## How retention policies work

1. **Automatic execution**: Retention policies run automatically based on the configured interval
2. **Age calculation**: Jobs are evaluated based on their `startTime` field
3. **Batch processing**: All jobs older than the specified age are processed in one operation
4. **Database cleanup**: When `includeDB: true`, corresponding database entries are removed
5. **Archive handling**: Based on policy (`delete` removes, `move` relocates)

## Best practices

### Planning retention periods

Consider these factors when setting the `age` parameter:

- **Accounting requirements**: Some organizations require job data for billing/auditing
- **Research needs**: Longer retention for research clusters where users may need historical data
- **Storage capacity**: Available disk space and growth rate
- **Compliance**: Legal or institutional data retention policies

**Recommended retention periods:**

| Use Case                     | Suggested Age                  |
| ---------------------------- | ------------------------------ |
| Development/testing          | 30-90 days                     |
| Production (limited storage) | 180-365 days                   |
| Production (ample storage)   | 365-730 days                   |
| Research/archival            | 730+ days or use `move` policy |

### Storage considerations

#### For `move` policy

- Mount the target `location` on slower, cheaper storage (e.g., spinning disks, network storage)
- Ensure sufficient space at the target location
- Consider periodic backups of the moved archive
- Document the archive structure for future retrieval

#### For `delete` policy

- **Create backups first**: Always backup your database and job archive before enabling deletion
- **Test on a copy**: Verify the retention policy works as expected on test data
- **Export important data**: Consider exporting summary statistics or critical job data before deletion

### Monitoring and maintenance

1. **Track archive size**: Monitor growth to adjust retention periods

   ```bash
   du -sh /var/job-archive
   du -sh /path/to/database.db
   ```

2. **Verify retention execution**: Check logs for retention policy runs

   ```bash
   grep -i retention /var/log/cc-backend.log
   ```

3. **Regular backups**: Backup before changing retention settings

   ```bash
   cp -r /var/job-archive /backup/job-archive-$(date +%Y%m%d)
   cp /var/clustercockpit.db /backup/clustercockpit-$(date +%Y%m%d).db
   ```

## Restoring deleted jobs

### If using `move` policy

Jobs moved to the retention location can be restored:

1. Stop `cc-backend`
2. Use the `archive-manager` tool to import jobs back:

   ```bash
   cd tools/archive-manager
   go build
   ./archive-manager -import \
     -src-config '{"kind":"file","path":"/mnt/archive/old-jobs"}' \
     -dst-config '{"kind":"file","path":"./var/job-archive"}'
   ```

3. Rebuild database from archive:

   ```bash
   ./cc-backend -init-db
   ```

4. Restart `cc-backend`

### If using `delete` policy

**Jobs cannot be restored** unless you have external backups. This is why backups are critical before enabling deletion.

## Related tools

- **[archive-manager](/docs/reference/cc-backend/tools/archive-manager/)**: Manage and validate job archives
- **[archive-migration](/docs/reference/cc-backend/tools/archive-migration/)**: Migrate archives between schema versions
- **Database migration**: See [database migration guide](/docs/how-to-guides/database-migration/)

## Troubleshooting

### Retention policy not running

**Check:**

1. Verify `archive.retention` is properly configured in `config.json`
2. Ensure `cc-backend` was restarted after configuration changes
3. Check logs for errors: `grep -i retention /var/log/cc-backend.log`

### Database size not decreasing

**Possible causes:**

- `includeDB: false` - Database entries are not being removed
- SQLite doesn't automatically reclaim space - run `VACUUM`:

  ```bash
  sqlite3 /var/clustercockpit.db "VACUUM;"
  ```

### Jobs not being moved to target location

**Check:**

1. Target directory exists and is writable
2. Sufficient disk space at target location
3. File permissions allow `cc-backend` to write to `location`
4. Path in `location` is absolute, not relative

### Performance impact

If retention policy execution causes performance issues:

- Consider running during off-peak hours (feature may require manual execution)
- Reduce the number of old jobs by running retention more frequently with shorter age periods
- Use more powerful hardware for the database operations

## See also

- [Job Archive Reference](/docs/reference/cc-backend/jobarchive/)
- [Configuration Reference](/docs/reference/cc-backend/ccb-configuration/)
- [Production Deployment Guide](/docs/tutorials/prod-intro/)
