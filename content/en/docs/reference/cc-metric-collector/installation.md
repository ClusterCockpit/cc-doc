---
title: Installation
description: Building and installing cc-metric-collector
categories: [cc-metric-collector]
tags: [Collector, Installation]
weight: 3
---

## Building from Source

### Prerequisites

- Go 1.16 or higher
- Git
- Make
- Standard build tools (gcc, etc.)

### Basic Build

In most cases, a simple `make` in the main folder is enough to get a `cc-metric-collector` binary:

```bash
git clone https://github.com/ClusterCockpit/cc-metric-collector.git
cd cc-metric-collector
make
```

The build process automatically:
- Downloads dependencies via `go get`
- Checks for LIKWID library (for LIKWID collector)
- Downloads and builds LIKWID as a static library if not found
- Copies required header files for cgo bindings

### Build Output

After successful build, you'll have:
- `cc-metric-collector` binary in the project root
- LIKWID library and headers (if LIKWID collector was built)

## System Integration

### Configuration Files

Create a directory for configuration files:

```bash
sudo mkdir -p /etc/cc-metric-collector
sudo cp example-configs/*.json /etc/cc-metric-collector/
```

Edit the configuration files according to your needs. See [Configuration](../configuration/) for details.

### User and Group Setup

It's recommended to run cc-metric-collector as a dedicated user:

```bash
sudo useradd -r -s /bin/false cc-metric-collector
sudo mkdir -p /var/log/cc-metric-collector
sudo chown cc-metric-collector:cc-metric-collector /var/log/cc-metric-collector
```

### Pre-configuration

The main configuration settings for system integration are pre-defined in `scripts/cc-metric-collector.config`. This file contains:
- UNIX user and group for execution
- PID file location
- Other system settings

Adjust and install it:

```bash
# Edit the configuration
editor scripts/cc-metric-collector.config

# Install to system location
sudo install --mode 644 \
             --owner root \
             --group root \
             scripts/cc-metric-collector.config /etc/default/cc-metric-collector
```

### Systemd Integration

If you are using `systemd` as your init system:

```bash
# Install the systemd service file
sudo install --mode 644 \
             --owner root \
             --group root \
             scripts/cc-metric-collector.service /etc/systemd/system/cc-metric-collector.service

# Reload systemd daemon
sudo systemctl daemon-reload

# Enable the service to start on boot
sudo systemctl enable cc-metric-collector

# Start the service
sudo systemctl start cc-metric-collector

# Check status
sudo systemctl status cc-metric-collector
```

### SysVinit Integration

If you are using an init system based on `/etc/init.d` daemons:

```bash
# Install the init script
sudo install --mode 755 \
             --owner root \
             --group root \
             scripts/cc-metric-collector.init /etc/init.d/cc-metric-collector

# Enable the service
sudo update-rc.d cc-metric-collector defaults

# Start the service
sudo /etc/init.d/cc-metric-collector start
```

The init script reads basic configuration from `/etc/default/cc-metric-collector`.

## Package Installation

### RPM Packages

To build RPM packages:

```bash
make RPM
```

Requirements:
- RPM tools (`rpm` and `rpmspec`)
- Git

The command uses the RPM SPEC file `scripts/cc-metric-collector.spec` and creates packages in the project directory.

Install the generated RPM:

```bash
sudo rpm -ivh cc-metric-collector-*.rpm
```

### DEB Packages

To build Debian packages:

```bash
make DEB
```

Requirements:
- `dpkg-deb`
- `awk`, `sed`
- Git

The command uses the DEB control file `scripts/cc-metric-collector.control` and creates a binary deb package.

Install the generated DEB:

```bash
sudo dpkg -i cc-metric-collector_*.deb
```

**Note**: DEB package creation is experimental and not as well tested as RPM packages.

### Customizing Packages

To customize RPM or DEB packages for your local system:

1. Fork the [cc-metric-collector repository](https://github.com/ClusterCockpit/cc-metric-collector)
2. Enable GitHub Actions in your fork
3. Make changes to scripts, code, etc.
4. Commit and push your changes
5. Tag the commit: `git tag v0.x.y-myversion`
6. Push tags: `git push --tags`
7. Wait for the Release action to complete
8. Download RPMs/DEBs from the Releases page of your fork

## Library Dependencies

### LIKWID Collector

The LIKWID collector requires the LIKWID library. There is currently no Golang interface to LIKWID, so `cgo` is used to create bindings.

The build process handles LIKWID automatically:
- Checks if LIKWID is installed system-wide
- If not found, downloads and builds LIKWID with `direct` access mode
- Copies necessary header files

To use a pre-installed LIKWID:

```bash
export LD_LIBRARY_PATH=/path/to/likwid/lib:$LD_LIBRARY_PATH
```

### Other Dynamic Libraries

Some collectors and sinks dynamically load shared libraries:

| Component         | Library           | Purpose                    |
| ----------------- | ----------------- | -------------------------- |
| LIKWID collector  | liblikwid.so      | Hardware performance data  |
| NVIDIA collector  | libnvidia-ml.so   | NVIDIA GPU metrics         |
| ROCm collector    | librocm_smi64.so  | AMD GPU metrics            |
| Ganglia sink      | libganglia.so     | Ganglia metric submission  |

Ensure required libraries are in your `LD_LIBRARY_PATH`:

```bash
export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH
```

## Permissions

### Hardware Access

Some collectors require special permissions:

| Collector        | Requirement                                    | Solution                                           |
| ---------------- | ---------------------------------------------- | -------------------------------------------------- |
| LIKWID (direct)  | Direct hardware access                         | Run as root or use `capabilities`                  |
| IPMI             | Access to IPMI devices                         | User must be in `ipmi` group                       |
| Temperature      | Access to `/sys/class/hwmon`                   | Usually readable by all users                      |
| GPU collectors   | Access to GPU management libraries             | User must have GPU access rights                   |

### Setting Capabilities (Alternative to Root)

For LIKWID direct access without running as root:

```bash
sudo setcap cap_sys_rawio=ep /path/to/cc-metric-collector
```

**Warning**: Direct hardware access can be dangerous if misconfigured. Use with caution.

## Verification

After installation, verify the collector is working:

```bash
# Test configuration
cc-metric-collector -config /etc/cc-metric-collector/config.json -once

# Check logs
journalctl -u cc-metric-collector -f

# Or for SysV
tail -f /var/log/cc-metric-collector/collector.log
```

## Troubleshooting

### Common Issues

**Issue**: `cannot find liblikwid.so`
- **Solution**: Set `LD_LIBRARY_PATH` or configure in systemd service file

**Issue**: `permission denied` accessing hardware
- **Solution**: Run as root, use capabilities, or adjust file permissions

**Issue**: Configuration file not found
- **Solution**: Use `-config` flag or place config.json in execution directory

**Issue**: Metrics not appearing in sink
- **Solution**: Check sink configuration, network connectivity, and router settings

### Debug Mode

Run in foreground with debug output:

```bash
cc-metric-collector -config /path/to/config.json -log stderr
```

Run collectors only once for testing:

```bash
cc-metric-collector -config /path/to/config.json -once
```
