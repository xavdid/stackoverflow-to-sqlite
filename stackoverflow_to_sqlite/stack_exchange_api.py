from itertools import count
from typing import Optional

import httpx

from stackoverflow_to_sqlite.types import QuestionResponse, ResponseWrapper

# https://api.stackexchange.com/2.3/users/474013/questions?pagesize=100&order=desc&sort=activity&site=math.stackexchange.com&filter=!OSaAEBD*BtuYwi(Zar.e4TBVOLdsyLhbieqkN9D*eGA
QUESTION_FILTER = "!OSaAEBD*BtuYwi(Zar.e4TBVOLdsyLhbieqkN9D*eGA"


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


def fetch_questions(user_id: str, site: str) -> list[QuestionResponse]:
    result: list[QuestionResponse] = []
    for page in count(1):
        response = _api_call(
            f"/users/{user_id}/questions",
            site,
            filter_=QUESTION_FILTER,
            params={"order": "desc", "sort": "creation", "page": page},
        )

        result += response["items"]
        if not response["has_more"]:
            break

    return result
