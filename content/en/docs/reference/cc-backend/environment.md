---
title: Environment
description: >
  ClusterCockpit Environment Variables
categories: [cc-backend]
tags: [Backend]
weight: 3
---

All security-related configurations, e.g. keys and passwords, are set using
environment variables. It is supported to set these by means of a `.env` file in
the project root.

## Environment Variables

An example env file is found in
[this directory](https://github.com/ClusterCockpit/cc-backend/tree/master/configs "env-template.txt").
Copy it as `.env` into the project root and adapt it for your needs.

- `JWT_PUBLIC_KEY` and `JWT_PRIVATE_KEY`: Base64 encoded Ed25519 keys used for
  JSON Web Token (JWT) authentication. You can generate your own keypair using `go
run ./tools/gen-keypair/`. The release binaries also include the
  `gen-keypair` tool for x86-64. For more information, see the
  [JWT documentation]({{< ref "jwtoken" >}} "JSON Web Token").
- `SESSION_KEY`: Some random bytes used as secret for cookie-based sessions.
- `LDAP_ADMIN_PASSWORD`: The LDAP admin user password (optional).
- `CROSS_LOGIN_JWT_HS512_KEY`: Used for token based logins via another
  authentication service.
- `LOGLEVEL`: Can be `crit`, `err`, `warn`, `info` or `debug`. Can be used to
  reduce logging. Default is `info`.
