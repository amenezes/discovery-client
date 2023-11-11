import logging
import socket

from aiohttp import web

from discovery import Consul, checks
from discovery.utils import Service

app = web.Application()
routes = web.RouteTableDef()
logging.basicConfig(level=logging.INFO)


async def register(app: web.Application) -> None:
    logging.info("Registering the eservice")
    app_service = Service(
        name="app",
        port=8080,
        address="",
        check=checks.http(
            f"http://{socket.gethostbyname(socket.gethostname())}:8080/health",
            timeout="15s",
            interval="10s",
        ),
    )
    consul = Consul()
    await consul.register(app_service)

    app["app_service"] = app_service
    app["consul"] = consul
    logging.info("Registered service")


async def deregister(app: web.Application) -> None:
    logging.info("Removing service registration")
    await app["consul"].deregister(app["app_service"].id)
    logging.info("Registered removed")


@routes.get("/")  # type: ignore
def home(request: web.Request) -> web.Response:
    body = """
    <html>
      <body>
      <p>discovery-client | aiohttp integration</p>
      <p>sample endpoints</p>
      <ul>
        <li><a href="http://localhost:8080/health">/health</a></li>
      </ul>
      </body>
    </html>
    """
    return web.Response(text=body, content_type="text/html")


@routes.get("/health")  # type: ignore
def health(request: web.Request) -> web.Response:
    return web.json_response({"status": "UP"})


app.add_routes(routes)
app.on_startup.append(register)
app.on_shutdown.append(deregister)
web.run_app(app)
