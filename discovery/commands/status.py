import asyncio

from cleo import Command

from discovery.client import Consul


class StatusCommand(Command):
    """
    Status API

    status
        {--l|leader : Get Raft Leader.}
        {--p|peers : List Raft Peers.}
    """

    def handle(self):
        loop = asyncio.get_event_loop()
        consul = Consul()
        try:
            if self.option("leader"):
                resp = loop.run_until_complete(consul.status.leader())
                resp = loop.run_until_complete(resp.json())
                self.line(f"{resp}")
            elif self.option("peers"):
                resp = loop.run_until_complete(consul.status.leader())
                resp = loop.run_until_complete(resp.json())
                self.line(f"{resp}")
        except Exception:
            self.line("<error>[!]</error> Falha ao realizar a operação.")
