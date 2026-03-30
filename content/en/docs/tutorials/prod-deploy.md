---
title: Deployment
weight: 15
description: Plan and implement deployment workflow
categories: [cc-backend cc-metric-store]
tags: [Admin]
---

## Deployment

{{< alert title="Why we do not provide a docker container" >}}
The ClusterCockpit web backend binary has no external dependencies, everything
is included in the binary. The external assets, SQL database and job archive,
would also be external in a docker setup. The only advantage of a docker setup
would be that the initial configuration is automated. But this only needs to be
done one time. We therefore think that setting up docker, securing and
maintaining it is not worth the effort.
{{< /alert >}}

It is recommended to install all ClusterCockpit components in a common
directory, e.g. `/opt/monitoring`, `var/monitoring` or `var/clustercockpit`. In
the following we use `/opt/monitoring`.

A Systemd service runs on the central monitoring server:

- clustercockpit : Binary cc-backend in `/opt/monitoring/cc-backend`.
- (Optional with external metric-store) cc-metric-store : Binary cc-metric-store in `/opt/monitoring/cc-metric-store`.

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
You also can run `cc-backend` behind a reverse proxy. In this case it can be
started with an unprivileged user and the reverse proxy takes care of TLS
encryption. This also enables to automatically show a maintenance page in case
ClusterCockpit is not reachable.
{{< /alert >}}

### Workflow to deploy new version

This example assumes you are deploying ClusterCockpit for the first time or the
DB and job archive versions did not change between versions.

- Stop systemd service:

```sh
sudo systemctl stop clustercockpit.service
```

- Backup the sqlite DB file! This is as simple as to copy it. You can also use a
  continuous replication service as e.g. litestream.
- Copy new `cc-backend` binary to `/opt/monitoring/cc-backend/archive` (Tip: Use a
  date tag like `YYYYMMDD-cc-backend`). Here is an example:

```sh
cp ~/cc-backend /opt/monitoring/cc-backend/archive/20231124-cc-backend
```

- Link from `cc-backend` root to current version

```sh
ln -s  /opt/monitoring/cc-backend/archive/20231124-cc-backend /opt/monitoring/cc-backend/cc-backend
```

- If the new version requires a database migration, run it before starting the service:

```sh
cd /opt/monitoring/cc-backend
./cc-backend -migrate-db
```

  Check the release notes to find out whether a migration is needed.

- Start systemd service:

```sh
sudo systemctl start clustercockpit.service
```

- Check if everything is ok:

```sh
sudo systemctl status clustercockpit.service
```

- Check log for errors:

```sh
sudo journalctl -u clustercockpit.service
```

- Check the ClusterCockpit web frontend and your Slurm adapters if anything is broken!
