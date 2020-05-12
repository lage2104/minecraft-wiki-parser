import json
from datetime import date
import sys
import logging

logger = logging.getLogger("minecraft-ontology-generator")
logger.setLevel(logging.INFO)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)15s - %(name)s - %(levelname)s - %(message)s')

ch.setFormatter(formatter)
logger.addHandler(ch)

def generateOntology(fileName):
  data = None
  with open('data.json') as file:
    data = json.load(file)
  
  output = []
  for idx,element in enumerate(data):
    element_triple = []
    
    label = "mc:{id}\trdf:label\t\"{name}\"^^xsd:string .".format(id=element['id'],name=element['name'])
    comment = "mc:{id}\trdf:comment\t\"{description}\"^^xsd:string .".format(id=element['id'],description=element['description'])
    stack_size = "mc:{id}\tmc:stackSize\t\"{size}\"^^xsd:positiveInteger .".format(id=element['id'],size=element['stack_size'])    
    url = "mc:{id}\tmc:wikiUrl\t\"{url}\"^^xsd:string .".format(id=element['id'],url=element['url'])

    if element ['receipe'] is None:
      rdf_type = "mc:{id}\trdf:type\tmc:CollectableItem .".format(id=element['id'])
      element_triple.append(rdf_type)
    else:
      rdf_type = "mc:{id}\trdf:type\tmc:CraftableItem .".format(id=element['id'])
      element_triple.append(rdf_type)
      
    element_triple.append(label)
    element_triple.append(comment)
    element_triple.append(url)
    element_triple.append(stack_size)

    if element ['receipe'] is not None:
      if element ['receipe']['type'] == "shapeless":
        shape = "mc:{id}\tmc:shapelessRecipe\t[".format(id=element['id'])
        element_triple.append(shape)
      else:
        shape = "mc:{id}\tmc:shapefulRecipe\t[".format(id=element['id'])
        element_triple.append(shape)
      
      element_triple.append("\t\trdf:type\trdf:Seq ;")
      output_amount = "\t\tmc:outputAmount\t\"{}\"^^xsd:positiveInteger ;".format(element['receipe']['output_amount'])
      element_triple.append(output_amount)
      element_triple.append("\t\trdf:li")
      
      ingredients_txt = []
      for ingredient in element['receipe']['ingredients']:
        ingredient_item = "\t\t\tmc:receipeItem\tmc:{} ;".format(ingredient['item'])
        slot = "\t\t\tmc:slot\t\"{}\"^^xsd:positiveInteger".format(ingredient['slot'])
        
        ingredients_txt.append("\n".join(["\t\t[",ingredient_item, slot, "\t\t]"]))

      element_triple.append(", \n".join(ingredients_txt))
        
      element_triple.append("\t] .")

    output.append(element_triple)
    
  with open(fileName,'w') as file:
    with open("header.ttl", "r") as header:
      file.writelines(header.readlines())
    
    file.write("\n\n")

    texts = []
    for element_triple in output:
      texts.append("\n".join(element_triple))
    file.write("\n\n".join(texts))

if __name__ == "__main__":
  fileName = "MCOntology_{}.ttl".format(date.today())
  logger.info("Generating Ontology...")
  generateOntology(fileName)
  logger.info("Ontology \"{}\" generated.".format(fileName))