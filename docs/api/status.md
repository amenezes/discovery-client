### [Status](https://developer.hashicorp.com/consul/api-docs/status)

Category | Endpoint         | Status
-------- |------------------| ------
Get Raft Leader | `/status/leader` | ✅
List Raft Peers | `/status/peers`  | ✅

## Examples

```python
from discovery.client import Consul


consul = Consul()

# leader
await consul.status.leader()

# peers
await consul.status.peers()
```
