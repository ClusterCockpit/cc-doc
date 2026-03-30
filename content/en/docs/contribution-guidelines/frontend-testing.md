---
title: Frontend Development Setup
weight: 30
description: How to set up cc-backend for fast frontend development iteration
categories: [cc-backend]
tags: [Developer]
---

## Overview

The cc-backend web frontend is built with Svelte. By default, the compiled
frontend assets are embedded directly in the Go binary. During frontend
development this is impractical — use the setup below to enable fast
rebuild-on-save iteration without recompiling the backend.

For all other aspects of the development process (branching, commits, PRs)
follow the [Developer Workflow]({{< ref "_index" >}}) guide.

---

## Setup

### 1. Disable embedded static files

In `config.json`, set:

```json
"embed-static-files": false,
"static-files": "./web/frontend/public/"
```

This tells cc-backend to serve assets from disk rather than from the embedded
filesystem.

### 2. Start the frontend build in watch mode

In the `./web/frontend` directory:

```bash
npm run dev
```

This starts the Rollup build in listen mode. Whenever you save a source file,
the affected JavaScript targets are rebuilt automatically.

If the output is minified when you expect it not to be, set the production flag
manually in `./web/frontend/rollup.config.mjs`:

```mjs
const production = false
```

This should normally be set automatically based on the npm script, but the
override is available if needed.

### 3. Start cc-backend

From the repository root:

```bash
./cc-backend -server -dev
```

Because assets are served by cc-backend (not a separate dev server), you must
reload the page in your browser manually after each frontend rebuild.

---

## Recommended Terminal Layout

A common setup is three terminals running concurrently:

| Terminal | Directory | Command |
|---|---|---|
| 1 | repository root | `./cc-backend -server -dev` |
| 2 | `./web/frontend` | `npm run dev` |
| 3 | any | editor / shell for source edits |
