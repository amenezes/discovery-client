### [Intentions](https://developer.hashicorp.com/consul/api-docs/connect/intentions)

| Category                        | Endpoint                   | Status 
|---------------------------------|----------------------------| ----- 
| Upsert Intention by Name        | `/connect/intentions/exact` | ✅ 
| Create Intention with ID        | `/connect/intentions`      | ❌ 
| Update Intention by ID          | `/connect/intentions/:uuid` | ❌ 
| Read Specific Intention by Name | `/connect/intentions/exact` | ✅ 
| Read Specific Intention by ID   | `/connect/intentions/:uuid` | ❌ 
| List Intentions                 | `/connect/intentions`  | ✅ 
| Delete Intention by Name        | `/connect/intentions/exact` | ✅ 
| Delete Intention by ID          | `/connect/intentions/:uuid` | ❌ 
| Check Intention Result          | `/connect/intentions/check` | ✅ 
| List Matching Intentions        | `/connect/intentions/match` | ✅ 
