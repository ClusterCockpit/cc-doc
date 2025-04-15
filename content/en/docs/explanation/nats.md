---
title: NATS messaging
description: NATS message broker infrastructure
categories: [cc-backend, cc-metric-store, cc-metric-collector]
tags: [Developer, Admin]
---

## Introduction

[NATS](https://docs.nats.io/) is a powerful messaging solution supporting many
paradigms. Since it is itself implemented in Golang it provides excellent
support for Golang based applications. Currently NATS is offered in most
ClusterCockpit applications as an alternative to the default REST API.
We plan to make NATS the default way to communicate within the ClusterCockpit
framework in the future.

Advantages for us to use NATS:

- Scalable and low overhead messaging infrastructure
- Flexible configuration free setup of message sources and consumers
- Builtin zero trust JWT-based authentication system
- Simple message filtering based on hierarchical subject names
- Multicast and message queue support

## Authentication

NATS provides a sophisticated [authentication scheme](https://docs.nats.io/running-a-nats-service/configuration/securing_nats/auth_intro/jwt) based on JWT tokens and NKeys.
It provides the [nsc tool](https://docs.nats.io/using-nats/nats-tools/nsc) to
create and manage tokens supporting fine grained authentication and
authorization control.
