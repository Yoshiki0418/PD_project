import logging
import re

from flask import current_app

from app.models import UnitConversion

logger = logging.getLogger(__name__)

# 食材名のマッピング辞書
INGREDIENT_MAPPING = {
    "グリーンアスパラガス": "アスパラ",
    "アスパラガス": "アスパラ",
    "春キャベツ": "キャベツ",
}


def map_ingredient_name(name):
    """食材名を標準名にマッピングする。"""
    return INGREDIENT_MAPPING.get(name, name)


def unit_conversion2(ingredients_dict, people_num):
    """食材の量を一人あたりの重量（g）に変換する。"""
    with current_app.app_context():
        converted_weights_per_person = {}
        for food_name, quantity_str in ingredients_dict.items():
            standardized_name = map_ingredient_name(food_name)

            match = re.match(
                r"(\d+(\.\d+)?)(\s*(g|gram|グラム|cm|本|個|片|切れ|束|杯|尾"
                r"|パック|袋|丁|合|カップ|杯|房|節|片|株|枚|かけ|パック))?",
                quantity_str,
            )
            if match:
                quantity, _, unit = match.groups()[:3]
                quantity = float(quantity)

                if unit and unit in ["g", "gram", "グラム"]:
                    weight_per_person = quantity / people_num
                else:
                    unit_data = UnitConversion.query.filter_by(
                        FoodName=standardized_name, Unit=unit
                    ).first()

                    if unit_data and unit_data.Weight:
                        total_weight = quantity * unit_data.Weight
                        weight_per_person = total_weight / people_num
                    else:
                        weight_per_person = None
                converted_weights_per_person[standardized_name] = (
                    weight_per_person
                )
            else:
                converted_weights_per_person[standardized_name] = None

        return converted_weights_per_person
