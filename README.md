[![Maintainability](https://api.codeclimate.com/v1/badges/fc7916aab464c8b7d742/maintainability)](https://codeclimate.com/github/amenezes/discovery-client/maintainability)
[![Build Status](https://travis-ci.org/amenezes/discovery-client.svg?branch=master)](https://travis-ci.org/amenezes/discovery-client)

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


dc = Consul('localhost', 8500)
dc.find_service('consul')
````

Integration with Flask + threading.

````python
import threading
import time

from discovery.client import Consul

from flask import Flask


app = Flask(__name__)

dc = Consul('localhost', 8500)
dc.register('myapp', 5000)

@app.before_first_request
def enable_service_registry():
    def probe_discovery_connection():
        while True:
            dc.consul_is_healthy()
            time.sleep(10)
    thread = threading.Thread(target=probe_discovery_connection)
    thread.start()
````

### using asyncio

client using asyncio

````python
import asyncio

from discovery import aioclient


loop = asyncio.get_event_loop()
dc = aioclient.Consul('localhost', 8500, loop)

search_one_task = loop.create_task(dc.find_service('consul'))
search_all_task = loop.create_task(dc.find_services('consul'))
loop.run_until_complete(search_one_task)
loop.run_until_complete(search_all_task)
````

### using aiohttp

server using iohttp + asyncio

````python
import asyncio

from aiohttp import web

from discovery.aioclient import Consul


async def service_discovery(app):
    app.loop.create_task(dc.register('myapp', 5000))


async def handle_info(request):
    return web.json_response({'app': 'myapp'})


async def handle_status(request):
    return web.json_response({'status': 'UP'})


app = web.Application()
dc = Consul('localhost', 8500, app.loop)

app.on_startup.append(service_discovery)
app.add_routes([web.get('/manage/health', handle_info),
                web.get('/manage/info', handle_status)])
web.run_app(app, host='0.0.0.0', port=5000)
````

## Links

- License: [Apache License](https://choosealicense.com/licenses/apache-2.0/)
- Code: https://github.com/amenezes/discovery-client
- Issue tracker: https://github.com/amenezes/discovery-client/issues