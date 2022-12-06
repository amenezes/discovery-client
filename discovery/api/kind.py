from enum import Enum, unique


@unique
class Kind(str, Enum):
    INGRESS_GATEWAY: str = "ingress-gateway"
    PROXY_DEFAULTS: str = "proxy-defaults"
    SERVICE_DEFAULTS: str = "service-defaults"
    SERVICE_INTENTIONS: str = "service-intentions"
    SERVICE_RESOLVER: str = "service-resolver"
    SERVICE_ROUTER: str = "service-router"
    SERVICE_SPLITTER: str = "service-splitter"
    TERMINATING_GATEWAY: str = "terminating-gateway"

    def __str__(self) -> str:
        return str.__str__(self)
