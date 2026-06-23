from html import unescape

from app.md_engine import session
from app.db import User


def test_login(init_database, test_client):

    response1 = test_client.get("/login")
    response2 = test_client.post(
        "/login",
        data={
            "email": "email@g.com",
            "password": "strong_password"
        }
    )
    response3 = test_client.post(
        "/login",
        data={
            "email": "wrong_email.com",
            "password": "strong_password"
        }
    )
    response4 = test_client.post(
        "/login",
        data={
            "email": "email@g.com",
            "password": "wrong_password"
        }
    )

    assert response1.status_code == 200
    assert response2.status_code == 302
    assert "/profile" in response2.location
    assert "Невірна адреса електронної пошти або пароль" in (
        response3.get_data(as_text=True)
    )
    assert "Невірна адреса електронної пошти або пароль" in (
        response4.get_data(as_text=True)
    )


def test_logout(test_client, init_database):
    test_client.post(
        "/login",
        data={
            "email": "email@g.com",
            "password": "strong_password"
        }
    )
    test_client.get("/logout")
    response = test_client.get(
        "/profile",
        follow_redirects=False
    )

    assert response.status_code == 302


def test_update_account(init_database, test_client):
    response1 = test_client.post(
        "/login",
        data={
            "email": "email@g.com",
            "password": "strong_password"
        }
    )

    response2 = test_client.post(
        "/update_account",
        data={
            "first_name": "NewName",
            "last_name": "NewLastName",
            "username": "new_username",
            "email": "new_email@g.com",
            "password": "new_password1",
            "confirm_password": "new_password1"
        }
    )

    user = session.query(User).filter_by(
        username="new_username",
        email="new_email@g.com"
    ).first()

    response3 = test_client.post(
        "/update_account",
        data={
            "first_name": "NewName",
            "last_name": "NewLastName",
            "username": "new_username",
            "email": "new_email@g.com",
            "password": "new_p",
            "confirm_password": "new_p"
        }
    )

    response4 = test_client.post(
        "/update_account",
        data={
            "first_name": "NewName",
            "last_name": "NewLastName",
            "username": "new_username",
            "email": "email2@g.com",
            "password": "new_password1",
            "confirm_password": "new_password1"
        }
    )

    response5 = test_client.post(
        "/update_account",
        data={
            "first_name": "NewName",
            "last_name": "NewLastName",
            "username": "test_username2",
            "email": "email2@g.com",
            "password": "new_password1",
            "confirm_password": "new_password1"
        }
    )

    response6 = test_client.post(
        "/update_account",
        data={
            "first_name": "NewName",
            "last_name": "NewLastName",
            "username": "test_username2",
            "email": "email2@g.com",
            "password": "new_password1",
            "confirm_password": "new_password"
        }
    )

    assert response1.status_code == 302
    assert user is not None
    assert user.first_name == "NewName"
    assert response2.status_code == 302
    assert "Пароль повинен містити мінімум 8 символів" in (
        response3.get_data(as_text=True)
    )
    assert "Користувач з таким ім'ям користувача вже існує" in (unescape(
        response4.get_data(as_text=True))
    )
    assert "Або користувач із цією електронною адресою вже зареєстрований" in (
        response4.get_data(as_text=True)
    )
    assert "Користувач з таким ім'ям користувача вже існує" in (unescape(
        response5.get_data(as_text=True))
    )
    assert "Або користувач із цією електронною адресою вже зареєстрований" in (
        response5.get_data(as_text=True)
    )
    assert "Паролі не співпадають" in (
        response6.get_data(as_text=True)
    )


def test_register(init_database, test_client):
    response1 = test_client.post(
        "/register",
        data={
            "first_name": "TestName",
            "last_name": "TestLastName",
            "username": "test_username3",
            "email": "email3@g.com",
            "password": "strong_password",
            "confirm_password": "strong_password"
        }
    )
    user = session.query(User).filter_by(
        username="test_username3"
    ).first()

    response2 = test_client.post(
        "/register",
        data={
            "first_name": "User",
            "last_name": "LastName",
            "username": "test_username2",
            "email": "email2@g.com",
            "password": "strong_password",
            "confirm_password": "strong_password"
        }
    )
    response3 = test_client.post(
        "/register",
        data={
            "first_name": "User",
            "last_name": "LastName",
            "username": "test_username2",
            "email": "email2@g.com",
            "password": "strong_password",
            "confirm_password": "str"
        }
        )

    response4 = test_client.post(
        "/register",
        data={
            "first_name": "User",
            "last_name": "LastName",
            "username": "test_username2",
            "email": "email2@g.com",
            "password": "str",
            "confirm_password": "str"
        }
        )

    response_text = unescape(response2.get_data(as_text=True))

    assert response1.status_code == 200
    assert user is not None
    assert user.email == "email3@g.com"
    assert "Користувач з таким ім'ям користувача вже існує" in (
        response_text
           )
    assert "Або користувач із цією електронною адресою вже зареєстрований" in (
        response_text
           )
    assert "Паролі не співпадають" in (
        response3.get_data(as_text=True)
    )
    assert "Пароль повинен містити мінімум 8 символів" in (
        response4.get_data(as_text=True)
    )


def test_delete_user(test_client):
    response = test_client.get("/delete_user")

    assert response.status_code == 200


def test_delete_account(test_client, init_database):
    response1 = test_client.post(
        "/login",
        data={
            "email": "email2@g.com",
            "password": "strong_password"
        }
                                )

    response2 = test_client.post(
        "/delete_account",
        follow_redirects=True)

    user = session.query(User).filter_by(
        email="email2@g.com"
    ).first()

    assert response1.status_code == 302
    assert response2.status_code == 200
    assert "Ваш акаунт було видалено" in (
        response2.get_data(as_text=True)
    )
    assert user is None
