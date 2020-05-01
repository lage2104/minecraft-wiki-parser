import re

url = "https://minecraft.gamepedia.com/"

def parseInfoBox(data, soup):
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

def parseItemType(data, soup):
  data["item_type"] = "Not set"

def parseReceipe(block_data,soup):
  #index for mutiple output
  index = -1
  receipe = {}

  #empty list
  receipe['ingredients'] = []

  crafting_table = soup.find("table",{"data-description":"Crafting recipes"}) 

  #check if there is at least one receipe on the site
  receipe_outputs = crafting_table.findAll("span",{"class":"mcui-output"})
  
  if receipe_outputs == None:
    return
  if len(receipe_outputs) == 0:
    return
  print(len(receipe_outputs))
  receipe_output = receipe_outputs[0]

  shapeless = soup.find("span",{"class":"mcui-shapeless"})
  if shapeless !=None:
    receipe['type'] = 'shapeless'
  else:
    receipe['type'] = 'shapefull'

  

  items = receipe_output.findAll("span",{"class":"invslot-item"})
  for idx, item in enumerate(items):
    itemDescription = item.find("a")
    itemname=""
    if itemDescription == None:
      itemDescription = item.find("span")
    if itemDescription == None:
      itemDescription = item.find("img")
    itemname = itemDescription['title']
    if itemname == block_data['name']:
      index = idx
      break
  
  if index == -1:
    return 
  
  receipe_input = soup.find("span",{"class":"mcui-input"})
  rows = receipe_input.findAll("span",{"class":"mcui-row"})
  for rownum, row in enumerate(rows):
    cols = row.findAll("span",{"class":"invslot"})
    for colnum,col in enumerate(cols):
      items = col.findAll("span",{"class":"invslot-item"})
      if len(items) > 1:
        item = items[(index % len(items))]
        itemDescription = item.find("a")
        itemname=""
        if itemDescription == None:
          itemDescription = item.find("span")
        
        itemname = itemDescription['title']

        slotnum=rownum*3+colnum+1
        receipe['ingredients'].append({"slot":slotnum,
        "item":itemname})
      elif len(items) == 1:
        item = items[0]
        itemname=""
        if itemDescription == None:
          itemDescription = item.find("span")
        
        itemname = itemDescription['title']
        slotnum=rownum*3+colnum+1
        receipe['ingredients'].append({"slot":slotnum,
        "item":itemname})

  return receipe