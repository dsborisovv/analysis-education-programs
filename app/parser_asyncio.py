import json
import time

import requests
from bs4 import BeautifulSoup
import fake_useragent
import asyncio
import aiohttp

vac = []
def iterator(soup):
    for a in soup.find_all("a", attrs={"class": "serp-item__title"}):
        yield f"{a.attrs['href'].split('?')[0]}"


async def get_page_data(session, iterator1):
    ua = fake_useragent.UserAgent()
    for url in iterator1:
        async with session.get(url=url, headers={
                    "user-agent": ua.random
                }) as response:
            response_text = await response.text()
            soup1 = BeautifulSoup(response_text, "lxml")
            title = soup1.find(attrs={"data-qa": "vacancy-title"}).text
            experience = soup1.find(attrs={"data-qa": "vacancy-experience"}).text
            salary = soup1.find(
                attrs={
                    "class": "bloko-header-section-2 bloko-header-section-2_lite"
                }
            ).text.replace("\xa0", "")
            employment = soup1.find(
                attrs={"data-qa": "vacancy-view-employment-mode"}
            ).text
            company = soup1.find(
                attrs={"data-qa": "bloko-header-2"}
            ).text.replace("\xa0", " ")
            try:
                description = soup1.find(attrs={"class": "g-user-content"}).text
            except:
                description = ""
            try:
                tags = [tag.text.replace("\xa0", " ") for tag in soup1.find(
                    attrs={"class": "bloko-tag-list"}
                ).find_all(attrs={"class": "bloko-tag__section_text"})]
            except:
                tags = []

            vac.append({
                'title': title,
                'link': url,
                'experience': experience,
                'salary': salary,
                'employment': employment,
                'company': company,
                'description': description,
                "tags": tags
            })








async def get_count_pages(text):
    ua = fake_useragent.UserAgent()
    url = f"https://hh.ru/search/vacancy?area=113&search_field=name&search_field=company_name&search_field=description&text={text}&from=suggest_post&page=1"
    async with aiohttp.ClientSession() as session:
        response = await session.get(url=url, headers={
                "user-agent": ua.random
            })
        soup = BeautifulSoup(await response.text(), "lxml")
        page_count = int(
            soup.find(
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

        for page in range(1):
            url1 = f"https://hh.ru/search/vacancy?area=113&search_field=name&search_field=company_name&search_field=description&text={text}&from=suggest_post&page={page}"
            response1 = await session.get(url=url1, headers={
                "user-agent": ua.random
            })
            soup1 = BeautifulSoup(await response1.text(), "lxml")
            iterator1 = iterator(soup1)
            task = asyncio.create_task(get_page_data(session, iterator1))
            tasks.append(task)
        await asyncio.gather(*tasks)

async def tasks():
    await get_count_pages("python")
if __name__ == "__main__":
    start_time = time.time()
    asyncio.get_event_loop().run_until_complete(tasks())
    # print(vac)
    print('All good!')
    print(f'Elapsed time {time.time() - start_time}')
