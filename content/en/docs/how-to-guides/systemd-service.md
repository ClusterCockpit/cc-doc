---
title: How to setup a systemd service
description: Run ClusterCockpit components as systemd services
categories: [cc-backend]
tags: [Admin]
---
## How to run as a systemd service.

The files in this directory assume that you install ClusterCockpit to
`/opt/monitoring/cc-backend`.
Of course you can choose any other location, but make sure you replace all paths
starting with `/opt/monitoring/cc-backend` in the `clustercockpit.service` file!

The `config.json` may contain the optional fields *user* and *group*. If
specified, the application will call
[setuid](https://man7.org/linux/man-pages/man2/setuid.2.html) and
[setgid](https://man7.org/linux/man-pages/man2/setgid.2.html) after reading the
config file and binding to a TCP port (so it can take a privileged port), but
before it starts accepting any connections. This is good for security, but also
means that the `var/` directory must be readable and writeable by this user.
The `.env` and `config.json` files may contain secrets and should not be
readable by this user. If these files are changed, the server must be restarted.

1. Clone this repository somewhere in your home

```sh
git clone git@github.com:ClusterCockpit/cc-backend.git
```

2. (Optional) Install dependencies and build. In general it is recommended to use the provided release binaries.

```sh
cd cc-backend && make
```

Copy the binary to the target folder (adapt if necessary):

```sh
sudo mkdir -p /opt/monitoring/cc-backend/
```

```sh
cp ./cc-backend /opt/monitoring/cc-backend/
```

3. Modify the `config.json` and `env-template.txt` file from the `configs` directory to your liking and put it in the target directory

```sh
cp ./configs/config.json /opt/monitoring/config.json && cp ./configs/env-template.txt /opt/monitoring/.env
```

```sh
vim /opt/monitoring/config.json # do your thing...
vim /opt/monitoring/.env # do your thing...
```

4. (Optional) Customization: Add your versions of the login view, legal texts, and logo image. You may use the templates in `./web/templates` as blueprint. Every overwrite is separate.

```sh
cp login.tmpl /opt/monitoring/cc-backend/var/
cp imprint.tmpl /opt/monitoring/cc-backend/var/
cp privacy.tmpl /opt/monitoring/cc-backend/var/
# Ensure your logo, and any images you use in your login template has a suitable size.
cp -R img /opt/monitoring/cc-backend/img
```

5. Copy the systemd service unit file. You may adopt it to your needs.

```sh
sudo cp ./init/clustercockpit.service /etc/systemd/system/clustercockpit.service
```

6. Enable and start the server

```sh
sudo systemctl enable clustercockpit.service # optional (if done, (re-)starts automatically)
```

```sh
sudo systemctl start clustercockpit.service
```

Check whats going on:

```sh
sudo systemctl status clustercockpit.service
```

```sh
sudo journalctl -u clustercockpit.service
```
