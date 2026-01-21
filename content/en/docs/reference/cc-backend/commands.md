---
title: Command Line
description: >
  ClusterCockpit Command Line Options
categories: [cc-backend]
tags: [Backend]
weight: 1
---

This page describes the command line options for the `cc-backend` executable.

---

```txt
-add-user <username>:[admin,support,manager,api,user]:<password>
```

_Function:_ Add a new user. Only one role can be assigned.

_Example:_ `-add-user abcduser:manager:somepass`

---

```txt
  -apply-tags
```

_Function:_ Run taggers on all completed jobs and exit.

---

```txt
  -config <path>
```

_Function:_ Specify alternative path to `config.json`.

_Default:_ `./config.json`

_Example:_ `-config ./configfiles/configuration.json`

---

```txt
  -del-user <username>
```

_Function:_ Remove an existing user.

_Example:_ `-del-user abcduser`

---

```txt
  -dev
```

_Function:_ Enable development components: GraphQL Playground and Swagger UI.

---

```txt
  -force-db
```

_Function:_ Force database version, clear dirty flag and exit.

---

```txt
  -gops
```

_Function:_ Listen via github.com/google/gops/agent (for debugging).

---

```txt
  -import-job <path-to-meta.json>:<path-to-data.json>, ...
```

_Function:_ Import a job. Argument format: `<path-to-meta.json>:<path-to-data.json>,...`

_Example:_ `-import-job ./to-import/job1-meta.json:./to-import/job1-data.json,./to-import/job2-meta.json:./to-import/job2-data.json`

---

```txt
  -init
```

_Function:_ Setup var directory, initialize sqlite database file, config.json and .env.

---

```txt
  -init-db
```

_Function:_ Go through job-archive and re-initialize the `job`, `tag`, and
`jobtag` tables (all running jobs will be lost!).

{{< alert color="warning">}}**Caution:** All running jobs will be lost!{{< /alert >}}

---

```txt
  -jwt <username>
```

_Function:_ Generate and print a JWT for the user specified by its username.

_Example:_ `-jwt abcduser`

---

```txt
  -logdate
```

_Function:_ Set this flag to add date and time to log messages.

---

```txt
  -loglevel <level>
```

_Function:_ Sets the logging level.

_Arguments:_ `debug | info | warn | err | crit`

_Default:_ `warn`

_Example:_ `-loglevel debug`

---

```txt
  -migrate-db
```

_Function:_ Migrate database to supported version and exit.

---

```txt
  -revert-db
```

_Function:_ Migrate database to previous version and exit.

---

```txt
  -server
```

_Function:_ Start a server, continues listening on port after initialization and
argument handling.

---

```txt
  -sync-ldap
```

_Function:_ Sync the `hpc_user` table with ldap.

---

```txt
  -version
```

_Function:_ Show version information and exit.
