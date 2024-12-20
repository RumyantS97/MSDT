import asyncio
import aiohttp
from bs4 import BeautifulSoup as BS

PY_PAGE = 'https://www.python.org'

async def get_page(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

def parse_upcoming_events(page_html):
    bs = BS(page_html, 'html.parser')
    event_block = bs.find(text='Upcoming Events')
    event_list = event_block.parent.parent.find(class_='menu').find_all('li')
    event_links = [event.a['href'] for event in event_list]
    return event_links

async def get_event_info(session, link):
    event_info = {}
    async with session.get(f'{PY_PAGE}{link}') as response:
        event_page = await response.text()
        bs = BS(event_page, 'html.parser')

        title = bs.find(class_='single-event-title')
        event_info['title'] = title.string.strip() if title else 'No title'

        location = bs.find(class_='single-event-location')
        event_info['location'] = location.string.strip() if location else 'No location'

        date = bs.find(class_='single-event-date')
        event_info['date'] = ' '.join(date.get_text().split()) if date else 'No date'

    return event_info

async def get_events_info(links):
    events_info = []
    async with aiohttp.ClientSession() as session:
        tasks = [get_event_info(session, link) for link in links]
        events_info = await asyncio.gather(*tasks)
    return events_info

def pprint_events(events):
    for event in events:
        print('-' * 10)
        print(f"Title: {event['title']}\nLocation: {event['location']}\nDate: {event['date']}")

async def main():
    page = await get_page(PY_PAGE)
    event_links = parse_upcoming_events(page)
    events_info = await get_events_info(event_links)
    pprint_events(events_info)

asyncio.run(main())