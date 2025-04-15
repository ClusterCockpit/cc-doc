---
title: Environment
description: >
  ClusterCockpit Environment Variables
categories: [cc-backend]
tags: [admin]
weight: 3
---

All security-related configurations, e.g. keys and passwords, are set using
environment variables. It is supported to set these by means of a `.env` file in
the project root.

## Environment Variables

- `JWT_PUBLIC_KEY` and `JWT_PRIVATE_KEY`: Base64 encoded Ed25519 keys used for
  JSON Web Token (JWT) authentication. You can generate your own keypair using `go
run ./tools/gen-keypair/`. The release binaries also include the
  `gen-keypair` tool for x86-64. For more information, see the
  [JWT documentation]({{< ref "jwtoken" >}} "JSON Web Token").
- `SESSION_KEY`: Some random bytes used as secret for cookie-based sessions
- `LDAP_ADMIN_PASSWORD`: The LDAP admin user password (optional)
- `CROSS_LOGIN_JWT_HS512_KEY`: Used for token based logins via another
  authentication service (optional)
- `OID_CLIENT_ID`: OpenID connect client id (optional)
- `OID_CLIENT_SECRET`: OpenID connect client secret (optional)
- `PROMETHEUS_PASSWORD`: Password for the Prometheus user (optional)

## Template `.env` file

Below is an example `.env` file.
Copy it as `.env` into the project root and adapt it for your needs.

``` text
# Base64 encoded Ed25519 keys (DO NOT USE THESE TWO IN PRODUCTION!)
# You can generate your own keypair using `go run tools/gen-keypair/main.go`
JWT_PUBLIC_KEY="kzfYrYy+TzpanWZHJ5qSdMj5uKUWgq74BWhQG6copP0="
JWT_PRIVATE_KEY="dtPC/6dWJFKZK7KZ78CvWuynylOmjBFyMsUWArwmodOTN9itjL5POlqdZkcnmpJ0yPm4pRaCrvgFaFAbpyik/Q=="

# Base64 encoded Ed25519 public key for accepting externally generated JWTs
# Keys in PEM format can be converted, see `tools/convert-pem-pubkey/Readme.md`
CROSS_LOGIN_JWT_PUBLIC_KEY=""

# Some random bytes used as secret for cookie-based sessions (DO NOT USE THIS ONE IN PRODUCTION)
SESSION_KEY="67d829bf61dc5f87a73fd814e2c9f629"

# Password for the ldap server (optional)
LDAP_ADMIN_PASSWORD="mashup"
```
