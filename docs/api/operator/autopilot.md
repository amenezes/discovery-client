### [Autopilot](https://developer.hashicorp.com/consul/api-docs-docs/operator/autopilot)

| Category             | Endpoint                            | Status 
| -------------------- | ----------------------------------- | ------ 
| Read Configuration   | `/operator/autopilot/configuration` | ✅ 
| Update Configuration | `/operator/autopilot/configuration` | ✅ 
| Read Health          | `/operator/autopilot/health`        | ✅ 
| Read the Autopilot State | `/operator/autopilot/state` | ✅ 

## Examples

```python
from discovery import Consul

consul = Consul()


# read_configuration
await consul.operator.autopilot.read_configuration()

# update_configuration
await consul.operator.autopilot.update_configuration()

# read_health
await consul.operator.autopilot.read_health()

# read_state
await consul.operator.autopilot.read_state()
```
