---
title: Settings
description: >
  Webinterface Settings Page
categories: [cc-backend]
tags: [Frontend, General, Admin]
weight: 1
---

The settings view allows [non-privileged users]({{< ref "roles#user-role" >}} "User Role") to choose their preferred paging style, to customize how metric plots are rendered, and to generate personalized tokes for use with the [API]({{< ref "rest-api" >}} "CC-Backend API"). Customization options include line width, number of plots per row (where applicable), whether backgrounds should be colored, and the color scheme of multi-line metric plots.

[Privileged users]({{< ref "roles#administrator-role" >}} "Admin Role") will also find an [administrative interface]({{< ref "#administration-options" >}} "Administration Options") for handling local user accounts. This includes creating local accounts from the interface, editing user roles, listing and deleting existing users, generating JSON Web Tokens for API usage, and delegating managed projects for [manager role]({{< ref "roles#manager-role" >}} "Manager Role") users.

## User Options

|Field|Options|Note|
|---|---|---|
|Paging Type|Classic / Continuous|Style of paging in job lists|
|Line Width|# Pixels|Width of the lines in the timeseries plots|
|Plots Per Row|# Plots|How many plots to show next to each other on pages such as the [job]({{< ref "job" >}} "Job View") or [nodes]({{< ref "nodes" >}} "Nodes View") views|
|Colored Backgrounds|Yes / No|Color plot backgrounds indicating mean values within warning thresholds|
|Color Scheme|See Below|Render multi-line metric plots in different color ranges|

### Generate JWT

This function will generate and return a personalized JWT, printed into the "Display JWT" field.

If working with the [ClusterCockpit API]({{< ref "rest-api" >}} "CC-Backend API"), this token is required to authorize the user against the REST API endpoints.

### Color Schemes

<table>
  <tr>
    <th>Name</th>
    <th>Colors</th>
  </tr>
  <tr>
    <td>Default</td>
    <td>
      <span  style="background-color: rgb(0, 191, 255);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(0, 0, 255);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(255, 0, 255);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(255, 0, 0);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(255, 128, 0);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(255, 255, 0);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(128, 255, 0);">&nbsp;&nbsp;&nbsp;</span>
    </td>
  </tr>
  <tr>
    <td>Autumn</td>
    <td>
      <span  style="background-color: rgb(255, 0, 0);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(255, 11, 0);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(255, 20, 0);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(255, 30, 0);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(255, 41, 0);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(255, 50, 0);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(255, 60, 0);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(255, 71, 0);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(255, 80, 0);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(255, 90, 0);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(255, 101, 0);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(255, 111, 0);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(255, 120, 0);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(255, 131, 0);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(255, 141, 0);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(255, 150, 0);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(255, 161, 0);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(255, 171, 0);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(255, 180, 0);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(255, 190, 0);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(255, 201, 0);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(255, 210, 0);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(255, 220, 0);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(255, 231, 0);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(255, 240, 0);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(255, 250, 0);">&nbsp;&nbsp;&nbsp;</span>
    </td>
  </tr>
  <tr>
    <td>Beach</td>
    <td>
      <span  style="background-color: rgb(0, 252, 0);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(0, 233, 0);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(0, 212, 0);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(0, 189, 0);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(0, 169, 0);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(0, 148, 0);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(0, 129, 4);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(0, 145, 46);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(0, 162, 90);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(0, 180, 132);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(29, 143, 136);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(73, 88, 136);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(115, 32, 136);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(81, 9, 64);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(124, 51, 23);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(162, 90, 0);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(194, 132, 0);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(220, 171, 0);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(231, 213, 0);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(0, 0, 13);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(0, 0, 55);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(0, 0, 92);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(0, 0, 127);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(0, 0, 159);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(0, 0, 196);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(0, 0, 233);">&nbsp;&nbsp;&nbsp;</span>
    </td>
  </tr>
  <tr>
    <td>BlueRed</td>
    <td>
      <span  style="background-color: rgb(0, 0, 131);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(0, 0, 168);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(0, 0, 208);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(0, 0, 247);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(0, 27, 255);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(0, 67, 255);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(0, 108, 255);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(0, 148, 255);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(0, 187, 255);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(0, 227, 255);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(8, 255, 247);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(48, 255, 208);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(87, 255, 168);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(127, 255, 127);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(168, 255, 87);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(208, 255, 48);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(247, 255, 8);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(255, 224, 0);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(255, 183, 0);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(255, 143, 0);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(255, 104, 0);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(255, 64, 0);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(255, 23, 0);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(238, 0, 0);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(194, 0, 0);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(150, 0, 0);">&nbsp;&nbsp;&nbsp;</span>
    </td>
  </tr>
  <tr>
    <td>Rainbow</td>
    <td>
      <span  style="background-color: rgb(125, 0, 255);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(85, 0, 255);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(39, 0, 255);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(0, 6, 255);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(0, 51, 255);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(0, 97, 255);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(0, 141, 255);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(0, 187, 255);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(0, 231, 255);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(0, 255, 233);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(0, 255, 189);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(0, 255, 143);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(0, 255, 99);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(0, 255, 53);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(0, 255, 9);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(37, 255, 0);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(83, 255, 0);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(127, 255, 0);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(173, 255, 0);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(217, 255, 0);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(255, 248, 0);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(255, 203, 0);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(255, 159, 0);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(255, 113, 0);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(255, 69, 0);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(255, 23, 0);">&nbsp;&nbsp;&nbsp;</span>
    </td>
  </tr>
  <tr>
    <td>Binary</td>
    <td>
      <span  style="background-color: rgb(215, 215, 215);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(206, 206, 206);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(196, 196, 196);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(185, 185, 185);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(176, 176, 176);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(166, 166, 166);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(155, 155, 155);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(145, 145, 145);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(136, 136, 136);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(125, 125, 125);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(115, 115, 115);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(106, 106, 106);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(95, 95, 95);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(85, 85, 85);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(76, 76, 76);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(66, 66, 66);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(55, 55, 55);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(46, 46, 46);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(36, 36, 36);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(25, 25, 25);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(16, 16, 16);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(6, 6, 6);">&nbsp;&nbsp;&nbsp;</span>
    </td>
  </tr>
  <tr>
    <td>GistEarth</td>
    <td>
      <span  style="background-color: rgb(0, 0, 0);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(2, 7, 117);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(9, 30, 118);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(16, 53, 120);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(23, 73, 122);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(31, 93, 124);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(39, 110, 125);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(47, 126, 127);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(51, 133, 119);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(57, 138, 106);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(62, 145, 94);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(66, 150, 82);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(74, 157, 71);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(97, 162, 77);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(121, 168, 83);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(136, 173, 85);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(153, 176, 88);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(170, 180, 92);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(185, 182, 94);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(189, 173, 99);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(192, 164, 101);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(203, 169, 124);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(215, 178, 149);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(226, 192, 176);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(238, 212, 204);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(248, 236, 236);">&nbsp;&nbsp;&nbsp;</span>
    </td>
  </tr>
  <tr>
    <td>BlueWaves</td>
    <td>
      <span  style="background-color: rgb(83, 0, 215);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(43, 6, 108);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(9, 16, 16);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(8, 32, 25);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(0, 50, 8);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(27, 64, 66);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(69, 67, 178);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(115, 62, 210);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(155, 50, 104);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(178, 43, 41);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(180, 51, 34);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(161, 78, 87);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(124, 117, 187);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(78, 155, 203);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(34, 178, 85);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(4, 176, 2);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(9, 152, 27);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(4, 118, 2);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(34, 92, 85);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(78, 92, 203);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(124, 127, 187);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(161, 187, 87);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(180, 248, 34);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(178, 220, 41);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(155, 217, 104);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(115, 254, 210);">&nbsp;&nbsp;&nbsp;</span>
    </td>
  </tr>
  <tr>
    <td>BlueGreenRedYellow</td>
    <td>
      <span  style="background-color: rgb(0, 0, 0);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(0, 0, 20);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(0, 0, 41);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(0, 0, 62);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(0, 25, 83);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(0, 57, 101);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(0, 87, 101);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(0, 118, 101);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(0, 150, 101);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(0, 150, 69);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(0, 148, 37);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(0, 141, 6);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(60, 120, 0);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(131, 87, 0);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(180, 25, 0);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(203, 13, 0);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(208, 36, 0);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(213, 60, 0);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(219, 83, 0);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(224, 106, 0);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(229, 129, 0);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(233, 152, 0);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(238, 176, 0);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(243, 199, 0);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(248, 222, 0);">&nbsp;&nbsp;&nbsp;</span><span  style="background-color: rgb(254, 245, 0);">&nbsp;&nbsp;&nbsp;</span>
    </td>
  </tr>
</table>

## Admin Options

### Create User

New users can be created directly via the web interface. On successful creation a green response message will be returned, and the user is directly visible in the "Special Users" table - If the user has at least two roles, or a single role other than `user`.

Error messages will also be displayed if the user creation process failed. No user account is saved to the database in this case.

{{< alert >}} *Please note:* Users are usually imported via LDAP on ClusterCockpit startup.{{< /alert >}}

|Field|Option|Note|
|-----|------|----|
|Username (ID)|`string`|**Required**, must be unique|
|Password|`string`|Only API users are allowed to have a blank password, users with a blank password can only authenticate via JW tokens|
|Project|`string`|Only manager users can have a project|
|Name|`string`|Name of the user, optional, can be blank|
|Email Address|`string`|Users email, optional, can be blank|
|Role|Select one|See [roles]({{< ref "roles" >}} "Roles") for more detailed information|
||`API`|Allowed to interact with REST API|
|*Default*|`User`|Same as if created via LDAP sync|
||`Manager`|Allows to inspect jobs and users of given project|
||`Support`|Allows to inspect jobs and users of all projects, has no admin view or settings access|
||`Admin`|General access|

### Special Users

{{< figure src="../figures/specialusers.png" alt="ClusterCockpit Special Users Table" width="100%" class="ccfigure mw-lg" >}}

This table does not contain users who only have `user` as their only role saved in the database. This is the case for all users created by LDAP import, and thus, these users will not be shown here. However, LDAP users' roles can still be [edited]({{< ref "#edit-user-roles" >}} "Edit Roles"), and will appear in the table as soon as a authority higher than `user` or two authorities were granted.

All other special case users, e.g. new users manually created with `support` role, will appear in the list.

User accounts can be deleted by pressing the respective function displayed for each user entry - A verification pop-up window will appear to stop accidental user deletion.

Additionally, JWT tokens for specific users can be generated here as well.

|Column|Example|Description|
|---|---|---|
|Username|`abcd1`|Username of this user|
|Name|`Paul Atreides`|Name of this user|
|Project(s)|`abcd`|Managed project(s) of this user|
|Email|`demo@demo.com`|Email adress of this user|
|Roles|`admin,api`|Role(s) of this user|
|JWT|Press button to reveal freshly generated token|Generate a JWT for this user for use with the CC REST API endpoints|
|Delete|Press button to verify deletion|Delete this user|

### Edit User Role

On creation, users can only have one role. However, it is allowed to assign multiple roles to an user account. The addition or removal of roles is performed here.

Enter an existing `username` and select an existing (for removal) or new (for addition) role in the drop-down menu.

Then press the respective button to remove or add the selected authority from the user account. Errors will be displayed if existing roles are added or non-existing roles are removed.

### Edit Managed Projects

On creation, users can only have one managed project. However, it is allowed to assign multiple projects to a manager account. The addition or removal of projects is performed here.

Enter an existing `username` and select an existing (for removal) or new (for addition) project by entering the respective `projectId`.

Then press the respective button to remove or add the selected project from the manager account. Errors will be displayed if existing projects are added, non-existing projects are removed, or if the user account is not authorized to manage projects at all.

### Scramble Names (Presentation Mode)

Activating this switch will replace all user names, person names, and project names with random strings. Intended for presentations on a production system while retaining critical information from a publc audience.

### Metric Plot Resampling

If "Resampling" of metric plots is enabled in the configuration file (`config.json`), and read correctly on start-up, this informational display will list both the amount of data points on whichthe next resolution will be requested ("Trigger") as well as the applicable resolutions themselves.

*Note*: Changes to the resampling options have to be perfofmed by changing the configuration file and restarting the application.

### Edit Notice Shown On Homepage

The contents of the text form field will be written into `$CCPATH/var/notice.txt` on submission. If this file does not exist, it will be created.

If any content is found, an informational card will be rendered above the home site table. The content will also be mirrored within the form field itself.

Removing any content from the form field, and submitting, will clear the file and remove the rendered card from the homepage. This state is indicated by the placeholder text "No Content." being shown in the form field.
