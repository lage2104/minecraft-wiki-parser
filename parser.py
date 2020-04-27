from bs4 import BeautifulSoup
import requests
import blocknames
import itemnames
import infobox

base_url = "https://minecraft.gamepedia.com/"

block_urls = blocknames.parseBlockNames()
item_urls = itemnames.parseItemNames()
data = []

def fetchInfoPage(url_name):
  response = requests.get(base_url + url_name)
  html = response.text
  soup = BeautifulSoup(html,'html.parser')
  return soup

for block_url in block_urls:
  soup = fetchInfoPage(block_url)
  block = infobox.parseInfoBox(soup)
  print(block)
  data.append(block)
for item_url in item_urls:
  soup = fetchInfoPage(block_url)
  item = infobox.parseInfoBox(item_url)
  print(item)
  data.append(item)
