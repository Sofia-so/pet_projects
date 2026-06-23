from flask import (
    Flask,
    render_template
)

from dotenv import load_dotenv
import os

import app.diaries, app.note


def create_app():

    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    config_type = os.getenv(
        "CONFIG_TYPE",
        default="app.config.Config"
    )
    app.config.from_object(config_type)

    from app.blueprint import (
        main_bp,
        auth_bp,
        diary_bp,
        note_bp
    )

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
    app.register_blueprint(diary_bp)
    app.register_blueprint(note_bp)

    return app
