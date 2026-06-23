def test_home_page(test_client):
    response = test_client.get("/")
    assert response.status_code == 200
    assert response.content_type.startswith("text/html")


def test_home_page_content(test_client):
    response = test_client.get("/")
    assert "Головна сторінка" in response.get_data(as_text=True)
    assert "Вхід" in response.get_data(as_text=True)
    assert "Реєстрація" in response.get_data(as_text=True)
