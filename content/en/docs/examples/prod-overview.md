---
title: Overview Production Setup
description: Background and recommended order for ClusterCockpit setup
categories: [cc-backend]
tags: [Admin]
---

## Introduction

ClusterCockpit requires the following components:

- A **node agent** running on all compute nodes that measures required metrics and
  forwards all data to a time series metrics database. ClusterCockpit provides
  its own node agent `cc-metric-collector`. This is the recommended setup, but ClusterCockpit
  can also be integrated with other node agents, e.g. `collectd`, `prometheus` or
  `telegraf`. In this case you have to use it with the accompanying time series database.
-

## Server Hardware
