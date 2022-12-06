class NoConsulLeaderException(Exception):
    def __init__(self, message="Error to identify Consul's leader."):
        super().__init__(message)
