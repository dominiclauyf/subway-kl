import json

import requests
from bs4 import BeautifulSoup

from .typings import OutletData

# URL to scrape
SUBWAY_URL = "https://subway.com.my/find-a-subway"


def _get_subway_kl_data_from_website() -> dict:
    """Get subway kl data from website and convert to json data

    Returns:
        dict: raw subway kl datasets
    """
    response = requests.get(SUBWAY_URL)
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract data from the page
    # javascript index might change depends on the page provider
    raw_string = soup.find_all("script", type="text/javascript")[21].string
    return json.loads(raw_string.split('markerData":')[-1].split(',"search"')[0])


def _process_website_json_datas(json_datas: dict) -> list[OutletData]:
    """Process raw subway datasets that craw from website

    Args:
        json_datas (dict): raw subway datasets

    Returns:
        list[OutletData]: Processed subway data
    """

    outles_datas: list[OutletData] = []
    for json_data in json_datas:
        content = json_data.get("infoBox", {}).get("content", "")
        position = json_data.get("position", {})
        if "kuala lumpur" in content.lower():
            soup_content = BeautifulSoup(content, "html.parser")

            name = soup_content.find("h4").text

            p_content = soup_content.find_all("p")
            address = p_content[0].text
            operation_time = p_content[2].text

            outles_datas.append(
                {
                    "name": name,
                    "address": address,
                    "operation_time": operation_time,
                    "lat": float(position["lat"]),
                    "long": float(position["lng"]),
                }
            )

    return outles_datas


def scrape_subway_kl_data() -> list[OutletData]:
    """Scrap subway kl data and process it

    Returns:
        list[OutletData]: Subway kl data
    """
    json_datas = _get_subway_kl_data_from_website()
    outles_datas = _process_website_json_datas(json_datas)
    return outles_datas


if __name__ == "__main__":
    scrape_subway_kl_data()
