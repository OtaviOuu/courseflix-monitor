import asyncio
import pytest

from scraper import Scraper


@pytest.mark.asyncio
async def test_get_courses_in_page():
    scraper = Scraper()
    page = 1
    url = f"https://courseflix.net/course?page={page}"
    html = """
    <html>
        <body>
            <a href="https://courseflix.net/course/1">Course 1</a>
            <a href="https://courseflix.net/course/2">Course 2</a>
            <a href="https://courseflix.net/course/3">Course 3</a>
        </body>
    </html>
    """

    async def mock_get(url):
        return html

    scraper._get_courses_in_page = mock_get
    response = await scraper._get_courses_in_page(page)

    assert response == html


@pytest.mark.asyncio
async def test_parse_courses():
    scraper = Scraper()
    html = """
    <html>
        <body>
            <a href="https://courseflix.net/course/1"><span>Course 1</span></a>
            <a href="https://courseflix.net/course/1"><span>Course 2</span></a>
            <a href="https://courseflix.net/course/1"><span>Course 3</span></a>

        </body>
    </html>
    """
    expected_courses = ["Course 1", "Course 2", "Course 3"]
    courses = await scraper._parse_courses(html)

    assert courses == expected_courses
