from flask import render_template
from app.blueprint import main_bp


@main_bp.route("/")
def home():
    return render_template("main_page.html")
