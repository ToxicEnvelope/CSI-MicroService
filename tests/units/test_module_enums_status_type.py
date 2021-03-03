import pytest
from tests import UnitTest
from enums import StatusType


class TestModuleStatusType(UnitTest):
    def test_status_type_success_value(self):
        self.assertEqual(StatusType.SUCCESS.value, 'success', "assert SUCCESS.value failed")

    def test_status_type_failed_value(self):
        self.assertEqual(StatusType.FAILED.value, 'failed', "assert FAILED.value failed")

    def test_status_type_pending_value(self):
        self.assertEqual(StatusType.PENDING.value, 'pending', "assert PENDING.value failed")


if __name__ == '__main__':
    pytest.main()
