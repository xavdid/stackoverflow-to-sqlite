from itertools import count
from typing import Literal, Optional

import httpx

from stackoverflow_to_sqlite.types import (
    AnswerResponse,
    CommentResopnse,
    QuestionResponse,
    ResponseWrapper,
)

# this works for responses of all types
# NOTE: includes comment.body in addition to comment.body_markdown because the latter doesn't reliably show up if the former is missing??
RESPONSE_FILTER = (
    "!FHoa8)KWO*ZQJclfFQ-ArYmMMP7me1YZuhJpcQSM(ORmcE)-)3oYySMQ.8K2CnuTRz0h0MPb"
)

# used for live tests to reduce API calls
SKIP_LOOP = False


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
        # TODO: control to not loop for tests

        result += response["items"]

        if SKIP_LOOP or not response["has_more"]:
            break

    print(flush=True)
    return result


def fetch_questions(user_id: str, site: str) -> list[QuestionResponse]:
    return _fetch_paged_resource("questions", user_id, site)


def fetch_answers(user_id: str, site: str) -> list[AnswerResponse]:
    return _fetch_paged_resource("answers", user_id, site)


def fetch_comments(user_id: str, site: str) -> list[CommentResopnse]:
    return _fetch_paged_resource("comments", user_id, site)
