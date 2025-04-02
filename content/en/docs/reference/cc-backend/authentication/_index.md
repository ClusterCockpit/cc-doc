---
title: Authentication Handbook
description: How to configure and use the authentication backends
categories: [cc-backend]
tags: [Admin, Developer]
weight: 5
---
## Introduction

`cc-backend` supports the following authentication methods:

- Local login with credentials stored in SQL database
- Login with authentication to a LDAP directory
- Authentication via JSON Web Token (JWT):
  - With token provided in HTML request header
  - With token provided in cookie
- Login via OpenID Connect (against a KeyCloak instance)

All above methods create a session cookie that is then used for subsequent
authentication of requests. Multiple authentication methods can be configured at
the same time. If LDAP is enabled it takes precedence over local
authentication. The OpenID Connect method against a
[KeyCloak](https://www.keycloak.org/) instance enables many more authentication
methods using the ability of KeyCloak to act as an Identity Broker.

The REST API uses stateless authentication via a JWT token, which means that
every requests must be authenticated.

## General configuration options

All configuration is part of the `cc-backend` configuration file `config.json`.
All security sensitive options as passwords and tokens are passed in terms of
environment variables. `cc-backend` supports to read an `.env` file upon startup
and set the environment variables contained there.

### Duration of session

Per default the maximum duration of a session is 7 days. To change this the
option `session-max-age` has to be set to a string that can be parsed by the
Golang [time.ParseDuration()](https://pkg.go.dev/time#ParseDuration) function.
For most use cases the largest unit `h` is the only relevant option.
Example:

``` json
"session-max-age": "24h",
```

To enable unlimited session duration set `session-max-age` either to 0 or empty
string.

## LDAP authentication

### Configuration

To enable LDAP authentication the following set of options are required as
attributes of the `ldap` JSON object:

- `url`: URL of the LDAP directory server. This must be a complete URL including
  the protocol and not only the host name. Example: `ldaps://ldsrv.mydomain.com`.
- `user_base`: Base DN of user tree root. Example: `ou=people,ou=users,dc=rz,dc=mydomain,dc=com`.
- `search_dn`: DN for authenticating an LDAP admin account with general read
rights. This is required for the sync on login and the sync options. Example:
`cn=monitoring,ou=adm,ou=profile,ou=manager,dc=rz,dc=mydomain,dc=com`
- `user_bind`: Expression used to authenticate users via LDAP bind. Must contain
`uid={username}`. Example:
`uid={username},ou=people,ou=users,dc=rz,dc=mydomain,dc=com`.
- `user_filter`:  Filter to extract users for syncing. Example: `(&(objectclass=posixAccount))`.

Optional configuration options are:

- `username_attr`:  Attribute with full user name. Defaults to `gecos` if not provided.
- `sync_interval`:  Interval used for syncing SQL user table with LDAP
directory. Parsed using time.ParseDuration. The sync interval is always relative
to the time `cc-backend` was started. Example: `24h`.
- `sync_del_old_users`: Type boolean. Delete users in SQL database if not in
LDAP directory anymore. This of course only applies to users that were added
from LDAP.
- `syncUserOnLogin`: Type boolean. Add non-existent user to DB at login attempt
if user exists in LDAP directory. This option enables that users can login at
once after they are added to the LDAP directory.

The LDAP authentication method requires the environment variable
`LDAP_ADMIN_PASSWORD` for the `search_dn` account that is used to sync users.

### Usage

If LDAP is configured it is the first authentication method that is tried if a
user logs in using the login form. A sync with the LDAP directory can also be
triggered from the command line using the flag `-sync-ldap`.

## Local authentication

No configuration is required for local authentication.

### Usage

You can add an user on the command line using the flag `-add-user`:

``` sh
./cc-backend -add-user <username>:<roles>:<password>

```

Example:

``` sh
./cc-backend -add-user fritz:admin,api:myPass
```

Roles can be admin, support, manager, api, and user.

Users can be deleted using the flag `-del-user`:

``` sh
./cc-backend -del-user fritz
```

{{< alert color="warning" title="Warning" >}}
The option `-del-user` as currently implemented will delete **ALL** users that
match the username independent of its origin. This means it will also delete
user records that were added from LDAP or JWT tokens.
{{< /alert >}}

## JWT token authentication

[JSON web tokens](https://jwt.io/) are a standardized method for representing
claims securely between two parties. In ClusterCockpit they are used for
authorization to use REST APIs as well as a method to delegate authentication to
a third party. This section only describes JWT based authentication for
initiating a user session.

There exist two variants:

- Session Authenticator: Passes JWT token in the HTTP header _Authorization_
using the Bearer prefix or using the query key _login-token_. Example for
Authorization header:

``` txt
Authorization: Bearer S0VLU0UhIExFQ0tFUiEK
```

- Cookie Session Authenticator: Passes the JWT token in a Cookie, that is
instantly deleted after the session is initiated. This is a more secure
alternative to the standard header based solution.

### Configuration

## Authorization control

`cc-backend` uses roles to decide if a user is authorized to access certain
information. The roles and their rights are described in more detail [here](/docs/concepts/roles/).
