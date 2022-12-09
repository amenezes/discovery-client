## [ACL](https://developer.hashicorp.com/consul/api-docs/acl)

Category | Endpoint | Status 
-------- | ------|-------- 
Bootstrap ACLs | `/acl/bootstrap` | ✅ 
Check ACL Replication | `/acl/replication` | ✅ 
Translate Rules | `/acl/rules/translate` | ✅ 
Translate a Legacy Token's Rules | `/acl/rules/translate/:accessor_id` | ❌ 
Login to Auth Method | `/acl/login` | ❌ 
Logout from Auth Method | `/acl/logout` | ❌
OIDC Authorization URL Request | `/acl/logout` | ❌
OIDC Callback | `/acl/logout` | ❌

## Usage

```python
from discovery import Consul


consul = Consul()

# bootstrap
await consul.acl.bootstrap()

# replication
await consul.acl.replication()

# translate
await consul.acl.translate({"policy": "read"})
```
