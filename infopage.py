import re
from bs4 import BeautifulSoup, SoupStrainer

url = "https://minecraft.gamepedia.com/"
def parseInfoBox(data):
  """
  Parses info box element on a block/item page on mincecraft wiki
  :param data: dict element for item or block
  :return: dict with enriched data
  """
  strainer = SoupStrainer("table", {"class": "infobox-rows"})
  soup = BeautifulSoup(data['html'],'lxml',parse_only=strainer)

  data["stack_size"] = 1
  infobox_table = soup.find("table", {"class": "infobox-rows"})
  if infobox_table == None:
    return data
  for row in infobox_table.findAll("tr"):
    key = row.find("th").get_text().strip()
    value = row.find("td").get_text().strip()
    if key == "Stackable":
      if "Yes" in value:
        data["stack_size"] = int(re.findall(r'\d+', value)[0])
  return data

def parseItemDescription(data):
  strainer = SoupStrainer("div", {"class": "mw-parser-output"})
  soup = BeautifulSoup(data['html'],'lxml',parse_only=strainer)
  desc = soup.find("div", {"class": "mw-parser-output"}).find("p", recursive=False).getText().strip()
  data["description"] = desc.replace("\n", " ").replace("\"", "").encode('ascii', 'ignore').decode("utf-8")
  return data

def parseItemType(data):
  # Only for items, blocks are always "placeable"
  data["item_type"] = "Not set"


def parse_shape(soup):
  """
  parses shape information
  :param soup: whole table
  :return: shapeinformation
  """
  shapeless = soup.find("span",{"class":"mcui-shapeless"})
  if shapeless is not None:
    return 'shapeless'
  else:
    return 'shapefull'

def parse_output_amount(soup):
  """
  parses output amount
  :param soup: mcui-output
  :return: output amount
  """
  output_stacksize = soup.find("span",{"class":"invslot-stacksize"})
  if output_stacksize is None:
    return 1
  else:
    return int(output_stacksize.text)

def get_output_index(objects,name):
  """
  parse index of item
  :param objects: mcui-output ==> invslot-item
  :param name: name block/item
  :return: index
  """
  for idx, item in enumerate(objects):
    itemDescription = item.find("a")
    itemname=""
    if itemDescription == None:
      itemDescription = item.find("span")
    if itemDescription == None:
      itemDescription = item.find("img")
    itemname = itemDescription['title']
    if itemname == name:
      return idx
  return -1

def parseReceipe(data):
  """
  parses receipe on a block/item page on minecraft wiki
  :param data: dict element for item/block
  :return: receipe
  """
  strainer = SoupStrainer("table",{"data-description":"Crafting recipes"})
  soup = BeautifulSoup(data['html'],'lxml',parse_only=strainer)

  #index for mutiple output
  receipe = {}

  crafting_table = soup.find("table",{"data-description":"Crafting recipes"}) 
  if crafting_table == None:
    return

  receipe_outputs = crafting_table.findAll("span",{"class":"mcui-output"})
  #check if there is at least one receipe on the site 
  if receipe_outputs == None:
    return
  if len(receipe_outputs) == 0:
    return

  #we only parse one object
  receipe_output = receipe_outputs[0]

  receipe['type'] = parse_shape(soup)

  receipe['output_amount'] = parse_output_amount(receipe_output)
  
  items = receipe_output.findAll("span",{"class":"invslot-item"})
  
  index = get_output_index(items,data['name'])
  if index == -1:
    return 
  
  #empty list
  receipe['ingredients'] = []

  receipe_input = soup.find("span",{"class":"mcui-input"})
  rows = receipe_input.findAll("span",{"class":"mcui-row"})
  for rownum, row in enumerate(rows):
    cols = row.findAll("span",{"class":"invslot"})
    for colnum,col in enumerate(cols):
      items = col.findAll("span",{"class":"invslot-item"})
      if len(items) > 1:
        item = items[(index % len(items))]
      elif len(items) == 1:
        item = items[0]
      if len(items) > 0:
        itemDescription = item.find("a")
        itemname=""
        if itemDescription is None:
          itemDescription = item.find("span")
        if itemDescription is None:
          itemname=""
        else:
          itemname = itemDescription['title'].replace(' ','_').lower()

        slotnum=rownum*3+colnum+1
        receipe['ingredients'].append({"slot":slotnum,
        "item":itemname})
  return receipe