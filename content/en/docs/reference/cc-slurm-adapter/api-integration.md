---
title: API Integration
description: Integration with cc-backend and NATS
categories: [cc-slurm-adapter]
tags: [Adapter, API]
weight: 8
---

## cc-backend REST API

The adapter communicates with cc-backend using its REST API to submit job information.

### Configuration

Set these required configuration options:

```json
{
  "ccRestUrl": "https://my-cc-backend-instance.example",
  "ccRestJwt": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
  "ccRestSubmitJobs": true
}
```

- **ccRestUrl**: URL to cc-backend's REST API (must not contain trailing slash)
- **ccRestJwt**: JWT token from cc-backend for REST API access
- **ccRestSubmitJobs**: Enable/disable REST API submissions (default: true)

### Endpoints Used

The adapter uses the following cc-backend API endpoints:

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/jobs/start_job/` | POST | Submit job start event |
| `/api/jobs/stop_job/<jobId>` | POST | Submit job completion event |

### Authentication

All API requests include a JWT bearer token in the Authorization header:

```
Authorization: Bearer <ccRestJwt>
```

### Job Data Format

Jobs are submitted in ClusterCockpit's job metadata format, including:

- Job ID and cluster name
- User and project information
- Start and stop times
- Resource allocation (nodes, CPUs, GPUs)
- Job state and exit code

### Error Handling

- **Connection Errors**: Adapter retries with exponential backoff
- **Authentication Errors**: Logged as errors; check JWT token validity
- **Validation Errors**: Logged with details about invalid fields

## NATS Messaging

NATS integration is optional and provides real-time job notifications to other services.

### Configuration

```json
{
  "natsServer": "mynatsserver.example",
  "natsPort": 4222,
  "natsSubject": "mysubject",
  "natsUser": "myuser",
  "natsPassword": "123456789"
}
```

Leave `natsServer` empty to disable NATS integration.

### Authentication Methods

The adapter supports multiple NATS authentication methods:

#### 1. Username/Password

```json
{
  "natsUser": "myuser",
  "natsPassword": "mypassword"
}
```

See: [NATS Username/Password Auth](https://docs.nats.io/running-a-nats-service/configuration/securing_nats/auth_intro/username_password)

#### 2. Credentials File

```json
{
  "natsCredsFile": "/etc/cc-slurm-adapter/nats.creds"
}
```

See: [NATS Credentials File](https://docs.nats.io/using-nats/developer/connecting/creds)

#### 3. NKey Authentication

```json
{
  "natsNKeySeedFile": "/etc/cc-slurm-adapter/nats.nkey"
}
```

See: [NATS NKey Auth](https://docs.nats.io/running-a-nats-service/configuration/securing_nats/auth_intro/nkey_auth)

### Message Format

Jobs are published as JSON messages to the configured subject:

```json
{
  "jobId": "12345",
  "cluster": "mycluster",
  "user": "username",
  "project": "projectname",
  "startTime": 1234567890,
  "stopTime": 1234567900,
  "numNodes": 4,
  "resources": { ... }
}
```

### Use Cases

NATS integration is useful for:

- **Real-time Monitoring**: Other services can subscribe to job events
- **Event-Driven Workflows**: Trigger actions when jobs start/stop
- **Alternative to REST**: Can disable REST submission and use NATS-only
- **Multi-Component Architecture**: Multiple services consuming job events

### Performance Considerations

- NATS adds minimal latency (typically < 1ms)
- Messages are fire-and-forget (no delivery guarantees by default)
- Consider using NATS JetStream for persistent queues if needed

## Dual Submission Mode

By default, the adapter submits jobs to **both** cc-backend REST API and NATS:

```json
{
  "ccRestSubmitJobs": true,
  "natsServer": "mynatsserver.example"
}
```

This ensures:
- cc-backend receives authoritative job data
- Other services can react to job events in real-time

### NATS-Only Mode

For specialized deployments, you can disable REST submission:

```json
{
  "ccRestSubmitJobs": false,
  "natsServer": "mynatsserver.example"
}
```

**Warning**: In this mode, you must ensure another component (e.g., a NATS subscriber) is forwarding job data to cc-backend, or jobs will not appear in the UI.
