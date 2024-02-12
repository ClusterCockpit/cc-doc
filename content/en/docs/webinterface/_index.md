---
title: Web Interface
description: How to use the web interface?
categories: [cc-backend]
tags: [Frontend, General]
weight: 3
---

## Home

{{< figure src="figures/home_table.png" alt="ClusterCockpit Home Table" width="100%" class="ccfigure mw-lg"
    caption="ClusterCockpit home table for two configured clusters"
>}}

The entrypoint for each login via the login mask is a table containing each configured cluster as a row with the following columns:

* **Name**: The configured clusters' name
* **Running Jobs**: Number of Jobs currently running longer than 5 minutes (or configured `shortRunning` amount of time)
  * Clicking the Link will forward to the [job list]({{< ref "views/joblist" >}} "Job List") with preset filters for cluster and running jobs
* **Total Jobs**: Number of Jobs in the respective job-archive
  * Clicking the Link will forward to the [job list]({{< ref "views/joblist" >}} "Job List") with preset filter for cluster
* **Status View**: Link to the [status view]({{< ref "views/status" >}} "Status View") of the respective cluster
  * This column is only shown for users with [admin]({{< ref "roles#administrator-role" >}} "Nodes View") authority.
* **Systems View**: Link to the [nodes view]({{< ref "views/nodes" >}} "Nodes View") view of the respective cluster
  * This column is only shown for users with [admin]({{< ref "roles#administrator-role" >}} "Nodes View") authority.

## Navigation Bar

The navigation bar allows direct access to ClusterCockpits' different views and functions. Depending on the users' authorization, the selectable views can differ.

For most viewports, the navigation bar is rendered fully expanded:

{{< figure src="figures/navbar.png" alt="ClusterCockpit Expanded Navbar" width="100%" class="ccfigure mw-xl" >}}

|Item|Title|Description|
|----|-----|-----------|
|**1**|Home Button|Leads back to the [home table]({{< ref "#home" >}} "Home Table")|
|**2**|Views|Leads to ClusterCockpits' different [views]({{< ref "views" >}} "Views"), will change dependent on user authority|
|**3**|Searchbar|Top-Level Searchbar, see full usage information [here]({{< ref "searchbar" >}} "Searchbar")|
|**4**|Logout|Logs out the active user|
|**5**|Settings|Leads to ClusterCockpit [settings]({{< ref "settings" >}} "Settings") page|

### Adaptive Render Versions

On smaller viewports, the navigation bar will be rendered in one of two collapsed states: 

{{< figure src="figures/navbar_views_collapsed.png" alt="ClusterCockpit Collapsed Navbar" width="100%" class="ccfigure mw-sm"
    caption="Partially collapsed navigation bar. 'Groups' will expand to show links for Users, Projects, Tags, and Nodes views. 'Stats' will expand to show links for Analysis and Status views. Searchbar, Logout and Settings not shown here, but are still rendered explicitly in this case."
>}}

{{< figure src="figures/navbar_burger.png" alt="ClusterCockpit Burger Navbar" width="100%" class="ccfigure mw-sm"
    caption="On mobile devices, the navigation bar as a whole is reduced into a burger navigation icon, and will display all views, as well as the searchbar, as stacked navigation menu."
>}}
