import blocknames
import infobox

blocks = blocknames.parseBlockNames()
for block in blocks:
  print(infobox.parseInfoBox(block))