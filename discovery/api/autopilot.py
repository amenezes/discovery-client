from typing import Optional

from discovery.api.abc import Api


class AutoPilot(Api):
    def __init__(self, endpoint: str = "/operator/autopilot", **kwargs) -> None:
        super().__init__(endpoint=endpoint, **kwargs)

    async def read_configuration(
        self, dc: Optional[str] = None, stale: Optional[bool] = None, **kwargs
    ) -> dict:
        url = self._prepare_request_url(f"{self.url}/configuration", dc=dc, stale=stale)
        async with self.client.get(url, **kwargs) as resp:
            return await resp.json()  # type: ignore

    async def update_configuration(
        self,
        cleanup_dead_servers: bool = True,
        last_contact_threshold: str = "200ms",
        max_trailing_logs: int = 250,
        min_quorum: int = 0,
        server_stabilization_time: str = "10s",
        redundancy_zone_tag: str = "",
        disable_upgrade_migration: bool = False,
        upgrade_version_tag: str = "",
        dc: Optional[str] = None,
        cas: Optional[int] = None,
        **kwargs,
    ) -> None:
        url = self._prepare_request_url(f"{self.url}/configuration", dc=dc, cas=cas)
        data = dict(
            CleanupDeadServers=cleanup_dead_servers,
            LastContactThreshold=last_contact_threshold,
            MaxTrailingLogs=max_trailing_logs,
            MinQuorum=min_quorum,
            ServerStabilizationTime=server_stabilization_time,
            RedundancyZoneTag=redundancy_zone_tag,
            DisableUpgradeMigration=disable_upgrade_migration,
            UpgradeVersionTag=upgrade_version_tag,
        )
        async with self.client.put(url, json=data, **kwargs):
            pass

    async def read_health(self, dc: Optional[str] = None, **kwargs) -> dict:
        url = self._prepare_request_url(f"{self.url}/health", dc=dc)
        async with self.client.get(url, **kwargs) as resp:
            return await resp.json()  # type: ignore

    async def read_state(self, dc: Optional[str] = None, **kwargs):
        url = self._prepare_request_url(f"{self.url}/state", dc=dc)
        async with self.client.get(url, **kwargs) as resp:
            return await resp.json()
