import pytest
from tests import UnitTest
from lambdas import stamp


class TestModuleLambdas(UnitTest):
    def test_stamp_function(self):
        from time import time
        self.assertAlmostEqual(stamp(), time().__str__()[:10], "assert stamp function failed")


if __name__ == '__main__':
    pytest.main()
