## [Status](https://developer.hashicorp.com/consul/api-docs/status)

Category | Endpoint         | Status
-------- |------------------| ------
Get Raft Leader | `/status/leader` | ✅
List Raft Peers | `/status/peers`  | ✅

## Usage

```python
from discovery import Consul


consul = Consul()

# leader
await consul.status.leader()

# peers
await consul.status.peers()
```
