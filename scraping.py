import requests
from bs4 import BeautifulSoup


input_ingredients =input()

# 入力された食材名を「、」で区切る
ingredients = input_ingredients.replace(",", "、")

print(ingredients)
    

# スクレイピングするURL
url = 'https://cookpad.com/search/材料：白菜、にんじん、豚肉'

# ページの内容を取得
response = requests.get(url)

# BeautifulSoupオブジェクトを作成し、HTMLをパース
soup = BeautifulSoup(response.text, 'html.parser')

# 'class'が'recipe-image'のすべての'div'要素を検索し、それぞれの中の'a'タグから'href'を取得
recipe_image_divs = soup.find_all('div', class_='recipe-image')

# hrefのリストを取得
hrefs = [div.find('a').get('href') for div in recipe_image_divs if div.find('a')]

for href in hrefs:
    print(href)