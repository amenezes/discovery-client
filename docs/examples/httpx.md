# httpx

Using httpx async client. 

```python
from discovery import Consul
from discovery.engine import HTTPXEngine


consul = Consul(client=HTTPXEngine())

resp = await consul.catalog.list_nodes_for_service('consul')
print(resp)
```
