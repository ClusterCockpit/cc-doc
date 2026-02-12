---
title: REST API
type: "swagger"
description: >
  ClusterCockpit RESTful API Endpoint Reference
categories: [cc-backend]
tags: [Backend]
weight: 4
---

## REST API Authorization

In ClusterCockpit JWTs are signed using a public/private key pair using ED25519.
Because tokens are signed using public/private key pairs, the signature also
certifies that only the party holding the private key is the one that signed it.
JWT tokens in ClusterCockpit are not encrypted, means all information is clear
text. Expiration of the generated tokens can be configured in config.json using
the `max-age` option in the jwts object. Example:

```json
"jwts": {
    "max-age": "168h"
},
```

The party that generates and signs JWT tokens has to be in possession of the
private key and any party that accepts JWT tokens must possess the public key to
validate it. `cc-backed` therefore requires both keys, the private one to
sign generated tokens and the public key to validate tokens that are provided by
REST API clients.

### Generate ED25519 key pairs

We provide a tool as part of `cc-backend` to generate a ED25519 keypair.
The tool is called `gen-keypair` and provided as part of the release binaries.
You can easily build it yourself in the `cc-backend` source tree with:

```bash
go build tools/gen-keypair
```

To use it just call it without any arguments:

```bash
./gen-keypair
```

## Usage of Swagger UI documentation

[Swagger UI](https://swagger.io/tools/swagger-ui/) is a REST API documentation
and testing framework. To use the [Swagger
UI](https://swagger.io/tools/swagger-ui/) for testing you have to run an
instance of cc-backend on localhost (and use the default port 8080):

```bash
./cc-backend -server
```

You may want to start the demo as described [here](/docs/getting-started/) .
This Swagger UI is also available as part of `cc-backend` if you start it with
the `dev` option:

```bash
./cc-backend -server -dev
```

You may access it at [this URL](http://localhost:8080/swagger/).

## Conditional Endpoints

When `api-subjects` is configured in the `main` section of `config.json` (i.e.,
NATS messaging is enabled for job events), the REST API endpoints
`/api/jobs/start_job/` and `/api/jobs/stop_job/` are **disabled**. Job
start/stop operations are then handled exclusively via NATS. All other REST
endpoints remain available regardless of NATS configuration.

## API Endpoint Groups

The REST API is organized into several route groups:

- **Admin API** (`/api/`): Full job and cluster management, requires admin/API role JWT.
- **User API** (`/userapi/`): Read-only job query endpoints for regular users.
- **Metric Store API** (`/metricstore/`): Metric data ingestion, health checks,
  and debugging endpoints.
- **Config API** (`/config/`): User management and configuration, uses session
  authentication.
- **Frontend API** (`/frontend/`): JWT generation and user config updates, uses
  session authentication.

## Swagger API Reference

{{< alert title="Non-Interactive Documentation" >}}
This reference is rendered using the `swaggerui` plugin based on the original definition file found in the ClusterCockpit [repository](https://github.com/ClusterCockpit/cc-backend/blob/master/api/swagger.json "ClusterCockpit GitHub"), _but without a serving backend_.</br></br>
This means that all interactivity ("Try It Out") will not return actual data. However, a `Curl` call and a compiled `Request URL` will still be displayed, if an API endpoint is executed.
{{< /alert >}}

{{< alert title="Administrator API" >}}
Endpoints displayed here correspond to the administrator `/api/` endpoints, but user-accessible `/userapi/` endpoints are functionally identical. See [these lists]({{< ref "userest" >}} "How-To REST API") for information about accessibility.
{{< /alert >}}

{{< swagger-ui "<https://raw.githubusercontent.com/ClusterCockpit/cc-backend/refs/heads/master/api/swagger.json>" >}}
