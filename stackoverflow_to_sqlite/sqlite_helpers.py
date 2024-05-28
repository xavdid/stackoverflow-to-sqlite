from typing import Callable, Literal, TypeVar

from sqlite_utils import Database

from stackoverflow_to_sqlite.types import (
    AnswerResponse,
    AnswerRow,
    CommentResopnse,
    CommentRow,
    QuestionResponse,
    QuestionRow,
    User,
    answer_to_row,
    comment_to_row,
    question_to_row,
    user_to_row,
)


def upsert_user(db: Database, user: User):
    # I want to insert(ignore=True) here, but
    # https://github.com/simonw/sqlite-utils/issues/554
    db["users"].upsert(  # type: ignore
        user_to_row(user),
        pk="account_id",  # type: ignore
    )


ResponseTypes = TypeVar(
    "ResponseTypes", QuestionResponse, AnswerResponse, CommentResopnse
)
RowTypes = TypeVar("RowTypes", QuestionRow, AnswerRow, CommentRow)


def _upsert_objects(
    db: Database,
    object_name: Literal["question", "answer", "comment"],
    objects: list[ResponseTypes],
    transformer: Callable[[ResponseTypes], RowTypes],
    column_order: list[str],
    include_tags=False,
):
    if objects:
        upsert_user(db, objects[0]["owner"])

    for o in objects:
        to_save = transformer(o)

        # don't really want to upsert
        t = db[f"{object_name}s"].upsert(  # type: ignore
            to_save,  # type:ignore
            pk=f"{object_name}_id",  # type: ignore
            alter=True,  # type:ignore
            foreign_keys=[("user", "users", "account_id")],  # type: ignore
            column_order=column_order,  # type:ignore
        )
        if include_tags and "tags" in o:
            t.m2m("tags", [{"name": t} for t in o["tags"]], pk="name")


def upsert_questions(db: Database, questions: list[QuestionResponse]):
    _upsert_objects(
        db,
        "question",
        questions,
        question_to_row,
        [
            "question_id",
            "link",
            "tags",
            "title",
            "score",
            "body_markdown",
            "answer_count",
            "has_accepted_answer",
            "is_considered_answered",
            "comment_count",
        ],
        include_tags=True,
    )


def upsert_answers(db: Database, answers: list[AnswerResponse]):
    _upsert_objects(
        db,
        "answer",
        answers,
        answer_to_row,
        [
            "answer_id",
            "link",
            "question_title",
            "score",
            "body_markdown",
        ],
        # would like to m2m here, but the API doesn't seem to return the question's tag(s) for an answer
        # see: https://stackapps.com/questions/7213/the-answer-object-returns-an-empty-array-for-tags
    )


def upsert_comments(db: Database, comments: list[CommentResopnse]):
    _upsert_objects(
        db,
        "comment",
        comments,
        comment_to_row,
        [
            "comment_id",
            "link",
            "score",
            "body_markdown",
        ],
    )


FTS_INSTRUCTIONS: list[tuple[str, list[str]]] = [
    ("questions", ["title", "body_markdown"]),
    ("answers", ["question_title", "body_markdown"]),
    ("comments", ["body_markdown"]),
]


def ensure_fts(db: Database):
    table_names = set(db.table_names())
    for table, columns in FTS_INSTRUCTIONS:
        if table in table_names and f"{table}_fts" not in table_names:
            db[table].enable_fts(columns, create_triggers=True)
