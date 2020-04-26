from bs4 import BeautifulSoup
import requests

url = "https://minecraft.gamepedia.com/Bucket"
response = requests.get(url)

html = response.text

soup = BeautifulSoup(html,'html.parser')

print(soup.title)