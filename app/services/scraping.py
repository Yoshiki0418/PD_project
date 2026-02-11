import logging
import re
from fractions import Fraction

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


def remove_non_japanese(text):
    """日本語（ひらがな、カタカナ、漢字）以外を除去する。"""
    return re.sub(r"[^\u3040-\u30FF\u3400-\u4DBF\u4E00-\u9FFF]", "", text)


def extract_numeric_value(text):
    """テキストから数値を抽出し、小数第2位まで四捨五入して返す。"""
    matches = re.findall(r"(\d+\.?\d*)", text)
    if matches:
        return round(float(matches[0]), 2)
    return 0


def create_ingredients_dict(ingredient_names, ingredient_amount):
    """食材名と量のリストから辞書を作成する。"""
    if len(ingredient_names) != len(ingredient_amount):
        logger.warning("食材の名前と量のリストの長さが一致しません。")
        return None

    ingredients_dict = {}
    for name, amount in zip(ingredient_names, ingredient_amount):
        ingredients_dict[name] = amount

    return ingredients_dict


def process_ingredient_amount(ingredient_amount):
    """食材の量を処理し、分数を小数に変換する。"""
    processed_amounts = []

    for amount in ingredient_amount:
        fraction_match = re.search(r"(\d+/\d+)", amount)
        if fraction_match:
            fraction_str = fraction_match.group(1)
            try:
                decimal = str(float(Fraction(fraction_str)))
                amount = amount.replace(fraction_str, decimal[:4])
            except ValueError:
                pass

        gram_match = re.search(r"(\d+(\.\d+)?\s*g)", amount)
        if gram_match:
            amount = gram_match.group(1)

        processed_amounts.append(amount)

    return processed_amounts


def scraping(input_ingredients, recipe_add):
    """クックパッドからレシピをスクレイピングする。"""
    ingredients = input_ingredients.replace(",", "、")
    url = f"https://cookpad.com/search/材料：{ingredients}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    recipe_image_divs = soup.find_all("div", class_="recipe-image")
    hrefs = [
        div.find("a").get("href")
        for div in recipe_image_divs
        if div.find("a")
    ]

    recipes = []
    for href in hrefs[:recipe_add]:
        recipe_url = f"https://cookpad.com{href}"
        response = requests.get(recipe_url)
        soup = BeautifulSoup(response.text, "html.parser")

        recipe_info = {}

        title_tag = soup.find("h1", class_="recipe-title")
        if title_tag:
            recipe_info["title"] = title_tag.get_text(strip=True)

        explanation = soup.find("div", class_="description_text")
        if explanation:
            recipe_info["explanation"] = explanation.get_text(strip=True)

        img_tag = soup.find("img", class_="photo large_photo_clickable")
        if img_tag:
            recipe_info["image_path"] = img_tag.get("src")

        ingredient_names = soup.find_all("span", class_="name")
        recipe_info["ingredients"] = ",".join(
            [name.text for name in ingredient_names]
        )

        ingredient_amount = soup.find_all(
            "div", class_="ingredient_quantity amount"
        )
        recipe_info["ingredients_amount"] = ",".join(
            [amount.text for amount in ingredient_amount]
        )

        procedures = soup.find_all("p", class_="step_text")
        recipe_info["procedures"] = ",".join(
            procedure.text.strip() for procedure in procedures
        )

        recipes.append(recipe_info)

        # 食材名と量を抽出
        ingredients_list = [
            remove_non_japanese(span.get_text())
            for span in soup.find_all("span", class_="name")
        ]
        amounts = [
            div.get_text()
            for div in soup.find_all(
                "div", class_="ingredient_quantity amount"
            )
        ]

        ingredient_dict = dict(zip(ingredients_list, amounts))

        for ingredient, amount in ingredient_dict.items():
            logger.debug("%s: %s", ingredient, amount)

    return recipes


def scraping2(input_ingredients, recipe_add):
    """味の素パークからレシピをスクレイピングする。"""
    ingredients = input_ingredients.replace(",", "、")
    url = (
        f"https://park.ajinomoto.co.jp/recipe/search/"
        f"?search_word={ingredients}"
    )
    response = requests.get(url)
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "html.parser")

    # 検索結果からレシピURLを取得
    fade_values = []
    img_divs = soup.find_all("div", class_="img")
    for div in img_divs:
        fade_element = div.find("a", class_="fade")
        if fade_element:
            fade_values.append(fade_element.get("href"))

    logger.debug("Found %d recipe links", len(fade_values))

    recipes = []
    for href in fade_values[:recipe_add]:
        response = requests.get(href)
        response.encoding = "utf-8"
        soup = BeautifulSoup(response.text, "html.parser")

        recipe_info = {}

        # レシピ名を取得（新セレクタ: h1.recipe__title）
        recipe_title_tag = soup.find("h1", class_="recipe__title")
        if recipe_title_tag:
            recipe_info["title"] = recipe_title_tag.get_text(strip=True)
        else:
            # フォールバック: 旧セレクタ
            old_title = soup.find("h1", class_="recipeTitle")
            if old_title:
                title_span = old_title.find("span", class_="titleText")
                recipe_info["title"] = (
                    title_span.get_text(strip=True)
                    if title_span
                    else old_title.get_text(strip=True)
                )

        # レシピの説明を取得（og:description メタタグから）
        og_desc = soup.find("meta", attrs={"property": "og:description"})
        if og_desc:
            recipe_info["explanation"] = og_desc.get("content", "")
        else:
            # フォールバック: 旧セレクタ
            intro_paragraph = soup.find("p", class_="recioeIntro")
            if intro_paragraph:
                recipe_info["explanation"] = intro_paragraph.get_text(
                    strip=True
                )
            else:
                recipe_info["explanation"] = None

        # 時間を取得（新セレクタ: div.recipeRequiredTime__main）
        time_div = soup.find("div", class_="recipeRequiredTime__main")
        if not time_div:
            # フォールバック: 旧セレクタ
            time_div = soup.find("div", class_="inTime")
        if time_div:
            time_text = time_div.get_text()
            numeric_part = "".join(filter(str.isdigit, time_text))
            if numeric_part:
                recipe_info["time"] = int(numeric_part)
            else:
                recipe_info["time"] = None
        else:
            recipe_info["time"] = None

        # レシピの画像を取得（新セレクタ: div.recipeImage > img）
        img_div = soup.find("div", class_="recipeImage")
        if not img_div:
            # フォールバック: 旧セレクタ
            img_div = soup.find("div", class_="recipeImageArea")
        if img_div:
            img_tag = img_div.find("img")
            if img_tag:
                recipe_info["image_path"] = img_tag.get("src", "")

        # 何人分のレシピか取得（セレクタ変更なし）
        people_num_text = soup.find("span", class_="bigTitle_quantity")
        if people_num_text:
            people_num = people_num_text.get_text()
            numeric_part = "".join(filter(str.isdigit, people_num))
            if numeric_part:
                recipe_info["number_of_people"] = int(numeric_part)
            else:
                recipe_info["number_of_people"] = None
        else:
            recipe_info["number_of_people"] = None

        # 材料を取得（新セレクタ: span.recipeIngredients__name）
        ingredient_names = []
        ingredient_amount = []

        new_ingredient_spans = soup.find_all(
            "span", class_="recipeIngredients__name"
        )
        new_quantity_spans = soup.find_all(
            "span", class_="recipeIngredients__quantity"
        )

        if new_ingredient_spans:
            # 新しいサイト構造
            for span in new_ingredient_spans:
                name = span.get_text(strip=True)
                if name:
                    ingredient_names.append(name)
            for span in new_quantity_spans:
                qty = span.get_text(strip=True)
                if qty:
                    ingredient_amount.append(qty)
        else:
            # フォールバック: 旧セレクタ
            material_list = soup.find("div", class_="recipeMaterialList")
            if material_list:
                for dt in material_list.find_all("dt"):
                    ingredient = dt.get_text().strip()
                    if ingredient:
                        ingredient_names.append(ingredient)
                for dd in material_list.find_all("dd"):
                    amount = dd.get_text().strip()
                    if amount:
                        ingredient_amount.append(amount)

        recipe_info["ingredients"] = ",".join(ingredient_names)
        recipe_info["ingredients_amount"] = ",".join(ingredient_amount)

        # 料理の作成手順を取得（新セレクタ: li.recipeProcess）
        cooking_steps = []
        new_steps = soup.find_all("li", class_="recipeProcess")

        if new_steps:
            for li in new_steps:
                step_text = li.get_text(strip=True)
                if step_text:
                    # 先頭の番号を除去（例: "1白菜を..." → "白菜を..."）
                    cleaned = re.sub(r"^\d+", "", step_text).strip()
                    if cleaned:
                        cooking_steps.append(cleaned)
        else:
            # フォールバック: 旧セレクタ
            make_list = soup.find("div", class_="makeList")
            if make_list:
                for li in make_list.find_all("li", class_="inGallery"):
                    step_div = li.find("div", class_="txt numberTxt")
                    if step_div:
                        step_text = step_div.get_text().strip()
                        if step_text:
                            cleaned_step_text = step_text[1:].lstrip(". ")
                            cooking_steps.append(cleaned_step_text)

        recipe_info["procedures"] = ",".join(cooking_steps)

        # 栄養情報を取得（新セレクタ: li.recipeNutrition__info-list-item）
        nutrients = {}
        new_nutrient_items = soup.find_all(
            "li", class_="recipeNutrition__info-list-item"
        )

        if new_nutrient_items:
            for item in new_nutrient_items:
                name_span = item.find(
                    "span", class_="recipeNutrition__name"
                )
                if name_span:
                    nutrient_name = name_span.get_text(strip=True)
                    full_text = item.get_text(strip=True)
                    nutrient_value = full_text.replace(
                        nutrient_name, ""
                    ).strip()
                    nutrients[nutrient_name] = nutrient_value
        else:
            # フォールバック: 旧セレクタ
            out_container = soup.find(
                "div", class_="nutrientListWrapper"
            )
            if out_container:
                nutrient_list_wrapper = out_container.find(
                    "ul", class_="clearfix"
                )
                if nutrient_list_wrapper:
                    for item in nutrient_list_wrapper.find_all("li"):
                        nutrient_divs = item.find_all("div")
                        if nutrient_divs:
                            for div in nutrient_divs:
                                spans = div.find_all("span")
                                if spans and len(spans) > 1:
                                    n_name = spans[0].get_text().strip()
                                    n_value = spans[1].get_text().strip()
                                    nutrients[n_name] = n_value

        recipe_info["calorie"] = extract_numeric_value(
            nutrients.get("・エネルギー", "")
        )
        recipe_info["salt"] = extract_numeric_value(
            nutrients.get("・塩分", "")
        )
        recipe_info["protein"] = extract_numeric_value(
            nutrients.get("・たんぱく質", "")
        )
        recipe_info["vegetable_intake"] = extract_numeric_value(
            nutrients.get("・野菜摂取量※", "")
        )

        processed_amounts = process_ingredient_amount(ingredient_amount)
        ingredients_dict = create_ingredients_dict(
            ingredient_names, processed_amounts
        )

        recipe_info["changed_unit"] = ingredients_dict
        recipes.append(recipe_info)

        logger.debug(
            "Scraped recipe: %s",
            recipe_info.get("title", "NO TITLE"),
        )

    return recipes
