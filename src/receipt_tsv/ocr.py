from typing import Protocol


class OCRProvider(Protocol):
    def extract_text(self, image_path: str) -> str:
        """Return OCR text from a receipt image."""

