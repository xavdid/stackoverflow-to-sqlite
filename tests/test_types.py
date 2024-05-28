import pytest

from stackoverflow_to_sqlite.types import _get_domain, _remove_keys


@pytest.mark.parametrize(
    ["url", "result"],
    [
        ("https://stackoverflow.com", "stackoverflow.com"),
        ("https://meta.stackoverflow.com", "meta.stackoverflow.com"),
        ("https://webapps.meta.stackexchange.com/", "webapps.meta.stackexchange.com"),
        ("https://superuser.com", "superuser.com"),
        ("whatever", "UNKNOWN"),
    ],
)
def test_get_domain(url, result):
    assert _get_domain(url) == result


def test_remove_keys():
    assert _remove_keys(
        {  # type:ignore
            "score": 3,
            "post_type": "asdf",
            "body_markdown": "asdf",
            "post_id": 3,
            "comment_id": 4,
            "link": "zxcv",
        },
        ("link", "comment_id", "post_id"),
    ) == {
        "score": 3,
        "post_type": "asdf",
        "body_markdown": "asdf",
    }
