import asyncio

from cleo import Command

from discovery.client import Consul


class HealthCommand(Command):
    """
    Health API

    health
        {--n|node : List checks for node.}
        {--s|service : List checks for service.}
        {--o|nodes : List nodes for service}
        {--a|state : List checks in state.}
    """

    def handle(self):
        loop = asyncio.get_event_loop()
        consul = Consul()
        try:
            if self.option("node"):
                resp = loop.run_until_complete(consul.health.node())
                resp = loop.run_until_complete(resp.json())
                self.line(f"{resp}")
            elif self.option("peers"):
                resp = loop.run_until_complete(consul.health.service())
                resp = loop.run_until_complete(resp.json())
                self.line(f"{resp}")
            elif self.option("state"):
                pass
            elif self.option("checks"):
                pass
        except Exception:
            self.line("<error>[!]</error> Falha ao realizar a operação.")
