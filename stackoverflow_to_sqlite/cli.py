import click
from sqlite_utils import Database

from stackoverflow_to_sqlite.sqlite_helpers import (
    ensure_fts,
    upsert_answers,
    upsert_comments,
    upsert_questions,
)
from stackoverflow_to_sqlite.stack_exchange_api import (
    fetch_answers,
    fetch_comments,
    fetch_questions,
)

DEFAULT_DB_NAME = "stack-exchange.db"
DB_PATH_HELP = "A path to a SQLite database file. If it doesn't exist, it will be created. While it can have any extension, `.db` or `.sqlite` is recommended."


@click.group()
@click.version_option()
def cli():
    "Save all the contributions for a StackOverflow user to a SQLite database. Optionally include their authored content from across the StackExchange network"


@cli.command()
@click.argument("user_id")
@click.option(
    "--db",
    "db_path",
    type=click.Path(file_okay=True, dir_okay=False, allow_dash=False),
    default=DEFAULT_DB_NAME,
    help=DB_PATH_HELP,
)
# TODO: no network / include network?
# TODO: custom filter? will have to ingest nicely
# TODO: full refresh? don't bail early (by default I'm going to stop fetching pages once I see an item created more than N days ago)
def user(db_path: str, user_id: str):
    # username = clean_username(username)
    click.echo(f"loading data about StackOverflow user_id: {user_id} into {db_path}")

    db = Database(db_path)

    click.echo("\nfetching questions", nl=False)
    questions = fetch_questions(user_id, "stackoverflow.com")
    click.echo("  writing questions")
    upsert_questions(db, questions)
    click.echo(f"  done! Archived {len(questions)} questions")

    click.echo("\nfetching answers", nl=False)
    answers = fetch_answers(user_id, "stackoverflow.com")
    click.echo("  writing answers")
    upsert_answers(db, answers)
    click.echo(f"  done! Archived {len(answers)} answers")

    click.echo("\nfetching comments", nl=False)
    comments = fetch_comments(user_id, "stackoverflow.com")
    click.echo("  writing comments")
    upsert_comments(db, comments)
    click.echo(f"  done! Archived {len(comments)} comments")

    if not (questions or answers or comments):
        raise click.ClickException(
            f"no data found for StackOverflow user_id: {user_id}"
        )

    ensure_fts(db)

    click.echo("\nDone!")
