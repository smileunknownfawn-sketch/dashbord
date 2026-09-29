from core.config import APP_VERSION, DEVELOPER


def test_release_version():
    assert APP_VERSION == "1.1.0"
    assert DEVELOPER == "В.О.М."
