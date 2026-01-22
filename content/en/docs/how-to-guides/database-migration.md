---
title: Database migrations
weight: 200
description: Database migrations
categories: [cc-backend]
tags: [Admin]
---

## Introduction

In general, an upgrade is nothing more than a replacement of the binary file.
All the necessary files, except the database file, the configuration file and
the job archive, are embedded in the binary file. It is recommended to use a
directory where the file names of the binary files are named with a version
indicator. This can be, for example, the date or the Unix epoch time. A symbolic
link points to the version to be used. This makes it easier to switch to earlier
versions.

The database and the job archive are versioned. Each release binary supports
specific versions of the database and job archive. If a version mismatch is
detected, the application is terminated and migration is required.

{{< alert color="warning" >}}
**IMPORTANT NOTE**</br>
It is recommended to make a backup copy of the database before each update. This
is mandatory in case the database needs to be migrated. In the case of sqlite,
this means to stopping `cc-backend` and copying the sqlite database file
somewhere.
{{< /alert >}}

## Migrating the database

{{< alert color="warning" >}}
**IMPORTANT NOTE**</br>
In case you database is larger than 10GB you may want to do a test migration on
a database copy to determine the expected downtime before attempting the
migration in production.
{{< /alert >}}

After you have backed up the database, run the following command to migrate the
database to the latest version:

```sh
> ./cc-backend -migrate-db
```

The migration files are embedded in the binary and can also be viewed in the cc
backend [source tree](https://github.com/ClusterCockpit/cc-backend/tree/master/internal/repository/migrations).
We use the [migrate library](https://github.com/golang-migrate/migrate).

If something goes wrong, you can check the status and get the current schema
(here for sqlite):

```sh
> sqlite3 var/job.db
```

In the sqlite console execute:

```sql
.schema
```

to get the current database schema.
You can query the current version and whether the migration failed with:

```sql
SELECT * FROM schema_migrations;
```

The first column indicates the current database version and the second column is
a dirty flag indicating whether the migration was successful.
