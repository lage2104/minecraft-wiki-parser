from bs4 import BeautifulSoup
import requests
import blocknames
import itemnames
import infopage
import crawl
import time

import json

import logging



base_url = "https://minecraft.gamepedia.com/"

logger = logging.getLogger("minecraft-wiki-parser")
logger.setLevel(logging.INFO)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)15s - %(name)s - %(levelname)s - %(message)s')

ch.setFormatter(formatter)
logger.addHandler(ch)


def main():

  # Retrive all block and item names (ex. Lava_Bucket)
  blocks = blocknames.parseBlockNames()
  block_urls = []
  for block in blocks:
    block_urls.append(block['url'])
  block_responses = crawl.fetch_url_contents(block_urls)

  time.sleep(2)
  items = itemnames.parseItemNames()
  item_urls = []
  for item in items:
    item_urls.append(item['url'])
  item_responses = crawl.fetch_url_contents(item_urls)
  data = []

  # Here everything happens
  for idx, block in enumerate(blocks):
    soup = BeautifulSoup(block_responses[idx].text,'lxml')
    # parseInfoBox appends information to the block_data dict.
    block = infopage.parseInfoBox(block, soup)
    # add it to the final array

    receipe = infopage.parseReceipe(block,soup)
    block['receipe'] = receipe
    data.append(block)
    print(block)

  # For items its the same procedure :D
  for idx, item in enumerate(items):
    soup = BeautifulSoup(item_responses[idx].text,'lxml')
    item = infopage.parseInfoBox(item, soup)

    receipe = infopage.parseReceipe(item,soup)
    item['receipe'] = receipe

    data.append(item)
    print(item)

  print(data)

def download_wiki():
  logger.info("retrieve block list from minecraft wiki...")

  start = time.time()
  #retrieve all block names (ex. Lava_Bucket) and urls
  blocks = blocknames.parseBlockNames()
  end = time.time()
  logger.info("time to get block list: {} seconds".format(round(end-start,2)))
  logger.info("number of blocks: {}".format(len(blocks)))

  logger.info("retrieve blocks from minecraft wiki...")
  #write urls in list
  block_urls = []
  for block in blocks:
    block_urls.append(block['url'])
  #fetch html asyncly 
  start = time.time()
  block_responses = crawl.fetch_url_contents(block_urls)
  end = time.time()
  logger.info("time to get blocks: {} seconds".format(round(end-start,2)))

  #need to sleep, because of stupid retry error ...
  time.sleep(3)

  logger.info("retrieve item list from minecraft wiki...")
  #retrieve all item names and urls
  start = time.time()
  items = itemnames.parseItemNames()
  end = time.time()
  logger.info("time to get item list: {} seconds".format(round(end-start,2)))
  logger.info("number of items: {}".format(len(items)))

  #write urls in list
  item_urls = []
  for item in items:
    item_urls.append(item['url'])
  #fetch html asyncly
  start = time.time()
  item_responses = crawl.fetch_url_contents(item_urls)
  end = time.time()
  logger.info("time to get items: {} seconds".format(round(end-start,2)))

  #add html to block dict
  for idx,block_response in enumerate(block_responses):
    print(type(block_response))
    print(block_response.__class__.__name__)
    blocks[idx]['html'] = block_response.text

  #write blocks to json
  logger.info("write block to blocks.json")
  with open('blocks.json', 'w') as fp:
    json.dump(blocks, fp)

  #add to html to item dict
  for idx,item_response in enumerate(item_responses):
    items[idx]['html'] = item_response.text

  #write items to json
  logger.info("write block to blocks.json")
  with open('items.json', 'w') as fp:
    json.dump(items, fp)
  pass


if __name__ == "__main__":
    main()
    #download_wiki()