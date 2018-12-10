# -*- coding: utf-8 -*-
#!/usr/bin/env python3
import urllib.request
from bs4 import BeautifulSoup
import json
import csv

with open('gulnur.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['name', 'company', 'region', 'payment_type', 'price'])

start_url = 'https://satu.kz/consumer-goods'
main_url = 'https://satu.kz'
example = 'https://satu.kz/Razvivayuschie-igrushki;2'

def get_len_of_pages(url):
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')
    div = soup.find('div', class_='x-pager__content')
    a = div.findAll('a')
    return int(a[-2].getText())


def get_tovary(url):
    tovary = []
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')
    divss = soup.find('div', class_='x-catalog-gallery__list')
    divs = divss.findAll('div', class_='x-gallery-tile__content')
    for div in divs:
        a = div.find('a', class_='x-gallery-tile__image-holder x-image-holder')
        tovary.append(a['href'])
    return tovary



def get_links(url):
    links = []
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')
    try:
        ul = soup.find('ul', class_='x-category-tile')
        lis = ul.findAll('li')
        for li in lis:
            div = li.find('div', class_='x-category-tile__title-holder')
            a = div.find('a', class_='x-category-tile__title')
            link = main_url + a['href']
            links.append(link)
        return (links)
    except AttributeError:
        pass


def get_infos(url):
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')
    name = soup.find('h1').getText(),
    company = soup.find('a', class_='x-company-info__name').getText()

    # data = json.loads(img["data-a-dynamic-image"])
    try:

        price = str(soup.find('span', class_='x-hidden').text.strip())
    except AttributeError:
        price='None'
    region = soup.find('span', class_='x-pseudo-link x-iconed-text__link').text.strip()
    payment_type = soup.find('div', class_='x-ellipsis').text.strip()
    contact = soup.find('span', {'data-qaid': 'show-all-phones-link'})
    # contact = soup.find('span', class_='x-pseudo-link x-iconed-text__link js-product-ad-conv-action')
    a = json.loads(contact["data-pl-phones"])
    cont = [x['number'] for x in a]
    try:
        price = price[:price.index('\n')]
    except ValueError:
        price = 'none'
    return [name, company, region, payment_type, price, cont]


links1 = get_links(start_url)
for link1 in links1:
    links2 = get_links(link1)
    for link2 in links2:
        links3 = get_links(link2)
        for link3 in links3:
            try:
                links4 = get_links(link3)
                for link4 in links4:
                    try:
                        links5 = get_links(link4)
                        for link5 in links5:
                            number = get_len_of_pages(link5)
                            for i in range(1, number + 1):
                                l = link5 + ';' + str(i)
                                tovary = get_tovary(l)
                                for tovar in tovary:
                                    infos = get_infos(tovar)

                                    with open('gulnur.csv', 'a') as csvfile:
                                        writer = csv.writer(csvfile)
                                        writer.writerow([infos[0], infos[1], infos[2], infos[3], infos[4], infos[5]])
                    except TypeError:
                        number = get_len_of_pages(link4)
                        for i in range(1, number + 1):
                            l = link4 + ';' + str(i)
                            tovary = get_tovary(l)
                            for tovar in tovary:
                                infos = get_infos(tovar)
                                with open('gulnur.csv', 'a') as csvfile:
                                    writer = csv.writer(csvfile)
                                    writer.writerow([infos[0], infos[1], infos[2], infos[3], infos[4], infos[5]])
            except TypeError:
                number = get_len_of_pages(link3)
                for i in range(1, number + 1):
                    l = link3 + ';' + str(i)
                    tovary = get_tovary(l)
                    for tovar in tovary:
                        infos = get_infos(tovar)
                        with open('gulnur.csv', 'a') as csvfile:
                            writer = csv.writer(csvfile)
                            writer.writerow([infos[0], infos[1], infos[2], infos[3], infos[4], infos[5]])


