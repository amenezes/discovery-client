### [KV Store](https://developer.hashicorp.com/consul/api-docs/kv)

Category | Endpoint | Status
-------- | -------- | ------
Read Key | `/kv/:key` | ✅
Create/Update Key | `/kv/:key` | ✅
Delete Key | `/kv/:key` | ✅

## Examples

```python
from discovery.client import Consul


consul = Consul()

# create key
await consul.kv.create("mysecret", "my super secret")

# read key
await consul.kv.read('mysecret')

# update key
await consul.kv.update("mysecret", "my new super secret")

# read key value
await consul.kv.read_value('mysecret')

# delete delete
await consul.kv.delete("mysecret")
```
