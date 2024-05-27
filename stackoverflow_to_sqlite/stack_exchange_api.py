from itertools import count
from typing import Literal, Optional

import httpx

from stackoverflow_to_sqlite.types import (
    AnswerResponse,
    QuestionResponse,
    ResponseWrapper,
)

# this works for responses of all types
RESPONSE_FILTER = "!S)wxxkXA5fyMMShzhUnJpTEaqB4NZq8VWklMWjBAqPt.BT6LDY0bt5*yNvTlYS7E"


def _api_call(
    path: str, site: str, filter_="", params: Optional[dict[str, str | int]] = None
) -> ResponseWrapper:
    assert path.startswith("/")
    response = httpx.get(
        f"https://api.stackexchange.com/2.3{path}",
        params={"pagesize": 100, "site": site, "filter": filter_, **(params or {})},
        headers={"user-agent": "stackoverflow-to-sqlite"},
    )
    response.raise_for_status()

    return response.json()


def _fetch_paged_resource(
    resource: Literal["questions", "answers", "comments"], user_id: str, site: str
) -> list:
    result = []
    for page in count(1):
        response = _api_call(
            f"/users/{user_id}/{resource}",
            site,
            filter_=RESPONSE_FILTER,
            params={"order": "desc", "sort": "creation", "page": page},
        )
        print(".", end="", flush=True)

        # TODO: handle error and save what we got

        result += response["items"]
        if not response["has_more"]:
            break

    return result


def fetch_questions(user_id: str, site: str) -> list[QuestionResponse]:
    return _fetch_paged_resource("questions", user_id, site)


def fetch_answers(user_id: str, site: str) -> list[AnswerResponse]:
    return _fetch_paged_resource("answers", user_id, site)
