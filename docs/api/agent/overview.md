### [Agent](https://developer.hashicorp.com/consul/api-docs/agent)

| Category                    | Endpoint                   | Status 
|-----------------------------|----------------------------| ------ 
| Host information            | `/agent/host`              | ✅ 
| List Members                | `/agent/members`           | ✅ 
| Read Configuration          | `/agent/self`              | ✅ 
| Reload Agent                | `/agent/reload`            | ✅ 
| Enable Maintenance Mode     | `/agent/maintenance`       | ✅ 
| View Metrics                | `/agent/metrics`           | ✅ 
| Stream Logs                 | `/agent/monitor`           | ✅ 
| Join Agent                  | `/agent/join/:address`     | ✅ 
| Graceful Leave and Shutdown | `/agent/leave`             | ✅ 
| Force Leave and Shutdown    | `/agent/force-leave/:node` | ✅ 
| Update ACL Tokens           | `/token/acl_token`         | ✅ 
