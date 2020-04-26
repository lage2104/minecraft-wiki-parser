from bs4 import BeautifulSoup
import requests

url = "https://minecraft.gamepedia.com/Item"

def parseItemNames():
  data = []
  response = requests.get(url)
  html = response.text
  soup = BeautifulSoup(html,'html.parser')

  item_list = soup.find(id = "Items_that_create_blocks,_fluids_or_entities").find_next("ul").findAll("li")
  for item_li in item_list:
    data.append(item_li.find("a").attrs["href"].replace("/", ""))
  
  item_list = soup.find(id = "Items_with_use_in_the_world").find_next("ul").findAll("li")
  for item_li in item_list:
    data.append(item_li.find("a").attrs["href"].replace("/", ""))

  item_list = soup.find(id = "Items_with_indirect_use_in_the_world").find_next("ul").findAll("li")
  for item_li in item_list:
    data.append(item_li.find("a").attrs["href"].replace("/", ""))

  return data
