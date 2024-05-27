from typing import NotRequired, TypedDict


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


class UserRow(TypedDict):
    account_id: int
    name: str
    stack_overflow_id: int | None
    network_profile_url: str


class QuestionResponse(TypedDict):
    tags: list[str]
    comment_count: int
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
    has_accepted_answer: bool
    accepted_answer_id: None
    is_considered_answered: bool
    is_answered: None
    owner: None
    user: int  # account_id
    site: str


class AnswerResponse(TypedDict):
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
    owner: User
    title: str
    # shows up, but is always empty
    # see: https://stackapps.com/questions/7213/the-answer-object-returns-an-empty-array-for-tags
    # I could do a second request for only the answer tags, but that's annoying
    tags: list[str]


class AnswerRow(AnswerResponse):
    owner: None
    user: int  # account_id
    site: str
    title: None
    question_title: str
    tags: None


class CommentResopnse(TypedDict):
    score: int
    post_type: str
    body_markdown: str
    post_id: int
    comment_id: int
    link: str
    owner: User
    body: str


class CommentRow(CommentResopnse):
    owner: None
    user: int  # account_id
    body: None
    site: str
