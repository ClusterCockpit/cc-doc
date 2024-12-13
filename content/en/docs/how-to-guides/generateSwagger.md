---
title: How to regenerate the Swagger UI documentation
categories: [cc-backend]
tags: [Developer]
---

## Overview

This project integrates [swagger ui](https://swagger.io/tools/swagger-ui/) to
document and test its REST API. The swagger documentation files can be found in
`./api/`.

{{% alert title="Note" color="error" %}}
To regenerate the Swagger UI files is only required if you change the files
`./internal/api/rest.go`. Otherwise the Swagger UI will already be correctly
build and is ready to use.
{{% /alert %}}

## Generate Swagger UI files

You can generate the swagger-ui configuration by running the following command
from the cc-backend root directory:

```sh
go run github.com/swaggo/swag/cmd/swag init -d ./internal/api,./pkg/schema -g rest.go -o ./api
```

You need to move one generated file:

```sh
mv ./api/docs.go ./internal/api/docs.go
```

Finally rebuild `cc-backend`:

```sh
make
```

## Use the Swagger UI web interface

If you start cc-backend with the `-dev` flag, the Swagger web interface is available
at [http://localhost:8080/swagger/](http://localhost:8080/swagger/).
To use the Try Out functionality, e.g. to test the REST API, you must enter a JWT
key for a user with the API role.

{{% alert title="Info" color="info" %}}
The user who owns the JWT key must not be logged into the same browser (have a
valid session), or the Swagger requests will not work. It is recommended to
create a separate user that has only the API role.
{{% /alert %}}
