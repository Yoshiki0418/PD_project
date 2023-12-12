import requests
from bs4 import BeautifulSoup
import re

def scraping(input_ingredients, recipe_add):
    ingredients = input_ingredients.replace(",", "、")
    url = f'https://cookpad.com/search/材料：{ingredients}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    recipe_image_divs = soup.find_all('div', class_='recipe-image')
    hrefs = [div.find('a').get('href') for div in recipe_image_divs if div.find('a')]

    recipes = []
    for href in hrefs[:recipe_add]:
        recipe_url = f"https://cookpad.com{href}"
        response = requests.get(recipe_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        recipe_info = {}

        title_tag = soup.find('h1', class_='recipe-title')
        if title_tag:
            recipe_info['title'] = title_tag.get_text(strip=True)

        explanation = soup.find("div", class_="description_text")
        if explanation:
            recipe_info['explanation'] = explanation.get_text(strip=True)

        img_tag = soup.find('img', class_="photo large_photo_clickable")
        if img_tag:
            recipe_info['image_path'] = img_tag.get('src')

        ingredient_names = soup.find_all('span', class_='name')
        # 材料名をコンマで連結して格納
        recipe_info['ingredients'] = ','.join([name.text for name in ingredient_names])

        procedures = soup.find_all("p", class_="step_text")
        recipe_info['procedures'] = ','.join(procedure.text.strip() for procedure in procedures)

        people_num = soup.find("span", class_="servings_for yield")
        if people_num:
            people_num_text = people_num.text # テキストを取得
            num_str = re.search(r'\d+', people_num_text).group() 
            num = int(num_str)
            print(num)
            recipe_info['num'] = num
            
        recipes.append(recipe_info)

    return recipes


# 使用例
input_ingredients = "にんじん,大根,豚小間切れ肉,なす"
recipe_add = 1
result = scraping(input_ingredients, recipe_add)
for recipe in result:
    print(recipe)


