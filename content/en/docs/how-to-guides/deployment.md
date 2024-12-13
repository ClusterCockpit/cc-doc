---
title: How to deploy and update cc-backend
description: Recommended deployment and update workflow for production use
categories: [cc-backend]
tags: [Admin]
---
## Workflow for deployment

{{< alert color="danger" title="Why we do not provide a docker container" >}}
The ClusterCockpit web backend binary has no external dependencies, everything
is included in the binary. The external assets, SQL database and job archive,
would also be external in a docker setup. The only advantage of a docker setup
would be that the initial configuration is automated. But this only needs to be
done one time. We therefore think that setting up docker, securing and
maintaining it is not worth the effort.
{{< /alert >}}

It is recommended to install all ClusterCockpit components in a common directory, e.g. `/opt/monitoring`, `var/monitoring` or `var/clustercockpit`.
In the following we use `/opt/monitoring`.

Two systemd services run on the central monitoring server:

* clustercockpit : binary cc-backend in `/opt/monitoring/cc-backend`.
* cc-metric-store : Binary cc-metric-store in `/opt/monitoring/cc-metric-store`.

ClusterCockpit is deployed as a single binary that embeds all static assets.
We recommend keeping all `cc-backend` binary versions in a folder `archive` and
linking the currently active one from the `cc-backend` root.
This allows for easy roll-back in case something doesn't work.

{{< alert title="Please Note" >}}
`cc-backend` is started with root rights to open the privileged ports (80 and
443). It is recommended to set the configuration options `user` and `group`, in
which case `cc-backend` will drop root permissions once the ports are taken.
You have to take care, that the ownership of the `./var` folder and
its contents are set accordingly.
{{< /alert >}}

### Workflow to update

This example assumes the DB and job archive versions did not change. In case the
new binary requires a newer database or job archive version [read
here](/docs/tutorials/migration) how to migrate to newer versions.

* Stop systemd service:

```sh
sudo systemctl stop clustercockpit.service
```

* Backup the sqlite DB file! This is as simple as to copy it.
* Copy new `cc-backend` binary to `/opt/monitoring/cc-backend/archive` (Tip: Use a
date tag like `YYYYMMDD-cc-backend`). Here is an example:

```sh
cp ~/cc-backend /opt/monitoring/cc-backend/archive/20231124-cc-backend
```

* Link from  `cc-backend` root to current version

```sh
ln -s  /opt/monitoring/cc-backend/archive/20231124-cc-backend /opt/monitoring/cc-backend/cc-backend
```

* Start systemd service:

```sh
sudo systemctl start clustercockpit.service
```

* Check if everything is ok:

```sh
sudo systemctl status clustercockpit.service
```

* Check log for issues:

```sh
sudo journalctl -u clustercockpit.service
```

* Check the ClusterCockpit web frontend and your Slurm adapters if anything is broken!
