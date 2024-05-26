from urllib.parse import urlencode

import pytest
from sqlite_utils import Database

from stackoverflow_to_sqlite.stack_exchange_api import QUESTION_FILTER


@pytest.fixture
def tmp_db_path(tmp_path):
    """
    returns a Database path in a temp dir
    """
    return str(tmp_path / "test.db")


@pytest.fixture
def tmp_db(tmp_db_path):
    """
    returns a Database in a temp dir
    """
    return Database(tmp_db_path)


@pytest.fixture
def questions_response(httpx_mock):
    params = {
        "pagesize": 100,
        "site": "stackoverflow.com",
        "filter": QUESTION_FILTER,
        "order": "desc",
        "sort": "creation",
        "page": 1,
    }

    mock_details = {
        "url": f"https://api.stackexchange.com/2.3/users/123/questions?{urlencode(params)}",
        "json": {
            "has_more": False,
            "page": 1,
            "page_size": 100,
            "total": 15,
            "type": "questions",
            "items": [
                {
                    "tags": ["macros", "elixir"],
                    "comments": [
                        {
                            "owner": {
                                "account_id": 10360,
                                "reputation": 5788,
                                "user_id": 19520,
                                "user_type": "registered",
                                "display_name": "ema",
                                "link": "https://stackoverflow.com/users/19520/ema",
                            },
                            "post_id": 77357478,
                            "comment_id": 136380173,
                        }
                    ],
                    "owner": {
                        "account_id": 2045145,
                        "reputation": 5204,
                        "user_id": 1825390,
                        "user_type": "registered",
                        "display_name": "xavdid",
                        "link": "https://stackoverflow.com/users/1825390/xavdid",
                    },
                    "is_answered": True,
                    "view_count": 104,
                    "favorite_count": 0,
                    "down_vote_count": 0,
                    "up_vote_count": 0,
                    "accepted_answer_id": 77359032,
                    "answer_count": 1,
                    "score": 0,
                    "last_activity_date": 1698233092,
                    "creation_date": 1698219631,
                    "question_id": 77357478,
                    "body_markdown": "a very cool elixir question and stuff",
                    "link": "https://stackoverflow.com/questions/77357478/is-it-possible-to-define-case-clauses-with-an-elixir-macro",
                    "title": "Is it possible to define `case` clauses with an elixir macro?",
                },
                {
                    "tags": ["javascript", "jquery", "iframe", "xss"],
                    "comments": [
                        {
                            "owner": {
                                "account_id": 1244536,
                                "reputation": 50506,
                                "user_id": 1206267,
                                "user_type": "registered",
                                "display_name": "Ohgodwhy",
                                "link": "https://stackoverflow.com/users/1206267/ohgodwhy",
                            },
                            "post_id": 19287918,
                            "comment_id": 28560850,
                        },
                        {
                            "owner": {
                                "account_id": 2045145,
                                "reputation": 5204,
                                "user_id": 1825390,
                                "user_type": "registered",
                                "display_name": "xavdid",
                                "link": "https://stackoverflow.com/users/1825390/xavdid",
                            },
                            "post_id": 19287918,
                            "comment_id": 28560912,
                        },
                        {
                            "owner": {
                                "account_id": 1244536,
                                "reputation": 50506,
                                "user_id": 1206267,
                                "user_type": "registered",
                                "display_name": "Ohgodwhy",
                                "link": "https://stackoverflow.com/users/1206267/ohgodwhy",
                            },
                            "post_id": 19287918,
                            "comment_id": 28560933,
                        },
                        {
                            "owner": {
                                "account_id": 2045145,
                                "reputation": 5204,
                                "user_id": 1825390,
                                "user_type": "registered",
                                "display_name": "xavdid",
                                "link": "https://stackoverflow.com/users/1825390/xavdid",
                            },
                            "post_id": 19287918,
                            "comment_id": 28561006,
                        },
                    ],
                    "owner": {
                        "account_id": 2045145,
                        "reputation": 5204,
                        "user_id": 1825390,
                        "user_type": "registered",
                        "display_name": "xavdid",
                        "link": "https://stackoverflow.com/users/1825390/xavdid",
                    },
                    "is_answered": False,
                    "view_count": 149,
                    "favorite_count": 0,
                    "down_vote_count": 0,
                    "up_vote_count": 0,
                    "closed_date": 1448182440,
                    "answer_count": 0,
                    "score": 0,
                    "last_activity_date": 1381383787,
                    "creation_date": 1381383787,
                    "question_id": 19287918,
                    "body_markdown": "a questiona about security and things",
                    "closed_reason": "Duplicate",
                    "title": "Implementing an XSS attack",
                    "link": "https://stackoverflow.com/questions/19287918/implementing-an-xss-attack",
                },
            ],
        },
    }

    httpx_mock.add_response(**mock_details)
