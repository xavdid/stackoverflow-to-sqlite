from typing import NotRequired, TypedDict


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


class CommentResopnse(CommentBase):
    owner: User
    body: str


class CommentRow(CommentBase):
    user: int  # account_id
    site: str
