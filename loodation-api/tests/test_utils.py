import pytest

from loodation.core.utils import camel_to_snake


@pytest.mark.parametrize(
    ("camel_case", "snake_case"),
    [
        ("Test", "test"),
        ("test", "test"),
        ("A", "a"),
        ("Ab", "ab"),
        ("ABC", "abc"),
        ("ApiKey", "api_key"),
        ("OAuth", "o_auth"),
        ("UserSessionStorage", "user_session_storage"),
        ("UuidVaultTestHexMath", "uuid_vault_test_hex_math"),
        ("Test1", "test1"),
        ("Test2Test", "test2_test"),
        ("SomeBIGStuff", "some_big_stuff"),
        ("FromHTMLToJsToCSS", "from_html_to_js_to_css"),
        ("PYTHON", "python"),
        ("", ""),
    ],
)
def test_camel_to_snake(camel_case: str, snake_case: str):
    assert camel_to_snake(camel_case) == snake_case
