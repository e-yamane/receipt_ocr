# receipt-ocr

Local CLI app for turning receipt data into TSV.

This first version intentionally starts after OCR: it parses OCR text and exports
normalized TSV rows. OCR providers can be added later without changing the
parser/exporter boundary.

## Requirements

- Python 3.11.15

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
```

## Test

```bash
pytest
```

## Current Scope

- Parse OCR text into `ReceiptData`
- Keep parsed receipt data as a Python model using `datetime.date`
- Leave OCR implementation behind an `OCRProvider` protocol
- Export TSV columns:
  - `Month`
  - `Day`
  - `Description`
  - `amount`
