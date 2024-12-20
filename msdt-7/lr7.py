import requests
from bs4 import BeautifulSoup as BS


PY_PAGE = 'https://www.python.org'


def get_page(url):
    page_html = requests.get(url).text
    return page_html


def parse_upcoming_events(page_html):
    bs = BS(page_html, 'html.parser')
    event_block = bs.find(text='Upcoming Events')
    event_list = event_block.parent.parent.find(class_='menu').find_all('li')
    event_links = [event.a['href'] for event in event_list]
    events_info = get_events_info(event_links)
    return events_info


def get_events_info(links):
    events_info = []
    for link in links:
        event_info = {}
        event_page = requests.get('{main_url}{event_link}'.format(
            main_url=PY_PAGE,
            event_link=link,
        )).text
        bs = BS(event_page, 'html.parser')

        title = bs.find(class_='single-event-title')
        event_info['title'] = title.string.strip()

        location = bs.find(class_='single-event-location')
        event_info['location'] = location.string.strip()

        date = bs.find(class_='single-event-date')
        event_info['date'] = ' '.join(date.get_text().split())

        events_info.append(event_info)

    return events_info


def pprint_events(events):
    for event in events:
        print('-'*10)
        print('Title: {title}\nLocation: {loc}\nDate: {date}'.format(
            title=event['title'],
            loc=event['location'],
            date=event['date'],
        ))


if __name__ == '__main__':
    page = get_page(PY_PAGE)
    upcoming_events = parse_upcoming_events(page)
    pprint_events(upcoming_events)