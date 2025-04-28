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

``` json
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

## Usage of Swagger UI

To use the [Swagger UI](https://swagger.io/tools/swagger-ui/) for testing you
have to run an instance of cc-backend on localhost (and use the default port
8080):

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

## Swagger API Reference

{{< alert title="Non-Interactive Documentation" >}}
This reference is rendered using the `swaggerui` plugin based on the original definition file found in the ClusterCockpit [repository](https://github.com/ClusterCockpit/cc-backend/blob/master/api/swagger.json "ClusterCockpit GitHub"), *but without a serving backend*.</br></br>
This means that all interactivity ("Try It Out") will not return actual data. However, a `Curl` call and a compiled `Request URL` will still be displayed, if an API endpoint is executed.
{{< /alert >}}

{{< alert title="Administrator API" >}}
Endpoints displayed here correspond to the administrator `/api/` endpoints, but user-accessible `/userapi/` endpoints are functionally identical. See [these lists]({{< ref "userest" >}} "How-To REST API") for information about accessibility.
{{< /alert >}}

{{< swagger-ui "https://raw.githubusercontent.com/ClusterCockpit/cc-backend/refs/heads/master/api/swagger.json" >}}
