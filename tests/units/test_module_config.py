import pytest
from tests import UnitTest
from common import config, Config


class TestModuleConfig(UnitTest):
    def test_config_as_Singleton(self):
        self.assertEqual(id(config), id(Config.Instance()), "assert config as Singleton failed")

    def test_config_get_host_as_localhost(self):
        self.assertEqual(config.get_host(), '0.0.0.0', "assert get_host failed")

    def test_config_get_port_as_41514(self):
        self.assertEqual(config.get_port(), 41514, "assert get_port failed")


if __name__ == '__main__':
    pytest.main()
