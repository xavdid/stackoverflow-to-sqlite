from sqlite_utils import Database

from stackoverflow_to_sqlite.types import QuestionResponse, QuestionRow


def question_to_row(question: QuestionResponse) -> QuestionRow:
    return {
        **question,
        "tags": None,  # str(question["tags"]).strip("[]"),
        "comments": None,
        "accepted_answer_id": None,
        "owner": None,
        "has_accepted_answer": bool(question.get("accepted_answer_id")),
        "comment_count": len(question.get("comments", [])),
        "asker": question["owner"]["account_id"],
        "site": question["link"].strip("https://"),
    }


def remove_none(d: dict) -> dict:
    return {k: v for k, v in d.items() if v is not None}


def upsert_questions(db: Database, questions: list[QuestionResponse]):
    # insert_tags(db, list(itertools.chain(*[x.get("tags", []) for x in questions])))

    db["users"].insert(
        {
            "account_id": questions[0]["owner"]["account_id"],
            "name": questions[0]["owner"]["display_name"],
        },
        pk="account_id",
    )

    for q in questions:
        db["questions"].insert(
            remove_none(question_to_row(q)),
            pk="question_id",
            alter=True,
            foreign_keys=[("owner", "users", "account_id")],
            column_order=[
                "question_id",
                "link",
                "title",
                "tags",
                "body_markdown",
                "score",
            ],
        ).m2m("tags", [{"name": t} for t in q["tags"]], pk="name")

    db["questions"].enable_fts(["title", "body_markdown"])
