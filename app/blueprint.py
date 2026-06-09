from flask import Blueprint

main_bp = Blueprint("main", __name__, "/")
auth_bp = Blueprint("auth", __name__,"/auth")
diary_bp = Blueprint("diary", __name__, "/diary")