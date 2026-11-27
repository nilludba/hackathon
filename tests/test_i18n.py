import ast
from pathlib import Path

from i18n import T


def ui_texts():
    """Every string literal passed to _() in app.py."""
    tree = ast.parse((Path(__file__).parent.parent / "app.py").read_text(encoding="utf-8"))
    return {n.args[0].value for n in ast.walk(tree)
            if isinstance(n, ast.Call) and getattr(n.func, "id", None) == "_"
            and n.args and isinstance(n.args[0], ast.Constant)}


def test_every_ui_text_has_en_and_ru():
    missing = sorted(t for t in ui_texts() if set(T.get(t, {})) < {"en", "ru"})
    assert not missing, missing
