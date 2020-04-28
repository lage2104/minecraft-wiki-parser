from bs4 import BeautifulSoup
import requests
import blocknames
import itemnames
import infopage

base_url = "https://minecraft.gamepedia.com/"

# Retrive all block and item names (ex. Lava_Bucket)
block_urls = blocknames.parseBlockNames()
item_urls = itemnames.parseItemNames()
data = []

# Fetches an infopage for given url_name. url_name = element of block or item list /\
# Returns soup object
def fetchInfoPage(url_name):
  response = requests.get(base_url + url_name)
  html = response.text
  soup = BeautifulSoup(html,'html.parser')
  return soup

# Here everything happens
for block_url in block_urls:
  soup = fetchInfoPage(block_url)
  # creating a first data dictionary with the name of the block
  block_data = { "name": block_url.replace("_", " ") }
  # parseInfoBox appends information to the block_data dict.
  infopage.parseInfoBox(block_data, soup)
  # add it to the final array
  data.append(block_data)
  print(block_data)

# For items its the same procedure :D
for item_url in item_urls:
  soup = fetchInfoPage(item_url)
  item_data = { "name": item_url.replace("_", " ") }
  infopage.parseInfoBox(item_data, soup)
  data.append(item_data)
  print(item_data)
