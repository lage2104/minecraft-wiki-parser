from bs4 import BeautifulSoup
import requests
import re

url = "https://minecraft.gamepedia.com/"

def parseInfoBox(url_name):
  data = { "name": url_name.replace("_", " "), "url_name": url_name, "stack_size": 1 }
  response = requests.get(url + url_name)
  html = response.text
  soup = BeautifulSoup(html,'html.parser')
  infobox_table = soup.find("table", {"class": "infobox-rows"})
  

  for row in infobox_table.findAll("tr"):
    key = row.find("th").get_text().strip()
    value = row.find("td").get_text().strip()
    if key == "Stackable":
      if "Yes" in value:
        data["stack_size"] = int(re.findall(r'\d+', value)[0])
      else:
        data["stack_size"] = 1
  
  return data