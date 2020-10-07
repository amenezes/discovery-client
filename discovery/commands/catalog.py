import asyncio
import logging
import os
import pickle
import sys
from pathlib import Path

from cleo import Command
from dotenv import load_dotenv

from discovery.client import Consul

logging.getLogger().addHandler(logging.NullHandler())
load_dotenv()


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
        loop = asyncio.get_event_loop()
        consul = Consul()
        try:
            resp = loop.run_until_complete(consul.catalog.services())
        except Exception:
            self.line(
                f"<error>[!]</error> falha ao conectar no Consul({os.getenv('CONSUL_HOST', 'localhost')}:{os.getenv('CONSUL_PORT', 8500)})"
            )
            sys.exit(1)
        resp = loop.run_until_complete(resp.json())
        for svc in resp:
            self.line(f"{svc}")
        sys.exit(0)

    def deregister_service(self):
        loop = asyncio.get_event_loop()
        consul = Consul()
        try:
            with open(self.option("deregister"), "rb") as f:
                service = pickle.loads(f.read())
        except FileNotFoundError:
            self.line("<error>[!]</error> arquivo não localizado")
            sys.exit(1)
        loop.run_until_complete(consul.deregister(service))
        Path(f"{self.option('deregister')}").unlink()
        sys.exit(0)
