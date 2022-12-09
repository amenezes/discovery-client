## [Config](https://developer.hashicorp.com/consul/api-docs/config)

| Category             | Endpoint              | Status 
| -------------------- | --------------------- | ------ 
| Apply Configuration  | `/config`             | ✅ 
| Get Configuration    | `/config/:kind/:name` | ✅ 
| List Configurations  | `/config/:kind`       | ✅ 
| Delete Configuration | `/config/:kind/:name` | ✅ 


## Usage

```python
from discovery import Consul, Kind


consult = Consul()

# list configurations
await consul.config.list(Kind.SERVICE_DEFAULTS)
```
