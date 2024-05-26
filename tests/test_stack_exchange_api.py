# from sqlite_utils import Database


from urllib.parse import urlencode

import pytest

from stackoverflow_to_sqlite.stack_exchange_api import QUESTION_FILTER, fetch_questions


@pytest.fixture
def build_paging_mock(httpx_mock):
    def build_page_response(num_pages: int):
        for page in range(1, num_pages + 1):
            params = {
                "pagesize": 100,
                "site": "stackoverflow.com",
                "filter": QUESTION_FILTER,
                "order": "desc",
                "sort": "creation",
                "page": page,
            }

            mock_details = {
                "url": f"https://api.stackexchange.com/2.3/users/123/questions?{
                urlencode(params)
            }",
                "json": {
                    "has_more": page != num_pages,
                    "page": page,
                    "page_size": 1,
                    "total": num_pages,
                    "type": "questions",
                    "items": [{"id": page}],
                },
            }

            httpx_mock.add_response(**mock_details)

    return build_page_response


@pytest.mark.parametrize("max_pages", [1, 3, 7])
def test_paging(build_paging_mock, max_pages: int):
    build_paging_mock(max_pages)

    assert fetch_questions("123", "stackoverflow.com") == [
        {"id": p} for p in range(1, max_pages + 1)
    ]
