---
title: How-to Guides
weight: 10
description: How-to solve concrete problems
---

This section contains practical how-to guides for common ClusterCockpit tasks.

## Setup & Deployment

| Guide | Description |
|-------|-------------|
| [Hands-On Demo]({{< relref "handson" >}}) | Basic ClusterCockpit setup and API usage walkthrough |
| [Deploy and Update cc-backend]({{< relref "deployment" >}}) | Recommended deployment and update workflow for production use |
| [Setup a systemd Service]({{< relref "systemd-service" >}}) | Run ClusterCockpit components as systemd services |
| [Create a `cluster.json` File]({{< relref "clusterConfig" >}}) | How to initially create a cluster configuration |

## Configuration & Customization

| Guide | Description |
|-------|-------------|
| [Customize cc-backend]({{< relref "customization" >}}) | Add legal texts, modify login page, and add custom logo |
| [Notification Banner]({{< relref "notificationBanner" >}}) | Add a message of the day banner on the homepage |
| [Auto-Tagging]({{< relref "auto-tagging" >}}) | Enable automatic job tagging for application detection and classification |
| [Resampling]({{< relref "resampling" >}}) | Plan and configure metric resampling |
| [Retention Policies]({{< relref "retention-policy" >}}) | Manage database and job archive size with retention policies |

## Metric Collection & Integration

| Guide | Description |
|-------|-------------|
| [Hierarchical Metric Collection]({{< relref "hierarchical-collection" >}}) | Configure multiple cc-metric-collector instances with forwarding |
| [External TSDB Integration]({{< relref "external-tsdb-integration" >}}) | Integrate Prometheus and InfluxDB data into cc-metric-store |
| [Sharing HPM Metrics (SLURM)]({{< relref "slurm-hwperf" >}}) | Share hardware performance counter access between monitoring and user jobs |

## API & Developer Tools

| Guide | Description |
|-------|-------------|
| [Generate JWT Tokens]({{< relref "generateJWT" >}}) | Generate JSON Web Tokens for API authentication |
| [Use the REST API]({{< relref "useRest" >}}) | How to use the REST API endpoints |
| [Use the Swagger UI]({{< relref "useSwagger" >}}) | Browse and test API endpoints via Swagger UI |
| [Regenerate Swagger Docs]({{< relref "generateSwagger" >}}) | Regenerate the Swagger UI documentation from source |

## Migrations

| Guide | Description |
|-------|-------------|
| [Database Migrations]({{< relref "database-migration" >}}) | Apply database schema migrations |
| [Job Archive Migrations]({{< relref "archive-migration" >}}) | Migrate job archive data between versions |
