### [Health](https://developer.hashicorp.com/consul/api-docs/health)

Category | Endpoint                   | Status
-------- |----------------------------| ------
List Checks for Node | `/health/node/:node`       | ✅
List Checks for Service  | `/health/checks/:service`  | ✅
List Service Instances for Service  | `/health/service/:service` | ✅
List Service Instances for Connect-enabled Service  | `/health/connect/:service` | ✅
List Service Instances for Ingress Gateways Associated with a Service  | `/health/ingress/:service` | ✅
List Checks in State  | `/health/state/:state` | ✅

## Examples

```python
from discovery import Consul, HealthState


consul = Consul()

# checks_for_node
await consul.health.checks_for_node('7f6d0d2ecb6d')

# checks_for_service
await consul.health.checks_for_service('consul')

# service_instances
await consul.health.service_instances('consul')

# service_instances_for_connect
await consul.health.service_instances_for_connect('consul')

# service_instances_for_ingress
await consul.health.service_instances_for_ingress('consul')

# checks_in_state
await consul.health.checks_in_state()
await consul.health.checks_in_state(HealthState.CRITICAL)
```
