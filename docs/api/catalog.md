### [Catalog](https://developer.hashicorp.com/consul/api-docs/catalog)

| Category                               | Endpoint                             | Status 
|----------------------------------------|--------------------------------------| ----- 
| Register Entity                        | `/catalog/register`                  | ✅ 
| Deregister Entity                      | `/catalog/deregister`                | ✅ 
| List Datacenters                       | `/catalog/datacenters`               | ✅ 
| List Nodes                             | `/catalog/nodes`                     | ✅ 
| List Services                          | `/catalog/services`                  | ✅ 
| List Nodes for Service                 | `/catalog/service/:service`          | ✅ 
| List Nodes for Connect-capable Service | `/catalog/connect/:service`          | ✅ 
| Retrieve Map of Services for a Node    | `/catalog/node/:node`                | ✅ 
| List Services for Node                 | `/catalog/node-services/:node`       | ✅ 
| List Services for Gateway              | `/catalog/gateway-services/:gateway` | ✅ 

## Examples

```python
from discovery import Consul

consul = Consul()

# register_entity
await consul.catalog.register_entity(service)

# deregister_entity
await consul.catalog.register_entity(service)

# list datacenters
await consul.catalog.list_datacenters()

# list_nodes
await consul.catalog.list_nodes()

# list services
await consul.catalog.list_services()

# list_nodes_for_service

# list_nodes_for_connect

# services_for_node

# list_services_for_node

# list_services_for_gateway
```
