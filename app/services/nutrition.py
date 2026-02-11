import json
import logging

import requests

logger = logging.getLogger(__name__)

# 食材名のマッピング辞書
INGREDIENT_MAPPING = {
    "玉ねぎ": "たまねぎ",
    "ゆでたけのこ": "たけのこ 若茎 生",
    "卵": "鶏卵",
    "白菜": "はくさい",
    "大根": "だいこん 根 皮むき 生",
    "にんじん": "にんじん 根 皮つき 生",
    "いか": "あかいか 生",
    "さけ": "しろさけ 生",
    "たこ": "まだこ ゆで",
    "たら": "まだら 生",
    "かぼちゃ": "日本かぼちゃ 果実 ゆで",
    "カリフラワー": "カリフラワー 花序 ゆで",
    "ゴーヤ": "にがうり",
    "ごぼう": "ごぼう 根 ゆで",
    "小松菜": "こまつな 葉 ゆで",
    "さやいんげん": "いんげんまめ さやいんげん 若ざや ゆで",
    "春菊": "しゅんぎく 葉 ゆで",
    "しょうが": "しょうが おろし",
    "にんにく": "にんにく りん茎 油いため",
    "ねぎ": "葉ねぎ 葉 生",
    "ピーマン": "青ピーマン 果実 油いため",
    "パプリカ": "赤ピーマン 果実 油いため",
    "ブロッコリー": "ブロッコリー 花序 ゆで",
    "水菜": "みずな 葉 ゆで",
    "もやし": "だいずもやし 生",
    "れんこん": "れんこん 根茎 ゆで",
    "さつまいも": "さつまいも 塊根 皮むき 蒸し",
    "さといも": "さといも 球茎 水煮",
    "ながいも": "ながいも ながいも 塊根 水煮",
    "えのきだけ": "えのきたけ ゆで",
    "しいたけ": "生しいたけ 菌床栽培 ゆで",
    "まいたけ": "まいたけ ゆで",
    "マッシュルーム": "マッシュルーム 油いため",
    "油揚げ": "油揚げ 油抜き 焼き",
    "厚揚げ": "油揚げ 油抜き 焼き",
    "豆腐": "木綿豆腐",
    "ご飯": "精白米 うるち米",
    "鶏むね肉": "むね 皮つき 焼き",
    "鶏もも肉": "もも 皮つき 焼き",
    "鶏ささ身": "ささ身 焼き",
    "こんにゃく": "板こんにゃく 精粉こんにゃく",
}


def _map_ingredient_name(food_name):
    """マッピング辞書を使って食材名を標準化する。"""
    return INGREDIENT_MAPPING.get(food_name, food_name)


def _fetch_data(food_name):
    """食材名から食品IDを取得する。"""
    standardized_name = _map_ingredient_name(food_name)
    url = (
        "https://script.google.com/macros/s/"
        "AKfycbzO6IMoPPbtBLb_AnRwgB1OheJyF5XwgNyj28NZdyjg76q4AzX0/exec"
        f"?name={standardized_name}"
    )
    response = requests.get(url)
    data = json.loads(response.text)

    if not data:
        return None

    first_key = list(data.keys())[0]
    return data[first_key].split(",")[0] if first_key in data else None


def _fetch_nutrients(food_id, weight):
    """食品IDと重量から栄養素データを取得する。"""
    base_url = (
        "https://script.google.com/macros/s/"
        "AKfycbx7WZ-wdIBLqVnCxPwzedIdjhC3CMjhAcV0MufN2gJd-xsO3xw/exec"
    )
    url = f"{base_url}?num={food_id}&weight={weight}"

    response = requests.get(url)
    data = json.loads(response.text)

    required_nutrients = [
        "脂質", "コレステロール", "炭水化物", "食物繊維総量",
        "ナトリウム", "カリウム", "カルシウム", "マグネシウム",
        "リン", "鉄", "亜鉛", "ビタミンD", "ビタミンK",
        "ビタミンB1", "ビタミンB2", "ビタミンB6", "ビタミンB12",
        "ビタミンC",
    ]
    nutrients_data = {
        key: data[key] for key in required_nutrients if key in data
    }

    return nutrients_data


def nutrients(food_list):
    """食材リストから合計栄養素を計算する。"""
    total_nutrients = {}

    for food_name, quantity in food_list.items():
        if quantity is None:
            continue

        ingredient_id = _fetch_data(food_name)
        if ingredient_id:
            nutrient_data = _fetch_nutrients(ingredient_id, quantity)

            for nutrient, value in nutrient_data.items():
                if nutrient in total_nutrients:
                    total_nutrients[nutrient] += value
                else:
                    total_nutrients[nutrient] = value

    for nutrient in total_nutrients:
        total_nutrients[nutrient] = round(total_nutrients[nutrient], 2)

    return total_nutrients
