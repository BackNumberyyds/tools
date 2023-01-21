from django.shortcuts import render
from lxml import html
import requests

# Create your views here.


def index(request, word):
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0",
    }

    def short(long):
        match long:
            case "adjective":
                return "a"
            case "adverb":
                return "ad"
            case "noun":
                return "n"
            case "verb":
                return "v"
            case "exclamation":
                return "e"
            case _:
                return "unknow"

    page = requests.get(
        'https://dictionary.cambridge.org/dictionary/english-chinese-simplified/' + word, headers=HEADERS)
    tree = html.fromstring(page.text)
    parts = tree.xpath(
        '//*[@id="page-content"]/div[2]/div[4]/div/div/div[@class="pr entry-body__el"]')
    lst = []
    for p in range(0, len(parts)):
        lst.append('')
        # 词性
        plst = parts[p].xpath('./div[2]/div[2]/span/text()')
        for i in range(0, len(plst)):
            plst[i] = short(plst[i])
        lst[-1] += '/'.join(plst) + '. '
        # 释义
        mlst = parts[p].xpath(
            './div[3]/div[contains(@class, "pr dsense")]/div[2]/div[@class="def-block ddef_block "]/div[3]/span/text()')
        if len(mlst) == 0:
            lst.pop()
        else:
            lst[-1] += '；'.join(mlst)

    return render(request, 'index.html', context={'text': '；'.join(lst)})
