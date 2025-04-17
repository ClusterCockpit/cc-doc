---
title: JSON Web Token
description: >
 JSON Web Token (JWT) usage in ClusterCockpit
categories: [cc-backend, cc-metric-store]
tags: [Developer, Admin]
---

## Introduction

ClusterCockpit uses [JSON Web Tokens](https://jwt.io/introduction) (JWT) for
authorization of its APIs. JSON Web Token (JWT) is an open standard (RFC 7519)
that defines a compact and self-contained way for securely transmitting
information between parties as a JSON object. This information can be verified
and trusted because it is digitally signed. In ClusterCockpit JWTs are signed
using a public/private key pair using ECDSA. Because tokens are signed using
public/private key pairs, the signature also certifies that only the party
holding the private key is the one that signed it. Expiration of the generated
tokens as well as the maximum length of a browser session can be configured in
the `config.json` file described
[here]({{< ref "docs/reference/cc-backend/configuration" >}} "Job Metadata Schema Reference").

The [Ed25519](https://ed25519.cr.yp.to/) algorithm for signatures was used
because it is compatible with other tools that require authentication, such as
NATS.io, and because these elliptic-curve methods provide simillar security with
smaller keys compared to something like RSA. They are sligthly more expensive to
validate, but that effect is negligible.

## JWT Payload

You may view the payload of a JWT token at [https://jwt.io/#debugger-io](https://jwt.io/#debugger-io).
Currently ClusterCockpit sets the following claims:

* `iat`: Issued at claim. The “iat” claim is used to identify the the time at which the JWT was issued. This claim can be used to determine the age of the JWT.
* `sub`: Subject claim. Identifies the subject of the JWT, in our case this is the username.
* `roles`: An array of strings specifying the roles set for the subject.
* `exp`: Expiration date of the token (only if explicitly configured)

It is important to know that JWTs are not encrypted, only signed. This means that outsiders cannot create new JWTs or modify existing ones, but they are able to read out the username.

## Accept externally generated JWTs provided via cookie

If there is an external service like an AuthAPI that can generate JWTs and hand
them over to ClusterCockpit via cookies, CC can be configured to accept them:

1. `.env`: CC needs a public ed25519 key to verify foreign JWT signatures.
   Public keys in PEM format can be converted with the instructions in
   [/tools/convert-pem-pubkey-for-cc](https://github.com/ClusterCockpit/cc-backend/blob/master/tools/convert-pem-pubkey/Readme.md)
   .

```bash
CROSS_LOGIN_JWT_PUBLIC_KEY="+51iXX8BdLFocrppRxIw52xCOf8xFSH/eNilN5IHVGc="
```

2. `config.json`: Insert a name for the cookie (set by the external service)
   containing the JWT so that CC knows where to look at. Define a trusted issuer
   (JWT claim 'iss'), otherwise it will be rejected. If you want usernames and
   user roles from JWTs ('sub' and 'roles' claim) to be validated against CC's
   internal database, you need to enable it here. Unknown users will then be
   rejected and roles set via JWT will be ignored.

```json
"jwts": {
    "cookieName": "access_cc",
    "forceJWTValidationViaDatabase": true,
    "trustedExternalIssuer": "auth.example.com"
}
```

3. Make sure your external service includes the same issuer (`iss`) in its JWTs.
   Example JWT payload:

```json
{
  "iat": 1668161471,
  "nbf": 1668161471,
  "exp": 1668161531,
  "sub": "alice",
  "roles": [
    "user"
  ],
  "jti": "a1b2c3d4-1234-5678-abcd-a1b2c3d4e5f6",
  "iss": "auth.example.com"
}
```
