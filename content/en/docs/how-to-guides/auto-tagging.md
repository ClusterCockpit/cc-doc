---
title: How to enable and configure auto-tagging
description: >
  Enable automatic job tagging for application detection and job classification
categories: [cc-backend]
tags: [Admin]
---

## Overview

ClusterCockpit provides automatic job tagging to classify and categorize jobs
based on configurable rules. The tagging system consists of two components:

1. **Application Detection** - Identifies which application a job is running by
   matching patterns in the job script
2. **Job Classification** - Analyzes job performance metrics to identify
   performance issues or characteristics

Tags are automatically applied when jobs start or stop, and can also be applied
retroactively to existing jobs. This feature is disabled by default and must be
explicitly enabled in the configuration.

## Enable auto-tagging

### Step 1: Copy configuration files

The tagging system requires configuration files to define application patterns
and classification rules. Example configurations are provided in the cc-backend
repository at `configs/tagger/`.

From the cc-backend root directory, copy the configuration files to the `var`
directory:

```bash
mkdir -p var/tagger
cp -r configs/tagger/apps var/tagger/
cp -r configs/tagger/jobclasses var/tagger/
```

This copies:

- **Application patterns** (`var/tagger/apps/`) - Text files containing regex
  patterns to match application names in job scripts (16 example applications)
- **Job classification rules** (`var/tagger/jobclasses/`) - JSON files defining
  rules to classify jobs based on metrics (3 example rules)
- **Shared parameters** (`var/tagger/jobclasses/parameters.json`) - Common
  threshold values used across multiple classification rules

### Step 2: Enable in configuration

Add or set the `enable-job-taggers` configuration option in your `config.json`:

```json
{
  "enable-job-taggers": true
}
```

**Important**: Automatic tagging is disabled by default. Setting this to `true`
activates automatic tagging for jobs that start or stop after cc-backend is
restarted.

### Step 3: Restart cc-backend

The tagging system loads configuration from `./var/tagger/` at startup:

```bash
./cc-backend -server
```

### Step 4: Verify configuration loaded

Check the logs for messages indicating successful initialization:

```
[INFO] Setup file watch for ./var/tagger/apps
[INFO] Setup file watch for ./var/tagger/jobclasses
```

These messages confirm the tagging system is active and watching for
configuration changes.

## How auto-tagging works

### Automatic tagging

When `enable-job-taggers` is set to `true`, tags are automatically applied at
two points in the job lifecycle:

- **Job Start** - Application detection runs immediately when a job starts,
  analyzing the job script to identify the application
- **Job Stop** - Job classification runs when a job completes, analyzing metrics
  to identify performance characteristics

**Note**: Only jobs that start or stop after enabling the feature are
automatically tagged. Existing jobs require manual tagging (see below).

### Manual tagging (retroactive)

To apply tags to existing jobs in the database, use the `-apply-tags` command
line option:

```bash
./cc-backend -apply-tags
```

This processes all jobs in the database and applies current tagging rules. This
is useful when:

- You have existing jobs created before tagging was enabled
- You've added new tagging rules and want to apply them to historical data
- You've modified existing rules and want to re-evaluate all jobs

The `-apply-tags` option works independently of the `enable-job-taggers`
configuration setting.

### Hot reload

The tagging system watches configuration directories for changes. You can modify
or add rules without restarting cc-backend:

- Changes to `var/tagger/apps/*` are detected automatically
- Changes to `var/tagger/jobclasses/*` are detected automatically

Simply edit the files and the new rules will be applied to subsequent jobs.

## Application detection

Application detection identifies which software a job is running by matching
patterns in the job script.

### Configuration format

Application patterns are stored in text files under `var/tagger/apps/`. Each
file represents one application, and the filename (without `.txt` extension)
becomes the tag name.

Each file contains one or more regular expression patterns, one per line:

**Example: `var/tagger/apps/vasp.txt`**

```
vasp
VASP
```

**Example: `var/tagger/apps/python.txt`**

```
python
pip
anaconda
conda
```

### How it works

1. When a job starts, the system retrieves the job script from metadata
2. Each line in the app configuration files is treated as a regex pattern
3. Patterns are matched case-insensitively against the lowercased job script
4. If a match is found, a tag of type `app` with the filename as tag name is
   applied
5. Only the first matching application is tagged

### Adding new applications

To add detection for a new application:

1. Create a new file in `var/tagger/apps/` (e.g., `tensorflow.txt`)
2. Add regex patterns, one per line:

   ```
   tensorflow
   tf\.keras
   import tensorflow
   ```

3. The file is automatically detected and loaded (no restart required)

The tag name will be the filename without the `.txt` extension (e.g.,
`tensorflow`).

### Provided application patterns

The example configuration includes patterns for 16 common HPC applications:

- vasp
- python
- gromacs
- lammps
- openfoam
- starccm
- matlab
- julia
- cp2k
- cpmd
- chroma
- flame
- caracal
- turbomole
- orca
- alf

## Job classification

Job classification analyzes completed jobs based on their metrics and properties
to identify performance issues or characteristics.

### Configuration format

Job classification rules are defined in JSON files under
`var/tagger/jobclasses/`. Each rule file contains:

- **Metrics required** - Which job metrics to analyze
- **Requirements** - Pre-conditions that must be met
- **Variables** - Computed values used in the rule
- **Rule expression** - Boolean expression that determines if the rule matches
- **Hint template** - Message displayed when the rule matches

### Shared parameters

The file `var/tagger/jobclasses/parameters.json` defines threshold values used
across multiple rules:

```json
{
  "lowcpuload_threshold_factor": 0.9,
  "excessivecpuload_threshold_factor": 1.1,
  "job_min_duration_seconds": 600.0,
  "sampling_interval_seconds": 30.0
}
```

These parameters can be referenced in rule expressions and make it easy to
maintain consistent thresholds across multiple rules.

### Rule file structure

Each classification rule is a JSON file with the following structure:

**Example: `var/tagger/jobclasses/lowload.json`**

```json
{
  "name": "Low CPU load",
  "tag": "lowload",
  "parameters": ["lowcpuload_threshold_factor", "job_min_duration_seconds"],
  "metrics": ["cpu_load"],
  "requirements": [
    "job.shared == \"none\"",
    "job.duration > job_min_duration_seconds"
  ],
  "variables": [
    {
      "name": "load_threshold",
      "expr": "job.numCores * lowcpuload_threshold_factor"
    }
  ],
  "rule": "cpu_load.avg < cpu_load.limits.caution",
  "hint": "Average CPU load {{.cpu_load.avg}} falls below threshold {{.cpu_load.limits.caution}}"
}
```

#### Field descriptions

| Field          | Description                                                                   |
| -------------- | ----------------------------------------------------------------------------- |
| `name`         | Human-readable description of the rule                                        |
| `tag`          | Tag identifier applied when the rule matches                                  |
| `parameters`   | List of parameter names from `parameters.json` to include in rule environment |
| `metrics`      | List of metrics required for evaluation (must be present in job data)         |
| `requirements` | Boolean expressions that must all be true for the rule to be evaluated        |
| `variables`    | Named expressions computed before evaluating the main rule                    |
| `rule`         | Boolean expression that determines if the job matches this classification     |
| `hint`         | Go template string for generating a user-visible message                      |

### Expression environment

Expressions in `requirements`, `variables`, and `rule` have access to:

**Job properties:**

- `job.shared` - Shared node allocation type
- `job.duration` - Job runtime in seconds
- `job.numCores` - Number of CPU cores
- `job.numNodes` - Number of nodes
- `job.jobState` - Job completion state
- `job.numAcc` - Number of accelerators
- `job.smt` - SMT setting

**Metric statistics** (for each metric in `metrics`):

- `<metric>.min` - Minimum value
- `<metric>.max` - Maximum value
- `<metric>.avg` - Average value
- `<metric>.limits.peak` - Peak limit from cluster config
- `<metric>.limits.normal` - Normal threshold
- `<metric>.limits.caution` - Caution threshold
- `<metric>.limits.alert` - Alert threshold

**Parameters:**

- All parameters listed in the `parameters` field

**Variables:**

- All variables defined in the `variables` array

### Expression language

Rules use the [expr](https://github.com/expr-lang/expr) language for
expressions. Supported operations:

- **Arithmetic**: `+`, `-`, `*`, `/`, `%`, `^`
- **Comparison**: `==`, `!=`, `<`, `<=`, `>`, `>=`
- **Logical**: `&&`, `||`, `!`
- **Functions**: Standard math functions (see expr documentation)

### Hint templates

Hints use Go's `text/template` syntax. Variables from the evaluation environment
are accessible:

```
{{.cpu_load.avg}}     # Access metric average
{{.job.duration}}     # Access job property
{{.load_threshold}}   # Access computed variable
```

### Adding new classification rules

To add a new classification rule:

1. Create a new JSON file in `var/tagger/jobclasses/` (e.g.,
   `memoryLeak.json`)
2. Define the rule structure following the format above
3. Add any new parameters to `parameters.json` if needed
4. The file is automatically detected and loaded (no restart required)

**Example: Detecting memory leaks**

```json
{
  "name": "Memory Leak Detection",
  "tag": "memory_leak",
  "parameters": ["memory_leak_slope_threshold"],
  "metrics": ["mem_used"],
  "requirements": ["job.duration > 3600"],
  "variables": [
    {
      "name": "mem_growth",
      "expr": "(mem_used.max - mem_used.min) / job.duration"
    }
  ],
  "rule": "mem_growth > memory_leak_slope_threshold",
  "hint": "Memory usage grew by {{.mem_growth}} bytes per second"
}
```

Don't forget to add `memory_leak_slope_threshold` to `parameters.json`.

### Provided classification rules

The example configuration includes 3 classification rules:

- **lowload** - Detects jobs with low CPU load (avg CPU load below caution
  threshold)
- **excessiveload** - Detects jobs with excessive CPU load (avg CPU load above
  peak × threshold factor)
- **lowutilization** - Detects jobs with low resource utilization (flop rate
  below alert threshold)

## Troubleshooting

### Tags not applied

1. **Check tagging is enabled**: Verify `enable-job-taggers: true` is set in
   `config.json`

2. **Check configuration exists**:

   ```bash
   ls -la var/tagger/apps
   ls -la var/tagger/jobclasses
   ```

3. **Check logs for errors**:

   ```bash
   ./cc-backend -server -loglevel debug
   ```

4. **Verify file permissions**: Ensure cc-backend can read the configuration
   files

5. **For existing jobs**: Use `./cc-backend -apply-tags` to retroactively tag
   jobs

### Rules not matching

1. **Enable debug logging**: Set log level to debug to see detailed rule
   evaluation:

   ```bash
   ./cc-backend -server -loglevel debug
   ```

2. **Check requirements**: Ensure all requirements in the rule are satisfied
3. **Verify metrics exist**: Classification rules require job metrics to be
   available in the job data
4. **Check metric names**: Ensure metric names in rules match those in your
   cluster configuration

### File watch not working

If changes to configuration files aren't detected automatically:

1. Restart cc-backend to reload all configuration
2. Check filesystem supports file watching (some network filesystems may not
   support inotify)
3. Check logs for file watch setup messages

## Best practices

1. **Start simple**: Begin with basic rules and refine based on results
2. **Use requirements**: Filter out irrelevant jobs early with requirements to
   avoid unnecessary metric processing
3. **Test incrementally**: Add one rule at a time and verify behavior before
   adding more
4. **Document rules**: Use descriptive names and clear hint messages
5. **Share parameters**: Define common thresholds in `parameters.json` for
   consistency
6. **Version control**: Keep your `var/tagger/` configuration in version control
   to track changes
7. **Backup before changes**: Test new rules on a development instance before
   deploying to production

## Tag types and usage

The tagging system creates two types of tags:

- **`app`** - Application tags (e.g., "vasp", "gromacs", "python")
- **`jobClass`** - Classification tags (e.g., "lowload", "excessiveload",
  "lowutilization")

Tags can be:

- Queried and filtered in the ClusterCockpit UI
- Used in API queries to find jobs with specific characteristics
- Referenced in reports and analytics

Tags are stored in the database and appear in the job details view, making it
easy to identify application usage and performance patterns across your cluster.
