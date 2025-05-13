---
title: Tags
description: >
  Lists Active Tags Used in the Frontend
categories: [cc-backend]
tags: [Frontend, User, Manager, Support, Admin]
weight: 11
---

{{< figure src="../../figures/tags.png" alt="Tag List View" width="100%" class="ccfigure mw-md">}}

This view lists all tags currently used within the ClusterCockpit instance:

* The `Tag Type` of the tag(s) is displayed as dark grey header, collecting all tags which share it, with a total count shown on the right.
* The `Name`s of all tags sharing one `Tag Type`, the number of matching jobs per name, and the scope are rendered as pills below the header, colored accordingly (see below).

Each tags' pill is clickable, and leads to a [job list]({{< ref "joblist" >}} "Job List") with a preset filter matching only jobs tagged with this specific label.

### Tag Scopes

Tags are categorized into three "Scopes" of visibility, and colored accordingly:

* Admin (Cyan): Only administrators can create and attach these tags. Only visible for administrators and support personnel.
* Global (Purple): Administrators and support personnel can create and attach these tags. Visible for everyone.
* Private (Yellow): Everyone can create and attach private tags, only visible to the creator.

### Remove Tags

Tags and all job attachements can be removed from the database if a red `X` symbol is attached to the tags' pill. A confirmation popup will appear after which the tag and all attachements are deleted, and the tag is removed from th list.

The following rules apply:

* Only _Administrators_ are authorized to remove tags with scopes "global" and "admin" via this functionality in this view.
* _Managers_ and _Support-Personnel_ can _not_ remove "global" and "admin" tags from the database this way.
* _Every User_, including staff, _can_ remove their own "private" tags (but not those of other users).

{{< alert >}}*Please note:* Creating tags and adding/removing them to/from jobs is either done by using the respective REST API calls, or manually from the [job view]({{< ref "job#tagging" >}} "Job View Tag Create").{{< /alert >}}