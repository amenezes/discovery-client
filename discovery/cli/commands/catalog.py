import asyncio
import logging
import os
import pickle
import sys
from pathlib import Path

from cleo import Command
from dotenv import load_dotenv

from discovery.client import Consul
from discovery.engine import AioEngine, aiohttp_session

logging.getLogger().addHandler(logging.NullHandler())


load_dotenv()
loop = asyncio.get_event_loop()
session = loop.run_until_complete(aiohttp_session())
client = Consul(AioEngine(session=session))


class CatalogCommand(Command):
    """
    Interact with Consul's catalog.

    catalog
        {--s|services : List services catalog.}
        {--d|deregister= : Deregister services from <file>.}
    """

    def handle(self):
        if self.option("services"):
            self.list_services()
        elif self.option("deregister"):
            self.deregister_service()

    def list_services(self):
        try:
            resp = loop.run_until_complete(client.catalog.services())
        except Exception:
            self.line(
                f"<error>[!]</error> falha ao conectar no Consul({os.getenv('CONSUL_HOST', 'localhost')}:{os.getenv('CONSUL_PORT', 8500)})"
            )
            sys.exit(1)
        resp = loop.run_until_complete(resp.json())
        for svc in resp.keys():
            self.line(f"{svc}")
        sys.exit(0)

    def deregister_service(self):
        try:
            with open(self.option("deregister"), "rb") as f:
                services = pickle.loads(f.read())
        except FileNotFoundError:
            self.line("<error>[!]</error> arquivo não localizado")
            sys.exit(1)
        for service_id in services.keys():
            loop.run_until_complete(client.agent.service.deregister(service_id))
            Path(f"{self.option('deregister')}").unlink()
        sys.exit(0)
