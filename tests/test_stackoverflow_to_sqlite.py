from click.testing import CliRunner
from sqlite_utils import Database

from stackoverflow_to_sqlite.cli import cli


def test_version():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ["--version"])
        assert 0 == result.exit_code
        assert result.output.startswith("cli, version ")


def test_full_backup(
    questions_response, answers_response, tmp_db_path, tmp_db: Database
):
    result = CliRunner().invoke(cli, ["user", "123", "--db", tmp_db_path])
    assert result.exit_code == 0

    assert {
        "users",
        "tags",
        "questions",
        "questions_fts",
        "questions_tags",
        "answers",
        "answers_fts",
    } <= set(tmp_db.table_names())

    assert list(tmp_db["users"].rows) == [
        {
            "account_id": 2045145,
            "name": "xavdid",
            "network_profile_url": "https://stackexchange.com/users/2045145/",
        }
    ]
    assert list(tmp_db["questions"].rows) == [
        {
            "answer_count": 0,
            "user": 2045145,
            "body_markdown": "a questiona about security and things",
            "closed_date": 1448182440,
            "closed_reason": "Duplicate",
            "comment_count": 4,
            "creation_date": 1381383787,
            "down_vote_count": 0,
            "favorite_count": 0,
            "has_accepted_answer": 0,
            "last_activity_date": 1381383787,
            "link": "https://stackoverflow.com/questions/19287918/implementing-an-xss-attack",
            "question_id": 19287918,
            "score": 0,
            "is_considered_answered": 0,
            "site": "stackoverflow.com",
            "title": "Implementing an XSS attack",
            "up_vote_count": 0,
            "view_count": 149,
        },
        {
            "answer_count": 1,
            "user": 2045145,
            "body_markdown": "a very cool elixir question and stuff",
            "closed_date": None,
            "closed_reason": None,
            "comment_count": 1,
            "creation_date": 1698219631,
            "down_vote_count": 0,
            "favorite_count": 0,
            "is_considered_answered": 1,
            "has_accepted_answer": 1,
            "last_activity_date": 1698233092,
            "link": "https://stackoverflow.com/questions/77357478/is-it-possible-to-define-case-clauses-with-an-elixir-macro",
            "question_id": 77357478,
            "score": 0,
            "site": "stackoverflow.com",
            "title": "Is it possible to define `case` clauses with an elixir macro?",
            "up_vote_count": 0,
            "view_count": 104,
        },
    ]

    assert list(tmp_db["answers"].rows) == [
        {
            "answer_id": 70934214,
            "body_markdown": "This is possible!",
            "comment_count": 4,
            "creation_date": 1643673277,
            "down_vote_count": 0,
            "is_accepted": 1,
            "last_edit_date": None,
            "link": "https://stackoverflow.com/questions/70901751/find-replace-data-in-a-csv-using-python-on-zapier/70934214#70934214",
            "question_title": "Find &amp; replace data in a CSV using Python on Zapier",
            "score": 0,
            "site": "stackoverflow.com",
            "up_vote_count": 0,
            "user": 2045145,
        },
        {
            "answer_id": 70934215,
            "body_markdown": "In javascript, variables",
            "comment_count": 2,
            "creation_date": 1643666093,
            "down_vote_count": 0,
            "is_accepted": 0,
            "last_edit_date": 1643666193,
            "link": "https://stackoverflow.com/questions/70598105/zapier-javascript-find-replace-special-characters/70933266#70933266",
            "question_title": "Zapier Javascript Find/Replace Special Characters",
            "score": 0,
            "site": "stackoverflow.com",
            "up_vote_count": 0,
            "user": 2045145,
        },
    ]

    # validate that the FK was set up correctly
    assert (
        "[user] INTEGER REFERENCES [users]([account_id])" in tmp_db["questions"].schema
    )
    assert "[user] INTEGER REFERENCES [users]([account_id])" in tmp_db["answers"].schema

    assert list(tmp_db["tags"].rows) == [
        {
            "name": "macros",
        },
        {
            "name": "elixir",
        },
        {
            "name": "javascript",
        },
        {
            "name": "jquery",
        },
        {
            "name": "iframe",
        },
        {
            "name": "xss",
        },
    ]

    assert list(tmp_db["questions_tags"].rows) == [
        {
            "questions_id": 77357478,
            "tags_id": "macros",
        },
        {
            "questions_id": 77357478,
            "tags_id": "elixir",
        },
        {
            "questions_id": 19287918,
            "tags_id": "javascript",
        },
        {
            "questions_id": 19287918,
            "tags_id": "jquery",
        },
        {
            "questions_id": 19287918,
            "tags_id": "iframe",
        },
        {
            "questions_id": 19287918,
            "tags_id": "xss",
        },
    ]


# TODO: live test to make sure my filter is still working as expected
