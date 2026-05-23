from __future__ import annotations

import csv
from io import StringIO
from typing import Iterable

from receipt_tsv.models import ReceiptData

TSV_COLUMNS = ["Month", "Day", "Description", "amount"]


def export_receipts_tsv(receipts: Iterable[ReceiptData]) -> str:
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=TSV_COLUMNS, delimiter="\t", lineterminator="\n")
    writer.writeheader()

    for receipt in receipts:
        writer.writerow(
            {
                "Month": receipt.purchased_on.month,
                "Day": receipt.purchased_on.day,
                "Description": receipt.description,
                "amount": _format_amount(receipt),
            }
        )

    return output.getvalue()


def _format_amount(receipt: ReceiptData) -> str:
    return str(receipt.amount.quantize(1)) if receipt.amount == receipt.amount.to_integral() else str(receipt.amount)

