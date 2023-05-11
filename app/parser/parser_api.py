import sys
import time
import re
import csv

import requests
from bs4 import BeautifulSoup
import fake_useragent
from parse_hh_data import download

JOBS = []


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


def get_profile(vacancy):
    vacancy_url = vacancy['alternate_url']
    vacancy_name = vacancy['name']
    employer_name = vacancy['employer']['name']
    area_name = vacancy['area']['name']
    schedule = vacancy['schedule']['name']
    employment = vacancy['employment']['name']
    experience = vacancy['experience']['name']
    if vacancy['salary']:
        salary_from = vacancy['salary']['from']
        salary_to = vacancy['salary']['to']
        salary_currency = vacancy['salary']['currency']
    else:
        salary_from = None
        salary_to = None
        salary_currency = None
    skills = [i.get('name') for i in vacancy['key_skills']]
    description = vacancy['description']

    return [
        vacancy_name,
        vacancy_url,
        employer_name,
        area_name,
        schedule,
        employment,
        experience,
        salary_from,
        salary_to,
        salary_currency,
        skills,
        description
    ]


if __name__ == "__main__":
    start_time = time.time()
    print('Start parsing...\t')
    vacancy_name = ' '.join(sys.argv[1:])
    page_count = get_count_pages(vacancy_name)
    print(f'Page count: {page_count}')
    count_vacancies = 0

    for link in get_links(vacancy_name, page_count):
        count_vacancies += 1
        vacancy_link = re.findall(r'\d+', link)[0]
        vacancy = download.vacancy(vacancy_link)
        profile = get_profile(vacancy)
        JOBS.append(profile)
        time.sleep(0.3)

    with open(r"../data/data.csv", "a", encoding="utf-8", errors="ignore") as file:
        writer = csv.writer(file, delimiter=';')
        for row in JOBS:
            writer.writerow(row)

    end_time = time.time()
    print(f'Count vacancies: {count_vacancies}')
    print(f'Elapsed time: {round(end_time - start_time, 2)} seconds')
