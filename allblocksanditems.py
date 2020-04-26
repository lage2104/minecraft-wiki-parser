import blocknames
import itemnames
import infobox

block_urls = blocknames.parseBlockNames()
item_urls = itemnames.parseItemNames()
data = []

for block_url in block_urls:
  block = infobox.parseInfoBox(block_url)
  print(block)
  data.append(block)
for item_url in item_urls:
  item = infobox.parseInfoBox(item_url)
  print(item)
  data.append(item)
