import pytest


class TestHttpxClient:
    @pytest.mark.asyncio
    async def test_status(self, httpx_engine):
        resp = await httpx_engine.get("https://httpbin.org/status/200")
        assert resp.status == 200

    @pytest.mark.asyncio
    async def test_url(self, httpx_engine):
        resp = await httpx_engine.get("https://httpbin.org/status/200")
        assert resp.url == "https://httpbin.org/status/200"

    @pytest.mark.asyncio
    async def test_content_type(self, httpx_engine):
        resp = await httpx_engine.get("https://httpbin.org/status/200")
        assert resp.content_type == "text/html; charset=utf-8"

    @pytest.mark.asyncio
    async def test_version(self, httpx_engine):
        resp = await httpx_engine.get("https://httpbin.org/status/200")
        assert resp.version == "1.1"

    @pytest.mark.asyncio
    async def test_json(self, httpx_engine):
        resp = await httpx_engine.get("https://httpbin.org/json")
        content = await resp.json()
        assert isinstance(content, dict)

    @pytest.mark.asyncio
    async def test_text(self, httpx_engine):
        resp = await httpx_engine.get("https://httpbin.org/html")
        content = await resp.text()
        assert isinstance(content, str)
    
    @pytest.mark.asyncio
    async def test_content(self, httpx_engine):
        resp = await httpx_engine.get("https://httpbin.org/html")
        content = await resp.content()
        assert isinstance(content, bytes)


class TestAioHttpClient:
    @pytest.mark.asyncio
    async def test_status(self, aiohttp_client):
        resp = await aiohttp_client.get("https://httpbin.org/status/200")
        assert resp.status == 200

    @pytest.mark.asyncio
    async def test_url(self, aiohttp_client):
        resp = await aiohttp_client.get("https://httpbin.org/status/200")
        assert resp.url == "https://httpbin.org/status/200"


    @pytest.mark.asyncio
    async def test_content_type(self, aiohttp_client):
        resp = await aiohttp_client.get("https://httpbin.org/status/200")
        assert resp.content_type == "text/html"

    @pytest.mark.asyncio
    async def test_version(self, aiohttp_client):
        resp = await aiohttp_client.get("https://httpbin.org/status/200")
        assert resp.version == "1.1"

    @pytest.mark.asyncio
    async def test_json(self, aiohttp_client):
        resp = await aiohttp_client.get("https://httpbin.org/json")
        content = await resp.json()
        assert isinstance(content, dict)

    @pytest.mark.asyncio
    async def test_text(self, aiohttp_client):
        resp = await aiohttp_client.get("https://httpbin.org/html")
        content = await resp.text()
        assert isinstance(content, str)

    @pytest.mark.asyncio
    async def test_content(self, aiohttp_client):
        resp = await aiohttp_client.get("https://httpbin.org/html")
        content = await resp.content()
        assert isinstance(content, bytes)
