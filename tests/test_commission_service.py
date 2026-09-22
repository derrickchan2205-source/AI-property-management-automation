from decimal import Decimal
import pytest

from services.commission_service import calculate_commission

def test_calculate_commission_at_two_percent():
    result = calculate_commission(6000000, Decimal("0.02"))

    assert result == Decimal("120000.00")

def test_calculate_commission_rejects_negative_price():
    with pytest.raises(ValueError):
        calculate_commission(-1000)