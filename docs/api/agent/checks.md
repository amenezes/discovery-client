## Compability Matrix

### [Checks](https://developer.hashicorp.com/consul/api-docs/agent/check)

| Category                | Endpoint               | Status 
| ----------------------- | ---------------------- | ------ 
| List Checks             | `/agent/check`         | ✅ 
| Register Check          | `/agent/check/register`| ✅ 
| Deregister Check        | `/agent/check/deregister/:check_id` | ✅ 
| TTL Check Pass | `/agent/check/pass/:check_id`   | ✅ 
| TTL Check Warn          | `/agent/check/warn/:check_id`   | ✅ 
| TTL Check Fail          | `/agent/check/fail/:check_id`   | ✅ 
| TTL Check Update        | `/agent/check/update/:check_id` | ✅ 

## Examples

```python
from discovery import Consul

consul = Consul()


# list
await consul.agent.checks.list()
await consul.agent.checks.list('ServiceName=="my-service"')

# register
await consul.agent.checks.register()

# deregister
await consul.agent.checks.deregister()

# check_pass
await consul.agent.checks.check_pass('my-check-id')

# check_warn
await consul.agent.checks.check_warn('my-check-id')

# check_fail
await consul.agent.checks.check_fail('my-check-id')

# check_update
await consul.agent.checks.check_update('my-check-id')
```
