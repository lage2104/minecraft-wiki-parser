import requests
import blocknames
import itemnames
import infopage
import crawl
import time

import json

import logging

import sys



base_url = "https://minecraft.gamepedia.com/"

logger = logging.getLogger("minecraft-wiki-parser")
logger.setLevel(logging.INFO)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)15s - %(name)s - %(levelname)s - %(message)s')

ch.setFormatter(formatter)
logger.addHandler(ch)

def download_wiki():
  """
  Downloads items and block from minecraft wiki into items.json and blocks.json
  :return:
  """
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

def main():
  data = []
  if len(sys.argv) == 2:
    if sys.argv[1] == '--init':
      download_wiki()

  logger.info("Reading blocks from blocks.json file")
  blocks = None
  with open('blocks.json') as file:
    blocks = json.load(file)

  logger.info("Reading items from items.json file")
  items = None
  with open('items.json') as file:
    items = json.load(file)

  blockslen = len(blocks)
  logger.info("Start to parse {} blocks".format(blockslen))
  # Here everything happens
  start = time.time()
  
  for idx,block in enumerate(blocks):
    if idx % 20 == 0:
      logger.info("Progress: {}/{}".format(idx,blockslen))
      end = time.time()
      logger.info("Elapsed time: {} seconds".format(round(end-start,2)))
    # parseInfoBox appends information to the block_data dict.
    block = infopage.parseInfoBox(block)

    receipe = infopage.parseReceipe(block)
    block['receipe'] = receipe
    if 'html' in block:
      block.pop('html')

    # add it to the array
    data.append(block)

  itemlen=len(items)
  # For items its the same procedure :D
  for idx,item in enumerate(items):
    if idx % 20 == 0:
      logger.info("Progress: {}/{}".format(idx,itemlen))
      end = time.time()
      logger.info("Elapsed time: {} seconds".format(round(end-start,2)))
    item = infopage.parseInfoBox(item)

    receipe = infopage.parseReceipe(item)
    item['receipe'] = receipe
    if 'html' in item:
      item.pop('html')

    # add it to the array
    data.append(item)

  with open('data.json', 'w') as fp:
    json.dump(data, fp)

if __name__ == "__main__":
    main()
    #items = None
    #with open('items.json') as file:
    #  items = json.load(file)
    #item = infopage.parseInfoBox(items[0])
    #item = infopage.parseReceipe(item)
    pass