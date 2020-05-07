from bs4 import BeautifulSoup
import requests

from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
baseurl = "https://minecraft.gamepedia.com/"
url = "https://minecraft.gamepedia.com/Item"



def parseItemNames():
  data = []
  session = requests.Session()
  retry = Retry(connect=5,backoff_factor=5)
  adapter = HTTPAdapter(max_retries=retry)
  session.mount('http://', adapter)
  session.mount('https://', adapter)
  response = session.get(url)
  html = response.text
  soup = BeautifulSoup(html,'html.parser')

  item_list = soup.find(id = "Items_that_create_blocks,_fluids_or_entities").find_next("ul").findAll("li")
  for item_li in item_list:
    itemname = item_li.find("a").attrs["href"].replace("/", "")
    data.append({"id": itemname.replace('(','').replace(')','').lower(), "name":itemname.replace("_", " "),"url":baseurl+itemname})
  
  item_list = soup.find(id = "Items_with_use_in_the_world").find_next("ul").findAll("li")
  for item_li in item_list:
    itemname = item_li.find("a").attrs["href"].replace("/", "")
    data.append({"id": itemname.replace("(", "").replace(")", "").lower(), "name":itemname.replace("_", " "),"url":baseurl+itemname})

  item_list = soup.find(id = "Items_with_indirect_use_in_the_world").find_next("ul").findAll("li")
  for item_li in item_list:
    itemname = item_li.find("a").attrs["href"].replace("/", "")
    data.append({"id": itemname.replace("(", "").replace(")", "").lower(), "name":itemname.replace("_", " "),"url":baseurl+itemname})

  return data
