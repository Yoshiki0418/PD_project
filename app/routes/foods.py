import logging
import os
from datetime import datetime, timedelta

from flask import Blueprint, current_app, jsonify, render_template, request
from werkzeug.utils import secure_filename

from app import db
from app.models import Ingredients
from app.services.food_judge import process_image
from app.services.meat_judge import analyze_food_categories
from app.services.object_detection import detect_food_items

logger = logging.getLogger(__name__)

foods_bp = Blueprint("foods", __name__)


@foods_bp.route("/foods")
def foods():
    vegetables = Ingredients.query.all()
    items = []
    current_date = datetime.now().date()

    for vegetable in vegetables:
        if vegetable.expiration_date:
            if isinstance(vegetable.expiration_date, datetime):
                expiry_date = vegetable.expiration_date.date()
            else:
                expiry_date = vegetable.expiration_date

            delta = expiry_date - current_date
            days_left = delta.days if delta.days >= 0 else 0
        else:
            expiry_date = None
            days_left = "無"

        veg_data = {
            "IngredientID": vegetable.IngredientID,
            "name": vegetable.name,
            "image_file": vegetable.image_path,
            "expiry": (
                expiry_date.strftime("%Y-%m-%d") if expiry_date else "無"
            ),
            "days_left": days_left,
            "is_present": vegetable.is_present,
            "category": vegetable.category,
        }
        items.append(veg_data)

    return render_template("foods.html", items=items)


@foods_bp.route("/upload", methods=["POST"])
def upload_file():
    if "image" not in request.files:
        return jsonify({"error": "No file part"})
    file = request.files["image"]
    if file.filename == "":
        return jsonify({"error": "No selected file"})
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
        file.save(file_path)

        # 画像を処理
        class_name, confidence_score = process_image(file_path)
        class_name = (
            class_name.split(" ", 1)[1] if " " in class_name else class_name
        )
        logger.debug("Detected class: %s", class_name)

        # OCR チェック
        if class_name == "肉":
            class_name, date = analyze_food_categories(file_path)
            if class_name == "":
                class_name = "判定できませんでした。もう一度撮影し直してください"

        # データベースから食材IDを検索
        ingredient = Ingredients.query.filter_by(name=class_name).first()
        ingredient_id = ingredient.IngredientID if ingredient else None
        logger.debug("Ingredient ID: %s", ingredient_id)

        # 単一のIDをリストに変換
        if not isinstance(ingredient_id, list):
            ingredient_id = [ingredient_id]

        response_data = {
            "image_url": "/" + file_path,
            "class_name": class_name,
            "confidence_score": confidence_score,
            "ingredient_id": ingredient_id,
        }
        return jsonify(response_data)
    return jsonify({"error": "File upload failed"})


@foods_bp.route("/save_image", methods=["POST"])
def save_image():
    image = request.files["image"]
    if image:
        filename = secure_filename(image.filename)
        save_path = os.path.join(
            current_app.config["UPLOAD_FOLDER"], filename
        )
        image.save(save_path)
        detected_foods = detect_food_items(save_path)
        logger.debug("Detected foods: %s", detected_foods)
        detected_foods = [
            ingredient.strip() for ingredient in detected_foods.split(",")
        ]
        response_data = []
        current_date = datetime.now().date()

        for ingredient_name in detected_foods:
            ingredient = Ingredients.query.filter_by(
                name=ingredient_name
            ).first()

            if ingredient:
                logger.debug(
                    "%s の平均賞味期限: %d日",
                    ingredient_name,
                    ingredient.average_shelf_life,
                )
                expiration_date = current_date + timedelta(
                    days=ingredient.average_shelf_life
                )
                formatted_date = expiration_date.strftime("%Y/%m/%d")
                response_data.append(
                    {
                        "IngredientID": ingredient.IngredientID,
                        "name": ingredient_name,
                        "ImageURL": ingredient.image_path,
                        "average_shelf_life": ingredient.average_shelf_life,
                        "expiration_date": formatted_date,
                    }
                )
        return jsonify(response_data)
    return jsonify({"message": "No image received"}), 400


@foods_bp.route("/save_image2", methods=["POST"])
def save_image2():
    image = request.files["image"]
    if image:
        filename = secure_filename(image.filename)
        save_path = os.path.join(
            current_app.config["UPLOAD_FOLDER"], filename
        )
        image.save(save_path)
        detected_foods = process_image(save_path)
        full_string = detected_foods[0]

        # 数字と空白を取り除く
        class_name = "".join(
            [i for i in full_string if not i.isdigit()]
        ).strip()
        response_data = []
        current_date = datetime.now().date()
        logger.debug("Detected class: %s", class_name)

        if class_name == "肉":
            class_name, date = analyze_food_categories(save_path)

        ingredient = Ingredients.query.filter_by(name=class_name).first()

        if ingredient:
            logger.debug(
                "%s の平均賞味期限: %d日",
                class_name,
                ingredient.average_shelf_life,
            )
            expiration_date = current_date + timedelta(
                days=ingredient.average_shelf_life
            )
            formatted_date = expiration_date.strftime("%Y/%m/%d")
            response_data.append(
                {
                    "IngredientID": ingredient.IngredientID,
                    "name": class_name,
                    "ImageURL": ingredient.image_path,
                    "average_shelf_life": ingredient.average_shelf_life,
                    "expiration_date": formatted_date,
                }
            )
        return jsonify(response_data)
    return jsonify({"message": "No image received"}), 400


@foods_bp.route("/add-ingredient", methods=["POST"])
def add_ingredient():
    data = request.json
    name = data.get("name")
    expiration_date = data.get("expiration_date")

    if name:
        ingredient = Ingredients.query.filter_by(name=name).first()

        if not ingredient:
            return (
                jsonify({"error": f"食材 {name} はデータベースに存在しません"}),
                404,
            )

        # 賞味期限が指定されていない場合、データベースから平均賞味期限を使用
        if expiration_date is None:
            current_date = datetime.now().date()
            expiration_date = current_date + timedelta(
                days=ingredient.average_shelf_life
            )
        else:
            expiration_date = datetime.strptime(
                expiration_date, "%Y-%m-%d"
            ).date()

        formatted_date = expiration_date.strftime("%Y/%m/%d")

        return (
            jsonify(
                {
                    "IngredientID": ingredient.IngredientID,
                    "name": ingredient.name,
                    "ImageURL": ingredient.image_path,
                    "expiration_date": formatted_date,
                }
            ),
            200,
        )
    else:
        return jsonify({"error": "食材名は必須です"}), 400


@foods_bp.route("/process_card_data", methods=["POST"])
def process_card_data():
    card_data = request.json
    logger.debug("Card data received: %s", card_data)

    for item in card_data:
        name = item.get("name")
        expiration_date_str = (
            item.get("expirationDate").replace("賞味期限", "").strip()
        )

        if name and expiration_date_str:
            expiration_date = datetime.strptime(
                expiration_date_str, "%Y/%m/%d"
            ).date()
            ingredient = Ingredients.query.filter_by(name=name).first()

            if ingredient:
                ingredient.expiration_date = expiration_date
                ingredient.is_present = 1
                db.session.add(ingredient)

    db.session.commit()
    return render_template("foods.html")
