# [httpx](https://www.python-httpx.org/)

Using httpx [**async client**](https://www.python-httpx.org/async/). 

``` py linenums="1"
import logging

from discovery import Consul
from discovery.engine import HTTPXEngine


logging.basicConfig(level=logging.DEBUG)

# *args must be: host, port and scheme
# **kwargs session arguments
consul = Consul(
    client=HTTPXEngine(
        "localhost", 8500, 'http',
        headers={'engine': 'discovery-client with HTTPX'} 
    )
)

await consul.leader_ip()
```
