from flask import (
    request,
    render_template,
    redirect,
    url_for,
    flash
)
from flask_login import login_required

from app.blueprint import note_bp
from app.db import Note, Diary
from app.md_engine import session


@note_bp.route("/create_note/<int:diary_id>", methods=["POST", "GET"])
@login_required
def create_note(diary_id):
    if request.method == "POST":
        comment = request.form.get("comment")
        note_content = request.form.get("note_content")

        note = Note(
            comment=comment,
            note_content=note_content,
            diary_id=diary_id
        )

        flash("Запис успішно створено")
        session.add(note)
        session.commit()

    return render_template(
            "create_note.html",
            diary_id=diary_id)


@note_bp.route("/notes/<int:diary_id>", methods=["GET"])
@login_required
def notes(diary_id):
    diary = session.query(Diary).filter(
        Diary.id == diary_id
    ).first()

    return render_template(
        "notes.html",
        notes_list=diary.notes,
        diary_id=diary_id
    )


@note_bp.route("/update_note/<int:note_id>", methods=["POST", "GET"])
@login_required
def update_note(note_id):

    note = session.query(Note).filter(
        Note.id == note_id
    ).first()

    if request.method == "POST":
        note.comment = request.form.get("comment")
        note.note_content = request.form.get("note_content")

        flash("Зміни збережено")

        session.commit()

        return redirect(
            url_for("note.notes", diary_id=note.diary_id)
        )

    return render_template(
        "update_note.html",
        note_id=note_id,
        diary_id=note.diary_id,
        note=note
    )


@note_bp.route("/delete_note/<int:note_id>", methods=["GET"])
@login_required
def delete_note(note_id):
    note = session.query(Note).filter(
        Note.id == note_id
    ).first()

    if not note:
        return "Запис не знайдено", 404

    return render_template(
        "delete_note.html",
        note_id=note.id,
        diary_id=note.diary_id,
        note=note
    )


@note_bp.route("/delete_finally_note/<int:note_id>", methods=["POST", "GET"])
@login_required
def delete_finally_note(note_id):
    note = session.query(Note).filter(
        Note.id == note_id
    ).first()

    if not note:
        flash("Запис не знайдено")
        return redirect(url_for("diary.diaries"))

    diary_id = note.diary_id

    session.delete(note)
    session.commit()
    flash("Запис було видалено")

    return redirect(url_for(
        "note.notes",
        diary_id=diary_id,
    ))
