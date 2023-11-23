from flask import Flask, request, render_template, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.utils import secure_filename
from food_judge import process_image
from datetime import datetime
from meat_judge import analyze_food_categories



app = Flask(__name__)
UPLOAD_FOLDER = 'static/UPLOAD_FOLDER'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# MySQLの設定
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Ingredients(db.Model):
    IngredientID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    expiration_date = db.Column(db.Date)
    image_path = db.Column(db.String(255))
    is_present = db.Column(db.Integer)
    category = db.Column(db.Integer)

class Recipe(db.Model):
    __tablename__ = 'Recipes'

    RecipeID = db.Column(db.Integer, primary_key=True)
    RecipeName = db.Column(db.String(255), nullable=False)
    Description = db.Column(db.Text, nullable=True)
    CookingTime = db.Column(db.Integer, nullable=True)
    ImageURL = db.Column(db.String(255), nullable=True)
    Ingredients = db.Column(db.Text, nullable=True)
    Instructions = db.Column(db.Text, nullable=True)

class IngredientsRecipes(db.Model):
    __tablename__ = 'IngredientsRecipes'  # テーブル名を指定

    ID = db.Column(db.Integer, primary_key=True)
    IngredientID = db.Column(db.Integer, db.ForeignKey('Ingredients.IngredientID'))
    RecipeID = db.Column(db.Integer, db.ForeignKey('Recipes.RecipeID'))

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
    query = db.session.query(IngredientsRecipes.RecipeID)\
        .filter(IngredientsRecipes.IngredientID.in_(selected_items))\
        .group_by(IngredientsRecipes.RecipeID)\
        .having(db.func.count(db.distinct(IngredientsRecipes.IngredientID)) == len(selected_items))

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
