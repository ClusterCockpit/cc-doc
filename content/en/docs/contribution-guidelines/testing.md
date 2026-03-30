---
title: Unit Tests
weight: 20
description: Go test conventions and how to run the test suite locally
tags: [Developer]
---

## Overview

ClusterCockpit uses the standard Go testing environment. Run the full test
suite locally before pushing to avoid CI failures — this is part of the
[pre-PR checklist]({{< ref "_index#pre-pr-checklist" >}}).

---

## Conventions

- **White-box unit tests** — tests for internal (unexported) functionality are
  placed in the same file as the code under test, within the same package.
- **Black-box unit tests** — tests for public interfaces are placed in a
  separate file named `<package_name>_test.go` and belong to the package
  `<package_name>_test`. There is at most one such file per package.
- **Integration tests** — tests that exercise multiple components are also
  placed in the `<package_name>_test.go` file under the `<package_name>_test`
  package.
- **Test assets** — any required fixture files are placed in a `./testdata/`
  directory within the package directory.

---

## Running Tests

The project `Makefile` provides a `test` target that runs:

```bash
go clean -testcache
go build ./...
go vet ./...
go test ./...
```

Run it with:

```bash
make test
```

You can also run any of the individual commands directly from the command line.

For debugging individual tests, Visual Studio Code has excellent Go test
integration including breakpoint support.

---

## Further Reading

- [Testing package](https://pkg.go.dev/testing)
- [go test command](https://pkg.go.dev/cmd/go#hdr-Test_packages)
