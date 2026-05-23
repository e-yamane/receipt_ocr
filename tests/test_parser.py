from datetime import date
from decimal import Decimal

import pytest

from receipt_tsv.parser import parse_receipt_text


def test_parse_receipt_text_extracts_date_description_and_amount() -> None:
    text = """
    2026年5月23日
    交通費
    合計 ¥1,240
    """

    receipt = parse_receipt_text(text)

    assert receipt.purchased_on == date(2026, 5, 23)
    assert receipt.description == "交通費"
    assert receipt.amount == Decimal("1240")


def test_parse_receipt_text_supports_slash_date_and_yen_suffix() -> None:
    text = """
    STORE SAMPLE
    2026/05/03
    消耗品費
    980円
    """

    receipt = parse_receipt_text(text)

    assert receipt.purchased_on == date(2026, 5, 3)
    assert receipt.description == "STORE SAMPLE"
    assert receipt.amount == Decimal("980")


def test_parse_receipt_text_raises_when_date_is_missing() -> None:
    with pytest.raises(ValueError, match="date"):
        parse_receipt_text("交通費\n1,000円")

