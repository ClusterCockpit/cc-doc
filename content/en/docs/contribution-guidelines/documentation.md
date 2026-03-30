---
title: Contributing to Documentation
weight: 40
description: How to set up a local Hugo environment and contribute to the documentation website
tags: [Developer]
---

The ClusterCockpit documentation is built with [Hugo](https://gohugo.io/) using
the [Docsy](https://github.com/google/docsy) theme. Pages are written in
Markdown. Hugo wraps them into a static site with navigation, search, and
versioning.

All documentation contributions follow the same branch and PR workflow
described in the [Developer Workflow]({{< ref "_index" >}}) guide. The
repository to fork or clone is
[ClusterCockpit/cc-doc](https://github.com/ClusterCockpit/cc-doc).

---

## Local Setup

You need the **Hugo extended** version (for SCSS support), at minimum Hugo
0.45 — the most recent available version is recommended.

Clone the repository with submodules (required for the Docsy theme):

```bash
git clone --recurse-submodules https://github.com/ClusterCockpit/cc-doc.git
cd cc-doc
```

Start the local development server:

```bash
hugo server
```

Your site is available at <http://localhost:1313/>. Hugo watches for file
changes and automatically rebuilds and reloads the page.

---

## Quick Edit via GitHub

For small corrections to an existing page, use the **Edit this page** link in
the top-right corner of any documentation page. GitHub will prompt you to fork
the repository if you have not already, open the file in edit mode, and guide
you through creating a PR.

---

## Creating an Issue

If you have found a problem but are not ready to fix it yourself, open an issue
in the [cc-doc repository](https://github.com/ClusterCockpit/cc-doc/issues).
You can also use the **Create Issue** button in the top-right corner of any
documentation page.

---

## Useful Resources

- [Docsy user guide](https://www.docsy.dev/docs/) — navigation, look and feel, multi-language support
- [Hugo documentation](https://gohugo.io/documentation/) — comprehensive Hugo reference
