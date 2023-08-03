from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd

exoplanet_url = "https://exoplanets.nasa.gov/discovery/exoplanet-catalog/"
browser = webdriver.Chrome()
browser.get(exoplanet_url)

time.sleep(10)

planets_data = []
headers = ["Name", "Light-years from Earth", "Planet mass", "Stellar magnitude", "Discovery date"]

def webscrapping():
    for page in range(0,10):
        time.sleep(1)
        print(f"Scrapping data...({page+1})")
        soup = BeautifulSoup(browser.page_source, "html.parser")
        
        for ul_tags in soup.find_all("ul", attrs={"class", "exoplanet"}):
            li_tags = ul_tags.find_all("li")
            temp_list = []

            for i, li_tag in enumerate(li_tags):
                if i == 0:
                    temp_list.append(li_tag.find_all("a")[0].contents[0])

                else:
                    try:
                        temp_list.append(li_tag.contents[0])

                    except:
                        temp_list.append("")

            planets_data.append(temp_list)
            
        browser.find_element(By.XPATH, value='//*[@id="primary_column"]/div[1]/div[2]/div[1]/div/nav/span[2]/a').click()

webscrapping()

planets_table = pd.DataFrame(planets_data, columns=headers)
planets_table.to_csv("planets_table.csv", index=True, index_label="id")