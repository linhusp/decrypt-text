import json
import time
from requests import session
from bs4 import BeautifulSoup


def main():
    # load header
    header = json.loads(open('./header.txt').read())

    # load user info
    info = json.loads(open('./info.txt').read())

    # get url
    base_url = 'http://teaching-quality-survey.tdt.edu.vn/stdlogin.aspx'
    querry = '?ReturnUrl=http%3a%2f%2flichhoc-lichthi.tdt.edu.vn%3a80%2ftkb2.aspx'
    url = base_url + querry

    # create session
    _session = session()

    # get login_page html
    login_page = get_soup(_session.get(url, headers=header))

    # fill login_page's payload
    payload = get_payload(login_page)
    for key in payload:
        l_key = key.lower()
        if 'mssv' in l_key or 'user' in l_key:
            payload[key] = info['username']
        elif 'pass' in l_key:
            payload[key] = info['password']

    # login
    login_direction = _session.post(url, data=payload)
    url = login_direction.url

    # get tkb_page
    tkb_page = get_soup(login_direction)

    # fill tkb_page's payload
    payload = get_payload(tkb_page)
    for option in tkb_page.find_all('option'):
        option_txt = option.find(text=True)
        if get_semester() in option_txt and get_years() in option_txt:
            option_parent = option.find_parent().get('name')
            payload[option_parent] = option.get('value')
            payload['__EVENTTARGET'] = option_parent
            break

    # get tkb's table
    tkb_page = get_soup(_session.post(url, data=payload))
    tkb_table = tkb_page.find(id='ThoiKhoaBieu1_tbTKBTheoTuan')

    # extracts tkb's data
    tkb_tr = [tkb_table.find('tr')] + tkb_table.find('tr').find_next_siblings()
    tkb_tr = [
        [
            td.find_all(text=True)
            for td in [tr.find()] + tr.find().find_next_siblings('td')
        ]
        for tr in tkb_tr
    ]

    for tr in tkb_tr:
        print(tr)


def get_payload(soup):
    return {t.get('name'): t.get('value') for t in soup.find_all('input')}


def get_soup(session):
    return BeautifulSoup(session.text, 'lxml')


def get_semester():
    return 'HK' + '1'


def get_years():
    return '2019-2020'


if __name__ == "__main__":
    t = time.time()
    main()
    print(time.time() - t)
