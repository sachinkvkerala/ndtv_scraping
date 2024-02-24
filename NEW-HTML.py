import pandas as pd
import requests
from bs4 import BeautifulSoup

heat_list = []

api = "https://www.energystar.gov/productfinder/product/certified-central-air-conditioners/results?page_number="
url_list = list(range(26)) + list(range(25, -1, -1))

for i in url_list:
    res = api + str(i)
    response = requests.get(res)
    text = response.text
    soup = BeautifulSoup(text, 'html.parser')
    rowheading = soup.find_all('div', attrs={'class': 'row'})
    
    for j in rowheading:
        heat_dict = {}
        title = j.find_all('div', attrs={'class': 'title'})
        
        for tit in title:
            brand_title = tit.text.replace("\n", "").strip()
            brand_title_split = brand_title.split("-")
            
            if len(brand_title_split) == 2:
                heat_dict['brand-name'] = brand_title_split[0].strip()
                heat_dict['name'] = brand_title_split[1].strip()
            else:
                heat_dict['brand-name'] = brand_title_split[0].strip()
                heat_dict['name'] = brand_title
            
        head = ""  # Initialize head with a default value
        field = j.find_all('div', attrs={'class': 'field'})
        
        for fei in field:
            label = fei.find_all('div', attrs={'class': 'label'})
            
            for lab in label:
                head = lab.text.replace("\n", "").strip()
                
            value = fei.find_all('div', attrs={'class': 'value'})
            
            for val in value:
                value_txt = val.text.replace("\n", "").strip()
                heat_dict[head] = value_txt
                
        if heat_dict:
            heat_list.append(heat_dict)

df = pd.DataFrame.from_dict(heat_list)

# Trim whitespace from all columns
df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

df.to_excel('Central Air Conditioners (Ducted)-RAW.xlsx', index=False)

print(len(heat_list))
