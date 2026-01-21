---
title: How to plan and configure resampling
description: Configure metric resampling
categories: [cc-backend]
tags: [Admin]
---

## Overview

### Enable timeseries resampling

ClusterCockpit now supports resampling of time series data to a lower frequency.
This dramatically improves load times for very large or very long jobs and we
recommend to enable it. Resampling is supported for running as well as for
finished jobs. For running jobs this currently only works with the newest
version of `cc-metric-store`. Resampling support for the Prometheus time series
database will be added in the future.

To enable resampling you have to add the following toplevel configuration key:

```json
  "enable-resampling": {
    "trigger": 30,
    "resolutions": [
      600,
      300,
      120,
      60
    ]
  },
```

Trigger configures at which minimum number of points in every timeseries plot
window the next finer level is loaded. Resolutions defines the resolution steps
in seconds. The finest resolution must be the native resolution. In case you
have different native solutions in your metric configuration you should use the
finest. The implementation will fallback to the finest available resolution in
this case.
