from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import time
import pandas as pd

exoplanet_url = "https://exoplanets.nasa.gov/discovery/exoplanet-catalog/"
browser = webdriver.Chrome()
browser.get(exoplanet_url)

time.sleep(10)

new_planets_data = []

def new_scrapper(hyperlink):
    try:
        page = requests.get(hyperlink)
        soup = BeautifulSoup(page.content, "html.parcel")
        temp_list = []

        for tr_tags in soup.find_all("tr", attrs={"class", "fact_row"}):
            td_tags = tr_tags.find_all("td")
            
            for td_tag in td_tags:
                try:
                    temp_list.append(td_tag.find_all("div", attrs={"class", "value"})[0].contents[0])
                
                except:
                    temp_list.append("")

        new_planets_data.append(temp_list)

    except:

        time.sleep(1)
        new_scrapper(hyperlink)

planets_table = pd.read_csv("planets_table.csv")

for i, row in planets_table.iterrows():
    print(row["hyperlink"])
    new_scrapper(row["hyperlink"])
    print(f"Completed data scrapping of hyperlink...({i+1})")

new_scrapper_data = []

for row in new_planets_data:
    replace = []

    for cell in row:
        cell = cell.replace("\n", "")
        replace.append(cell)

    new_scrapper_data.append(replace)

print(new_scrapper_data)
headers = ["Planet Type", "Discovery Date", "Mass", "Planet Radius", "Orbital Radius", "Orbital Period", "Eccentricity", "Detection Method"]

planets_detail_table = pd.DataFrame(new_scrapper_data, columns=headers)
planets_detail_table.to_csv("planets_detail_table.csv", index=True, index_label="id")