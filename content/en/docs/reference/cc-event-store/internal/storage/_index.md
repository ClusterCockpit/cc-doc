---
title: cc-event-store's storage backends
description: Documentation of cc-event-store's storage backends
categories: [cc-event-store]
tags: [cc-event-store, Storage, General]
weight: 40
---

# Storage component

This component contains different backends for storing `CCEvent` and `CCLog` messages. The this in only a short term storage, so all backends have a notion of retention time to delete older entries.

# Backends

Each backend uses it's own configuration file entries. Check the backend-specific page for more information.

- [`sqlite`](./sqliteStorage.md)
- [`portgres`](./postgresStorage.md)