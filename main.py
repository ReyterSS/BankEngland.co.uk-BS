import requests
import json
from bs4 import BeautifulSoup
import lxml
import csv
import re
import math
import os

HEADERS = {
            'authority': 'www.bankofengland.co.uk',
            'method': 'POST',
            'path': '/_api/News/RefreshPagedNewsList',
            'scheme': 'https',
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-length': '231',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://www.bankofengland.co.uk',
            'referer': 'https://www.bankofengland.co.uk/news/prudential-regulation?NewsTypes'
                       '=65d34b0d42784c6bb1dd302c1ed63653&Taxonomies=b0e4487511a44c31b3c239c3d6470f42&InfiniteScrolling=False&Direction=Latest',
            'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
            'sec-ch-ua-mobile': '?0',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/92.0.4515.159 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest'
}

HEADERS2 = {
    'authority': 'www.bankofengland.co.uk',
    'method': 'GET',
    'path': '/prudential-regulation/regulatory-digest/2021/july',
    'scheme': 'https',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'max-age=0',
    'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
    'sec-ch-ua-mobile': '?0',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
}

data2 = {'Id': '{CE377CC8-BFBC-418B-B4D9-DBC1C64774A8}',
                 'PageSize': '30',
                 'NewsTypesAvailable[]': '65d34b0d42784c6bb1dd302c1ed63653',
                 'Taxonomies[]': 'b0e4487511a44c31b3c239c3d6470f42',
                  'Page': 2, #'Page': f'1',
                 'Direction': '1',
                 'Grid': 'false',
                 'InfiniteScrolling': 'false'
}

url = 'https://www.bankofengland.co.uk/_api/News/RefreshPagedNewsList'
url2 = 'https://www.bankofengland.co.uk/news/prudential-regulation?NewsTypes=65d34b0d42784c6bb1dd302c1ed63653&Taxonomies=b0e4487511a44c31b3c239c3d6470f42&InfiniteScrolling=False&Direction=Latest'
HOST = 'https://www.bankofengland.co.uk'

def number_realese():
    s = requests.post(url, headers=HEADERS, data=data2)  # , , ,
    soup = str(BeautifulSoup(s.text, 'html.parser'))
    json_file = json.loads(soup)
    req = requests.post(url, headers=HEADERS2, data=data2)  # ,
    soup34 = str(BeautifulSoup(req.text, 'html.parser'))
    json_file1 = json.loads(soup34)
    info11 = json_file.get('Results')
    soup2345 = BeautifulSoup(info11, 'lxml')
    num_pages = soup2345.find(id="resultCount").text
    number1 = re.sub('\D+', '', num_pages)
    num_pages2 = math.ceil(int(number1) / 30) + 1
    return (num_pages2)

def pagenation(num_pages2):
    os.path.dirname("PDF")
    if not os.path.exists("PDF"):
        os.makedirs("PDF")
    for page in range(1, int(num_pages2)):
        data1 = {'Id': '{CE377CC8-BFBC-418B-B4D9-DBC1C64774A8}',
                 'PageSize': '30',
                 'NewsTypesAvailable[]': '65d34b0d42784c6bb1dd302c1ed63653',
                 'Taxonomies[]': 'b0e4487511a44c31b3c239c3d6470f42',
                 'Page': page,
                 'Direction': '1',
                 'Grid': 'false',
                 'InfiniteScrolling': 'false'
        }
        s = requests.post(url,headers = HEADERS,data=data1)#, , ,
        soup = str(BeautifulSoup(s.text, 'html.parser'))
        json_file = json.loads(soup)
        info1 = json_file.get('Results')
        soup = BeautifulSoup(info1, 'lxml')
        material = soup.find_all('a')[:-4]
        project_url=[]
        for i in material:
            hrefs = HOST + i.get('href')
            project_url.append(hrefs)
        for link1 in project_url:
            r = requests.get(url=link1)
            soup5 = BeautifulSoup(r.text, 'html.parser')
            block5 = soup5.find(class_='btn btn-pubs btn-has-img btn-lg')
            if link1:
                name_f1 = 'PRA Regulatory Digest ' + link1.split('/')[-2] + ' ' + link1.split('/')[-1]
            else:
                name_f1 = ''
            if block5:
                if block5:
                    block6 = HOST + block5.get('href')
                    if block6:
                        r2 = requests.get(block6, 'html.parser')
                        with open(f'PDF/{name_f1}.pdf', 'wb') as file:
                            file.write(r2.content)
                    else:
                        r2 = ' '
                else:
                    block6 = print(' Block 6 is missing')
            else:
                block5 = print('Block 5 is missing')

        for x in project_url:
            each_page = requests.get(x, headers=HEADERS2)
            soup2 = BeautifulSoup(each_page.text, 'html.parser')
            page22 = soup2.find_all(class_='page-section')[0]
            date = page22.find('div', class_='published-date')
            if date:
                date1 = date.text.strip()
            else:
                date1 = ''
            title = soup2.title.string
            if title:
                title1 = title.strip()
            else:
                title1 = ''
            begin = soup2.find(class_='page-banner').find(class_='hero')#.text
            if begin:
                begin1 = begin.text.strip()
            else:
                begin1 = ''
            titles = soup2.find_all('div', class_='page-content')
            project_titles = []
            if titles:
                for y in titles:
                    titles2 = y.find_all('h2')
                    for b in titles2:
                        titles3 = b.text
                        project_titles.append(titles3)
            else:
                titles3 = ' '
            data = {'Дата публікаціі': date1,
                            'Титулка': title1,
                            'Вступ': begin1,
                            'Зміст': project_titles,
                    }
            write_csv(data)

def write_csv(data):
    file_name = 'Bank_England.csv'
    with open(file_name, 'a',encoding='utf-8') as f:
        w = csv.DictWriter(f, data.keys())
        if f.tell() == 0:
            w.writeheader()
        w.writerow(data)

def main():
    numb_realese = number_realese()
    pag = pagenation(numb_realese)
    csv_file = write_csv(pag)


if __name__ == '__main__':
    main()