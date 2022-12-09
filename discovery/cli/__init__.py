import asyncio

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from discovery import Consul, __version__

CONTEXT_SETTINGS = dict(
    help_option_names=["-h", "--help"],
)
console = Console()
loop = asyncio.get_event_loop()
consul = Consul()


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version=__version__)
def cli():
    pass


@cli.command()
@click.option("-l", "--leader", is_flag=True, help="Get Raft Leader.")
@click.option("-p", "--peers", is_flag=True, help="List Raft Peers.")
def status(leader, peers):
    """Status API."""
    try:
        if leader:
            resp = loop.run_until_complete(consul.status.leader())
        elif peers:
            resp = loop.run_until_complete(consul.status.leader())
    except Exception:
        click.echo("<error>[!]</error> Falha ao realizar a operação.")
    click.echo(resp)


@cli.command()
@click.option("-s", "--services", is_flag=True, help="List services catalog.")
@click.option("-d", "--datacenters", is_flag=True, help="List datacenters.")
@click.option("-n", "--nodes", is_flag=True, help="List nodes.")
def catalog(services, datacenters, nodes):
    """Catalog API."""
    table = Table.grid(padding=(0, 1))
    table.add_column(style="cyan", justify="right")
    table.add_column(style="magenta")

    try:
        if services:
            resp = loop.run_until_complete(consul.catalog.list_services())
            for i, svc in enumerate(resp, start=1):
                table.add_row(f"{i}[yellow]:[/yellow]", svc)
        elif datacenters:
            resp = loop.run_until_complete(consul.catalog.list_datacenters())
            for i, dc in enumerate(resp, start=1):
                table.add_row(f"{i}[yellow]:[/yellow]", dc)
        elif nodes:
            resp = loop.run_until_complete(consul.catalog.list_nodes())
            leader_id = loop.run_until_complete(consul.leader_id())
            for i, node in enumerate(resp, start=1):
                if node["ID"] == leader_id:
                    table.add_row(
                        f"{i}[yellow]:[/yellow]",
                        node["Node"],
                        node["Address"],
                        "[yellow][bold]leader[/bold][/yellow]",
                    )
                else:
                    table.add_row(
                        f"{i}[yellow]:[/yellow]", node["Node"], node["Address"]
                    )
    except Exception:
        click.echo("<error>[!]</error> Falha ao realizar a operação.")
    console.print(
        Panel(
            table,
            border_style="yellow",
            expand=True,
        )
    )


@cli.command()
@click.option("-n", "--node", help="Node name.")
@click.option("-s", "--service", help="Service name.")
@click.option("--state", help="State name.")
def health(node, service, state):
    """Health API."""
    try:
        if node:
            resp = loop.run_until_complete(consul.health.checks_for_node(node))
        elif service:
            resp = loop.run_until_complete(consul.health.checks_for_service(service))
        elif state:
            resp = loop.run_until_complete(consul.health.checks_in_state(state))
    except Exception:
        click.echo("<error>[!]</error> Falha ao realizar a operação.")
        raise SystemExit(1)
    click.echo(
        resp
        # f"{highlight(json.dumps(resp, indent=4, sort_keys=True), JsonLexer(), TerminalFormatter())}"
    )


@cli.command()
@click.option("-r", "--read", is_flag=True, help="Read configuration.")
@click.option("-d", "--delete", help="Delete raft peer.")
def raft(read, delete):
    """Raft API."""
    try:
        if read:
            resp = loop.run_until_complete(consul.operator.raft.read_configuration())
            click.echo(resp)
        elif delete:
            resp = loop.run_until_complete(consul.operator.raft.delete_peer())
            click.echo(resp)
    except Exception:
        click.echo("<error>[!]</error> Falha ao realizar a operação.")
