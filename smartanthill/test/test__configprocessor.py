# See LICENSE for details.

from twisted.trial.unittest import TestCase

from smartanthill.configprocessor import ConfigProcessor


class ConfigProcessorCase(TestCase):

    def setUp(self):
        self.config = ConfigProcessor(".", {})

    def test__singleton(self):
        self.assertEqual(self.config, ConfigProcessor())

    def test_structure(self):
        self.assertIn("logger", self.config)
        self.assertIn("services", self.config)
        self.assertTrue(self.config.get("logger.level"))

        _service_structure = set(["enabled", "priority", "options"])
        for v in self.config["services"].values():
            self.assertEqual(set(v.keys()), _service_structure)
