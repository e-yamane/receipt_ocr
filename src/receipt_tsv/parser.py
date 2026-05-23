from __future__ import annotations

import re
from datetime import date
from decimal import Decimal

from receipt_tsv.models import ReceiptData

DATE_PATTERNS = [
    re.compile(r"(?P<year>\d{4})[/-](?P<month>\d{1,2})[/-](?P<day>\d{1,2})"),
    re.compile(r"(?P<year>\d{4})年\s*(?P<month>\d{1,2})月\s*(?P<day>\d{1,2})日"),
    re.compile(r"(?P<year>\d{4})\.(?P<month>\d{1,2})\.(?P<day>\d{1,2})"),
]

AMOUNT_PATTERN = re.compile(r"(?:[¥￥]\s*)?(?P<amount>\d{1,3}(?:,\d{3})+|\d+)\s*(?:円)?")


def parse_receipt_text(text: str) -> ReceiptData:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        raise ValueError("receipt text is empty")

    purchased_on = _extract_date(text)
    amount = _extract_amount(lines)
    description = _extract_description(lines)

    return ReceiptData(
        purchased_on=purchased_on,
        description=description,
        amount=amount,
    )


def _extract_date(text: str) -> date:
    for pattern in DATE_PATTERNS:
        match = pattern.search(text)
        if match:
            return date(
                int(match.group("year")),
                int(match.group("month")),
                int(match.group("day")),
            )

    raise ValueError("could not find receipt date")


def _extract_amount(lines: list[str]) -> Decimal:
    candidates: list[Decimal] = []

    for line in lines:
        if _looks_like_date(line):
            continue
        for match in AMOUNT_PATTERN.finditer(line):
            candidates.append(Decimal(match.group("amount").replace(",", "")))

    if not candidates:
        raise ValueError("could not find receipt amount")

    return max(candidates)


def _extract_description(lines: list[str]) -> str:
    for line in lines:
        if _looks_like_date(line) or _looks_like_amount(line):
            continue
        return line

    raise ValueError("could not find receipt description")


def _looks_like_date(line: str) -> bool:
    return any(pattern.search(line) for pattern in DATE_PATTERNS)


def _looks_like_amount(line: str) -> bool:
    return bool(AMOUNT_PATTERN.search(line))

