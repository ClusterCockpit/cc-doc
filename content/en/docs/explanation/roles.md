---
title: Roles
description: >
 Description of roles used in the web interface
---

ClusterCockpit uses a specified set of user roles to steer data access and discriminate authorizations, primarily used in the [web interface]({{< ref "webinterface" >}} "ClusterCockpit Web Interface") for different display of views, but also limiting data access when requsts return from the server backend.

The roles currently implemented are:

### User Role

The standard role for all users. By default, granted to all users imported from LDAP. It is also the default selection for the administrative "Create User" [form]({{< ref "settings#create-user" >}} "Admin: Create User").

*Use Case:* View and list personal jobs, view personal job detail, inspect metrics of personal jobs.

*Access:* Jobs started from the users account only.

### Manager Role

A privileged role for project supervisors. This role has to be granted manually by administrators. If ClusterCockpit is configured to accept JWT logins from external management applications, it is possible to retain roles granted in the respective application, see [JWT docs]({{< ref "jwtoken" >}} "ClusterCockpit JWT Handling").

In addition to the role itself, one ore more projects need to be [assigned]({{< ref "settings#edit-managed-projects" >}} "Add Managed Project") to the user by administrators.

*Use Case:* In addition to personal job access, this role is intended to view and inspect all jobs of all users of the assigned projects (usergroups), in order to self-manage and identify problems of the subordinate user group.

*Access:* Personally started jobs, regardless of project. Additionally, all jobs started from all users of the assigned projects (usergroups).

### Support Role

A privileged role for support staff. This role has to be granted manually by administrators. If ClusterCockpit is configured to accept JWT logins from external management applications, it is possible to retain roles granted in the respective application, see [JWT docs]({{< ref "jwtoken" >}} "ClusterCockpit JWT Handling").

In regard to job view access, this role is identical to administrators. However, webinterface view access differs and, most importantly, acces to administrative options is prohibited.

*Use Case:* In addition to personal job access, this role is intended to view and inspect all jobs of all users active on the clusters, in order to identify problems and give guidance for the userbase as a whole, *supporting* the administrative staff in these tasks.

*Access:* Personally started jobs, regardless of project. Additionally, all jobs started from all users on all configured clusters.

### Administrator Role

The highest available authority for administrative staff only. This role has to be granted manually by other administrators. No JWT can ever grant this role.

All jobs from all active users on all systems can be accessed, as well as all webinterface views. In addition, the administrative options in the [settings view]({{< ref "settings" >}} "ClusterCockpit Settings") are accessible.

*Use Case:* General access and ClusterCockpit administrative tasks from the settings page.

*Access:* General access.

### API Role

An optional, technical role given to users in order to enable usage of the [RESTful API endpoints]({{< ref "rest-api" >}} "ClusterCockpit REST API"). This role has to be granted manually by administrators. No JWT can ever grant this role.

This role can either be granted to a specialized "API User", which does not have a password or any other roles, and therefore, can not log in by itself. Such an user is only intended to be used to generate JWT access tokens for scripted API access, for example.

Still, this role can be granted to actual users, for example, administrators to generate personal API tokens for testing.

*Use Case:* Interact with ClusterCockpits' REST API.

*Access:* Allows usage of ClusterCockpits' REST API.
