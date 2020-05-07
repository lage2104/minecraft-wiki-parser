from bs4 import BeautifulSoup
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


baseurl = "https://minecraft.gamepedia.com/"
url = "https://minecraft.gamepedia.com/Block"

def parseBlockNames():
  data = []
  session = requests.Session()
  retry = Retry(connect=3,backoff_factor=1)
  adapter = HTTPAdapter(max_retries=retry)
  session.mount('http://', adapter)
  session.mount('https://', adapter)
  response = session.get(url)
  html = response.text
  soup = BeautifulSoup(html,'html.parser')

  block_list = soup.find(id = "List_of_blocks").find_next("ul").findAll("li")
  for block_li in block_list:
    if len(block_li.findAll("a")) == 1:
      blockname = block_li.find("a").attrs["href"].replace("/", "")
      data.append({"id": blockname.replace("(", "").replace(")", "").lower(), "name":blockname.replace("_", " "),"url":baseurl+blockname})
    else:
      blockname = block_li.findAll("a")[1].attrs["href"].replace("/", "")
      data.append({"id": blockname.replace("(", "").replace(")", "").lower(), "name":blockname.replace("_", " "),"url":baseurl+blockname})
  return data