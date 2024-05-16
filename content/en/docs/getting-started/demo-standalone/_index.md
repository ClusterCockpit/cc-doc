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

Open `config.json` in an editor of your choice to edit the existing clusters
name and add a second cluster. Name the clusters `fritz` and `alex`. The file
should look as below afterwards:

```json {linenos=table,hl_lines=[9,31]}
{
    "addr": "127.0.0.1:8080",
    "archive": {
        "kind": "file",
        "path": "./var/job-archive"
    },
    "jwts": {
        "session-max-age": "24h",
    },
    "clusters": [
        {
            "name": "fritz",
            "metricDataRepository": {
                "kind": "cc-metric-store",
                "url": "http://localhost:8082",
                "token": ""
            },
            "filterRanges": {
                "numNodes": {
                    "from": 1,
                    "to": 64
                },
                "duration": {
                    "from": 0,
                    "to": 86400
                },
                "startTime": {
                    "from": "2023-01-01T00:00:00Z",
                    "to": null
                }
            }
        },
        {
            "name": "alex",
            "metricDataRepository": {
                "kind": "cc-metric-store",
                "url": "http://localhost:8082",
                "token": ""
            },
            "filterRanges": {
                "numNodes": {
                    "from": 1,
                    "to": 64
                },
                "duration": {
                    "from": 0,
                    "to": 86400
                },
                "startTime": {
                    "from": "2023-01-01T00:00:00Z",
                    "to": null
                }
            }
        }
    ]
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
