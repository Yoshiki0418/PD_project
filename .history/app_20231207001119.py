from flask import Flask, request, render_template, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.utils import secure_filename
from food_judge import process_image
from datetime import datetime
from meat_judge import analyze_food_categories
from sqlalchemy import func
from scraping import scraping
from flask_migrate import Migrate



app = Flask(__name__) 
UPLOAD_FOLDER = 'static/UPLOAD_FOLDER'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# MySQLの設定
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Ingredients(db.Model): 
    IngredientID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    expiration_date = db.Column(db.Date)
    image_path = db.Column(db.String(255))
    is_present = db.Column(db.Integer)
    category = db.Column(db.Integer)

class Recipe(db.Model):
    __tablename__ = 'Recipes'

    RecipeID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    RecipeName = db.Column(db.String(255), nullable=False)
    Description = db.Column(db.Text, nullable=True)
    CookingTime = db.Column(db.Integer, nullable=True)
    ImageURL = db.Column(db.String(255), nullable=True)
    Ingredients = db.Column(db.Text, nullable=True)
    Instructions = db.Column(db.Text, nullable=True)

class IngredientsRecipes(db.Model):
    __tablename__ = 'IngredientsRecipes'  # テーブル名を指定

    ID = db.Column(db.Integer, primary_key=True)
    IngredientID = db.Column(db.Integer)
    RecipeID = db.Column(db.Integer)
    Must = db.Column(db.Boolean)
 
class IngredientSubstitutes(db.Model): 
    __tablename__ = 'IngredientSubstitutes'

    SubstituteID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    RecipeID = db.Column(db.Integer, db.ForeignKey('Recipes.RecipeID'), nullable=True)
    PrimaryIngredientID = db.Column(db.Integer, db.ForeignKey('Ingredients.IngredientID'), nullable=True)
    SubstituteIngredientID = db.Column(db.Integer, db.ForeignKey('Ingredients.IngredientID'), nullable=True)

class AddIngredientsRecipes(db.Model):
    __tablename__ = 'AddIngredientsRecipes'

    ID = db.Column(db.Integer, primary_key=True)
    IngredientID = db.Column(db.Integer)
    RecipeID = db.Column(db.Integer)
    Must = db.Column(db.Boolean)



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/Login')
def rogin():
    return render_template('login.html')

@app.route('/recipe')
def recipe():
    return render_template('recipe.html')

#コメント

@app.route('/works')
def works():
    return render_template('works.html')

@app.route('/foods')
def foods():
    vegetables = Ingredients.query.all()
    items = []
    current_date = datetime.now().date()  # 現在の日付のみを取得

    for vegetable in vegetables:
        if vegetable.expiration_date:
            if isinstance(vegetable.expiration_date, datetime):
                expiry_date = vegetable.expiration_date.date()  # datetimeオブジェクトから日付のみを取得
            else:
                expiry_date = vegetable.expiration_date  # 既に日付オブジェクトの場合

            delta = expiry_date - current_date
            days_left = delta.days if delta.days >= 0 else 0  # 賞味期限が過ぎている場合は0日と表示
        else:
            # expiration_dateが設定されていない場合の処理
            expiry_date = None
            days_left = '不明'  # または適切なデフォルト値

        veg_data = {
            "IngredientID": vegetable.IngredientID,
            'name': vegetable.name,
            'image_file': vegetable.image_path,
            'expiry': expiry_date.strftime('%Y-%m-%d') if expiry_date else '不明',  # 日付を文字列に変換、または'不明'
            'days_left': days_left,
            'is_present': vegetable.is_present,
            'category': vegetable.category  # 新しく追加されたカテゴリー情報
        }
        items.append(veg_data)

    return render_template('foods.html', items=items)

@app.route('/path/to/server/endpoint', methods=['POST'])
def handle_data():
    data = request.json
    selected_items = data['selectedItems']
    # ここで selected_items に対する処理を行う
    print(selected_items)
    # SQLクエリの構築と実行
   # MUST属性が1の食材を含むレシピの検索
    must_recipes = db.session.query(IngredientsRecipes.RecipeID)\
        .filter(IngredientsRecipes.Must == True)\
        .filter(db.or_(
            IngredientsRecipes.IngredientID.in_(selected_items),
            db.and_(
                IngredientSubstitutes.RecipeID == IngredientsRecipes.RecipeID,
                IngredientsRecipes.IngredientID == IngredientSubstitutes.PrimaryIngredientID,
                IngredientSubstitutes.SubstituteIngredientID.in_(selected_items)
            )
        ))\
        .subquery()

   # 各レシピにおけるMUST以外の食材の総数を計算するサブクエリ
    non_must_ingredient_count = db.session.query(
        IngredientsRecipes.RecipeID,
        func.count(IngredientsRecipes.IngredientID).label('total_non_must')
    ).filter(IngredientsRecipes.Must.isnot(True))\
    .group_by(IngredientsRecipes.RecipeID)\
    .subquery()

    # MUST以外の食材を含むレシピの検索
    non_must_recipes = db.session.query(
        IngredientsRecipes.RecipeID,
        func.count(db.distinct(IngredientsRecipes.IngredientID)).label('selected_non_must_count'),
        non_must_ingredient_count.c.total_non_must
    ).join(
        non_must_ingredient_count,
        IngredientsRecipes.RecipeID == non_must_ingredient_count.c.RecipeID
    ).filter(
        IngredientsRecipes.IngredientID.in_(selected_items),
        IngredientsRecipes.Must.isnot(True)
    ).group_by(
        IngredientsRecipes.RecipeID,
        non_must_ingredient_count.c.total_non_must
    ).having(
        func.count(db.distinct(IngredientsRecipes.IngredientID)) >= func.ceil(2/3 * non_must_ingredient_count.c.total_non_must)
    ).subquery()

    # 最終的に作成可能なレシピの特定
    possible_recipes = db.session.query(must_recipes.c.RecipeID)\
        .join(non_must_recipes, non_must_recipes.c.RecipeID == must_recipes.c.RecipeID)
    recipe_ids = [recipe.RecipeID for recipe in possible_recipes.all()]

    print(recipe_ids)

    #作成できるレシピIDを用いてレシピIDを参照する
    # 指定されたRecipeIDのレシピを取得
    recipes = Recipe.query.filter(Recipe.RecipeID.in_(recipe_ids)).all()
    
    if not recipes:
        # 指定されたIDのレシピが見つからない場合はエラーを返します。
        return jsonify({'error': 'No Recipes found for provided IDs'}), 404
    
    print(len(recipes)) #作成可能なレシピがいくつあったか
    #初期表示レシピ数を８に設定する
    recipes_num = 8
    recipe_add = recipes_num - len(recipes)

    ingredients = Ingredients.query.filter(Ingredients.IngredientID.in_(selected_items)).all()
    ingredient_names = [ingredient.name for ingredient in ingredients]
    ingredient_names_str = ", ".join(ingredient_names)

    print(ingredient_names_str)
    scraped_data_list = scraping(ingredient_names_str, recipe_add)

    # スクレイピングされた各レシピに対してループを行い、データベースに追加
    for scraped_data in scraped_data_list:
        # 既にデータベースに存在するレシピ名をチェック
        existing_recipe = Recipe.query.filter_by(RecipeName=scraped_data['title']).first()
        new_recipe = None  # new_recipe の初期化
        
        # レシピ名がデータベースに存在しない場合のみ、新しいレシピを追加
        if not existing_recipe:
            new_recipe = Recipe(
                RecipeName=scraped_data['title'],
                Description=scraped_data['explanation'],
                ImageURL=scraped_data['image_path'],
                Ingredients=scraped_data['ingredients'],
                Instructions=scraped_data['procedures']
            )
            db.session.add(new_recipe)
            db.session.flush()  # レシピIDを取得するためにflushを使用
            db.session.commit()
        if new_recipe:  # new_recipe が None でない場合のみ実行
            # 以下のコードは、new_recipe が実際に作成された場合のみ実行されます
            db.session.commit()

            mapping_dict = {
                "にんじん": ["にんじん", "人参", "ニンジン"],
                "玉ねぎ" : ["玉ねぎ", "タマネギ","たまねぎ"],
                "じゃがいも" : ["じゃがいも","ジャガイモ"],
                "なす" : ["茄子", "なす","ナス"],
                "ねぎ" : ["ねぎ","ネギ"],
                "大根" : ["大根","だいこん", "ダイコン"],
                "レンコン" : ["蓮根","レンコン","れんこん"],
                "さつまいも" : ["さつまいも","サツマイモ"],
                "ほうれん草" : ["ほうれん草","ホウレンソウ"],
                "青梗菜" : ["青梗菜","チンゲンサイ"],
                "ともろこし" : ["とうもろこし","トウモロコシ"],
                "鶏むね肉" : ["鶏むね肉","鶏胸肉","鶏肉","鶏肉(むね)","鶏肉(胸)","鶏肉(ムネ)"],
                "鶏もも肉" : ["鶏もも肉","鶏モモ肉","鶏肉","鶏肉(もも)","鶏肉(モモ)"],
                "ひき肉" : ["ひき肉","挽き肉"],
                "牛小間切れ" : ["牛小間切れ","牛肉"],
                "牛バラ" : ["牛バラ","牛肉"],
                "豚小間切れ" : ["豚小間切れ","豚肉"],
                "豚ヒレ" : ["豚肉","豚ひれ肉","豚ヒレ肉"],
                "豚バラ" : ["豚肉","豚バラ","豚バラ肉"],
                "牛もも肉" : ["牛もも肉","牛もも","牛肉"],
            }

            ingredient_names = scraped_data['ingredients'].split(',')

            for ingredient_name in ingredient_names:
                ingredient_name = ingredient_name.strip()  # 余分な空白を削除

                # マッピング辞書を使用して名前の変換
                for db_name, scraped_names in mapping_dict.items():
                    if ingredient_name in scraped_names:
                        ingredient_name = db_name
                        break

                # データベースで材料を検索
                ingredient = Ingredients.query.filter_by(name=ingredient_name).first()
                if ingredient:
                    IngredientID = ingredient.IngredientID
                    print(ingredient_name)
                    print(IngredientID)
                    RecipeID = new_recipe.RecipeID
                    print(RecipeID)

                    # タイトルに食材名が含まれているかチェック
                    is_must = 1 if ingredient_name in new_recipe.RecipeName else None
                    print(is_must)
                    
                    if IngredientID is not None and RecipeID is not None:
                        new_ingredient_recipe = IngredientsRecipes(
                            IngredientID=IngredientID,
                            RecipeID=RecipeID,
                            Must=is_must # True、False、または None を設定
                        )
                        db.session.add(new_ingredient_recipe)
                        db.session.commit()

    # 取得したレシピオブジェクトを辞書リストに変換
    recipes_data = [{
        'RecipeID': recipe.RecipeID,
        'RecipeName': recipe.RecipeName,
        'Description': recipe.Description,
        'CookingTime': recipe.CookingTime,
        'ImageURL': recipe.ImageURL,
        'Ingredients': recipe.Ingredients,
        'Instructions': recipe.Instructions
    } for recipe in recipes]

    print(recipes_data)


    #クックパッドからレシピをスクレイピング
    #scraping()
    
    # JSONとしてレシピデータを返す
    return jsonify(recipes_data)



@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/search', methods=['GET', 'POST'])
def search_foods():
    query = ''
    if request.method == 'POST':
        query = request.form['query']
        print(query)
        # ここで検索処理やデータベースへのクエリを行う。
    return render_template('index.html', query=query)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        # 画像を処理
        class_name, confidence_score = process_image(file_path)
        class_name = class_name.split(' ', 1)[1] if ' ' in class_name else class_name
        print(class_name)
        #OCRチェック
        if(class_name=="肉"):
            class_name, date = analyze_food_categories(file_path)
            if(class_name == ""):
                class_name = "判定できませんでした。もう一度撮影し直してください"
        
        # データベースから食材IDを検索
        ingredient = Ingredients.query.filter_by(name=class_name).first()
        if ingredient:
            ingredient_id = ingredient.IngredientID
        else:
            ingredient_id = None
        print(ingredient_id)

        # 単一のIDをリストに変換
        if not isinstance(ingredient_id, list):
            ingredient_id = [ingredient_id]

        response_data = {
            'image_url': '/' + file_path,
            'class_name': class_name,
            'confidence_score': confidence_score,
            "ingredient_id": ingredient_id
        }

        return jsonify(response_data)
        #return jsonify({'image_url': '/' + file_path})
    return jsonify({'error': 'File upload failed'})

@app.route('/get-recipes', methods=['POST'])
def get_recipes():
    print(request.json)
    ingredient_ids = request.json.get('ingredient_id')
    if not ingredient_ids:
        return jsonify({'error': 'No ingredient IDs provided'}), 400
    
    query = db.session.query(IngredientsRecipes.RecipeID)\
            .filter(IngredientsRecipes.IngredientID.in_(ingredient_ids))\
            .group_by(IngredientsRecipes.RecipeID)\
            .having(db.func.count(db.distinct(IngredientsRecipes.IngredientID)) == len(ingredient_ids))

    recipe_ids = [recipe.RecipeID for recipe in query.all()]
    print(recipe_ids)

    #作成できるレシピIDを用いてレシピIDを参照する
    # 指定されたRecipeIDのレシピを取得
    recipes = Recipe.query.filter(Recipe.RecipeID.in_(recipe_ids)).all()
    
    if not recipes:
        # 指定されたIDのレシピが見つからない場合はエラーを返します。
        return jsonify({'error': 'No Recipes found for provided IDs'}), 404
    
    # 取得したレシピオブジェクトを辞書リストに変換
    recipes_data = [{
        'RecipeID': recipe.RecipeID,
        'RecipeName': recipe.RecipeName,
        'Description': recipe.Description,
        'CookingTime': recipe.CookingTime,
        'ImageURL': recipe.ImageURL,
        'Ingredients': recipe.Ingredients,
        'Instructions': recipe.Instructions
    } for recipe in recipes]

    print(recipes_data)
    
    # JSONとしてレシピデータを返す
    return jsonify(recipes_data)

@app.route('/recipe-details/<recipe_id>')
def recipe_details(recipe_id):
    print(recipe_id)
    # レシピIDに基づいてデータを取得
    # 指定されたRecipeIDのレシピを取得
    recipe = Recipe.query.filter_by(RecipeID=recipe_id).first()
    if not recipe:
        # 指定されたIDのレシピが見つからない場合はエラーを返します。
        return jsonify({'error': 'No Recipes found for provided IDs'}), 404
    
    # 取得したレシピオブジェクトを辞書リストに変換
    recipe_data = {
        'RecipeID': recipe.RecipeID,
        'RecipeName': recipe.RecipeName,
        'Description': recipe.Description,
        'CookingTime': recipe.CookingTime,
        'ImageURL': recipe.ImageURL,
        'Ingredients': recipe.Ingredients,
        'Instructions': recipe.Instructions
    }

    return render_template('recipe_details.html', recipe=recipe_data)
 


if __name__ == '__main__': 
    app.run(debug=True)
