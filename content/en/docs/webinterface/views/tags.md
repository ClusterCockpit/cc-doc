---
title: Tags
description: >
  Lists Active Tags Used in the Frontend
categories: [cc-backend]
tags: [Frontend, User, Manager, Support, Admin]
weight: 10
---

{{< figure src="../../figures/tags.png" alt="Tag List View" width="100%" class="ccfigure mw-md">}}

This view lists all tags currently used within the ClusterCockpit instance:

* The `Tag Type` of the tag(s) is displayed as dark grey header, collecting all tags which share it, with a total count shown on the right.
* The `Name`s of all tags sharing one `Tag Type`, the number of matching jobs per name, and the scope are rendered as pills below the header, colored accordingly (see below).

Each tags' pill is clickable, and leads to a [job list]({{< ref "joblist" >}} "Job List") with a preset filter matching only jobs tagged with this specific label.

Tags are categorized into three "Scopes" of visibility, and colored accordingly:

* Admin (Cyan): Only administrators can create and attach these tags. Only visible for administrators and support personnel.
* Global (Purple): Administrators and support personnel can create and attach these tags. Visible for everyone.
* Private (Yellow): Everyone can create and attach private tags, only visible to the creator.

{{< alert >}}*Please note:* Creating tags and adding them to jobs is either done by using the respective REST API call, or manually from the [job view]({{< ref "job#tagging" >}} "Job View Tag Create").{{< /alert >}}