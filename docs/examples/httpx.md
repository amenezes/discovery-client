# httpx

Using httpx async client on the AIOHTTPEngine. 

```python
from discovery.client import Consul
from discovery.engine import HTTPXEngine


consul = Consul(client=HTTPXEngine())

resp = await consul.catalog.service('consul')
resp = await resp.json()
print(resp)
```

## Flask + httpx

Using discovery-client to display some queries to Consul API.

```python
import asyncio

from flask import Flask, jsonify
import httpx

from discovery.client import Consul
from discovery.engine import HTTPXEngine


loop = asyncio.get_event_loop()
app = Flask(__name__)

consul = Consul(client=HTTPXEngine())


@app.route('/status/leader')
def leader():
    response = loop.run_until_complete(consul.status.leader())
    response = loop.run_until_complete(response.text())
    return response

@app.route('/catalog/service/<service>')
def catalog(service):
    response = loop.run_until_complete(
        consul.catalog.service(service)
    )
    response = loop.run_until_complete(response.json())

    return jsonify(response)
```
