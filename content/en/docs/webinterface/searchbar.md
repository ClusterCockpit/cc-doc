---
title: Searchbar
description: >
  Toplevel Searchbar Functionality
categories: [cc-backend]
tags: [Frontend, General]
weight: 2
---

{{< figure src="../figures/searchbar.png" caption="ClusterCockpit Searchbar" alt="ClusterCockpit Searchbar" width="100%" class="ccfigure mw-xs" >}}

The top searchbar will handle page wide searches either by entering a searchterm directly as `<query>`, or by using a "keyword" implemented in the form of `<keyword>:<query>`. Entering a searchterm directly will start a hierarchical search which will return the first match in the hierarchy (see table below). It is recommended to supply the search with a keyword to specify the searched entity. For example, `jobName:myJobName` will specifically search for all jobs which have the queried string (or a part thereof) in their metadata `jobName` field. For all keywords with examples, see the table below.

Both keywords and queries are trimmed of all spaces before performing the search, returning the same results independently of location and number of spaces, e.g. ` name : Paul` and `name:  paul  ` are both handled identically.

Unprocessable queries will return a message detailing the cause of the error.

### Available Keywords

{{< alert >}}*Please note:* Hovering over the information icon right of the query field will list all keywords in the webinterface. {{< /alert >}}

|Keyword|Example Query|Destination|Note|
|---|-------------|-----------|----|
|No Keyword Used | `abcd100`           | [Joblist]({{< ref "views/joblist" >}} "Joblist") or [User Joblist]({{< ref "views/userjobs" >}} "User Joblist") | Performs hierarchical search `jobId -> username -> name -> projectId -> jobName` |
|JobId       | `jobId:123456`      | [Joblist]({{< ref "views/joblist" >}} "Joblist")         | Allows multiple identical matches, e.g. JobIds from different clusters |
|JobName     | `jobName:myJobName` | [Joblist]({{< ref "views/joblist" >}} "Joblist")         | Works with partial queries. Allows multiple identical matches, e.g. JobNames from different clusters. An additional `Last 30 Days` filter is active by default. |
|ProjectId   | `projectId:abcd100` | [Joblist]({{< ref "views/joblist" >}} "Joblist")         | All Jobs of the given project |
|Username    | `username:abcd100a` | [Users Table]({{< ref "views/users" >}} "Users Table")   | Only active users are returned. Users without jobs are not shown. An additional `Last 30 Days` filter is active by default. **Admin Only**|
|Name        | `name:Paul`         | [Users Table]({{< ref "views/users" >}} "Users Table")   | Works with partial queries. Only active users are returned. Users without jobs are not shown.  An additional `Last 30 Days` filter is active by default. **Admin Only**|
|ArrayJobId  | `arrayJobId:891011` | [Joblist]({{< ref "views/joblist" >}} "Joblist")         | All Jobs of the given arrayJobId. An additional `Last 30 Days` filter is active by default. |
