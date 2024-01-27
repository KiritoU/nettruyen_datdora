from bs4 import BeautifulSoup
from slugify import slugify


class Chapter:
    def get_chapter_slug(self, chapter_href: str, comic_id: int) -> str:
        chapter_href_splitted = chapter_href.split("/")

        if not chapter_href_splitted:
            return ""

        chapter_slug = chapter_href_splitted[-1]
        if chapter_slug.isdigit() and len(chapter_href_splitted) > 1:
            chapter_slug = chapter_href_splitted[-2]

        return slugify(f"{chapter_slug}-{comic_id}")

    def get_chapter_detail(self, chapter_name: str, soup: BeautifulSoup) -> dict:
        result = {}

        ctl00_divCenter = soup.find("div", {"id": "ctl00_divCenter"})
        if not ctl00_divCenter:
            return result

        page_chapters = ctl00_divCenter.find_all("div", class_="page-chapter")
        for index, page_chapter in enumerate(page_chapters):
            img = page_chapter.find("img")
            if not img:
                continue

            img_alt = img.get("alt")
            img_src = img.get("src")
            img_data_index = img.get("data-index")

            if not img_src:
                continue

            if not img_data_index:
                img_data_index = index

            if not img_src.startswith("https:"):
                img_src = "https:" + img_src

            result[img_data_index] = {
                "alt": img_alt,
                "src": img_src,
            }

        return result


_chapter = Chapter()
