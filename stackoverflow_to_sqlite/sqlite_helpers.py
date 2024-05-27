from urllib.parse import urlparse

from sqlite_utils import Database

from stackoverflow_to_sqlite.types import (
    AnswerResponse,
    AnswerRow,
    QuestionResponse,
    QuestionRow,
)


def question_to_row(question: QuestionResponse) -> QuestionRow:
    return {
        **question,
        "tags": None,  # str(question["tags"]).strip("[]"),
        "owner": None,
        "user": question["owner"]["account_id"],
        "accepted_answer_id": None,
        "has_accepted_answer": bool(question.get("accepted_answer_id")),
        "is_answered": None,
        "is_considered_answered": question["is_answered"],
        "site": urlparse(question["link"]).hostname or "INVALID",
    }


def answer_to_row(answer: AnswerResponse) -> AnswerRow:
    return {
        **answer,
        "owner": None,
        "user": answer["owner"]["account_id"],
        "site": urlparse(answer["link"]).hostname or "INVALID",
        "title": None,
        "question_title": answer["title"],
        "tags": None,
    }


def remove_none(d: dict) -> dict:
    return {k: v for k, v in d.items() if v is not None}


def upsert_questions(db: Database, questions: list[QuestionResponse]):
    # insert_tags(db, list(itertools.chain(*[x.get("tags", []) for x in questions])))

    # TODO: split users out
    # I want to insert(ignore=True) here, but
    # https://github.com/simonw/sqlite-utils/issues/554
    db["users"].upsert(
        {
            "account_id": (aid := questions[0]["owner"]["account_id"]),
            # just `name` because it shows up nicer in datasette that way
            "name": questions[0]["owner"]["display_name"],
            "network_profile_url": f"https://stackexchange.com/users/{aid}/",
        },
        pk="account_id",
        # ignore=True,  # ignore existing users
    )

    for q in questions:
        db["questions"].insert(
            remove_none(question_to_row(q)),
            pk="question_id",
            alter=True,
            foreign_keys=[("user", "users", "account_id")],
            column_order=[
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
        ).m2m("tags", [{"name": t} for t in q["tags"]], pk="name")


def upsert_answers(db: Database, answers: list[AnswerResponse]):
    # insert_tags(db, list(itertools.chain(*[x.get("tags", []) for x in questions])))

    # in case a user has no questions, only answers
    # I want to insert(ignore=True) here, but
    # https://github.com/simonw/sqlite-utils/issues/554
    db["users"].upsert(
        {
            "account_id": (aid := answers[0]["owner"]["account_id"]),
            # just `name` because it shows up nicer in datasette that way
            "name": answers[0]["owner"]["display_name"],
            "network_profile_url": f"https://stackexchange.com/users/{aid}/",
        },
        pk="account_id",
        # ignore=True,  # ignore existing users
    )

    for a in answers:
        db["answers"].insert(
            remove_none(answer_to_row(a)),
            pk="answer_id",
            alter=True,
            foreign_keys=[("user", "users", "account_id")],
            column_order=[
                "answer_id",
                "link",
                "question_title",
                "score",
                "body_markdown",
            ],
        )
        # TODO m2m here, but the API doesn't seem to return the question's tag(s) for an answer


FTS_INSTRUCTIONS: list[tuple[str, list[str]]] = [
    ("questions", ["title", "body_markdown"]),
    ("answers", ["question_title", "body_markdown"]),
    # ("comments", ["text", "text"]),
]


def ensure_fts(db: Database):
    table_names = set(db.table_names())
    for table, columns in FTS_INSTRUCTIONS:
        if table in table_names and f"{table}_fts" not in table_names:
            db[table].enable_fts(columns, create_triggers=True)
