import re
from google.cloud import vision
from collections import Counter
from datetime import datetime

def analyze_food_categories(image_path):
    client = vision.ImageAnnotatorClient()

    with open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.document_text_detection(image=image)
    document = response.full_text_annotation

    expiration_date_pattern = r'\d{2}\.\d{2}\.\d{2}'  # 賞味期限のパターン
    expiration_dates = []

    # 基本カテゴリーのマッピング
    basic_categories = {
        '牛': ['牛'],
        '豚': ['豚'],
        '鶏': ['鶏']
    }

    # 詳細カテゴリーのマッピング
    detailed_mappings = {
        '小間切れ': ['小間切れ', '切り落とし'],
        'ロース': ['牛ロース', '薄切りロース', "ステーキ"],
        'むね': ['胸', 'むね', 'ムネ'],
        'もも': ['もも', 'モモ', "モ　モ", "モ モ", "も　も", "も も", "も も"],
        '皮': ['皮'],
        '手羽': ['手羽先', '手羽元', "手羽"],
        'ささみ': ['ささみ', 'ササミ'],
        'ひき肉': ['ひき肉', '挽肉', "挽き肉"],
        'タン': ['タン', '牛たん', "牛タン"],
        'スジ': ['牛すじ', '牛スジ'],
        'バラ': ['バラ', 'ばら'],
        'ヒレ': ['ヒレ']
    }

    # 詳細カテゴリーの初期化
    detailed_categories_found = set()

    # 処理
    for page in document.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    word_text = ''.join([symbol.text for symbol in word.symbols])

                    # 賞味期限の検出
                    date_matches = re.findall(expiration_date_pattern, word_text)
                    expiration_dates.extend(date_matches)

                    # 基本カテゴリーの識別
                    for category, keywords in basic_categories.items():
                        if any(keyword in word_text for keyword in keywords):
                            basic_categories[category].append(word_text)
                            break
                    else:
                        # 詳細カテゴリーの識別
                        for category, keywords in detailed_mappings.items():
                            if word_text in keywords:
                                detailed_categories_found.add(category)
                                break

    most_common_basic_key = None
    if basic_categories:
        basic_counts = Counter([item for sublist in basic_categories.values() for item in sublist])
        if basic_counts:
            most_common_basic = basic_counts.most_common(1)[0][0]

    # 詳細カテゴリーで最も多かったキーを特定
    most_common_detailed_key = None
    if detailed_categories_found:
        detailed_counts = Counter(detailed_categories_found)
        if detailed_counts:
            most_common_detailed = detailed_counts.most_common(1)[0][0]

    name = ""

    #テスト
    if(most_common_basic == "牛"):
        if(most_common_detailed == "バラ"):
            name = "牛バラ肉"
        elif(most_common_detailed == "ヒレ"):
            name = "牛ヒレ"
        elif(most_common_detailed == "ロース"):
            name = "牛ロース肉"
        elif(most_common_detailed == "もも"):
            name = "牛もも肉"
        elif(most_common_detailed == "小間切れ"):
            name = "牛小間切れ"
        elif(most_common_detailed == "スジ"):
            name = "牛スジ"
        elif(most_common_detailed == "タン"):
            name = "牛タン"

    if(most_common_basic == "豚"):
        if(most_common_detailed == "バラ"):
            name = "豚バラ肉"
        elif(most_common_detailed == "ヒレ"):
            name = "豚ヒレ"
        elif(most_common_detailed == "ロース"):
            name = "豚ロース"
        elif(most_common_detailed == "小間切れ"):
            name = "豚小間切れ"

    if(most_common_basic == "鶏"):
        if(most_common_detailed == "手羽"):
            name = "鶏手羽肉"
        elif(most_common_detailed == "皮"):
            name = "鶏皮"
        elif(most_common_detailed == "むね"):
            name = "鶏むね肉"
        elif(most_common_detailed == "もも"):
            name = "鶏もも肉"
        elif(most_common_detailed == "ささみ"):
            name = "鶏ささみ"

    if(most_common_detailed == "ひき肉"):
            name = "ひき肉"

    if(most_common_detailed == "皮"):
            name = "鶏皮"

    if(most_common_detailed == "ささみ"):
            name = "鶏ささみ"

    if(most_common_detailed == "手羽"):
            name = "鶏手羽肉"

    if(most_common_detailed == "タン"):
            name = "牛タン"

    if(most_common_detailed == "スジ"):
            name = "牛スジ"


    date=None

    print("基本カテゴリーで最も多かった要素:", most_common_basic)
    print("詳細カテゴリーで最も多かった要素:", most_common_detailed)
    print("判別した食材", name)
    print("\n賞味期限:")
    if expiration_dates:
    # 賞味期限リストの最初の要素を取得（複数ある場合）
        date = expiration_dates[0]

        if date:
            # 賞味期限の形式を確認し、正しい場合のみ日付変換を行う
            try:
                formatted_date = datetime.strptime(date, "%y.%m.%d").strftime("%Y-%m-%d")
                print("賞味期限（変換後）:", formatted_date)
                return name, formatted_date
            except ValueError:
                print("賞味期限の形式が不正です:", date)
                return name, date
    else:
        print("賞味期限が検出されませんでした。")
        return name, None

##noneだっだらGPTにテキスト全体を入れる
