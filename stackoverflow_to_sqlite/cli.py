import click
from sqlite_utils import Database

from stackoverflow_to_sqlite.sqlite_helpers import upsert_questions
from stackoverflow_to_sqlite.stack_exchange_api import fetch_questions

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

    click.echo("\nfetching comments")
    questions = fetch_questions(user_id, "stackoverflow.com")
    upsert_questions(db, questions)
    print("Wrote to db!")
    # print(questions)
    # save_comments(db, comments)
    # click.echo(f"saved/updated {len(comments)} comments")

    # click.echo("\nfetching (up to 10 pages of) posts")
    # posts = load_posts_for_user(username)
    # save_posts(db, posts)
    # click.echo(f"saved/updated {len(posts)} posts")

    # if not (comments or posts):
    #     raise click.ClickException(f"no data found for username: {username}")

    # ensure_fts(db)
