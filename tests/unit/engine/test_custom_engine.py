import pytest

from discovery.engine.abc import Engine


class CustomEngine(Engine):
    pass


@pytest.fixture
def custom_engine():
    return CustomEngine()


@pytest.mark.asyncio
async def test_get(custom_engine):
    with pytest.raises(NotImplementedError):
        await custom_engine.get("https://httpbin.org/get")


@pytest.mark.asyncio
async def test_put(custom_engine):
    with pytest.raises(NotImplementedError):
        await custom_engine.put("https://httpbin.org/put")


@pytest.mark.asyncio
async def test_delete(custom_engine):
    with pytest.raises(NotImplementedError):
        await custom_engine.delete("https://httpbin.org/delete")


@pytest.mark.asyncio
async def test_post(custom_engine):
    with pytest.raises(NotImplementedError):
        await custom_engine.post("https://httpbin.org/post")
