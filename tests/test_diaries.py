from app.db import Diary
from app.md_engine import session


def test_create_diary(test_client, init_database):
    test_client.post(
        "/login",
        data={
            "email": "email@g.com",
            "password": "strong_password"
        }
    )
    response = test_client.post(
        "/create_diary",
        data={
            "title": "t1",
            "content": "c1"
        },
        follow_redirects=True
    )

    request = session.query(Diary).filter_by(
        title="t1"
    ).first()

    assert response.status_code == 200
    assert "Щоденник успішно створено" in (
        response.get_data(
            as_text=True
        )
    )
    assert request is not None


def test_diaries(test_client, init_database):
    test_client.post(
        "/login",
        data={
            "email": "email@g.com",
            "password": "strong_password"
        }
    )
    response = test_client.get(
        "/diaries"
    )

    assert "t1" in (response.get_data(as_text=True))
    assert "Diary1" in (response.get_data(as_text=True))


def test_update_diaries(test_client, init_database):
    test_client.post(
        "/login",
        data={
            "email": "email@g.com",
            "password": "strong_password"
        }
    )
    diary = session.query(Diary).filter_by(
        title="t1"
    ).first()

    response = test_client.post(
        f"/update_diary/{diary.id}",
        data={
            "title": "new_t1",
            "content": "new_c1"
        },
        follow_redirects=True
    )

    response2 = test_client.get(
        "/update_diary/1111111",
        follow_redirects=True
    )

    response3 = test_client.get(
        f"/update_diary/{diary.id}",
        follow_redirects=True
    )

    updated_diary = session.get(Diary, diary.id)

    assert "Зміни збережено" in (response.get_data(as_text=True))
    assert "Щоденник не знайдено" in (response2.get_data(as_text=True))
    assert response.status_code == 200
    assert response2.status_code == 200
    assert response3.status_code == 200
    assert updated_diary.title == "new_t1"
    assert updated_diary.content == "new_c1"


def test_delete_diar(test_client, init_database):
    test_client.post(
        "/login",
        data={
            "email": "email2@g.com",
            "password": "strong_password"
        }
    )
    diary = session.query(Diary).filter_by(
        title="Diary2"
    ).first()

    response1 = test_client.get(
        f"/delete_diar/{diary.id}",
        follow_redirects=True
    )

    response2 = test_client.get(
        "/delete_diar/999999",
        follow_redirects=True
    )

    assert response1.status_code == 200
    assert response2.status_code == 200


def test_delete_diary(test_client, init_database):
    test_client.post(
        "/login",
        data={
            "email": "email2@g.com",
            "password": "strong_password"
        }
    )
    diary = session.query(Diary).filter_by(
        title="Diary2"
    ).first()

    response = test_client.post(
        f"/delete_diary/{diary.id}",
        follow_redirects=True
    )
    response2 = test_client.post(
        "/delete_diary/111111",
        follow_redirects=True
    )
    deleted_diary = session.get(Diary, diary.id)

    assert deleted_diary is None
    assert "Щоденник було видалено" in (
        response.get_data(as_text=True)
    )
    assert response.status_code == 200
    assert response2.status_code == 200
    assert "Щоденник не знайдено" in (
        response2.get_data(as_text=True)
    )
