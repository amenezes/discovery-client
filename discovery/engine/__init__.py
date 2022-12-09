from discovery.engine.abc import Engine

try:
    from discovery.engine.aiohttp import AIOHTTPEngine
except ImportError:
    aiohttp = None

try:
    from discovery.engine.httpx import HTTPXEngine
except ImportError:
    httpx = None
