# Einleitung
Die Domain "http://minecraft-item-resolver.mc" basiert auf den Rezepten und Gegenständen (Items, bzw. Blocks) aus dem Videospiel [Minecraft](https://www.minecraft.net/de-de/).
Minecraft ist ein survival Spiel in welchem das Crafting, also das Herstellen von Gegenständen, mithilfe eines 3x3 Feldes, in das die Zutaten gelegt werden können, erfolgt.
![Craftingtable 3x3](images/Crafting3x3.png)



## Hinweis:
* Die Grundlegenden Informationen sowie die Rezepte der Items wurden mithilfe eines selbst entwickelten Parsers automatisch generiert. Daher gibt es eine hohe Anzahl an Tripeln. Der Parser ist im öffentlichen Github Repository https://github.com/lage2104/minecraft-wiki-parser einsehbar.
* Zusätzlich wurden für folgende Items die "Smelting Recipes" angegeben:
  * mc:iron_ingot
  * mc:gold_ingot
* Einzelne Items wurden mit DBPedia Elementen verknüpft. 
  * mc:iron_ingot
  * mc:gold_ingot
  * mc:diamond
  * mc:oak_log
  * mc:cauldron
  * mc:lapis_lazuli
  * mc:dirt
  * mc:map
  * mc:minecart
* Informationen zur Verwendung des Parses befinden sich am Ende des Dokuments.


# Anfragen

## Anfrage 1 - allItems
Ermittelt alle verfügbaren Items innerhalb des Triple Stores

## Anfrage 2 - oneItem
Ermittlet Informationen zu einem, in der BIND-Funktion angegebenen, Item.

## Anfrage 3 - recipe
Ermittelt alle Rezeptbestandteile auf erster Ebene eines Items.

### Variante a
Alle Informationen werden unformatiert ausgegeben.

### Variante b
#### Teil a
Ermittelt Metadaten zu einem Item (Rezepttyp, Ausgabemenge)
#### Teil b
Stellt ausschließlich Informationen zu den Rezeptbestandteilen auf erster Ebene dar.

### Variante c
Mithilfe von zwei Subqueries (Kombination von Variante ba und bb) zur "formatierten" Darstellung.

## Anfrage 4 - item occurrences
Ermittelt die Anzahl der Vorkommen eines Items in allen Rezepten. Mehrfache Aufkommen eines Items innerhalb eines Rezeptes werden (absichtlich) nicht gezählt. 

## Anfrage 5 - craftableItems
### Variante a
Ermittelt alle Items in deren Rezept das angegebene Item in erster Ebene vorkommt.
### Variante b
Ermittelt alle Items in deren Rezept das angegebene Item ab der ersten Ebene vorkommt.

## Anfrage 6 - essential elements
Ermittelt alle Items die für die Umsetzung eines Rezeptes notwendig sind. Für jedes Element aus einem Rezept wird wiederrum das Rezept ermittelt. 

Im Beispiel "mc:bookshelf" ist das Ergebnis:
* mc:oak_log
* mc:sugar_cane
* mc:rabbit_hide

**oak_log** wird benötigt um oak_planks herzustellen, die im Rezept für bookshelfs vorkommen.
**sugar_cane** wird benötigt um Papier(mc:paper) hezustellen, das benötigt wird um Bücher herszustellen, die im Rezept für bookshelfs vorkommen.
**rabbit_hide** wird benötigt um Leder(mc:leather) herszustellen, das benötigt wird um Bücher herzustellen, die im Rezept für bookshelfs vorkommen.



# Installation Wiki-Parser

1. Beautifulsoup für Python installieren
```
pip install beautifulsoup4
```
2. Requests für Python installieren
```
pip install requests
```
3. lxml für Python installieren
```
pip install lxml
```
4. Fetches all item information from https://minecraft.gamepedia.com/Minecraft_Wiki and stores it locally. Stores data.json with parsed information.
```
python3 parser.py --init
```
5. Create ontology ttl file from data.json. Static information from header.ttl and addidtional.ttl are included. 
```
python3 ontology.py
```