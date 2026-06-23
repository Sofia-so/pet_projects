import pytest
import os
from werkzeug.security import generate_password_hash

from app import create_app


@pytest.fixture(scope="module")
def app():
    os.environ["CONFIG_TYPE"] = "app.config.TestingConfig"
    app = create_app()

    with app.app_context():
        yield app


@pytest.fixture(scope="module")
def test_client(app):
    with app.test_client() as testing_client:
        with app.app_context():
            yield testing_client


@pytest.fixture(scope="module")
def init_database(test_client):
    from app.md_engine import session
    from app.db import (
        User,
        Diary,
        Note
    )

    password = "strong_password"

    test_default_user = User(
        first_name="User",
        last_name="LastName",
        username="test_username1",
        email="email@g.com",
        password_hash=generate_password_hash(password)
    )

    test_second_user = User(
        first_name="User",
        last_name="LastName",
        username="test_username2",
        email="email2@g.com",
        password_hash=generate_password_hash(password)
    )

    session.add(test_default_user)
    session.add(test_second_user)
    session.commit()

    test_diary1 = Diary(
        user_id=test_default_user.id,
        title="Diary1",
        content="notices"
    )

    test_diary2 = Diary(
        user_id=test_second_user.id,
        title="Diary2",
        content="meetings"
    )

    session.add_all([test_diary1, test_diary2])
    session.commit()

    test_note1 = Note(
        diary_id=test_diary1.id,
        comment="notice1",
        note_content="Text"
    )

    test_note2 = Note(
        diary_id=test_diary1.id,
        comment="notice2",
        note_content="Text"
    )

    test_note3 = Note(
        diary_id=test_diary2.id,
        comment="meeting1",
        note_content="Text"
    )

    session.add_all([test_note1, test_note2, test_note3])
    session.commit()

    yield {
        "user": test_default_user,
        "second_user": test_second_user,
        "diary": test_diary1,
        "second_diary": test_diary2,
        "note": test_note1,
        "second_note": test_note2,
        "third_note": test_note3
    }

    session.delete(test_default_user)
    session.delete(test_second_user)

    session.commit()
