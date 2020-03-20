from discovery.__version__ import __version__
from discovery.abc import BaseClient
from discovery.client import Consul
from discovery.engine import AioEngine, Engine, aiohttp_session, httpx_client
from discovery.model.agent.checks import alias, docker, grpc, http, script, tcp, ttl
from discovery.model.agent.service import service
