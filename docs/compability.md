# Compability Matrix

Reference: [Consul HTTP API](https://www.consul.io/api-docs)

### [ACL](https://www.consul.io/api/acl/acl.html)

Category | Endpoint | Status 
-------- | ------|-------- 
Bootstrap ACLs | `/acl/bootstrap` | ✅ 
Check ACL Replication | `/acl/replication` | ✅ 
Translate Rules | `/acl/rules/translate` | ✅ 
Translate a Legacy Token's Rules | `/acl/rules/translate/:accessor_id` | ❌ 
Login to Auth Method | `/acl/login` | ❌ 
Logout from Auth Method | `/acl/logout` | ❌ 

#### [Tokens](https://www.consul.io/api/acl/tokens.html)

| Category        | Endpoint                       | Status |
| --------------- | ------------------------------ | ------ |
| Create a Token  | `/acl/token`                   | ✅     |
| Read a Token    | `/acl/token/:AccessorID`       | ✅     |
| Read Self Token | `/acl/token/self`              | ❌     |
| Update a Token  | `/acl/token/:AccessorID`       | ✅     |
| Clone a Token   | `/acl/token/:AccessorID/clone` | ❌     |
| Delete a Token  | `/acl/token/:AccessorID`       | ✅ |
| List Tokens     | `/acl/tokens`                  | ✅ |

#### [Legacy Tokens](https://www.consul.io/api/acl/legacy.html)

| Category         | Endpoint             | Status |
| ---------------- | -------------------- | ------ |
| Create ACL Token | `/acl/create`        | ❌     |
| Update ACL Token | `/acl/update`        | ❌     |
| Delete ACL Token | `/acl/destroy/:uuid` | ❌     |
| Read ACL Token   | `/acl/info/:uuid`    | ❌     |
| Clone ACL Token  | `/acl/clone/:uuid`   | ❌     |
| List ACLs        | `/acl/list`          | ❌     |

#### [Policies](https://www.consul.io/api/acl/policies.html)

| Category        | Endpoint          | Status |
| --------------- | ----------------- | ------ |
| Create a Policy | `/acl/policy`     | ✅     |
| Read a Policy   | `/acl/policy/:id` | ✅     |
| Update a Policy | `/acl/policy/:id` | ✅     |
| Delete a Policy | `/acl/policy/:id` | ✅     |
| List Policies   | `/acl/policies`   | ✅     |

#### [Roles](https://www.consul.io/api/acl/roles.html)

| Category            | Endpoint               | Status |
| ------------------- | ---------------------- | ------ |
| Create a Role       | `/acl/role`            | ✅      |
| Read a Role         | `/acl/role/:id`        | ✅      |
| Read a Role by Name | `/acl/role/name/:name` | ✅      |
| Update a Role       | `/acl/role/:id`        | ✅      |
| Delete a Role       | `/acl/role/:id`        | ✅      |
| List Roles          | `/acl/roles`           | ✅      |

#### [Auth Methods](https://www.consul.io/api/acl/auth-methods.html)

| Category              | Endpoint                 | Status |
| --------------------- | ------------------------ | ------ |
| Create an Auth Method | `/acl/auth-method`       | ✅      |
| Read an Auth Method   | `/acl/auth-method/:name` | ✅      |
| Update an Auth Method | `/acl/auth-method/:name` | ✅      |
| Delete an Auth Method | `/acl/auth-method/:name` | ✅      |
| List Auth Methods     | `/acl/auth-methods`      | ✅      |

#### [Binding Rules](https://www.consul.io/api/acl/binding-rules.html)

| Category              | Endpoint                | Status |
| --------------------- | ----------------------- | ------ |
| Create a Binding Rule | `/acl/binding-rule`     | ✅     |
| Read a Binding Rule   | `/acl/binding-rule/:id` | ✅     |
| Update a Binding Rule | `/acl/binding-rule/:id` | ✅     |
| Delete a Binding Rule | `/acl/binding-rule/:id` | ✅     |
| List Binding Rules    | `/acl/binding-rules`    | ✅     |

### [Agent](https://www.consul.io/api/agent.html)

| Category                    | Endpoint                   | Status |
| --------------------------- | -------------------------- | ------ |
| List Members                | `/acl/members`             | ✅     |
| Read Configuration          | `/agent/self`              | ✅     |
| Reload Agent                | `/agent/reload`            | ✅     |
| Enable Maintenance Mode     | `/agent/maintenance`       | ✅     |
| View Metrics                | `/agent/metrics`           | ✅     |
| Stream Logs                 | `/agent/monitor`           | ❌     |
| Join Agent                  | `/agent/join/:address`     | ✅     |
| Graceful Leave and Shutdown | `/agent/leave`             | ✅     |
| Force Leave and Shutdown    | `/agent/force-leave/:node` | ✅     |
| Update ACL Tokens           | `/token/acl_token`         | ✅     |

#### [Checks](https://www.consul.io/api/agent/check.html)

| Category                | Endpoint               | Status |
| ----------------------- | ---------------------- | ------ |
| List Checks             | `/agent/check`         | ✅     |
| Register Check          | `/agent/check/register`| ✅     |
| Deregister Check        | `/agent/check/deregister/:check_id` | ✅ |
| TTL Check Pass | `/agent/check/pass/:check_id`   | ✅     |
| TTL Check Warn          | `/agent/check/warn/:check_id`   | ✅ |
| TTL Check Fail          | `/agent/check/fail/:check_id`   | ✅ |
| TTL Check Update        | `/agent/check/update/:check_id` | ✅ |

#### [Services](https://www.consul.io/api/agent/service.html)

| Category                           | Endpoint                                   | Status |
| ---------------------------------- | ------------------------------------------ | ------ |
| List Services                      | `/agent/services`                          | ✅     |
| Get Service Configuration          | `/agent/service/:service_id`               | ✅     |
| Get local service health           | `/agent/health/service/name/:service_name` | ✅     |
| Get local service health by its ID | `/agent/health/service/id/:service_id`     | ✅     |
| Register Service                   | `/agent/service/register`                  | ✅     |
| Deregister Service                 | `/agent/service/deregister/:service_id`    | ✅     |
| Enable Maintenance Mode            | `/agent/service/maintenance/:service_id`   | ✅     |

#### [Connect](https://www.consul.io/api/agent/connect.html)

| Category                         | Endpoint                          | Status |
| -------------------------------- | --------------------------------- | ------ |
| Authorize                        | `/agent/connect/authorize`        | ✅      |
| Certificate Authority (CA) Roots | `/agent/connect/ca/roots`         | ✅      |
| Service Leaf Certificate         | `/agent/connect/ca/leaf/:service` | ✅      |

### [Catalog](https://www.consul.io/api/catalog.html)

| Category                               | Endpoint                       | Status |
| -------------------------------------- | ------------------------------ | ------ |
| Register Entity                        | `/catalog/register`            | ✅      |
| Deregister Entity                      | `/catalog/deregister`          | ✅      |
| List Datacenters                       | `/catalog/datacenters`         | ✅      |
| List Nodes                             | `/catalog/nodes`               | ✅      |
| List Services                          | `/catalog/services`            | ✅      |
| List Nodes for Service                 | `/catalog/service/:service`    | ✅      |
| List Nodes for Connect-capable Service | `/catalog/connect/:service`    | ✅      |
| Retrieve Map of Services for a Node    | `/catalog/node/:node`          | ❌      |
| List Services for Node                 | `/catalog/node-services/:node` | ❌      |

### [Config](https://www.consul.io/api/config.html)

| Category             | Endpoint              | Status |
| -------------------- | --------------------- | ------ |
| Apply Configuration  | `/config`             | ✅      |
| Get Configuration    | `/config/:kind/:name` | ✅      |
| List Configurations  | `/config/:kind`       | ✅      |
| Delete Configuration | `/config/:kind/:name` | ✅      |

### [Connect](https://www.consul.io/api/connect.html)

#### [Certificate Authority (CA)]()

| Category                  | Endpoint                    | Status |
| ------------------------- | --------------------------- | ------ |
| List CA Root Certificates | `/connect/ca/roots`         | ✅      |
| Get CA Configuration      | `/connect/ca/configuration` | ✅      |
| Update CA Configuration   | `/connect/ca/configuration` | ✅      |

#### [Intentions](https://www.consul.io/api/connect/intentions.html)

| Category                 | Endpoint                    | Status |
| ------------------------ | --------------------------- | ------ |
| Create Intention         | `/connect/intentions`       | ✅      |
| Read Specific Intention  | `/connect/intentions/:uuid` | ✅      |
| List Intentions          | `/connect/intentions`       | ✅      |
| Update Intention         | `/connect/intentions/:uuid` | ✅      |
| Delete Intention         | `/connect/intentions/:uuid` | ✅      |
| Check Intention Result   | `/connect/intentions/check` | ✅      |
| List Matching Intentions | `/connect/intentions/match` | ✅      |

### [Coordinates](https://www.consul.io/api/coordinate.html)

Category | Endpoint | Status
-------- | -------- | ------
Read WAN Coordinates | `/coordinate/datacenters` | ✅ 
Read LAN Coordinates for all nodes | `/coordinate/nodes` | ✅ 
Read LAN Coordinates for a node | `/coordinate/node/:node` | ✅ 
Update LAN Coordinates for a node | `/coordinate/update` | ✅ 

### [Discovery Chain](https://www.consul.io/api/discovery-chain.html)

Category | Endpoint | Status
-------- | -------- | ------
Read Compiled Discovery Chain | `/discovery-chain/:service` | ❌

### [Events](https://www.consul.io/api/event.html)

| Category    | Endpoint                    | Status |
| ----------- | --------------------------- | ------ |
| Fire Event  | `/discovery-chain/:service` | ✅     |
| List Events | `/event/list`               | ✅     |

### [Health](https://www.consul.io/api/health.html)

Category | Endpoint | Status
-------- | -------- | ------
List Checks for Node | `/health/node/:node` | ✅
List Checks for Service  | `/health/checks/:service` | ✅
List Nodes for Service  | `/health/service/:service` | ✅
List Nodes for Connect-capable Service  | `/health/connect/:service` | ✅
List Checks in State  | `/health/state/:state` | ✅

### [KV Store](https://www.consul.io/api/kv.html)

Category | Endpoint | Status
-------- | -------- | ------
Read Key | `/kv/:key` | ✅
Create/Update Key | `/kv/:key` | ✅
Delete Key | `/kv/:key` | ✅

### [Operator](https://www.consul.io/api/operator.html)

#### [Area](https://www.consul.io/api-docs/operator/area)

| Category                   | Endpoint                       | Status |
| -------------------------- | ------------------------------ | ------ |
| Create Network Area        | `/operator/area`               | ✅      |
| List Network Areas         | `/operator/area`               | ✅      |
| Update Network Area        | `/operator/area/:uuid`         | ✅      |
| List Specific Network Area | `/operator/area/:uuid`         | ✅      |
| Delete Network Area        | `/operator/area/:uuid`         | ✅      |
| Join Network Area          | `/operator/area/:uuid/join`    | ✅      |
| List Network Area Members  | `/operator/area/:uuid/members` | ✅      |

#### [Autopilot](https://www.consul.io/api-docs/operator/autopilot)

| Category             | Endpoint                            | Status |
| -------------------- | ----------------------------------- | ------ |
| Read Configuration   | `/operator/autopilot/configuration` | ✅      |
| Update Configuration | `/operator/autopilot/configuration` | ✅      |
| Read Health          | `/operator/autopilot/health`        | ✅      |

#### [Keyring](https://www.consul.io/api-docs/operator/keyring)

| Category                             | Endpoint            | Status |
| ------------------------------------ | ------------------- | ------ |
| List Gossip Encryption Keys          | `/operator/keyring` | ✅      |
| Add New Gossip Encryption Key        | `/operator/keyring` | ✅      |
| Change Primary Gossip Encryption Key | `/operator/keyring` | ✅      |
| Delete Gossip Encryption Key         | `/operator/keyring` | ✅      |

#### [License](https://www.consul.io/api-docs/operator/license)

Category | Endpoint | Status
-------- | -------- | ------
Getting the Consul License | `/operator/license` | ✅
Update the Consul License | `/operator/license` | ✅
Resetting the Consul License | `/operator/license` | ✅

#### [Raft](https://www.consul.io/api-docs/operator/raft)

| Category           | Endpoint                       | Status |
| ------------------ | ------------------------------ | ------ |
| Read Configuration | `/operator/raft/configuration` | ✅      |
| Delete Raft Peer   | `/operator/raft/peer`          | ✅      |

#### [Segment](https://www.consul.io/api-docs/operator/segment)

| Category              | Endpoint            | Status |
| --------------------- | ------------------- | ------ |
| List Network Segments | `/operator/segment` | ✅      |

### [Namespaces](https://www.consul.io/api/namespaces.html)

| Category            | Endpoint           | Status |
| ------------------- | ------------------ | ------ |
| Create a Namespace  | `/namespace`       | ✅      |
| Read a Namespace    | `/namespace/:name` | ✅      |
| Update a Namespace  | `/namespace/:name` | ✅      |
| Delete a Namespace  | `/namespace/:name` | ✅      |
| List all Namespaces | `/namespaces`      | ✅      |

### [Prepared Queries](https://www.consul.io/api/query.html)

| Category              | Endpoint | Status |
| --------------------- | -------- | ----- |
| Create Prepared Query | `/query` | ❌      |
| Read Prepared Query   | `/query` | ❌      |

### [Sessions](https://www.consul.io/api/session.html)

Category | Endpoint | Status
-------- | -------- | ------
Create Session | `/session/create` | ✅
Delete Session | `/session/destroy/:uuid` | ✅
Read Session | `/session/info/:uuid` | ✅
List Sessions for Node | `/session/node/:node` | ✅
List Sessions | `/session/list` | ✅
Renew Session | `/session/renew/:uuid` | ✅

### [Snapshots](https://www.consul.io/api/snapshot.html)

Category | Endpoint | Status
-------- | -------- | ------
Generate Snapshot | `/snapshot` | ✅
Restore Snapshot | `/snapshot` | ✅

### [Status](https://www.consul.io/api/status.html)

Category | Endpoint | Status
-------- | -------- | ------
Get Raft Leader | `/Status/leader` | ✅
List Raft Peers | `/Status/peers` | ✅

### [Transactions](https://www.consul.io/api/txn.html)

Category | Endpoint | Status
-------- | -------- | ------
Create Transaction | `/txn` | ✅
