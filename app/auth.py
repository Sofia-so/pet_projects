from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)
from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user
)
from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from sqlalchemy.exc import IntegrityError

from app.blueprint import main_bp, auth_bp

from app.db import User

from app.md_engine import session

from app.login_manager import login_manager


def authent():
    @auth_bp.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "POST":
            first_name = request.form.get("first_name")
            last_name = request.form.get("last_name")
            username = request.form.get("username")
            email = request.form.get("email")
            password = request.form.get("password")
            confirm_password = request.form.get("confirm_password")

            has_errors = False

            if len(password) < 8:
                flash("Пароль повинен містити мінімум 8 символів")
                has_errors = True

            if password != confirm_password:
                flash("Паролі не співпадають")
                has_errors = True

            if has_errors:
                return render_template("register.html")

            password_hash = generate_password_hash(password)

            try:
                user = User(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password_hash=password_hash
                )
                session.add(user)
                session.commit()
                return render_template("success_register.html")
            except IntegrityError:
                session.rollback()
                flash("Користувач з таким ім'ям користувача вже існує")
                flash("Або користувач із цією електронною адресою вже зареєстрований")
                return render_template("register.html")

        return render_template("register.html")


    @login_manager.user_loader
    def load_user(user_id):
        return session.get(User, int(user_id))


    @auth_bp.route("/login", methods=["POST", "GET"])
    def login():
        if request.method == "POST":
            email = request.form.get("email")
            password = request.form.get("password")

            user = session.query(User).filter_by(email=email).first()

            if user and check_password_hash(
                    user.password_hash,
                    password
            ):
                login_user(user)
                return redirect(
                    url_for("main.profile")
                )
            else:
                flash("Невірна адреса електронної пошти або пароль")

        return render_template("login.html")

    @auth_bp.route("/logout")
    def logout():
        logout_user()
        return redirect(url_for("main.home"))


    @main_bp.route("/profile")
    @login_required
    def profile():
        return render_template("account_login.html")


    @auth_bp.route("/delete_user")
    def delete_user():
        return render_template("delete_account.html")


    @auth_bp.route("/delete_account", methods=["POST"])
    @login_required
    def delete_account():
        user = current_user._get_current_object()

        logout_user()
        flash("Ваш акаунт було видалено")
        session.delete(user)
        session.commit()

        return redirect(url_for("auth.delete_user"))


    @auth_bp.route("/update_account", methods=["POST", "GET"])
    @login_required
    def update_account():
        user = current_user._get_current_object()

        if request.method == "GET":
            return render_template("update_account.html")

        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        has_errors = False

        if len(password) < 8:
            flash("Пароль повинен містити мінімум 8 символів")
            has_errors = True

        if password != confirm_password:
            flash("Паролі не співпадають")
            has_errors = True

        if has_errors:
            return render_template("update_account.html")

        password_hash = generate_password_hash(password)

        try:
             user.first_name = first_name
             user.last_name = last_name
             user.username = username
             user.email = email
             user.password_hash = password_hash

             session.commit()

             flash("Дані облікового запису успішно оновлено")

             return redirect(url_for("main.profile"))

        except IntegrityError:
            session.rollback()
            flash("Користувач з таким ім'ям користувача вже існує")
            flash("Або користувач із цією електронною адресою вже зареєстрований")
            return render_template("update_account.html")
