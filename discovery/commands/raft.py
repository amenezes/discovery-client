import asyncio
import json

from cleo import Command
from pygments import highlight
from pygments.formatters.terminal import TerminalFormatter
from pygments.lexers import JsonLexer

from discovery.client import Consul


class RaftCommand(Command):
    """
    Raft API

    raft
        {--r|read : Read Configuration.}
        {--d|delete : Delete Raft Peer.}
    """

    def handle(self):
        loop = asyncio.get_event_loop()
        consul = Consul()
        try:
            if self.option("read"):
                resp = loop.run_until_complete(
                    consul.operator.raft.read_configuration()
                )
                resp = loop.run_until_complete(resp.json())
                self.line(
                    f"{highlight(json.dumps(resp, indent=4, sort_keys=True), JsonLexer(), TerminalFormatter())}"
                )
            elif self.option("delete"):
                resp = loop.run_until_complete(consul.operator.raft.delete_peer())
                resp = loop.run_until_complete(resp.json())
                self.line(f"{resp}")
        except Exception:
            self.line("<error>[!]</error> Falha ao realizar a operação.")
