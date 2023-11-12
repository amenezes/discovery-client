# [AIOHTTP](https://docs.aiohttp.org/en/stable/)

## default client

Using default client: 

``` py linenums="1"
from discovery import Consul

consul = Consul()
```

## custom client

``` py linenums="1"
import logging

from discovery import Consul
from discovery.engine import AIOHTTPEngine


logging.basicConfig(level=logging.DEBUG)

# *args must be: host, port and scheme
# **kwargs session arguments
consul = Consul(
    client=AIOHTTPEngine(
        "localhost", 8500, 'http',
        headers={'engine': 'discovery-client with AIOHTTP'} 
    )
)
await consul.leader_ip()
```
