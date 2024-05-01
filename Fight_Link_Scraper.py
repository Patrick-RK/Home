import requests
from bs4 import BeautifulSoup
from fight_link_loop import random_sleep, date_check
import pandas as pd
import random
import re

def update_csv(file_path, new_data):

    existing_data = pd.read_csv(file_path)

    new_data_df = pd.DataFrame(new_data)

    # Append the new data to the existing data
    result_df = existing_data.append(new_data_df, ignore_index=True)

    # Write the combined data back to the CSV file
    result_df.to_csv(file_path, index=False)

    random_sleep()

def get_card_links(url):

    response = requests.get(url)

    if response.status_code == 200:

        soup = BeautifulSoup(response.text, 'html.parser')

        card_details = soup.find_all('li',class_="b-list__box-list-item")
        card_details_data = []

        for i in card_details:
            details_string = (i.get_text())
            cleaned_text = re.sub(r'\s+', ' ', str(details_string))
            split_details = cleaned_text.split(":")
            card_details_data.append(split_details[1])


        title = soup.find('span', class_='b-content__title-highlight')
        title_text = title.text.strip()


        # Find all links with the specified class and structure
        links = soup.find_all(class_="b-fight-details__table-col b-fight-details__table-col_style_align-top")

        link_text = []


         # Extract the data and store it in the lists
        for link in links:

            a_element = link.find('a')

            # Extract the 'href' attribute of the <a> element to get the link
            link_url = a_element['href']

            # Extract the link URL

            link_text.append(link_url)

        # Create a DataFrame

        data = {'Link': link_text, 'Event': title_text, 'Date': card_details_data[0], 'Location': card_details_data[1], 'Progress': False }
        df = pd.DataFrame(data)

        # Save the data to an Excel file
        old_file_path = 'ufc_card_links3.csv'

        update_csv(old_file_path, df)


    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")





