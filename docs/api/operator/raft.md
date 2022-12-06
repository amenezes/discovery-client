### [Raft](https://developer.hashicorp.com/consul/api-docs-docs/operator/raft)

| Category           | Endpoint                       | Status 
| ------------------ | ------------------------------ | ------ 
| Read Configuration | `/operator/raft/configuration` | ✅ 
| Delete Raft Peer   | `/operator/raft/peer`          | ✅ 

## Examples

```python
from discovery.client import Consul


consul = Consul()

# read_configuration
await consul.operator.raft.read_configuration()

# delete_peer
await consul.operator.raft.delete_peer()
```
