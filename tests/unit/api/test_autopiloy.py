import json
import unittest

from discovery.api.autopilot import AutoPilot
from discovery.core.engine.standard import StandardEngine


class TestAutoPilot(unittest.TestCase):

    def setUp(self):
        client = StandardEngine()
        self.autopilot = AutoPilot(client)

    def test_read_configuration(self):
        self.assertIsNotNone(self.autopilot.read_configuration())

    def test_update_configuration(self):
        sample_payload = {
            'CleanupDeadServers': True,
            'LastContactThreshold': '200ms',
            'MaxTrailingLogs': 250,
            'ServerStabilizationTime': '10s',
            'RedundancyZoneTag': '',
            'DisableUpgradeMigration': False,
            'UpgradeVersionTag': '',
            'CreateIndex': 4,
            'ModifyIndex': 4
        }
        self.assertIsNotNone(
            self.autopilot.update_configuration(
                json.dumps(sample_payload)
            )
        )

    def test_read_health(self):
        self.assertIsNotNone(self.autopilot.read_health())
