import asyncio
import json

from cleo import Command
from pygments import highlight
from pygments.formatters.terminal import TerminalFormatter
from pygments.lexers import JsonLexer

from discovery.client import Consul


class HealthCommand(Command):
    """
    Health API

    health
        {option : node or service name}
        {--node : node name.}
        {--service : service name.}
        {--state : state name.}
    """

    def handle(self):
        loop = asyncio.get_event_loop()
        consul = Consul()
        try:
            if self.option("node"):
                resp = loop.run_until_complete(
                    consul.health.node(self.argument("option"))
                )
                resp = loop.run_until_complete(resp.json())
            elif self.option("service"):
                resp = loop.run_until_complete(
                    consul.health.service(self.argument("option"))
                )
                resp = loop.run_until_complete(resp.json())
            elif self.option("state"):
                resp = loop.run_until_complete(
                    consul.health.state(self.argument("option"))
                )
                resp = loop.run_until_complete(resp.json())
        except Exception:
            self.line("<error>[!]</error> Falha ao realizar a operação.")
            raise SystemExit(1)
        self.line(
            f"{highlight(json.dumps(resp, indent=4, sort_keys=True), JsonLexer(), TerminalFormatter())}"
        )
