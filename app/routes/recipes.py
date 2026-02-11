import html
import json
import logging

from flask import Blueprint, jsonify, render_template, request
from sqlalchemy import func

from app import db
from app.models import (
    AddIngredientsRecipes,
    Ingredients,
    IngredientsRecipes,
    Recipe,
)
from app.services.nutrition import nutrients
from app.services.scraping import scraping2
from app.services.unit_conversion import unit_conversion2

logger = logging.getLogger(__name__)

recipes_bp = Blueprint("recipes", __name__)


@recipes_bp.route("/recipe")
def recipe():
    return render_template("recipe.html")


@recipes_bp.route("/search-recipes", methods=["POST"])
def search_recipes():
    data = request.json
    selected_items = data["selectedItems"]
    logger.debug("Selected items: %s", selected_items)

    # 各レシピにおける必要な食材の総数を計算するサブクエリ
    total_ingredient_count = (
        db.session.query(
            IngredientsRecipes.RecipeID,
            func.count(IngredientsRecipes.IngredientID).label("total_count"),
        )
        .group_by(IngredientsRecipes.RecipeID)
        .subquery()
    )

    # 選択された食材に基づいて、各レシピの選択された食材のカウントを行う
    selected_recipes = (
        db.session.query(
            IngredientsRecipes.RecipeID,
            func.count(db.distinct(IngredientsRecipes.IngredientID)).label(
                "selected_count"
            ),
            total_ingredient_count.c.total_count,
        )
        .join(
            total_ingredient_count,
            IngredientsRecipes.RecipeID
            == total_ingredient_count.c.RecipeID,
        )
        .filter(IngredientsRecipes.IngredientID.in_(selected_items))
        .group_by(
            IngredientsRecipes.RecipeID,
            total_ingredient_count.c.total_count,
        )
        .having(
            func.count(db.distinct(IngredientsRecipes.IngredientID))
            >= func.ceil(2 / 3 * total_ingredient_count.c.total_count)
        )
    )

    recipe_ids = [recipe.RecipeID for recipe in selected_recipes.all()]
    logger.debug("Matching recipe IDs: %s", recipe_ids)

    # 作成できるレシピIDを用いてレシピIDを参照する
    recipes = Recipe.query.filter(Recipe.RecipeID.in_(recipe_ids)).all()
    logger.debug("Found %d recipes", len(recipes))

    # 初期表示レシピ数を10に設定する
    recipes_num = 10
    recipe_add = recipes_num - len(recipes)

    ingredients = Ingredients.query.filter(
        Ingredients.IngredientID.in_(selected_items)
    ).all()
    ingredient_names = [ingredient.name for ingredient in ingredients]
    ingredient_names_str = ",".join(ingredient_names)

    logger.debug("Ingredient names: %s", ingredient_names_str)
    logger.debug("Additional recipes needed: %d", recipe_add)
    
    try:
        scraped_data_list = scraping2(ingredient_names_str, recipe_add)
        logger.debug("Scraped data count: %d", len(scraped_data_list))
    except Exception as e:
        logger.error("Scraping failed: %s", e)
        scraped_data_list = []

    # マッピング辞書
    mapping_dict = {
        "にんじん": ["にんじん", "人参", "ニンジン"],
        "玉ねぎ": ["玉ねぎ", "タマネギ", "たまねぎ"],
        "じゃがいも": ["じゃがいも", "ジャガイモ"],
        "なす": ["茄子", "なす", "ナス"],
        "ねぎ": ["ねぎ", "ネギ", "小ねぎ", "長ネギ"],
        "大根": ["大根", "だいこん", "ダイコン"],
        "レンコン": ["蓮根", "レンコン", "れんこん"],
        "さつまいも": ["さつまいも", "サツマイモ"],
        "ほうれん草": ["ほうれん草", "ホウレンソウ"],
        "青梗菜": ["青梗菜", "チンゲンサイ"],
        "とうもろこし": ["とうもろこし", "トウモロコシ"],
        "鶏むね肉": [
            "鶏むね肉", "鶏胸肉", "鶏肉", "鶏肉(むね)",
            "鶏肉(胸)", "鶏肉(ムネ)",
        ],
        "鶏もも肉": [
            "鶏もも肉", "鶏モモ肉", "鶏肉", "鶏肉(もも)", "鶏肉(モモ)",
        ],
        "ひき肉": ["ひき肉", "挽き肉", "鶏ひき肉", "合いびき肉"],
        "牛小間切れ": ["牛小間切れ", "牛肉"],
        "牛バラ": ["牛バラ", "牛肉"],
        "牛ヒレ": ["牛肉", "牛ひれ肉", "牛ヒレ肉"],
        "豚小間切れ": ["豚小間切れ", "豚肉"],
        "豚ヒレ": ["豚肉", "豚ひれ肉", "豚ヒレ肉"],
        "豚バラ": ["豚肉", "豚バラ", "豚バラ肉"],
        "牛もも肉": ["牛もも肉", "牛もも", "牛肉"],
    }

    # スクレイピングされた各レシピに対してループを行い、データベースに追加
    for scraped_data in scraped_data_list:
        # Check if title exists
        if "title" not in scraped_data:
            logger.warning("Skipping recipe without title: %s", scraped_data)
            continue

        # 一人あたりの重さを算出する
        ChangedUnit = None
        if scraped_data.get("changed_unit") and isinstance(
            scraped_data["changed_unit"], dict
        ):
            changed_unit = unit_conversion2(
                scraped_data["changed_unit"],
                scraped_data["number_of_people"],
            )
            logger.debug("Changed unit: %s", changed_unit)
            ChangedUnit = json.dumps(changed_unit)

        # 既にデータベースに存在するレシピ名をチェック
        existing_recipe = Recipe.query.filter_by(
            RecipeName=scraped_data["title"]
        ).first()
        new_recipe = None

        # レシピ名がデータベースに存在しない場合のみ、新しいレシピを追加
        if not existing_recipe:
            new_recipe = Recipe(
                RecipeName=scraped_data["title"],
                Description=scraped_data.get("explanation"),
                CookingTime=scraped_data.get("time"),
                ImageURL=scraped_data.get("image_path"),
                Ingredients=scraped_data.get("ingredients"),
                Instructions=scraped_data.get("procedures"),
                IngredientsAmount=scraped_data.get("ingredients_amount"),
                Calorie=scraped_data.get("calorie"),
                Salt=scraped_data.get("salt"),
                Protein=scraped_data.get("protein"),
                VegetableIntake=scraped_data.get("vegetable_intake"),
                ChangedUnit=ChangedUnit,
            )
            db.session.add(new_recipe)
            db.session.flush()
            db.session.commit()

        if new_recipe:
            db.session.commit()
            ingredient_names_list = scraped_data["ingredients"].split(",")

            for ingredient_name in ingredient_names_list:
                ingredient_name = ingredient_name.strip()

                # マッピング辞書を使用して名前の変換
                for db_name, scraped_names in mapping_dict.items():
                    if ingredient_name in scraped_names:
                        ingredient_name = db_name
                        break

                # データベースで材料を検索
                ingredient = Ingredients.query.filter_by(
                    name=ingredient_name
                ).first()
                if ingredient:
                    IngredientID = ingredient.IngredientID
                    RecipeID = new_recipe.RecipeID

                    # タイトルに食材名が含まれているかチェック
                    is_must = (
                        1
                        if ingredient_name in new_recipe.RecipeName
                        else None
                    )

                    if IngredientID is not None and RecipeID is not None:
                        new_ingredient_recipe = IngredientsRecipes(
                            IngredientID=IngredientID,
                            RecipeID=RecipeID,
                            Must=is_must,
                        )
                        db.session.add(new_ingredient_recipe)
                        db.session.commit()

    # 取得したレシピオブジェクトを辞書リストに変換
    recipes_data = [
        {
            "RecipeID": r.RecipeID,
            "RecipeName": r.RecipeName,
            "Description": r.Description,
            "CookingTime": r.CookingTime,
            "ImageURL": r.ImageURL,
            "Ingredients": r.Ingredients,
            "Instructions": r.Instructions,
        }
        for r in recipes
    ]

    logger.debug("Recipes data: %s", recipes_data)
    return jsonify(recipes_data)


@recipes_bp.route("/get-recipes", methods=["POST"])
def get_recipes():
    logger.debug("Request JSON: %s", request.json)
    ingredient_ids = request.json.get("ingredient_id")
    if not ingredient_ids:
        return jsonify({"error": "No ingredient IDs provided"}), 400

    query = (
        db.session.query(IngredientsRecipes.RecipeID)
        .filter(IngredientsRecipes.IngredientID.in_(ingredient_ids))
        .group_by(IngredientsRecipes.RecipeID)
        .having(
            db.func.count(db.distinct(IngredientsRecipes.IngredientID))
            == len(ingredient_ids)
        )
    )

    recipe_ids = [recipe.RecipeID for recipe in query.all()]
    logger.debug("Recipe IDs: %s", recipe_ids)

    recipes = Recipe.query.filter(Recipe.RecipeID.in_(recipe_ids)).all()

    if not recipes:
        return (
            jsonify({"error": "No Recipes found for provided IDs"}),
            404,
        )

    recipes_data = [
        {
            "RecipeID": r.RecipeID,
            "RecipeName": r.RecipeName,
            "Description": r.Description,
            "CookingTime": r.CookingTime,
            "ImageURL": r.ImageURL,
            "Ingredients": r.Ingredients,
            "Instructions": r.Instructions,
        }
        for r in recipes
    ]

    logger.debug("Recipes data: %s", recipes_data)
    return jsonify(recipes_data)


@recipes_bp.route("/recipe-details/<recipe_id>")
def recipe_details(recipe_id):
    logger.debug("Recipe ID: %s", recipe_id)
    recipe = Recipe.query.filter_by(RecipeID=recipe_id).first()
    if not recipe:
        return (
            jsonify({"error": "No Recipes found for provided IDs"}),
            404,
        )

    recipe_data = {
        "RecipeID": recipe.RecipeID,
        "RecipeName": recipe.RecipeName,
        "Description": recipe.Description,
        "CookingTime": recipe.CookingTime,
        "ImageURL": recipe.ImageURL,
        "Ingredients": recipe.Ingredients,
        "Instructions": recipe.Instructions,
        "Calorie": recipe.Calorie,
        "Salt": recipe.Salt,
        "Protein": recipe.Protein,
        "VegetableIntake": recipe.VegetableIntake,
        "ChangedUnit": recipe.ChangedUnit,
    }

    return render_template("recipe_details.html", recipe=recipe_data)


@recipes_bp.route("/nutririon", methods=["POST"])
def nutririon():
    nutrition_data = request.json
    changed_unit_str = nutrition_data["ChangedUnit"]

    # HTMLエンティティをデコード
    decoded_str = html.unescape(changed_unit_str)

    # JSON文字列を辞書に変換
    changed_unit_dict = json.loads(decoded_str)
    logger.debug("Changed unit dict: %s", changed_unit_dict)
    logger.debug("Nutrients: %s", nutrients(changed_unit_dict))

    return jsonify({"OK": "Nice"}), 400
