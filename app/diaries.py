from flask import request, render_template, flash, redirect, url_for
from flask_login import login_required, current_user

from app.blueprint import diary_bp
from app.db import Diary
from app.md_engine import session


@diary_bp.route("/create_diary", methods=["GET", "POST"])
@login_required
def create_diary():
    if request.method == "POST":
        diary = Diary(
        user=current_user,
        title=request.form.get("title"),
        content=request.form.get("content")
        )
        session.add(diary)
        session.commit()
        flash("Щоденник успішно створено")

        return redirect(
            url_for("diary.create_diary")
        )

    return render_template("create_diary.html")


@diary_bp.route("/diaries", methods=["GET"])
@login_required
def diaries():
    user = current_user

    if len(user.diaries) == 0:
        flash("У вас немає щоденників")

    return render_template(
        "list_diaries.html",
        diary_list=user.diaries
    )


@diary_bp.route("/update_diary/<int:diary_id>", methods=["POST", "GET"])
@login_required
def update_diary(diary_id):

    diary = session.query(Diary).filter(
        Diary.id == diary_id,
        Diary.user_id == current_user.id
    ).first()

    if diary is None:
        flash("Щоденник не знайдено")
        return redirect(url_for("diary.diaries"))

    if request.method == "POST":
        diary.title = request.form.get("title")
        diary.content = request.form.get("content")

        session.commit()
        flash("Зміни збережено")

        return redirect(
            url_for("diary.update_diary", diary_id=diary_id,)
        )

    return render_template(
        "update_diary.html",
        diary_id=diary_id,
        diary=diary)


@diary_bp.route("/delete_diary/<int:diary_id>", methods=["POST", "GET"])
@login_required
def delete_diary(diary_id):
    diary = session.query(Diary).filter(
        Diary.id == diary_id,
        Diary.user_id == current_user.id
    ).first()

    if diary is None:
        flash("Щоденник не знайдено")
        return redirect(url_for("diary.diaries"))

    flash("Щоденник було видалено")
    session.delete(diary)
    session.commit()

    return redirect(url_for(
        "diary.delete_diar",
        diary_id=diary_id
    ))


@diary_bp.route("/delete_diar/<int:diary_id>", methods=["POST", "GET"])
@login_required
def delete_diar(diary_id):
    return render_template(
        "delete_diary.html",
        diary_id=diary_id
    )
