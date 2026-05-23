from datetime import date
from decimal import Decimal

from receipt_tsv.exporter import export_receipts_tsv
from receipt_tsv.models import ReceiptData


def test_export_receipts_tsv_writes_requested_columns() -> None:
    receipt = ReceiptData(
        purchased_on=date(2026, 5, 23),
        description="交通費",
        amount=Decimal("1240"),
    )

    tsv = export_receipts_tsv([receipt])

    assert tsv == "Month\tDay\tDescription\tamount\n5\t23\t交通費\t1240\n"


def test_export_receipts_tsv_writes_multiple_rows() -> None:
    receipts = [
        ReceiptData(date(2026, 5, 1), "消耗品費", Decimal("980")),
        ReceiptData(date(2026, 5, 2), "会議費", Decimal("1200")),
    ]

    tsv = export_receipts_tsv(receipts)

    assert tsv == (
        "Month\tDay\tDescription\tamount\n"
        "5\t1\t消耗品費\t980\n"
        "5\t2\t会議費\t1200\n"
    )

