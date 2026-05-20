import httpx
from bs4 import BeautifulSoup
from decimal import Decimal


def price_scrape(url: str) -> Decimal | None:
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = httpx.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        price_tag = soup.find(class_=lambda c: c and "price" in c.lower())
        if not price_tag:
            return None

        raw = price_tag.get_text()
        cleaned = "".join(char for char in raw if char.isdigit() or char == ".")
        return Decimal(cleaned) if cleaned else None

    except Exception:
        return None
