---
title: REST API
description: >
  ClusterCockpit Metric Store RESTful API Endpoint description
categories: [cc-metric-store]
tags: [Backend]
weight: 3
---
## Authentication

### JWT tokens

### NATS

## Usage of Swagger UI

This Swagger UI is also available as part of `cc-metric-store` if you start it
with the `dev` option:

```bash
./cc-metric-store -dev
```

You may access it at [this URL](http://localhost:8082/swagger/).

## Swagger API Reference

{{< alert title="Non-Interactive Documentation" >}}
This reference is rendered using the `swaggerui` plugin based on the original definition file found in the ClusterCockpit
[repository](https://github.com/ClusterCockpit/cc-metric-store/blob/master/api/swagger.json "ClusterCockpit GitHub"),
*but without a serving backend*.</br></br>
This means that all interactivity ("Try It Out") will not return actual data. However, a `Curl` call and a compiled `Request URL` will still be displayed, if an API endpoint is executed.
{{< /alert >}}

{{< swagger-ui "https://raw.githubusercontent.com/ClusterCockpit/cc-metric-store/refs/heads/main/api/swagger.json" >}}
