# Copyright (C) Ivan Kravets <me@ikravets.com>
# See LICENSE for details.

import os.path

from twisted.trial.unittest import TestCase

from smartanthill.configprocessor import ConfigProcessor
from smartanthill.exception import ConfigKeyError


class ConfigProcessorCase(TestCase):

    def setUp(self):
        self.config = ConfigProcessor(
            os.path.dirname(os.path.realpath(__file__)),
            {"logger.level": "DEBUG"})

    def test__singleton(self):
        self.assertEqual(self.config, ConfigProcessor())

    def test_structure(self):
        self.assertIn("logger", self.config)
        self.assertIn("services", self.config)
        self.assertTrue(self.config.get("logger.level"))

        _service_structure = set(["enabled", "priority", "options"])
        for v in self.config.get("services").values():
            self.assertEqual(set(v.keys()), _service_structure)

    def test_useroptions(self):
        self.assertEqual(self.config.get("logger.level"), "DEBUG")

    def test_invalidkey(self):
        self.assertRaises(ConfigKeyError, self.config.get, "invalid.key")
        self.assertEqual(self.config.get("invalid.key", "default"), "default")
