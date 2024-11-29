import requests
from bs4 import BeautifulSoup
import datetime
import time
import csv

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    # 'Accept-Encoding': 'gzip, deflate, br',
    "DNT": "1",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
}


def scrape_billboard_charts(current_date: str) -> list:
    """
    Scrapes the Billboard Hot 100 chart for a given date and returns a list of songs with their details.
    Args:
        current_date (str): The date for which to scrape the Billboard Hot 100 chart in the format 'YYYY-MM-DD'.
    Returns:
        list: A list of dictionaries, each containing details of a song such as its position, title, artist, peak position, and weeks on chart.
    """
    chart = []
    while current_date:
        print(f"Scraping songs for {current_date}")

        current_url = f"https://www.billboard.com/charts/hot-100/{current_date}"
        response = requests.get(current_url, headers=headers)
        if response.status_code != 200:
            print(
                f"Failed to retrieve the page for date {current_date} ({current_url}). Status code: {response.status_code}"
            )
            continue

        soup = BeautifulSoup(response.content, "html.parser")
        last_index = chart[-1]["index"] if chart else 0

        for index, item in enumerate(
            soup.select("div.o-chart-results-list-row-container")
        ):
            isFirstSong = index == 0
            position = (
                item.select("span.c-label.a-font-primary-bold-l")[0].text.strip()
                if isFirstSong
                else item.select_one("span.c-label.a-font-primary-bold-l").text.strip()
            )
            title = item.select_one("h3.c-title").text.strip()
            artist = item.select_one("span.c-label.a-no-trucate").text.strip()
            last_week = (
                item.select("span.c-label.a-font-primary-bold-l")[1].text.strip()
                if isFirstSong
                else item.select("span.c-label.a-font-primary-m")[0].text.strip()
            )
            peak_position = (
                item.select("span.c-label.a-font-primary-bold-l")[2].text.strip()
                if isFirstSong
                else item.select("span.c-label.a-font-primary-m")[1].text.strip()
            )
            weeks_on_chart = (
                item.select("span.c-label.a-font-primary-bold-l")[3].text.strip()
                if isFirstSong
                else item.select("span.c-label.a-font-primary-m")[2].text.strip()
            )

            chart.append(
                {
                    "index": last_index + index + 1,
                    "position": position,
                    "title": title,
                    "artist": artist,
                    "last week": last_week,
                    "peak position": peak_position,
                    "weeks on chart": weeks_on_chart,
                    "week of": current_date,
                }
            )

        current_date = get_next_date(current_date)

        print(f"{len(chart)} songs in total")

        # set 5 seconds interval to prevent billboard from blocking our ip address
        time.sleep(5)

    return chart


def save_to_csv(chart, filename="billboard_charts.csv"):
    keys = chart[0].keys()
    with open(filename, "w", newline="") as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(chart)


def get_next_date(recent=None):
    recent_date = datetime.datetime.strptime(recent, "%Y-%m-%d")
    next_date = recent_date + datetime.timedelta(days=7)

    if next_date > datetime.datetime.today():
        return None

    return next_date.strftime("%Y-%m-%d")


if __name__ == "__main__":
    start_date = "2010-01-02"
    charts = scrape_billboard_charts(start_date)
    save_to_csv(charts)
