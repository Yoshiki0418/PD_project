import requests
from bs4 import BeautifulSoup
import re
from fractions import Fraction
from flask import Flask, current_app

# 日本語以外を除去するための関数
def remove_non_japanese(text):
    # 日本語（ひらがな、カタカナ、漢字）以外を除去
    return re.sub(r'[^\u3040-\u30FF\u3400-\u4DBF\u4E00-\u9FFF]', '', text)

def extract_numeric_value(text):
    # 正規表現を使用して数値を抽出
    matches = re.findall(r"(\d+\.?\d*)", text)
    if matches:
        # 小数第2位まで四捨五入
        return round(float(matches[0]), 2)
    else:
        return 0


def create_ingredients_dict(ingredient_names, ingredient_amount):
    if len(ingredient_names) != len(ingredient_amount):
        print("食材の名前と量のリストの長さが一致しません。")
        return None
        #raise ValueError("食材の名前と量のリストの長さが一致しません。")

    ingredients_dict = {}
    for name, amount in zip(ingredient_names, ingredient_amount):
        ingredients_dict[name] = amount

    return ingredients_dict

def process_ingredient_amount(ingredient_amount):
    processed_amounts = []

    for amount in ingredient_amount:
        # 分数を含む場合、それを小数に変換し元の文字列に組み込む
        fraction_match = re.search(r'(\d+/\d+)', amount)
        if fraction_match:
            fraction_str = fraction_match.group(1)
            try:
                decimal = str(float(Fraction(fraction_str)))
                amount = amount.replace(fraction_str, decimal[:4])  # 小数点以下2桁までに制限
            except ValueError:
                pass  # 数値以外の場合は変換せずにスキップ

        # 'g' 単位が含まれる場合はそれを優先
        gram_match = re.search(r'(\d+(\.\d+)?\s*g)', amount)
        if gram_match:
            amount = gram_match.group(1)

        processed_amounts.append(amount)

    return processed_amounts

#クックパッドからのスクレイピング
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

        #レシピ名を取得
        title_tag = soup.find('h1', class_='recipe-title')
        if title_tag:
            recipe_info['title'] = title_tag.get_text(strip=True)

        #レシピの一言を取得
        explanation = soup.find("div", class_="description_text")
        if explanation:
            recipe_info['explanation'] = explanation.get_text(strip=True)

        #レシピの画像を取得
        img_tag = soup.find('img', class_="photo large_photo_clickable")
        if img_tag:
            recipe_info['image_path'] = img_tag.get('src')

        ingredient_names = soup.find_all('span', class_='name')
        # 材料名をコンマで連結して格納
        recipe_info['ingredients'] = ','.join([name.text for name in ingredient_names])

        ingredient_amount = soup.find_all('div', class_='ingredient_quantity amount')
        # 材料量をコンマで連結して格納
        recipe_info['ingredients_amount'] = ','.join([amount.text for amount in ingredient_amount])

        procedures = soup.find_all("p", class_="step_text")
        recipe_info['procedures'] = ','.join(procedure.text.strip() for procedure in procedures)

        """
        people_num = soup.find("span", class_="servings_for yield")
        if people_num:
            people_num_text = people_num.text # テキストを取得
            num_str = re.search(r'\d+', people_num_text).group() 
            num = int(num_str)
            print(num)
            recipe_info['num'] = num
        """
        



        recipes.append(recipe_info)

        # 食材名と量を抽出
        ingredients = [remove_non_japanese(span.get_text()) for span in soup.find_all('span', class_='name')]
        amounts = [div.get_text() for div in soup.find_all('div', class_='ingredient_quantity amount')]

        # 辞書で食材名と量を結び付ける
        ingredient_dict = dict(zip(ingredients, amounts))

        # 結果の出力
        for ingredient, amount in ingredient_dict.items():
            print(f'{ingredient}: {amount}')

    return recipes

#味の素パークからのレシピ取得
def scraping2(input_ingredients, recipe_add):
    ingredients = input_ingredients.replace(",", "、")
    url = f'https://park.ajinomoto.co.jp/recipe/search/?search_word={ingredients}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 'div'タグでクラスが'img'であるものを見つけ、その中の'a'タグでクラスが'fade'である要素を検索
    fade_values = []
    img_divs = soup.find_all('div', class_='img')
    for div in img_divs:
        fade_element = div.find('a', class_='fade')
        if fade_element:
            fade_values.append(fade_element.get('href'))

    recipes = []
    for href in fade_values[:recipe_add]:
        response = requests.get(href)
        soup = BeautifulSoup(response.text, 'html.parser')

        recipe_info = {}

        # レシピ名を取得
        recipe_title_tag = soup.find('h1', class_='recipeTitle')
        if recipe_title_tag:
            title_text_span = recipe_title_tag.find('span', class_='titleText')
            if title_text_span:
                recipe_info['title'] = title_text_span.get_text() 

        # レシピの一言を取得
        intro_paragraph = soup.find('p', class_='recioeIntro')
        if intro_paragraph:
            recipe_info['explanation'] = intro_paragraph.get_text()  # get_text()を呼び出す
        else:
            recipe_info['explanation'] = None

        # 時間を取得
        time = soup.find("div", class_="inTime")
        if time:
            time_text = time.get_text()  # 時間の文字列を取得
            numeric_part = ''.join(filter(str.isdigit, time_text))  # 数字部分を抽出
            if numeric_part:
                recipe_info["time"] = int(numeric_part)  # 整数に変換して格納
            else:
                recipe_info["time"] = None  # 数字が見つからない場合はNoneに設定
        else:
            recipe_info["time"] = None 

        # レシピの画像を取得
        img_out_divs = soup.find("div", class_="recipeImageArea")
        if img_out_divs:
            img_tag = img_out_divs.find('img')  # 'img'タグを検索
            if img_tag:
                recipe_info['image_path'] = img_tag['src']  # src属性を直接取得

        # 何人分のレシピか取得
        people_num_text = soup.find("span", class_="bigTitle_quantity")
        if people_num_text:
            people_num = people_num_text.get_text()
            numeric_part = ''.join(filter(str.isdigit, people_num))  # 数字部分を抽出
            if numeric_part:
                recipe_info["number_of_people"] = int(numeric_part)  # 整数に変換して格納
            else:
                recipe_info["number_of_people"] = None  # 数字が見つからない場合はNoneに設定
        else:
            recipe_info["number_of_people"] = None

        #材料を取得
        material_list = soup.find('div', class_='recipeMaterialList')
        ingredient_names = []
        if material_list:
            for dt in material_list.find_all('dt'):
                ingredient = dt.get_text().strip()
                if ingredient:  # Only add if the text is not empty
                    ingredient_names.append(ingredient)
            recipe_info['ingredients'] = ','.join(ingredient_names)

        #recipes.append(recipe_info)

        #各食材の必要な量を取得
        material_list = soup.find('div', class_='recipeMaterialList')
        ingredient_amount = []
        if material_list:
            for dd in material_list.find_all('dd'):
                ingredient = dd.get_text().strip()
                if ingredient:  # Only add if the text is not empty
                    ingredient_amount.append(ingredient)
            recipe_info["ingredients_amount"] = ','.join(ingredient_amount)

       # 料理の作成手順を取得
        make_list = soup.find('div', class_='makeList')
        cooking_steps = []

        if make_list:
            for li in make_list.find_all('li', class_='inGallery'):
                step_div = li.find('div', class_='txt numberTxt')
                if step_div:
                    # ステップテキストから最初の文字を取り除く
                    step_text = step_div.get_text().strip()
                    if step_text:
                        # 先頭の番号とその後のピリオドまたは空白を取り除く
                        cleaned_step_text = step_text[1:].lstrip('. ')
                        cooking_steps.append(cleaned_step_text)
            recipe_info['procedures'] = ','.join(cooking_steps)

        # 栄養情報を取得
        out_container = soup.find("div", class_="nutrientListWrapper")
        if out_container:
            nutrient_list_wrapper = out_container.find('ul', class_="clearfix")
            nutrients = {}

            if nutrient_list_wrapper:
                nutrient_list_items = nutrient_list_wrapper.find_all('li')
                for item in nutrient_list_items:
                    print(item)
                    nutrient_divs = item.find_all('div') 
                    if nutrient_divs:
                        print(1)
                        for div in nutrient_divs:
                            spans = div.find_all('span')
                            if spans and len(spans) > 1:
                                nutrient_name = spans[0].get_text().strip()
                                nutrient_value = spans[1].get_text().strip()
                                nutrients[nutrient_name] = nutrient_value

        # カロリーを取得して変換
        recipe_info['calorie'] = extract_numeric_value(nutrients.get("・エネルギー", ""))
        # 塩分を取得して変換
        recipe_info['salt'] = extract_numeric_value(nutrients.get("・塩分", ""))
        # タンパク質を取得して変換
        recipe_info['protein'] = extract_numeric_value(nutrients.get("・たんぱく質", ""))
        # 野菜摂取量を取得して変換
        recipe_info['vegetable_intake'] = extract_numeric_value(nutrients.get("・野菜摂取量※", ""))

        processed_amounts = process_ingredient_amount(ingredient_amount)
        #print(processed_amounts)

        ingredients_dict = create_ingredients_dict(ingredient_names, processed_amounts)
        #print(ingredients_dict)

        """
        #app.pyの中で実行することに変更
        unit_change = unit_conversion2(ingredients_dict , 4)
        print(unit_change)
        """

        

        recipe_info["changed_unit"] = ingredients_dict
        #recipes.append(ingredients_dict)

        recipes.append(recipe_info)

    return recipes  # 修正: 複数のレシピ情報をリストで返す

"""
# 使用例
input_ingredients = "にんじん、白菜"
recipe_add = 1 
result = scraping2(input_ingredients, recipe_add)
for recipe in result:
    print(recipe)
"""


