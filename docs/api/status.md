# Reference

- [Status HTTP API](https://www.consul.io/api-docs/status)

### Get Raft Leader

```python
from discovery.client import Consul


consul = Consul()
await consul.status.leader()
```

### List Raft Peers

```python
from discovery.client import Consul


consul = Consul()
await consul.status.peers()
```
