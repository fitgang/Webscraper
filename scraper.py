'''
Importing the required modules into the program.
'''
import pandas as pd
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import re
# from geopy.geocoders import Nominatim

'''
Pulling the web page containing the data about the stores.
'''
url = "https://www.nykaa.com/nykaa-stores-and-events-copy"

options = Options()
options.add_argument("--headless")

driver = webdriver.Firefox(options=options)
driver.get(url)
time.sleep(5)

html = driver.page_source
soup  = BeautifulSoup(html, 'html5lib')
soup.find('title').text

'''
Extracting the required data from the web page.
'''
# geolocator = Nominatim(user_agent="Extractor")

# # Input: a link of the form 'https://goo.gl/maps/LVg1WHTeQdy'
# # Output: a tuple with two floats like (27.487, 36.7896)
# def get_coordinates(address):
#     location = geolocator.geocode(address)
#     if location is None:
#         return ''
    
#     return (location.latitude, location.longitude)

df = pd.DataFrame(columns=['name', 'address', 'timing', 'phone'])
stores_list = soup.find('div', class_='nw-store-list').find_all('li')
for list_item in stores_list:
    bn_elem = list_item.find('div', class_='nw-store-box-name')

    name = bn_elem.contents[0] # STORE NAME

    timing = bn_elem.find('div', class_='time-text').text[7:] # STORE TIMIMG
    
    add_and_ph_text = list_item.find('div', class_='nw-store-box-address').text
    ap_arr = re.split("Ph:", add_and_ph_text, re.I)

    address = ap_arr[0] # STORE ADDRESS

    if len(ap_arr) == 2: 
        phone = ap_arr[1] # STORE PHONE NUMBER
    else:
        phone = '' # STORE PHONE NUMBER NOT FOUND

    # coordinates = get_coordinates(address) # STORE GEOGRAPHICAL COORDINATES
    
    new_entry = {'name': name, 'timing': timing, 'address': address, 'phone': phone}
    df = df.append(new_entry, ignore_index=True)

'''
Converting the extracted data to a CSV file.
'''
df.to_csv('nykaa stores.csv', index=False)