---
title: How to regenerate the Swagger UI documentation
categories: [cc-backend]
tags: [Developer]
---

## Overview

This project integrates [swagger ui](https://swagger.io/tools/swagger-ui/) to
document and test its REST API. The swagger documentation files can be found in
`./api/`.

## Generate Swagger UI files

You can generate the swagger-ui configuration by running the following command
from the cc-backend root directory:

```sh
go run github.com/swaggo/swag/cmd/swag init -d ./internal/api,./pkg/schema -g rest.go -o ./api
```

You need to move the created files `./api/docs.go` to `./internal/api/docs.go`.

## Use the Swagger UI web interface

If you start cc-backend with the `-dev` flag, the Swagger web interface is available
at [http://localhost:8080/swagger/](http://localhost:8080/swagger/).
You must enter a JWT key for a user with the
API role.

{{% alert title="Info" color="info" %}}
The user who owns the JWT key must not be logged into the same browser (have a
valid session), or the Swagger requests will not work. It is recommended to
create a separate user that has only the API role.
{{% /alert %}}
