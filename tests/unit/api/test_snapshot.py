from pathlib import Path

import pytest

from discovery import api


@pytest.fixture
async def snapshot(consul_api):
    return api.Snapshot(client=consul_api)


async def test_generate(snapshot):
    await snapshot.generate()


@pytest.mark.skip
async def test_restore(snapshot, mocker):
    spy = mocker.spy(snapshot.client, "put")
    await snapshot.restore(data=Path("README.md").read_bytes())
    spy.assert_called_with(
        "/v1/snapshot",
        data=b"[![ci](https://github.com/amenezes/discovery-client/workflows/ci/badge.svg)](https://github.com/amenezes/discovery-client/actions)\n[![Maintainability](https://api.codeclimate.com/v1/badges/fc7916aab464c8b7d742/maintainability)](https://codeclimate.com/github/amenezes/discovery-client/maintainability)\n[![codecov](https://codecov.io/gh/amenezes/discovery-client/branch/master/graph/badge.svg)](https://codecov.io/gh/amenezes/discovery-client)\n[![PyPI version](https://badge.fury.io/py/discovery-client.svg)](https://badge.fury.io/py/discovery-client)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/discovery-client)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n# discovery-client\n\nAsync Python client for [consul](https://consul.io).\n\nHTTP engine options available:\n\n- aiohttp `default`;\n- httpx.\n\n## Installing\n\nInstall and update using pip:\n\n### default client\n\n````bash\npip install -U discovery-client\n````\n\n### httpx client\n\n````bash\npip install -U 'discovery-client[httpx]'\n````\n\n## Links\n\n- License: [Apache License](https://choosealicense.com/licenses/apache-2.0/)\n- Code: [https://github.com/amenezes/discovery-client](https://github.com/amenezes/discovery-client)\n- Issue tracker: [https://github.com/amenezes/discovery-client/issues](https://github.com/amenezes/discovery-client/issues)\n- Docs: [https://discovery-client.amenezes.net](https://discovery-client.amenezes.net)\n",
    )
