import asyncio
import logging

from aiohttp import web

from discovery.client import Consul
from discovery.engine import HTTPXEngine
from discovery import service, check


async def service_discovery(app):
    asyncio.gather(
        dc.register(app["service"]),
        dc.watch_connection(app["service"])
    )


async def handle_info(request):
    return web.json_response({"app": "aio-client"})


async def handle_status(request):
    return web.json_response({"status": "UP"})


async def handle_services(request):
    service_name = request.match_info.get("service_name", "consul")
    response = await dc.find_services(service_name)
    return web.json_response(response)


async def handle_service(request):
    service_name = request.match_info.get("service_name", "consul")
    response = {}

    try:
        response = await dc.find_services(service_name)
    except IndexError:
        logging.info(f"Service {service_name} not found!")
    return web.json_response(response)


async def shutdown_server(app):
    loop = asyncio.get_event_loop()
    await loop.create_task(dc.deregister(app["service"]))


logging.basicConfig(level=logging.INFO)
app = web.Application()
dc = Consul(client=HTTPXEngine())
app["service"] = service(
    "httpx-client",
    5000,
    check=[
        check.http("http://httpx-client:5000/manage/health"),
        check.alias("aio-client", "aio-client-test-service"),
    ],
)

app.on_startup.append(service_discovery)
app.on_shutdown.append(shutdown_server)
app.add_routes(
    [
        web.get("/manage/health", handle_status),
        web.get("/manage/info", handle_info),
        web.get("/services/{service_name}", handle_services),
        web.get("/service/{service_name}", handle_service),
    ]
)
web.run_app(app, host="0.0.0.0", port=5000)
