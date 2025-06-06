---
title: How to use the REST API Endpoints
categories: [cc-backend]
tags: [User, Admin, Developer]
---

## Overview

ClusterCockpit offers several REST API Endpoints. While some are integral part of the ClusterCockpit-Stack Workflow (such as`start_job`), others are optional.
These optional endpoints supplement the functionality of the webinterface with information reachable from scripts or the command line. For example, job metrics could be requested for specific jobs and handled in external statistics programs.

All of the endpoints listed for both administrators and users are secured by [JWT]({{< ref "jwtoken" >}} "JSON Web Token") authentication. As such, all prerequisites applicable to JSON Web Tokens apply in this case as well, e.g. [private and public key setup]({{< ref "generatejwt" >}} "Key Setup").

See also [the Swagger Reference]({{< ref "rest-api" >}} "Swagger REST") for more detailed information on each endpoint and the payloads.

## Admin Accessible REST API

{{< alert >}}
Endpoints described here should be restricted to administrators only, as they include integral functions.
{{< /alert >}}

### Admin API Prerequisites

1. JWT has to be generated by either a dedicated API user (has only `api` role) or by an *administrator* with both `admin` and `api` [roles]({{< ref "roles" >}} "ClusterCockpit Roles").
2. JWTs have a limited lifetime, i.e. will become invalid after a configurable amount of time (see `jwt.max-age` [config option]({{< ref "configuration" >}} "ClusterCockpit Configuration")).
3. Administrator endpoints are additionally subjected to a configurable IP whitelist (see `apiAllowedIPs` [config option]({{< ref "configuration" >}} "ClusterCockpit Configuration")). The config option has to be present with at least the wildcard `*` as only entry or the endpoints will block all requests.

### Admin API Endpoints and Functions

| Endpoint | Method | Request Payload(s) | Description |
|----------|--------|---------|-------------|
| `/api/users/`                 | GET         | - | Lists all Users |
| `/api/clusters/`              | GET         | - | Lists all Clusters |
| `/api/tags/`                  | DELETE      | JSON Payload | Removes payload array of tags specified with `Type, Name, Scope` from DB. Private Tags cannot be removed. |
| `/api/jobs/start_job/`        | POST, PUT   | JSON Payload | Starts Job |
| `/api/jobs/stop_job/`         | POST, PUT   | JSON Payload | Stops Jobs |
| `/api/jobs/`                  | GET         | URL-Query Params | Lists Jobs |
| `/api/jobs/{id}`              | POST        | $id, JSON Payload | Loads specified job metadata |
| `/api/jobs/{id}`              | GET         | $id | Loads specified job with metrics |
| `/api/jobs/tag_job/{id}`      | POST, PATCH | $id, JSON Payload | Adds payload array of tags specified with `Type, Name, Scope` to Job with $id. Tags are created in BD. |
| `/api/jobs/tag_job/{id}`      | POST, PATCH | $id, JSON Payload | Removes payload array of tags specified with `Type, Name, Scope` from Job with $id. Tags remain in DB. |
| `/api/jobs/edit_meta/{id}`    | POST, PATCH | $id, JSON Payload | Edits meta_data db colums info |
| `/api/jobs/metrics/{id}`      | GET         | $id, URL-Query Params | Loads specified jobmetrics for metric and scope params |
| `/api/jobs/delete_job/`       | DELETE      | JSON Payload | Deletes job specified in payload |
| `/api/jobs/delete_job/{id}`   | DELETE      | $id, JSON Payload | Deletes job specified by db id |
| `/api/jobs/delete_job_before/{ts}` | DELETE | $ts | Deletes all jobs before specified unix timestamp |

## User Accessible REST API

{{< alert >}}
Endpoints described here can be used by users to write scripted job analysis for their jobs only.
{{< /alert >}}

### User API Prerequisites

1. JWT has to be generated by either a dedicated API user (Has only `api` role) or an *User* with additional `api` [role]({{< ref "roles" >}} "ClusterCockpit Roles").
2. JWTs have a limited lifetime, i.e. will become invalid after a configurable amount of time (see `jwt.max-age` [config option]({{< ref "configuration" >}} "ClusterCockpit Configuration")).

### User API Endpoints and Functions

| Endpoint | Method | Request | Description |
|----------|--------|---------|-------------|
| `/userapi/jobs/`                  | GET         | URL-Query Params | Lists Jobs |
| `/userapi/jobs/{id}`              | POST        | $id, JSON Payload | Loads specified job metadata |
| `/userapi/jobs/{id}`              | GET         | $id | Loads specified job with metrics |
| `/userapi/jobs/metrics/{id}`      | GET         | $id, URL-Query Params | Loads specified jobmetrics for metric and scope params |
