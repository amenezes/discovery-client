from enum import StrEnum, unique


@unique
class Kind(StrEnum):
    INGRESS_GATEWAY = "ingress-gateway"
    PROXY_DEFAULTS = "proxy-defaults"
    SERVICE_DEFAULTS = "service-defaults"
    SERVICE_INTENTIONS = "service-intentions"
    SERVICE_RESOLVER = "service-resolver"
    SERVICE_ROUTER = "service-router"
    SERVICE_SPLITTER = "service-splitter"
    TERMINATING_GATEWAY = "terminating-gateway"
