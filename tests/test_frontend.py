from pathlib import Path
from streamlit.testing.v1 import AppTest


def test_frontend_loads():
    app = AppTest.from_file(str(Path(__file__).resolve().parents[1] / "frontend" / "app.py")).run()
    assert not app.exception
    assert app.title[0].value == "Student Support"
    assert len(app.chat_input) == 1
