class HttpResponse:
    def __init__(self, response):
        self._response = response

    @property
    def status(self) -> int:
        try:
            return int(self._response.status)
        except AttributeError:
            return int(self._response.status_code)

    @property
    def url(self) -> str:
        return str(self._response.url)

    @property
    def content_type(self) -> str:
        try:
            return str(self._response.content_type)
        except AttributeError:
            return str(self._response.headers["content-type"])

    @property
    def version(self) -> str:
        try:
            http_version = self._response.version
            return f"{http_version.major}.{http_version.minor}"
        except AttributeError:
            return str(self._response.http_version.split("/")[1])

    @property
    def raw_response(self):
        return self._response

    async def json(self):
        try:
            response = await self._response.json()
            return response
        except TypeError:
            return self._response.json()

    async def text(self):
        try:
            response = await self._response.text()
            return response
        except TypeError:
            return self._response.text

    async def content(self) -> bytes:
        try:
            response = await self._response.content.read()
            return bytes(response)
        except AttributeError:
            return bytes(self._response.content)
