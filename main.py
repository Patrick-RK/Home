

from bs4 import BeautifulSoup
import pandas as pd
import requests


all_events_url = 'http://www.ufcstats.com/statistics/events/completed?page=all'


response = requests.get(all_events_url)


if response.status_code == 200:

    soup = BeautifulSoup(response.text, 'html.parser')

    elements = soup.find_all(class_='b-statistics__table-content')


    event_names = []
    event_dates = []
    event_links = []

    for element in elements:
        event_name = element.find('a').text.strip()
        event_date = element.find('span', class_='b-statistics__date').text.strip()
        link = element.find('a')['href']

        event_names.append(event_name)
        event_dates.append(event_date)
        event_links.append(link)

    data = {'Event Name': event_names, 'Event Date': event_dates, 'Event Link': event_links, 'Scrape_Progress': False }
    df = pd.DataFrame(data)

    df.to_csv('ufc_events_test.csv', index=False)

else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")