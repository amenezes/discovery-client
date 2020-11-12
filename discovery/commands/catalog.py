import asyncio
import pickle
from pathlib import Path

from cleo import Command

from discovery.client import Consul


class CatalogCommand(Command):
    """
    Catalog API

    catalog
        {--s|services : List services catalog.}
        {--d|deregister= : Deregister services from <file>.}
    """

    def handle(self):
        loop = asyncio.get_event_loop()
        consul = Consul()
        try:
            if self.option("services"):
                resp = loop.run_until_complete(consul.catalog.services())
                resp = loop.run_until_complete(resp.json())
                for svc in resp:
                    self.line(f"{svc}")
            elif self.option("deregister"):
                with open(self.option("deregister"), "rb") as f:
                    service = pickle.loads(f.read())
                loop.run_until_complete(consul.deregister(service))
                Path(f"{self.option('deregister')}").unlink()
        except Exception:
            self.line("<error>[!]</error> Falha ao realizar a operação.")
