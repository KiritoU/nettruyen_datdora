import json
import sys
from time import sleep

from icecream import ic

from _db import Database
from crawler import Crawler
from settings import CONFIG
from telegram_noti import send_direct_message

LINK_FILE = "links.json"


def write_links(links: list[str], is_append: bool = False):
    if is_append:
        existing_links = get_all_links()
        links.extend(existing_links)

    with open(LINK_FILE, "w") as f:
        f.write(json.dumps(links, indent=4))


def get_all_links() -> list[str]:
    try:
        with open(LINK_FILE, "r") as f:
            links = json.loads(f.read())
            return links
    except:
        return []


def get_link() -> str:
    try:
        links = get_all_links()
        link = links[0]
        links.remove(link)
        write_links(links)
        return link
    except:
        return ""


def main():
    database_for_crawl_links = Database()
    print(f"Using database: {database_for_crawl_links} for crawl_links.py file...")
    _crawler = Crawler(database=database_for_crawl_links)

    try:
        is_netttruyen_domain_work = _crawler.is_nettruyen_domain_work()
        if not is_netttruyen_domain_work:
            send_direct_message(msg="Nettruyen domain might be changed!!!")
            sys.exit(1)

        while True:
            link = get_link()
            ic(link)
            _crawler.crawl_comic(href=link)
            sleep(10)

    except Exception as e:
        ic(e)


if __name__ == "__main__":
    main()
