from flask import Flask

from dotenv import load_dotenv
import os

from app import (
    diaries,
    note,
    home,
    auth
)


def create_app():

    app = Flask(__name__)
    
    load_dotenv()
    
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

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(diary_bp)
    app.register_blueprint(note_bp)

    return app
