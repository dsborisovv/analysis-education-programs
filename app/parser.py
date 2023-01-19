import json
import time

import requests
from bs4 import BeautifulSoup
import fake_useragent


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
        return 1
    return


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


def get_links(text, page_count):
    for page in range(page_count):
        soup = get_content(f"https://hh.ru/search/vacancy?area=113&search_field=name&search_field=company_name&search_field=description&text={text}&from=suggest_post&page={page}")
        if soup:
            for a in soup.find_all("a", attrs={"class": "serp-item__title"}):
                yield f"{a.attrs['href'].split('?')[0]}"
        else:
            continue


def get_vacancies(link):
    soup = get_content(link)
    if soup:
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
            description = soup.find(attrs={"class": "g-user-content"}).text
        except:
            description = ""
        try:
            tags = [tag.text.replace("\xa0", " ") for tag in soup.find(
                attrs={"class": "bloko-tag-list"}
            ).find_all(attrs={"class": "bloko-tag__section_text"})]
        except:
            tags = []

        vacancy = {
            'title': title,
            'link': link,
            'experience': experience,
            'salary': salary,
            'employment': employment,
            'company': company,
            'description': description,
            "tags": tags
        }

        return vacancy
    return


if __name__ == "__main__":
    start_time = time.time()
    data = []
    page_count = get_count_pages("python")
    for link in get_links("python", page_count):
        vacancy = get_vacancies(link)
        if not vacancy:
            continue
        data.append(vacancy)
        time.sleep(1)
        with open(r"data\data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=5, ensure_ascii=False)
    print('All good!')
    print(f'Elapsed time {time.time() - start_time}')
