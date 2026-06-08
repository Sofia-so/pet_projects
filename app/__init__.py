from flask import (
    Flask,
    render_template
)

from app.md_engine import session

from dotenv import load_dotenv
import os


def create_app():

    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

    from app.blueprint import main_bp, auth_bp

    from app.db import User

    from app.login_manager import login_manager

    login_manager.init_app(app)

    load_dotenv()


    @main_bp.route('/')
    def home():
        return render_template("main_page.html")


    from app.auth import authent

    authent()

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)

    return app
