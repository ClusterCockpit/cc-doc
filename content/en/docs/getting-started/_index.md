---
title: Getting Started
description: Information on how to setup our demo and build cc-backend
weight: 2
---

The central component of ClusterCockpit is the web- and api backend
`cc-backend`. We provide a demo setup that allows you to get an impression of
the web interface. If you just want to try the demo and you have a Linux OS you
can do so using the `cc-backend` [release binary](https://github.com/ClusterCockpit/cc-backend/releases).
You find detailed instructions on how to setup the demo with the release binary [here](/docs/getting-started/demo-standalone)
If you have a different OS or want to build `cc-backend` yourself follow the instructions below.

## Prerequisites

To build `cc-backend` you need:

* A [go compiler](https://go.dev/dl/), version 1.20 or newer. Most recent os environments should have a package with a recent enough version. On MacOS we recommend to use [Homebrew](https://brew.sh) to install on.
* A node.js environment including the `npm` package manager.
* A git revision control client.
* For the demo shell script you need `wget` to download the example job archive

## Try it out!

{{< youtube id="INPU1d-TGJ0" title="How to get the ClusterCockpit demo up and running" >}}

All ClusterCockpit components are available within the [GitHub ClusterCockpit project](https://github.com/ClusterCockpit).

Clone `cc-backend` and change directory into the repository:

```bash
git clone https://github.com/ClusterCockpit/cc-backend.git && cd cc-backend
```

{{< alert title="Note" >}}The startDemo script will download a tar file with 38MB (223MB on disk)!{{< /alert >}}

Execute the demo start script:

```bash
./startDemo.sh
```

What follows is output from building `cc-backend` and downloading the job-archive

```txt
HTTP server listening at 127.0.0.1:8080...
```

Open a web browser and access [http://localhost:8080](http://localhost:8080).
You should see the ClusterCockpit login page:
{{< figure src="./demo-standalone/cc-login-screen.png" alt="ClusterCockpit Login page" class="ccfigure">}}

Enter `demo` for the Username and `demo` for the Password and press the Submit button. After that the ClusterCockpit index page should be displayed:
{{< figure src="./demo-standalone/cc-index-screen.png" alt="ClusterCockpit Index page" class="ccfigure">}}

The demo user has the admin role and therefore can see all views.
{{< alert title="Note" >}}Because the demo only loads data from the job archive some views as the status and systems view do not work!{{< /alert >}}

For details about the features of the web interface have a look at the [user guide](/docs/userguide).

## Installation

## Setup

Is there any initial setup users need to do after installation to try your project?
