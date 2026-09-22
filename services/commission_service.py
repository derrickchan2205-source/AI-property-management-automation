from decimal import Decimal, ROUND_HALF_UP


def calculate_commission(sale_price, commission_rate=Decimal("0.02")):
    sale_price = Decimal(str(sale_price))

    if sale_price <= 0:
        raise ValueError("Sale price must be greater than zero")

    if commission_rate < 0 or commission_rate > 1:
        raise ValueError("Commission rate must be between 0 and 1")

    commission = sale_price * commission_rate

    return commission.quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP
    )