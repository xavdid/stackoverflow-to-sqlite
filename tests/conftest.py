from urllib.parse import urlencode

import pytest
from sqlite_utils import Database

from stackoverflow_to_sqlite.stack_exchange_api import RESPONSE_FILTER


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
        "filter": RESPONSE_FILTER,
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
                    "comment_count": 1,
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
                    "comment_count": 4,
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


@pytest.fixture
def answers_response(httpx_mock):
    params = {
        "pagesize": 100,
        "site": "stackoverflow.com",
        "filter": RESPONSE_FILTER,
        "order": "desc",
        "sort": "creation",
        "page": 1,
    }

    mock_details = {
        "url": f"https://api.stackexchange.com/2.3/users/123/answers?{urlencode(params)}",
        "json": {
            "has_more": False,
            "page": 1,
            "page_size": 100,
            "total": 15,
            "type": "questions",
            "items": [
                {
                    "tags": [],
                    "owner": {
                        "account_id": 2045145,
                        "reputation": 5204,
                        "user_id": 1825390,
                        "user_type": "registered",
                        "display_name": "xavdid",
                        "link": "https://stackoverflow.com/users/1825390/xavdid",
                    },
                    "comment_count": 4,
                    "down_vote_count": 0,
                    "up_vote_count": 0,
                    "is_accepted": True,
                    "score": 0,
                    "creation_date": 1643673277,
                    "answer_id": 70934214,
                    "body_markdown": "This is possible!",
                    "link": "https://stackoverflow.com/questions/70901751/find-replace-data-in-a-csv-using-python-on-zapier/70934214#70934214",
                    "title": "Find &amp; replace data in a CSV using Python on Zapier",
                },
                {
                    "tags": [],
                    "owner": {
                        "account_id": 2045145,
                        "reputation": 5204,
                        "user_id": 1825390,
                        "user_type": "registered",
                        "display_name": "xavdid",
                        "link": "https://stackoverflow.com/users/1825390/xavdid",
                    },
                    "comment_count": 2,
                    "down_vote_count": 0,
                    "up_vote_count": 0,
                    "is_accepted": False,
                    "score": 0,
                    "creation_date": 1643666093,
                    "last_edit_date": 1643666193,
                    "body_markdown": "In javascript, variables",
                    "link": "https://stackoverflow.com/questions/70598105/zapier-javascript-find-replace-special-characters/70933266#70933266",
                    "title": "Zapier Javascript Find/Replace Special Characters",
                },
            ],
        },
    }

    httpx_mock.add_response(**mock_details)
