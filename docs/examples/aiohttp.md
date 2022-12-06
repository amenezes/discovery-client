

# aiohttp

## client

Using aiohttp client on the AIOHTTPEngine. 

```python
from discovery import Consul

consul = Consul()

# query a service from catalog filtering by health status
resp = await consul.catalog.list_nodes_for_service('consul')
print(resp)
```
