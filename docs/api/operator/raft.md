# Reference

- [Raft Operator HTTP API](https://www.consul.io/api-docs/operator/raft)

### Read Configuration

```python
from discovery.client import Consul


consul = Consul()
await consul.operator.raft.read_configuration()
```

### Delete Raft Peer

```python
from discovery.client import Consul


consul = Consul()
await consul.operator.raft.delete_peer()
```
