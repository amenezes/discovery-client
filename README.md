# discovery-client

discovery-client package sync/async for [consul](https://consul.io).

## Installing

Install and update using pip:

````bash
pip install -U discovery-client
````

## Dependencies

- [python-consul](https://python-consul.readthedocs.io/en/latest)

### Async client only 
  - [asyncio](https://docs.python.org/3.6/library/asyncio.html)
  - [aiohttp](https://aiohttp.readthedocs.io/en/stable)

## Usage Example

### using standard client

````python
from discovery.client import Consul


discovery_client = Consul('localhost', 8500)
discovery_client.register('myapp', 5000)
discovery_client.find_service('consul')
````

Integration with Flask + threading.

````python
import threading
import time

from discovery.client import Consul
from flask import Flask


app = Flask(__name__)
discovery_client = Consul('localhost', 8500)
discovery_client.register('myapp', 5000)

@app.before_first_request
def enable_service_registry():
    def probe_discovery_connection():
        while True:
            discovery_client.consul_is_healthy()
            time.sleep(10)
    thread = threading.Thread(target=probe_discovery_connection)
    thread.start()
````

### using asyncio

client using asyncio

````python
import asyncio
from discovery.aioclient import Consul


loop = asyncio.get_event_loop()

async def service_discovery():
    await discovery_client.register('myapp', 5000)

discovery_client = Consul('localhost', 8500, loop)
loop.run_until_complete(service_discovery)
````

### using aiohttp

server using iohttp + asyncio

````python
from discovery.aioclient import Consul
from aiohttp import web

import asyncio


async def service_discovery():
    await discovery_client.register('myapp', 5000)

async def handle(request):
    name = request.match_info.get('name', 'Anonymous')
    text = "Hello, " + name
    return web.Response(text=text)

app = web.Application()
app.on_startup(service_discovery)
app.add_routes([web.get('/', handle),
                web.get('/{name}', handle)])
web.run_app(app)
````

## Links

- License: [Apache License](https://choosealicense.com/licenses/apache-2.0/)
- Code: https://github.com/amenezes/discovery-client
- Issue tracker: https://github.com/amenezes/discovery-client/issues
