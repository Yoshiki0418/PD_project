import logging

from flask import Blueprint, render_template, request

logger = logging.getLogger(__name__)

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def open():
    return render_template("pd.html")


@main_bp.route("/logout")
def logout():
    return render_template("pd.html")


from sqlalchemy.sql.expression import func
from app.models import Recipe

@main_bp.route("/home")
def index():
    # ランダムに3つのレシピを取得
    recipes = Recipe.query.order_by(func.random()).limit(3).all()
    return render_template("index.html", recipes=recipes)


@main_bp.route("/Login")
def login():
    return render_template("login.html")


@main_bp.route("/works")
def works():
    return render_template("works.html")


@main_bp.route("/contact")
def contact():
    return render_template("contact.html")


@main_bp.route("/privacy")
def privacy():
    return render_template("privacy.html")


@main_bp.route("/main_nutrition")
def main_nutrition():
    return render_template("nutrition.html")


@main_bp.route("/search", methods=["GET", "POST"])
def search_foods():
    query = ""
    if request.method == "POST":
        query = request.form["query"]
        logger.debug("Search query: %s", query)
    return render_template("index.html", query=query)
