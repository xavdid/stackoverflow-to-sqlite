from typing import Any, NotRequired, TypedDict


class ResponseWrapper[T](TypedDict):
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


class QuestionResponse(TypedDict):
    tags: list[str]
    comments: NotRequired[list[Any]]
    owner: User
    is_answered: bool
    view_count: int
    favorite_count: int
    down_vote_count: int
    up_vote_count: int
    accepted_answer_id: NotRequired[int]
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


class QuestionRow(QuestionResponse):
    # these get dumped out as a stringified list, which isn't great
    # but neither is support for m2m relationships: https://github.com/simonw/datasette/issues/484
    tags: None
    comments: None
    comment_count: int
    has_accepted_answer: bool
    accepted_answer_id: None
    is_considered_answered: bool
    is_answered: None
    owner: None
    site: str
    asker: int  # account_id
