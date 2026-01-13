import aiohttp


async def test_get(consul):
    async with consul.client.get("https://postman-echo.com/get") as response:
        assert response.status == 200
        assert response.version == "1.1"


async def test_put(consul):
    async with consul.client.put("https://postman-echo.com/put") as response:
        assert response.status == 200


async def test_delete(consul):
    async with consul.client.delete("https://postman-echo.com/delete") as response:
        assert response.status == 200


async def test_post(consul):
    async with consul.client.post("https://postman-echo.com/post") as response:
        assert response.status == 200


def test_url(consul):
    assert consul.client.url == "http://localhost:8500"


def test_repr(consul):
    assert (
        str(consul)
        == "Consul(engine=AIOHTTPEngine(host='localhost', port=8500, scheme='http'))"
    )


async def test_response_repr(consul):
    async with consul.client.get("https://postman-echo.com/get") as response:
        assert (
            str(response)
            == "Response(status=200, http_version='1.1', url='https://postman-echo.com/get')"
        )


async def test_raw_response(consul):
    async with consul.client.get("https://postman-echo.com/get") as response:
        assert isinstance(response.raw_response, aiohttp.client_reqrep.ClientResponse)
