from bs4 import BeautifulSoup
import requests

url = "https://minecraft.gamepedia.com/Block"

def parseBlockNames():
  data = []
  response = requests.get(url)
  html = response.text
  soup = BeautifulSoup(html,'html.parser')

  block_list = soup.find(id = "List_of_blocks").find_next("ul").findAll("li")
  for block_li in block_list:
    if len(block_li.findAll("a")) == 1:
      data.append(block_li.find("a").attrs["href"].replace("/", ""))
    else:
      data.append(block_li.findAll("a")[1].attrs["href"].replace("/", ""))
  return data