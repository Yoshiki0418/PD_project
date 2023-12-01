import requests
from bs4 import BeautifulSoup


#input_ingredients =input()

# 入力された食材名を「、」で区切るようにする
#ingredients = input_ingredients.replace(",", "、")

# スクレイピングするURL
url = 'https://cookpad.com/search/材料：白菜、にんじん、豚肉'

# ページの内容を取得
response = requests.get(url)

# BeautifulSoupオブジェクトを作成し、HTMLをパース
soup = BeautifulSoup(response.text, 'html.parser')

"""
'class'が'recipe-image'のすべての'div'要素を検索し、それぞれの中の'a'タグから'href'を取得
これで、複数のページIDを取得することができる。
"""
recipe_image_divs = soup.find_all('div', class_='recipe-image')

# hrefのリストを取得
hrefs = [div.find('a').get('href') for div in recipe_image_divs if div.find('a')]

for href in hrefs:
    print(href)

    if href:
        # hrefがNoneでない場合のみ処理を実行
        recipe_url = f"https://cookpad.com{href}"  # URLの形式に注意
        response = requests.get(recipe_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # タイトルの取得。タイトルが存在しない場合のためにNoneチェックを行う
        title_tag = soup.find('h1', class_='recipe-title')
        if title_tag:
            title = title_tag.get_text(strip=True)
            print(title)
