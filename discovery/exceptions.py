from typing import Optional


class NoConsulLeaderException(Exception):
    def __init__(
        self,
        message: str = "Error to identify Consul's leader",
        details: Optional[str] = None,
    ) -> None:
        if details:
            message = f"{message}: [details='{details}']"
        super().__init__(message)
