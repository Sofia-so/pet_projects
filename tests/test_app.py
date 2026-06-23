def test_config(app):
    assert app.config["TESTING"] is True


def test_blueprint(app):
    assert "main" in app.blueprints
    assert "auth" in app.blueprints
    assert "diary" in app.blueprints
    assert "note" in app.blueprints
