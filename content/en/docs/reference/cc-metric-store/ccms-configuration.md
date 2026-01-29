---
title: Configuration
description: >
  ClusterCockpit Metric Store Configuration Option References
categories: [cc-metric-store]
tags: [Backend]
weight: 2
---

Configuration options are located in a JSON file. Default path is `config.json`
in current working directory. Alternative paths to the configuration file can be
specified using the command line switch `-config <filename>`.

All durations are specified as string that will be parsed [like
this](https://pkg.go.dev/time#ParseDuration) (Allowed suffixes: `s`, `m`, `h`,
...).

The configuration is organized into four main sections: `main`, `metrics`,
`nats`, and `metric-store`.

## Main Section

- `main`: Server configuration (required)
  - `addr`: Address to bind to, for example `localhost:8080` or `0.0.0.0:443`
  (required)
  - `https-cert-file`: Filepath to SSL certificate. If also `https-key-file` is
  set, use HTTPS (optional)
  - `https-key-file`: Filepath to SSL key file. If also `https-cert-file` is
  set, use HTTPS (optional)
  - `user`: Drop root permissions to this user once the port was bound. Only
  applicable if using privileged port (optional)
  - `group`: Drop root permissions to this group once the port was bound. Only
  applicable if using privileged port (optional)
  - `backend-url`: URL of cc-backend for querying job information, e.g.,
  `https://localhost:8080` (optional)
  - `jwt-public-key`: Base64 encoded Ed25519 public key, use this to verify
  requests to the HTTP API (required)
  - `debug`: Debug options (optional)
    - `dump-to-file`: Path to file for dumping internal state (optional)
    - `gops`: Enable gops agent for debugging (optional)

## Metrics Section

- `metrics`: Map of metric-name to objects with the following properties
(required)
  - `frequency`: Timestep/Interval/Resolution of this metric in seconds
  (required)
  - `aggregation`: Can be `"sum"`, `"avg"` or `null` (required)
    - `null` means aggregation across topology levels is disabled for this
    metric (use for node-scope-only metrics)
    - `"sum"` means that values from the child levels are summed up for the
    parent level
    - `"avg"` means that values from the child levels are averaged for the
    parent level

## NATS Section

- `nats`: NATS server connection configuration (optional)
  - `address`: URL of NATS.io server, example: `nats://localhost:4222` (required
  if nats section present)
  - `username`: NATS username for authentication (optional)
  - `password`: NATS password for authentication (optional)

## Metric-Store Section

- `metric-store`: Storage engine configuration (required)
  - `checkpoints`: Checkpoint configuration (required)
    - `interval`: Create checkpoints every X seconds/minutes/hours (required)
    - `directory`: Path to checkpoint directory (required)
  - `retention-in-memory`: Keep all values in memory for at least that amount of
  time. Should be long enough to cover common job durations (required)
  - `memory-cap`: Maximum percentage of system memory to use (optional)
  - `cleanup`: Cleanup/archiving configuration (required)
    - `mode`: Either `"archive"` (move and compress old checkpoints) or
    `"delete"` (remove old checkpoints) (required)
    - `interval`: Perform cleanup every X seconds/minutes/hours (required)
    - `directory`: Path to archive directory (required if mode is `"archive"`)
  - `nats-subscriptions`: Array of NATS subscription configurations (optional,
  requires `nats` section)
    - `subscribe-to`: NATS subject to subscribe to (required)
    - `cluster-tag`: Default cluster tag for incoming metrics (required)
