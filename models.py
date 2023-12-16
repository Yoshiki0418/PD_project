from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Ingredients(db.Model): 
    IngredientID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    expiration_date = db.Column(db.Date)
    image_path = db.Column(db.String(255))
    is_present = db.Column(db.Integer)
    category = db.Column(db.Integer)
    average_shelf_life = db.Column(db.Integer)

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

class unit_conversion(db.Model):
    __tablename__ = 'unit_conversion'

    id = db.Column(db.Integer, primary_key=True)
    FoodName = db.Column(db.String(255))
    Unit = db.Column(db.String(50))
    Weight = db.Column(db.Integer)