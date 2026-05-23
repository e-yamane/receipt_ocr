from dataclasses import dataclass
from datetime import date
from decimal import Decimal


@dataclass(frozen=True)
class ReceiptData:
    purchased_on: date
    description: str
    amount: Decimal

