import sys
import time
import csv

from bs4 import BeautifulSoup
import fake_useragent
import asyncio
import aiohttp
import requests

# jobs = []
#
#
# def get_content(link):
#     ua = fake_useragent.UserAgent()
#     try:
#         data = requests.get(
#             url=link,
#             headers={
#                 "user-agent": ua.random
#             }
#         )
#         if data.status_code != 200:
#             return
#         soup = BeautifulSoup(data.content, "lxml")
#         return soup
#     except:
#         return
#
#
# def get_count_pages(text):
#     link = f"https://hh.ru/search/vacancy?area=113&search_field=name&search_field=company_name&search_field=description&text={text}&from=suggest_post&page=1"
#     soup = get_content(link)
#     if soup:
#         page_count = int(
#             soup.find(
#                 "div",
#                 attrs={
#                     "class": "pager"
#                 }
#             ).find_all(
#                 "span",
#                 recursive=False
#             )[-1].find("a").find("span").text
#         )
#         return page_count
#     return
#
#
# async def get_html(url):
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url, headers=HEADERS) as resp:
#             return await resp.text()
#
#
# async def get_data(url):
#     response = await get_html(url)
#     soup = BeautifulSoup(response, 'lxml')
#     iterator_page = link_iterator(soup)
#     try:
#         title = soup.find(attrs={"data-qa": "vacancy-title"}).text
#     except:
#         title = ""
#     try:
#         experience = soup.find(attrs={"data-qa": "vacancy-experience"}).text
#     except:
#         experience = ""
#     try:
#         salary = soup.find(
#             attrs={
#                 "class": "bloko-header-section-2 bloko-header-section-2_lite"
#             }
#         ).text.replace("\xa0", "")
#     except:
#         salary = ""
#     try:
#         employment = soup.find(
#             attrs={"data-qa": "vacancy-view-employment-mode"}
#         ).text
#     except:
#         employment = ""
#     try:
#         company = soup.find(
#             attrs={"data-qa": "bloko-header-2"}
#         ).text.replace("\xa0", " ")
#     except:
#         company = ""
#     try:
#         description = soup.find(
#             attrs={"class": "vacancy-branded-user-content"}).text
#     except:
#         try:
#             description = soup.find(attrs={"class": "g-user-content"}).text
#         except:
#             description = ""
#     try:
#         tags = [tag.text.replace("\xa0", " ") for tag in soup.find(
#             attrs={"class": "bloko-tag-list"}
#         ).find_all(attrs={"class": "bloko-tag__section_text"})]
#     except:
#         tags = []
#
#     jobs.append(
#         [
#             title,
#             url,
#             experience,
#             salary,
#             employment,
#             company,
#             description,
#             tags
#         ]
#     )
#
# def link_iterator(soup):
#     for a in soup.find_all("a", attrs={"class": "serp-item__title"}):
#         yield f"{a.attrs['href'].split('?')[0]}"
#
#
# async def get_page_data(session, iterator_page):
#     ua = fake_useragent.UserAgent()
#     for url in iterator_page:
#         async with session.get(url=url, headers={
#                     "user-agent": ua.random
#                 }) as response:
#             print(url)
#             response_text = await response.text()
#             soup = BeautifulSoup(response_text, "lxml")
#             try:
#                 title = soup.find(attrs={"data-qa": "vacancy-title"}).text
#             except:
#                 title = ""
#             try:
#                 experience = soup.find(attrs={"data-qa": "vacancy-experience"}).text
#             except:
#                 experience = ""
#             try:
#                 salary = soup.find(
#                     attrs={
#                         "class": "bloko-header-section-2 bloko-header-section-2_lite"
#                     }
#                 ).text.replace("\xa0", "")
#             except:
#                 salary = ""
#             try:
#                 employment = soup.find(
#                     attrs={"data-qa": "vacancy-view-employment-mode"}
#                 ).text
#             except:
#                 employment = ""
#             try:
#                 company = soup.find(
#                     attrs={"data-qa": "bloko-header-2"}
#                 ).text.replace("\xa0", " ")
#             except:
#                 company = ""
#             try:
#                 description = soup.find(attrs={"class": "vacancy-branded-user-content"}).text
#             except:
#                 try:
#                     description = soup.find(attrs={"class": "g-user-content"}).text
#                 except:
#                     description = ""
#             try:
#                 tags = [tag.text.replace("\xa0", " ") for tag in soup.find(
#                     attrs={"class": "bloko-tag-list"}
#                 ).find_all(attrs={"class": "bloko-tag__section_text"})]
#             except:
#                 tags = []
#
#             jobs.append(
#                 [
#                     title,
#                     url,
#                     experience,
#                     salary,
#                     employment,
#                     company,
#                     description,
#                     tags
#                 ]
#             )
#
#
# async def get_tasks(text):
#     ua = fake_useragent.UserAgent()
#     url_base = f"https://hh.ru/search/vacancy?area=113&search_field=name&search_field=company_name&search_field=description&text={text}&from=suggest_post&page=1"
#     async with aiohttp.ClientSession() as session:
#         response_base = await session.get(url=url_base, headers={
#                 "user-agent": ua.random
#             })
#         soup_base = BeautifulSoup(await response_base.text(), "lxml")
#         page_count = int(
#             soup_base.find(
#                 "div",
#                 attrs={
#                     "class": "pager"
#                 }
#             ).find_all(
#                 "span",
#                 recursive=False
#             )[-1].find("a").find("span").text
#         )
#
#         tasks = []
#
#         for page in range(page_count):
#             url_page = f"https://hh.ru/search/vacancy?area=113&search_field=name&search_field=company_name&search_field=description&text={text}&from=suggest_post&page={page}"
#             response_page = await session.get(
#                 url=url_page, headers={
#                     "user-agent": ua.random
#                 }
#             )
#             soup_page = BeautifulSoup(await response_page.text(), "lxml")
#             iterator_page = link_iterator(soup_page)
#             task = asyncio.create_task(get_page_data(session, iterator_page))
#             tasks.append(task)
#         await asyncio.gather(*tasks)
#
#
# async def _tasks(vac_name):
#     await get_tasks(vac_name)
#
#
# if __name__ == "__main__":
#     jobs = []
#     print("Start parsing...")
#     start_time = time.time()
#     vacancy_name = ' '.join(sys.argv[1:])
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(_tasks(vacancy_name))
#     asyncio.get_event_loop().run_until_complete(_tasks(vacancy_name))
#     with open(r"data\data.csv", "a", encoding="utf-8", errors="ignore") as file:
#         writer = csv.writer(file, delimiter=';')
#         for row in jobs:
#             writer.writerow(row)
#     print(f'Elapsed time: {round(time.time() - start_time, 2)}')
#
# if __name__ == "__main__":
#     stock_list = []
#     loop = asyncio.get_event_loop()
#
#     for i in range(1, 4):
#         html = loop.run_until_complete(get_html(url + "/?page=" + str(i)))
#         soup = BeautifulSoup(html, 'html.parser')
#         stock_list.extend(soup.find_all('a', class_='deal__discount-kz'))
#
#     try:
#         start = time.time()
#         coroutines = [loop.create_task(get_stock_data(i)) for i in stock_list]
#         loop.run_until_complete(asyncio.wait(coroutines))
#     finally:
#         loop.close()
#         print(f"Время выполнения: {time.time() - start}")

semaphore = asyncio.BoundedSemaphore(3)
jobs = []
urls = []

def get_content(link):
    ua = fake_useragent.UserAgent()
    try:
        data = requests.get(
            url=link,
            headers={
                "user-agent": ua.random
            }
        )
        if data.status_code != 200:
            return
        soup = BeautifulSoup(data.content, "lxml")
        return soup
    except:
        return


def get_count_pages(text):
    link = f"https://hh.ru/search/vacancy?area=113&search_field=name&search_field=company_name&search_field=description&text={text}&from=suggest_post&page=1"
    soup = get_content(link)
    if soup:
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
        return page_count
    return

def get_links(text, page_count):
    for page in range(page_count):
        soup = get_content(f"https://hh.ru/search/vacancy?area=113&search_field=name&search_field=company_name&search_field=description&text={text}&from=suggest_post&page={page}")
        if soup:
            for a in soup.find_all("a", attrs={"class": "serp-item__title"}):
                yield f"{a.attrs['href'].split('?')[0]}"
        else:
            continue


async def get_page_data(session, url):
    async with semaphore, session.get(url) as resp:
        assert resp.status == 200
        resp_text = await resp.text()
        soup = BeautifulSoup(resp_text, "lxml")
        title = soup.find(attrs={"data-qa": "vacancy-title"}).text
        experience = soup.find(attrs={"data-qa": "vacancy-experience"}).text
        salary = soup.find(
                                attrs={
                                    "class": "bloko-header-section-2 bloko-header-section-2_lite"
                                }
                            ).text.replace("\xa0", "")
        try:
            employment = soup.find(
                            attrs={"data-qa": "vacancy-view-employment-mode"}
                        ).text
        except:
            employment = ""
        try:
            company = soup.find(
                            attrs={"data-qa": "bloko-header-2"}
                        ).text.replace("\xa0", " ")
        except:
            company = ""
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

        jobs.append([
            title,
            url,
            experience,
            salary,
            employment,
            company,
            description,
            tags
        ])

async def load_site_data(urls):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            task = asyncio.create_task(get_page_data(session, url))
            tasks.append(task)
        await asyncio.gather(*tasks)

page_count = get_count_pages("python")
print('Start')
for link in get_links("python", page_count):
    urls.append(link)
    time.sleep(2)
print(f'Count links {len(urls)}')

async def _tasks(urls):
    await load_site_data(urls)

loop = asyncio.get_event_loop()
loop.run_until_complete(_tasks(urls))

with open(r"../data/data.csv", "a", encoding="utf-8", errors="ignore") as file:
    writer = csv.writer(file, delimiter=';')
    for row in jobs:
        writer.writerow(row)
print('The end')
