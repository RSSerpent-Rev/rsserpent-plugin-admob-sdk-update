from typing import Any

import arrow
from lxml import html
from rsserpent_rev.utils import HTTPClient, cached

path = "/admob/sdk-update/{platform}"


def __get_date(date_str: str) -> arrow.Arrow:
    formats = ["YYYY-MM-DD", "YYYY-M-DD", "MMMM D, YYYY", "YYYY‑MM‑DD"]
    for fmt in formats:
        try:
            date = arrow.get(date_str.strip(), fmt)
            break
        except Exception:
            date = arrow.now()

    return date


@cached
async def provider(platform: str) -> dict[str, Any]:
    """Return three latest AdMob SDK updates.

    Args:
        platform (str): Platform to get updates for.

    Raises:
        ValueError: Unsupported platform.

    Returns:
        Dict[str, Any]: AdMob SDK updates.
    """
    map_dict = {
        "ios": "iOS",
        "android": "Android",
        "cpp": "C++",
    }
    if platform.lower() not in map_dict:
        raise ValueError(f"Unsupported platform: {platform}")  # noqa: TRY003

    async with HTTPClient() as client:
        platform_in_url = platform.replace("-", "_")
        url = f"https://developers.google.com/admob/{platform_in_url}/rel-notes"
        html_text = (await client.get(url)).content.decode("utf-8")
        tree = html.fromstring(html_text)
        table = tree.xpath("//table")[0]

        items = []
        for row in table.xpath(".//tr"):
            if not row.xpath(".//td"):
                continue
            version = row.xpath(".//td")[0].text_content()
            date_str = row.xpath(".//td")[1].text_content().strip()
            # get html content
            note = row.xpath(".//td")[2]
            items.append(
                {
                    "title": f"AdMob SDK {map_dict[platform]} {version} Update",
                    "description": html.tostring(note, encoding="unicode"),
                    "link": url,
                    "pub_date": __get_date(date_str),
                }
            )

    return {
        "title": f"AdMob SDK {map_dict[platform]} Update",
        "link": url,
        "description": "Latest AdMob SDK update.",
        "pub_date": items[0]["pub_date"],
        "items": items,
    }
