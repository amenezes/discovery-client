

# aiohttp

## client

Using aiohttp client on the AIOHTTPEngine. 

```python
from discovery.client import Consul

consul = Consul()

# query a service from catalog filtering by health status
resp = await consul.catalog.service('consul')
resp = await resp.json()
print(resp)
```

## aiohttp server + client

Using discovery-client to display some queries to Consul API.

```python
from aiohttp import web

from discovery import Consul


app = web.Application()
routes = web.RouteTableDef()


async def consul(app):
    consul = Consul()
    app['consul'] = consul


@routes.get('/status/leader')
async def index(request):
    response = await app['consul'].status.leader()
    response = await response.text()
    return web.Response(text=response)


@routes.get('/catalog/service/{service}')
async def svc(request):
    response = await app['consul'].catalog.service(
        f"{request.match_info['service']}"
    )
    response = await response.json()
    return web.json_response(response)


app.add_routes(routes)
app.on_startup.append(consul)
web.run_app(app)
```
