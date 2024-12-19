---
title: How to use the Swagger UI documentation
categories: [cc-backend]
tags: [User, Admin, Developer]
---

## Overview

This project integrates [swagger ui](https://swagger.io/tools/swagger-ui/) to
document and test its REST API.
`./api/`.

## Access the Swagger UI web interface

If you start cc-backend with the `-dev` flag, the Swagger web interface is available
at [http://localhost:8080/swagger/](http://localhost:8080/swagger/).
To use the Try Out functionality, e.g. to test the REST API, you must enter a JWT
key for a user with the API role.

{{% alert title="Info" color="info" %}}
The user who owns the JWT key must not be logged into the same browser (have a
valid session), or the Swagger requests will not work. It is recommended to
create a separate user that has only the API role.
{{% /alert %}}
