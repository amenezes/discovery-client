## 🚨 [Namespaces](https://developer.hashicorp.com/consul/api-docs/namespaces)

| Category            | Endpoint           | Status 
| ------------------- | ------------------ | ------ 
| Create a Namespace  | `/namespace`       | ✅ 
| Read a Namespace    | `/namespace/:name` | ✅ 
| Update a Namespace  | `/namespace/:name` | ✅ 
| Delete a Namespace  | `/namespace/:name` | ✅ 
| List all Namespaces | `/namespaces`      | ✅ 


## Usage

```python
from discovery import Consul


consul = Consul()

# leader
await consul.status.leader()

# peers
await consul.status.peers()
```
