from selenium import webdriver
from bs4 import BeautifulSoup

import time
import csv

START_URL="https://exoplanets.nasa.gov/discovery/exoplanet-catalog/"

browser= webdriver.Chrome("/Users/madanmohan/Desktop/class127/chromedriver")
browser.get(START_URL)
time.sleep(10)
planets_data = []
headers = ["name", "light_years_from_earth", "planet_mass", "stellar_magnitude", "discovery_date","hyperlink"]

def scrape():
    for i in range(1,5):
        while True:
            soup = BeautifulSoup(browser.page_source, "html.parser")

            #checking page number
            current_page_num=int(soup.find_all("input",attrs={"class","page_num"})[0].get("value"))

            if current_page_num<i:
               browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click() 
            elif current_page_num>i:
                browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[1]/a').click()
            else:
                break
        
        for ul_tag in soup.find_all("ul", attrs={"class", "exoplanet"}):
            li_tags = ul_tag.find_all("li")
            temp_list = []
            for index, li_tag in enumerate(li_tags):
                if index == 0:
                    temp_list.append(li_tag.find_all("a")[0].contents[0])
                else:
                    try:
                        temp_list.append(li_tag.contents[0])
                    except:
                        temp_list.append("")
            # get hyperlink
            hyperlink_li_tag=li_tags[0]
            temp_list.append("https://exoplanets.nasa.gov"+hyperlink_li_tag.find_all("a",href=True)[0]["href"])

            planets_data.append(temp_list)
        
        browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
        print(f"Page {i} scraping completed")


#calling function
scrape()   

new_planets_data=[]

def scrape_more_data(hyperlink):



#Calling method

for index, data in enumerate(planets_data):
    scrape_more_data(data[5])
    print(f"scraping at hyperlink {index+1} is completed.")

print(new_planets_data[0:10])

final_planet_data = []

for index, data in enumerate(planets_data):
    new_planet_data_element = new_planets_data[index]
    new_planet_data_element = [elem.replace("\n", "") for elem in new_planet_data_element]
    new_planet_data_element = new_planet_data_element[:7]
    final_planet_data.append(data + new_planet_data_element)


with open("final.csv", "w") as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(headers)
        csvwriter.writerows(final_planet_data)