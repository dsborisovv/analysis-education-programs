import sys
import time
import csv

from bs4 import BeautifulSoup
import fake_useragent
import asyncio
import aiohttp

jobs = []


def link_iterator(soup):
    for a in soup.find_all("a", attrs={"class": "serp-item__title"}):
        yield f"{a.attrs['href'].split('?')[0]}"


async def get_page_data(session, iterator_page):
    ua = fake_useragent.UserAgent()
    for url in iterator_page:
        async with session.get(url=url, headers={
                    "user-agent": ua.random
                }) as response:
            response_text = await response.text()
            soup = BeautifulSoup(response_text, "lxml")
            title = soup.find(attrs={"data-qa": "vacancy-title"}).text
            experience = soup.find(attrs={"data-qa": "vacancy-experience"}).text
            salary = soup.find(
                attrs={
                    "class": "bloko-header-section-2 bloko-header-section-2_lite"
                }
            ).text.replace("\xa0", "")
            employment = soup.find(
                attrs={"data-qa": "vacancy-view-employment-mode"}
            ).text
            company = soup.find(
                attrs={"data-qa": "bloko-header-2"}
            ).text.replace("\xa0", " ")
            try:
                description = soup.find(attrs={"class": "vacancy-branded-user-content"}).text
            except:
                description = soup.find(attrs={"class": "g-user-content"}).text
            try:
                tags = [tag.text.replace("\xa0", " ") for tag in soup.find(
                    attrs={"class": "bloko-tag-list"}
                ).find_all(attrs={"class": "bloko-tag__section_text"})]
            except:
                tags = []

            jobs.append(
                [
                    title,
                    url,
                    experience,
                    salary,
                    employment,
                    company,
                    description,
                    tags
                ]
            )


async def get_tasks(text):
    ua = fake_useragent.UserAgent()
    url_base = f"https://hh.ru/search/vacancy?area=113&search_field=name&search_field=company_name&search_field=description&text={text}&from=suggest_post&page=1"
    async with aiohttp.ClientSession() as session:
        response_base = await session.get(url=url_base, headers={
                "user-agent": ua.random
            })
        soup_base = BeautifulSoup(await response_base.text(), "lxml")
        page_count = int(
            soup_base.find(
                "div",
                attrs={
                    "class": "pager"
                }
            ).find_all(
                "span",
                recursive=False
            )[-1].find("a").find("span").text
        )

        tasks = []

        for page in range(5):
            url_page = f"https://hh.ru/search/vacancy?area=113&search_field=name&search_field=company_name&search_field=description&text={text}&from=suggest_post&page={page}"
            response_page = await session.get(
                url=url_page, headers={
                    "user-agent": ua.random
                }
            )
            soup_page = BeautifulSoup(await response_page.text(), "lxml")
            iterator_page = link_iterator(soup_page)
            task = asyncio.create_task(get_page_data(session, iterator_page))
            tasks.append(task)
            await asyncio.sleep(1)
        await asyncio.gather(*tasks)


async def _tasks(vac_name):
    await get_tasks(vac_name)


if __name__ == "__main__":
    print("Start parsing...")
    start_time = time.time()
    vacancy_name = ' '.join(sys.argv[1:])
    asyncio.get_event_loop().run_until_complete(_tasks(vacancy_name))
    with open(r"data\data.csv", "a", encoding="utf-8", errors="ignore") as file:
        writer = csv.writer(file)
        for row in jobs:
            writer.writerow(row)
    print(f'Elapsed time: {round(time.time() - start_time, 2)}')
