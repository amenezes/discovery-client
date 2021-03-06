import asyncio
import logging

from aiohttp import web

from discovery.aioclient import Consul
from discovery.service import Service
from discovery.check import Check, http


async def service_discovery(app):
    app.loop.create_task(dc.register())
    asyncio.sleep(15)
    app.loop.create_task(dc.check_consul_health())


async def handle_info(request):
    return web.json_response({'app': 'aio-client'})


async def handle_status(request):
    return web.json_response({'status': 'UP'})


async def handle_services(request):
    service_name = request.match_info.get('service_name', "consul")
    response = await dc.find_services(service_name)
    return web.json_response(response)


async def handle_service(request):
    service_name = request.match_info.get('service_name', "consul")
    response = {}

    try:
        response = await dc.find_services(service_name)
    except IndexError:
        logging.info(f'Service {service_name} not found!')
    return web.json_response(response)


async def shutdown_server(app):
    app.loop.run_until_complete(dc.deregister())
    app.loop.close()


app = web.Application()

dc = Consul(
    host='discovery',
    port=8500,
    app=app.loop,
    service=Service(
        'aio-client',
        5000,
        check=Check(
            'app-check',
            http('http://aio-client:5000/manage/health')
        )
    )
)

app.on_startup.append(service_discovery)
app.on_shutdown.append(shutdown_server)
app.add_routes([web.get('/manage/health', handle_status),
                web.get('/manage/info', handle_info),
                web.get('/services/{service_name}', handle_services),
                web.get('/service/{service_name}', handle_service)])
web.run_app(app, host='0.0.0.0', port=5000)
