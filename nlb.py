import requests
import cachetools.func
from bs4 import BeautifulSoup

CATALOGUE_URL = 'https://catalogue.nlb.gov.sg/cgi-bin/spydus.exe/ENQ/WPAC/BIBENQ'
CATALOGUE_TITLE_DETAILS_URL = 'https://catalogue.nlb.gov.sg/cgi-bin/spydus.exe/XFULL/WPAC/BIBENQ/{magic_number}/{bid}?FMT=REC'
CATALOGUE_AVAILABILITIES_URL = 'https://catalogue.nlb.gov.sg/cgi-bin/spydus.exe/XHLD/WPAC/BIBENQ/{magic_number}/{bid}?RECDISP=REC'

## Cache the magic number for 5 minutes
@cachetools.func.ttl_cache(maxsize=1, ttl=5*60)
def _get_magic_number():
    res = requests.get(CATALOGUE_URL)
    soup = BeautifulSoup(res.text, 'html.parser')

    data_returnurl = soup.find('nlb-mylibrary').get('data-returnurl').strip()
    magic_number = int(data_returnurl.split('/')[-1])
    return magic_number

## { title: ..., author: ... }
def get_title_details(bid):
    magic_number = _get_magic_number()
    title_details_url = CATALOGUE_TITLE_DETAILS_URL.format(magic_number=magic_number, bid=bid)

    res = requests.get(title_details_url)
    soup = BeautifulSoup(res.text, 'html.parser')

    title = soup.find(class_='card-title').find('a').text
    author = soup.find(class_='recdetails').find('span').text

    if title is None or author is None:
        raise Exception('Title details could not be found, perhaps the book id is incorrect?')

    return { 'title': title, 'author': author }

## [ { branch_name: ..., shelf_location: ..., call_number: ..., status_desc: ... } ]
def get_availability_info(bid):
    magic_number = _get_magic_number()
    availabilities_url = CATALOGUE_AVAILABILITIES_URL.format(magic_number=magic_number, bid=bid)

    res = requests.get(availabilities_url)
    soup = BeautifulSoup(res.text, 'html.parser')

    dispatch_td_caption = {
        'Library':                lambda td: { 'branch_name': td.find('a').find('span').text.strip() },
        'Section/Shelf Location': lambda td: { 'shelf_location': td.find('book-location').text.strip() },
        'Call Number':            lambda td: { 'call_number': ' '.join(span.text for span in td.find_all('span')).strip() },
        'Item Status':            lambda td: { 'status_desc': td.find('span').text.strip() }
    }

    def parse_tr(tr):
        tds = tr.find_all('td')
        properties = [dispatch_td_caption[td.get('data-caption')](td) for td in tds]
        merged_properties = { k: v for d in properties for k, v in d.items() }
        return merged_properties

    trs = soup.find('tbody').find_all('tr')
    properties_dict = [parse_tr(tr) for tr in trs]

    return properties_dict


## For testing purposes
if __name__ == '__main__':

    ## 149910874 -- The Annotated Alice
    a = get_title_details(149910874)
    b = get_availability_info(149910874)

    ## 188992694 -- Aristotle and Dante
    c = get_title_details(188992694)
    d = get_availability_info(188992694)

    ## 274100838 -- This Is What Inequality Looks Like
    e = get_title_details(274100838)
    f = get_availability_info(274100838)
