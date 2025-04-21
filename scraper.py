import aiohttp
from parsel.selector import Selector


class Scraper:
    def __init__(self):
        self.base_url = "https://courseflix.net"

    async def _get_courses_in_page(self, page: int):
        url = f"{self.base_url}/course?page={page}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, ssl=True) as response:
                if response.status == 200:
                    return await response.text()
                raise Exception(f"Failed to fetch data from {url}")

    async def _parse_courses(self, html: str):
        tree = Selector(text=html)
        courses = tree.css(
            f"a[href*='{self.base_url}/course/'] span:first-of-type::text"
        ).getall()

        return courses
