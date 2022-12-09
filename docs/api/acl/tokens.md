## [Tokens](https://developer.hashicorp.com/consul/api-docs/acl/tokens)

| Category        | Endpoint                       | Status
| --------------- |--------------------------------| ------
| Create a Token  | `/acl/token`                   | ✅ 
| Read a Token    | `/acl/token/:AccessorID`       | ✅ 
| Read Self Token | `/acl/token/self`              | ✅ 
| Update a Token  | `/acl/token/:AccessorID`       | ✅ 
| Clone a Token   | `/acl/token/:AccessorID/clone` | ✅ 
| Delete a Token  | `/acl/token/:AccessorID`       | ✅ 
| List Tokens     | `/acl/tokens`                  | ✅ 

## [Legacy Tokens](https://developer.hashicorp.com/consul/api-docs/acl/legacy)

| Category         | Endpoint             | Status |
| ---------------- | -------------------- | ------ |
| Create ACL Token | `/acl/create`        | ❌     |
| Update ACL Token | `/acl/update`        | ❌     |
| Delete ACL Token | `/acl/destroy/:uuid` | ❌     |
| Read ACL Token   | `/acl/info/:uuid`    | ❌     |
| Clone ACL Token  | `/acl/clone/:uuid`   | ❌     |
| List ACLs        | `/acl/list`          | ❌     |

## Usage

```python
from discovery import Consul


consul = Consul()

# Create a Token
await consul.acl.token.create(
    "Agent token for 'node1",
    [{"ID": "165d4317-e379-f732-ce70-86278c4558f7"}, {"Name": "node-read"}],
)

# Read a Token
await consul.acl.token.read()

# Read Self Token
await consul.acl.token.details()

# Update a Token
await consul.acl.token.update()

# Clone a Token
await consul.acl.token.clone()

# Delete a Token
await consul.acl.token.delete()

# List Tokens
await consul.acl.token.list()
```
