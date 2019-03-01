import asyncio

from aiohttp import web

from discovery.aioclient import Consul


async def service_discovery(app):
    app.loop.create_task(dc.register('aio-client', 5000))
    asyncio.sleep(15)
    app.loop.create_task(dc.consul_is_healthy())


async def handle_info(request):
    return web.json_response({'app': 'aio-client'})


async def handle_status(request):
    return web.json_response({'status': 'UP'})


app = web.Application()
dc = Consul('discovery', 8500, app.loop)

app.on_startup.append(service_discovery)
app.add_routes([web.get('/manage/health', handle_status),
                web.get('/manage/info', handle_info)])
web.run_app(app, host='0.0.0.0', port=5000)
