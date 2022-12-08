## [Services](https://developer.hashicorp.com/consul/api-docs/agent/service)

| Category                       | Endpoint                                   | Status 
|--------------------------------| ------------------------------------------ | ------ 
| List Services                  | `/agent/services`                          | ✅ 
| Get Service Configuration      | `/agent/service/:service_id`               | ✅ 
| Get local service health by Name | `/agent/health/service/name/:service_name` | ✅ 
| Get local service health by ID | `/agent/health/service/id/:service_id`     | ✅ 
| Register Service               | `/agent/service/register`                  | ✅ 
| Deregister Service             | `/agent/service/deregister/:service_id`    | ✅ 
| Enable Maintenance Mode        | `/agent/service/maintenance/:service_id`   | ✅ 

## Usage

```python
from discovery import Consul


consul = Consul()

# list
await consul.agent.service.list()

# configuration
await consul.agent.service.configuration('my-service-id')

# health_by_name
await consul.agent.service.health_by_name('')

# health_by_id
await consul.agent.service.health_by_id()

# register
await consul.agent.service.register()

# deregister
await consul.agent.service.deregister()

# enable_maintenance
await consul.agent.service.enable_maintenance()
```
