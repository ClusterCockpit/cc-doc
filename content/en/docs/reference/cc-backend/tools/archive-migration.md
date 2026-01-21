---
title: archive-migration
description: >
  Job Archive Schema Migration Tool
categories: [cc-backend]
tags: [Backend, Tools]
weight: 2
---

The `archive-migration` tool migrates job archives from old schema versions to the current schema version. It handles schema changes such as the `exclusive` → `shared` field transformation and adds/removes fields as needed.

## Features

- **Parallel Processing**: Uses worker pool for fast migration
- **Dry-Run Mode**: Preview changes without modifying files
- **Safe Transformations**: Applies well-defined schema transformations
- **Progress Reporting**: Shows real-time migration progress
- **Error Handling**: Continues on individual failures, reports at end

## Build

```bash
cd tools/archive-migration
go build
```

## Command-Line Options

---

```txt
-archive <path>
```

_Function:_ Path to job archive to migrate (required).

_Example:_ `-archive /data/job-archive`

---

```txt
-dry-run
```

_Function:_ Preview changes without modifying files.

---

```txt
-workers <n>
```

_Function:_ Number of parallel workers.

_Default:_ `4`

_Example:_ `-workers 8`

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

_Function:_ Add date and time to log messages.

## Schema Transformations

### Exclusive → Shared

Converts the old `exclusive` integer field to the new `shared` string field:

- `0` → `"multi_user"`
- `1` → `"none"`
- `2` → `"single_user"`

### Missing Fields

Adds fields required by current schema:

- `submitTime`: Defaults to `startTime` if missing
- `energy`: Defaults to `0.0`
- `requestedMemory`: Defaults to `0`
- `shared`: Defaults to `"none"` if still missing after transformation

### Deprecated Fields

Removes fields no longer in schema:

- `mem_used_max`, `flops_any_avg`, `mem_bw_avg`
- `load_avg`, `net_bw_avg`, `net_data_vol_total`
- `file_bw_avg`, `file_data_vol_total`

## Usage Examples

### Preview Changes (Dry Run)

```bash
./archive-migration --archive /data/job-archive --dry-run
```

### Migrate Archive

```bash
# IMPORTANT: Backup your archive first!
cp -r /data/job-archive /data/job-archive-backup

# Run migration
./archive-migration --archive /data/job-archive
```

### Migrate with Verbose Logging

```bash
./archive-migration --archive /data/job-archive --loglevel debug
```

### Migrate with More Workers

```bash
./archive-migration --archive /data/job-archive --workers 8
```

## Safety

{{< alert color="warning">}}**Always backup your archive before running migration!**{{< /alert >}}

The tool modifies `meta.json` files in place. While transformations are designed to be safe, unexpected issues could occur. Follow these safety practices:

1. **Always run with `--dry-run` first** to preview changes
2. **Backup your archive** before migration
3. **Test on a copy** of your archive first
4. **Verify results** after migration

## Verification

After migration, verify the archive:

```bash
# Use archive-manager to check the archive
cd ../archive-manager
./archive-manager -s /data/migrated-archive

# Or validate specific jobs
./archive-manager -s /data/migrated-archive --validate
```

## Troubleshooting

### Migration Failures

If individual jobs fail to migrate:

- Check the error messages for specific files
- Examine the failing `meta.json` files manually
- Fix invalid JSON or unexpected field types
- Re-run migration (already-migrated jobs will be processed again)

### Performance

For large archives:

- Increase `--workers` for more parallelism
- Use `--loglevel warn` to reduce log output
- Monitor disk I/O if migration is slow

## Technical Details

The migration process:

1. Walks archive directory recursively
2. Finds all `meta.json` files
3. Distributes jobs to worker pool
4. For each job:
   - Reads JSON file
   - Applies transformations in order
   - Writes back migrated data (if not dry-run)
5. Reports statistics and errors

Transformations are idempotent - running migration multiple times is safe (though not recommended for performance).
