import requests
import pandas as pd
import openpyxl
from bs4 import BeautifulSoup
url="https://www.ndtv.com/news"

response=requests.get(url)
ndtv=response.content
# print(ndtv)

soup=BeautifulSoup(ndtv,'html.parser')

# import pandas as pd

# Assuming you have already fetched and parsed the HTML content
soup = BeautifulSoup(ndtv, "html.parser")

# Find all elements with the class "item-title"
ajit = soup.find_all("a", class_="item-title")

# Create lists to store the text and link
txt_list = []
link_list = []

# Extract the text content and link of each element and append them to the respective lists
for element in ajit:
    txt = element.text
    # about_index = txt.find("About Us")
    # if about_index != -1:
    #     txt = txt[:about_index]
    link = element["href"]
    
    txt_list.append(txt)
    link_list.append(link)

# Create a DataFrame with the txt_list and link_list
df = pd.DataFrame({"current": txt_list, "link": link_list})

# Save the DataFrame to an Excel file
df.to_excel("output.xlsx", index=False)