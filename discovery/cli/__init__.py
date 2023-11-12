import asyncio
import os

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
@click.option("-v", "--verbose", is_flag=True, help="Extend output info.")
def status(leader, peers, verbose):
    """Status API."""
    if verbose:
        _show_verbose()

    try:
        if leader:
            resp = loop.run_until_complete(consul.status.leader())
        else:
            resp = loop.run_until_complete(consul.status.leader())
    except Exception as err:
        console.print(f"[red][*][/red] Failed to process request: [details='{err}']")
        raise SystemExit
    console.print(resp)


@cli.command()
@click.option("-s", "--services", is_flag=True, help="List services catalog.")
@click.option("-d", "--datacenters", is_flag=True, help="List datacenters.")
@click.option("-n", "--nodes", is_flag=True, help="List nodes.")
@click.option("-v", "--verbose", is_flag=True, help="Extend output info.")
def catalog(services, datacenters, nodes, verbose):
    """Catalog API."""
    table = Table.grid(padding=(0, 1))
    table.add_column(style="cyan", justify="right")
    table.add_column(style="magenta")

    if verbose:
        _show_verbose()

    try:
        if datacenters:
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
        else:
            resp = loop.run_until_complete(consul.catalog.list_services())
            for i, svc in enumerate(resp, start=1):
                table.add_row(f"{i}[yellow]:[/yellow]", svc)
    except Exception as err:
        console.print(f"[red][*][/red] Failed to process request: [details='{err}']")
        raise SystemExit
    console.print(
        Panel(
            table,
            border_style="yellow",
            expand=True,
        )
    )


@cli.command()
@click.argument("argument")
@click.option("-n", "--node", is_flag=True, help="List checks for node.")
@click.option("-s", "--service", is_flag=True, help="List checks for service.")
@click.option("--state", is_flag=True, help="List checks for state.")
@click.option("-v", "--verbose", is_flag=True, help="Extend output info.")
def health(argument, node, service, state, verbose):
    """Health API."""
    if verbose:
        _show_verbose()

    try:
        if node:
            resp = loop.run_until_complete(consul.health.checks_for_node(argument))
        elif service:
            resp = loop.run_until_complete(consul.health.checks_for_service(argument))
        elif state:
            resp = loop.run_until_complete(consul.health.checks_in_state(argument))
    except Exception as err:
        console.print(f"[red][*][/red] Failed to process request: [details='{err}']")
        raise SystemExit
    console.print(resp)


@cli.command()
@click.option("-r", "--read", is_flag=True, help="Read configuration.")
@click.option("-d", "--delete", help="Delete raft peer.")
@click.option("-v", "--verbose", is_flag=True, help="Extend output info.")
def raft(read, delete, verbose):
    """Raft API."""
    if verbose:
        _show_verbose()

    try:
        if delete:
            resp = loop.run_until_complete(consul.operator.raft.delete_peer())
            console.print(resp)
        else:
            resp = loop.run_until_complete(consul.operator.raft.read_configuration())
            console.print(resp)
    except Exception as err:
        console.print(f"[red][*][/red] Failed to process request: [details='{err}']")
        raise SystemExit


def _show_verbose():
    engine, *_ = repr(consul.client).split("(")

    table = Table.grid(padding=(0, 1))
    table.add_column(style="cyan", justify="right")
    table.add_column(style="magenta")

    table.add_row("engine[yellow]:[/yellow] ", f"{engine}")
    table.add_row("scheme[yellow]:[/yellow] ", f"{consul.client.scheme}")
    table.add_row("host[yellow]:[/yellow] ", f"{consul.client.host}")
    table.add_row("port[yellow]:[/yellow] ", f"{consul.client.port}")
    table.add_row("URL[yellow]:[/yellow] ", f"{consul.client.url}")
    table.add_row("reconnect timeout[yellow]:[/yellow] ", f"{consul.reconnect_timeout}")
    console.print(
        Panel(
            table,
            title="[bold yellow]client details[/bold yellow]",
            border_style="yellow",
            expand=True,
        )
    )
