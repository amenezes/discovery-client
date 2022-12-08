## 🚨 [License](https://developer.hashicorp.com/consul/api-docs/operator/license)

Category | Endpoint | Status
-------- | -------- | ------
Getting the Consul License | `/operator/license` | ✅
Update the Consul License | `/operator/license` | ✅
Resetting the Consul License | `/operator/license` | ✅

## Usage

```python
from discovery import Consul

consul = Consul()


# current
await consul.operator.license.current()

# update_configuration
await consul.operator.autopilot.update_configuration()

# update
my_license = b'mylicense'
await consul.operator.license.update(my_license)

# reset
await consul.operator.license.reset()
```
