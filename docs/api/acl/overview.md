## methods

```python
from discovery.client import Consul


consul = Consul()

# bootstrap
response = await consul.status.leader() # returns discovery.engine.response.

# replication

# translate
await response.text()
```
