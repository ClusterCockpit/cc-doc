---
title: Demo with release binary
---

{{% pageinfo color="primary" %}}
The demo setup with the release binary only works with a Linux system running on a x86-64 processor.
{{% /pageinfo %}}

Grab the release binary at [GitHub](https://github.com/ClusterCockpit/cc-backend/releases).
The following description assumes you perform all tasks from your home folder.
Extract the tar archive:

```shell
tar xzf cc-backend_Linux_x86_64.tar.gz
```

Create an empty folder and copy the binary `cc-backend` from the extracted archive folder to this folder:

```shell
mkdir ./demo
```

```shell
cp cc-backend ./demo
```

Change to the demo folder and run the following command to setup the required `var`
directory, initialize the sqlite database, `config.json` and `.env` files:

```shell
./cc-backend -init
```

The `./cc-backend -init` command creates a `config.json` with sensible defaults.
The cluster configurations (`fritz` and `alex`) are embedded in the job archive
you will download below — no manual cluster configuration is needed in
`config.json`. The generated file should look similar to:

```json
{
  "main": {
    "addr": "127.0.0.1:8080",
    "short-running-jobs-duration": 300,
    "resampling": {
      "minimum-points": 600,
      "trigger": 300,
      "resolutions": [240, 60]
    },
    "api-allowed-ips": ["*"],
    "emission-constant": 317
  },
  "cron": {
    "commit-job-worker": "1m",
    "duration-worker": "5m",
    "footprint-worker": "10m"
  },
  "archive": {
    "kind": "file",
    "path": "./var/job-archive"
  },
  "auth": {
    "jwts": {
      "max-age": "2000h"
    }
  }
}
```

Download the demo job archive:

```bash
wget https://hpc-mover.rrze.uni-erlangen.de/HPC-Data/0x7b58aefb/eig7ahyo6fo2bais0ephuf2aitohv1ai/job-archive-demo.tar
```

Extract the job archive:

```bash
tar xf job-archive-demo.tar
```

Initialize the database using the data from the job archive and create the demo user:

```bash
./cc-backend -init-db -add-user demo:admin:demo -loglevel info
```

Start the web server:

```bash
./cc-backend -server -dev -loglevel info
```

Open a web browser and access [http://localhost:8080](http://localhost:8080).
You should see the ClusterCockpit login page:
{{< figure src="cc-login-screen.png" alt="ClusterCockpit Login page" class="ccfigure">}}

Enter `demo` for the Username and `demo` for the Password and press the Submit button. After that the ClusterCockpit index page should be displayed:
{{< figure src="cc-index-screen.png" alt="ClusterCockpit Index page" class="ccfigure">}}

The demo user has the admin role and therefore can see all views.
{{< alert title="Note" >}}Because the demo only loads data from the job archive some views as the status and systems view do not work!{{< /alert >}}

For details about the features of the web interface have a look at the [user guide](/docs/webinterface).
