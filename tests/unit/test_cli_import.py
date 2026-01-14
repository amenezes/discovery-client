import asyncio
import threading

import pytest

from discovery import Consul


@pytest.mark.parametrize("attr", ["cli", "loop", "consul", "console"])
def test_cli_module_attributes(attr):
    import discovery.cli

    assert hasattr(discovery.cli, attr)


def test_cli_thread_import():
    result = {}

    def import_in_thread():
        try:
            from discovery.cli import loop

            result.update({"success": True, "loop": loop})
        except RuntimeError as e:
            result.update({"error": str(e), "success": False})

    thread = threading.Thread(target=import_in_thread)
    thread.start()
    thread.join()

    assert result["success"]
    assert result["loop"] is not None


def test_cli_types():
    from discovery.cli import cli, consul, loop

    assert isinstance(loop, asyncio.AbstractEventLoop)
    assert isinstance(consul, Consul)
    assert callable(cli)


def test_cli_singleton():
    import discovery.cli as cli1
    import discovery.cli as cli2

    assert cli1.cli is cli2.cli
    assert cli1.loop is cli2.loop
    assert cli1.consul is cli2.consul
    assert cli1.console is cli2.console
