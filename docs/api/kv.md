# Reference

- [KV Store Endpoints](https://www.consul.io/api-docs/kv)

### Read Key

```python
from discovery.client import Consul


consul = Consul()
# read key
resp = await consul.kv.read('mysecret')
await resp.json()
# [{'LockIndex': 0, 'Key': 'mysecret', 'Flags': 0, 'Value': 'bXkgc3VwZXIgc2VjcmV0', 'CreateIndex': 825, 'ModifyIndex': 825}]

# read key value
await consul.kv.read_value('mysecret')
# b'my super secret'
```

### Create/Update Key

```python
from discovery.client import Consul


consul = Consul()
# create key
await consul.kv.create("mysecret", "my super secret")

# update key
await consul.kv.update("mysecret", "my super secret")
```

### Delete Key

```python
from discovery.client import Consul


consul = Consul()
# delete delete
await consul.kv.delete("mysecret")
```
