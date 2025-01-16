---
title: Metric Store REST API
type: "swagger"
description: >
  ClusterCockpit Metric Store RESTful API Endpoint description
categories: [cc-metric-store]
tags: [Backend]
weight: 3
---

## Authentication

### JWT tokens

`cc-metric-store` supports only JWT tokens using the EdDSA/Ed25519 signing
method. The token is provided using the Authorization Bearer header.

Example script to test the endpoint:

```bash
#Only use JWT token if the JWT authentication has been setup
JWT="eyJ0eXAiOiJKV1QiLCJhbGciOiJFZERTQSJ9.eyJ1c2VyIjoiYWRtaW4iLCJyb2xlcyI6WyJST0xFX0FETUlOIiwiUk9MRV9BTkFMWVNUIiwiUk9MRV9VU0VSIl19.d-3_3FZTsadPjDEdsWrrQ7nS0edMAR4zjl-eK7rJU3HziNBfI9PDHDIpJVHTNN5E5SlLGLFXctWyKAkwhXL-Dw"

curl -X 'GET' 'http://localhost:8081/api/query/' -H "Authorization: Bearer $JWT" -d "{ \"cluster\": \"alex\", \"from\": 1720879275, \"to\": 1720964715, \"queries\": [{\"metric\": \"cpu_load\",\"host\": \"a0124\"}] }"
```

### NATS

TODO

## Usage of Swagger UI

This Swagger UI is also available as part of `cc-metric-store` if you start it
with the `dev` option:

```bash
./cc-metric-store -dev
```

You may access it at [this URL](http://localhost:8082/swagger/).

## Payload format for write endpoint

The data comes in Influx DB line protocol format.

```txt
<metric>,cluster=<cluster>,hostname=<hostname>,type=<node/hwthread/etc> value=<value> <epoch_time_in_ns_or_s>
```

Real example:

```txt
proc_run,cluster=fritz,hostname=f2163,type=node value=4i 1725620476214474893
```

A more detailed description of the ClusterCockpit flavored Influx DB line protocol and their types can be found
[here](https://github.com/ClusterCockpit/cc-specifications/blob/9b4ec9809ff66d40c262e0746d6a0be772d03d76/interfaces/lineprotocol/README.md)
in CC specification.

Example script to test endpoint:

```bash
#Only use JWT token if the JWT authentication has been setup
JWT="eyJ0eXAiOiJKV1QiLCJhbGciOiJFZERTQSJ9.eyJ1c2VyIjoiYWRtaW4iLCJyb2xlcyI6WyJST0xFX0FETUlOIiwiUk9MRV9BTkFMWVNUIiwiUk9MRV9VU0VSIl19.d-3_3FZTsadPjDEdsWrrQ7nS0edMAR4zjl-eK7rJU3HziNBfI9PDHDIpJVHTNN5E5SlLGLFXctWyKAkwhXL-Dw"

curl -X 'GET' 'http://localhost:8081/api/write/?cluster=alex' -H "Authorization: Bearer $JWT" -d "proc_run,cluster=fritz,hostname=f2163,type=node value=4i 1725620476214474893"
```

## Usage of Swagger UI

This Swagger UI is also available as part of `cc-metric-store` if you start it
with the `dev` option:

```bash
./cc-metric-store -dev
```

You may access it at [this URL](http://localhost:8082/swagger/).

## Swagger API Reference

{{< alert title="Non-Interactive Documentation" >}}
This reference is rendered using the `swagger-ui` plugin based on the original definition file found in the ClusterCockpit
[repository](https://raw.githubusercontent.com/ClusterCockpit/cc-metric-store/refs/heads/main/api/swagger.json),
_but without a serving backend_.</br></br>
This means that all interactivity ("Try It Out") will not return actual data.
However, a `Curl` call and a compiled `Request URL` will still be displayed, if
an API endpoint is executed.
{{< /alert >}}

{{< swagger-ui "<https://raw.githubusercontent.com/ClusterCockpit/cc-metric-store/refs/heads/main/api/swagger.json>" >}}
