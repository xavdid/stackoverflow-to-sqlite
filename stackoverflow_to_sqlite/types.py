from typing import NotRequired, TypedDict, cast
from urllib.parse import urlparse


class ResponseWrapper[T](TypedDict):
    """
    Individual API items live in `items` and the whole thing is wrapped in this
    """

    has_more: bool
    quota_max: int
    quota_remaining: int
    page: int
    page_size: int
    total: int
    type: str
    items: list[T]


class User(TypedDict):
    account_id: int
    reputation: int
    user_id: int
    user_type: str
    display_name: str
    link: str


class UserRow(TypedDict):
    account_id: int
    name: str
    stack_overflow_id: int | None
    network_profile_url: str


"""
Each of question / answer / comment have 3 classes:

- the base, which has common fields for the other two
- the response, which has raw API data
- the row, which is what gets puts into sqlite

There's a `X_to_row` function for each to translate from Response to Row,
renaming and tweaking keys to match the output type
"""


class QuestionBase(TypedDict):
    comment_count: int
    view_count: int
    favorite_count: int
    down_vote_count: int
    up_vote_count: int
    answer_count: int
    score: int
    last_activity_date: int
    creation_date: int
    question_id: int
    body_markdown: str
    link: str
    title: str
    closed_date: NotRequired[int]
    closed_reason: NotRequired[str]


class QuestionResponse(QuestionBase):
    # these get dumped out as a stringified list, which isn't great
    # but neither is support for m2m relationships: https://github.com/simonw/datasette/issues/484
    tags: list[str]
    owner: User
    is_answered: bool
    accepted_answer_id: NotRequired[int]


class QuestionRow(QuestionBase):
    has_accepted_answer: bool
    is_considered_answered: bool
    user: int  # account_id
    site: str


class AnswerBase(TypedDict):
    down_vote_count: int
    up_vote_count: int
    is_accepted: bool
    comment_count: int
    score: int
    last_edit_date: NotRequired[int]
    creation_date: int
    answer_id: int
    body_markdown: str
    link: str


class AnswerResponse(AnswerBase):
    owner: User
    title: str
    # shows up, but is always empty
    # see: https://stackapps.com/questions/7213/the-answer-object-returns-an-empty-array-for-tags
    # I could do a second request for only the answer tags, but that's annoying
    tags: list[str]


class AnswerRow(AnswerBase):
    user: int  # account_id
    site: str
    question_title: str


class CommentBase(TypedDict):
    score: int
    post_type: str
    body_markdown: str
    post_id: int
    comment_id: int
    link: str
    creation_date: int


class CommentResopnse(CommentBase):
    owner: User
    body: str


class CommentRow(CommentBase):
    user: int  # account_id
    site: str


def _get_domain(url: str) -> str:
    return urlparse(url).hostname or "UNKNOWN"


def _remove_keys(
    d: QuestionResponse | AnswerResponse | CommentResopnse, keys: tuple[str, ...]
) -> dict[str, object]:
    return {k: v for k, v in d.items() if k not in keys}


def user_to_row(user: User) -> UserRow:
    return {
        "account_id": (aid := user["account_id"]),
        # just `name` because it shows up nicer in datasette that way
        "name": user["display_name"],
        "network_profile_url": f"https://stackexchange.com/users/{aid}/",
        # only record user id if we're sourcing from SO
        # it's probably useful for this to exist
        "stack_overflow_id": user["user_id"]
        if "https://stackoverflow.com" in user["link"]
        else None,
    }


def question_to_row(question: QuestionResponse) -> QuestionRow:
    return {
        **cast(
            QuestionBase,
            _remove_keys(
                question, ("tags", "owner", "is_answered", "accepted_answer_id")
            ),
        ),
        "user": question["owner"]["account_id"],
        # "accepted_answer_id": None,
        "has_accepted_answer": bool(question.get("accepted_answer_id")),
        "is_considered_answered": question["is_answered"],
        "site": _get_domain(question["link"]),
    }


def answer_to_row(answer: AnswerResponse) -> AnswerRow:
    return {
        **cast(AnswerBase, _remove_keys(answer, ("tags", "owner", "title"))),
        "user": answer["owner"]["account_id"],
        "site": _get_domain(answer["link"]),
        "question_title": answer["title"],
    }


def comment_to_row(comment: CommentResopnse) -> CommentRow:
    return {
        **cast(CommentBase, _remove_keys(comment, ("owner", "body"))),
        "user": comment["owner"]["account_id"],
        "site": _get_domain(comment["link"]),
    }
