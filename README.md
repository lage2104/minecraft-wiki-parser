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