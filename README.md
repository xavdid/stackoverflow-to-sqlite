# stackoverflow-to-sqlite

Downloads all your contributions to StackOverflow into a searchable, sortable, sqlite database. This includes your questions, answers, and comments.

## Install

The best way to install the package is by using [pipx](https://pypa.github.io/pipx/):

```bash
pipx install stackoverflow-to-sqlite
```

It's also available via [brew](https://brew.sh/):

```bash
brew install xavdid/projects/stackoverflow-to-sqlite
```

## Usage

```
Usage: stackoverflow-to-sqlite [OPTIONS] USER_ID

  Save all the contributions for a StackOverflow user to a SQLite database.

Options:
  --version  Show the version and exit.
  --db FILE  A path to a SQLite database file. If it doesn't exist, it will be
             created. While it can have any extension, `.db` or `.sqlite` is
             recommended.
  --help     Show this message and exit.
```

The CLI takes a single required argument: a StackOverflow user id. The easiest way to get this is from a user's profile page:

![](https://cdn.zappy.app/3564b18ce469812a367422b8e8eed1ab.png)

The simplest usage is to pass that directly to the CLI and use the default database location:

```shell
% stackoverflow-to-sqlite 1825390
```

## Viewing Data

The resulting SQLite database pairs well with [Datasette](https://datasette.io/), a tool for viewing SQLite in the web. Below is my recommended configuration.

First, install `datasette`:

```bash
pipx install datasette
```

Then, add the recommended plugins (for rendering timestamps and markdown):

```bash
pipx inject datasette datasette-render-markdown datasette-render-timestamps
```

Finally, create a `metadata.json` file next to your `stackoverflow.db` with the following:

```json
{
  "databases": {
    "stackoverflow": {
      "tables": {
        "questions": {
          "sort_desc": "creation_date",
          "plugins": {
            "datasette-render-markdown": {
              "columns": ["body_markdown"]
            },
            "datasette-render-timestamps": {
              "columns": ["creation_date", "closed_date", "last_activity_date"]
            }
          }
        },
        "answers": {
          "sort_desc": "creation_date",
          "plugins": {
            "datasette-render-markdown": {
              "columns": ["body_markdown"]
            },
            "datasette-render-timestamps": {
              "columns": ["last_edit_date", "creation_date"]
            }
          }
        },
        "comments": {
          "sort_desc": "creation_date",
          "plugins": {
            "datasette-render-markdown": {
              "columns": ["body_markdown"]
            },
            "datasette-render-timestamps": {
              "columns": ["creation_date"]
            }
          }
        },
        "tags": {
          "sort": "name"
        }
      }
    }
  }
}
```

Now when you run

```bash
datasette serve stackoverflow.db --metadata metadata.json
```

You'll get a nice, formatted output!

## Motivation

I got nervous when I saw Reddit's [notification of upcoming API changes](https://old.reddit.com/r/reddit/comments/12qwagm/an_update_regarding_reddits_api/). To ensure I could always access data I created, I wanted to make sure I had a backup in place before anything changed in a big way.

## FAQs

### Why are users stored under an "account_id" instead of their user id?

At some point, I'd like to crawl the entire Stack Exchange network. An account id is shared across all sites while a user id is specific to each site. So I'm using the former as the primary key to better represent that.

### Why are my longer contributions truncated in Datasette?

Datasette truncates long text fields by default. You can disable this behavior by using the `truncate_cells_html` flag when running `datasette` ([see the docs](https://docs.datasette.io/en/stable/settings.html#truncate-cells-html)):

```shell
datasette reddit.db --setting truncate_cells_html 0
```

### Does this tool refetch old data?

Yes, currently it does a full backup every time the command is run. It technically does upserts on every row, so it'll update existing rows with new data.

I'd like to stop saving items once we've seen an item we've saved already, but doing it that way hasn't been a priority.

## Development

This section is people making changes to this package.

When in a virtual environment, run the following:

```bash
just install
```

This installs the package in `--edit` mode and makes its dependencies available. You can now run `stackoverflow-to-sqlite` to invoke the CLI.

### Running Tests

In your virtual environment, a simple `just test` should run the unit test suite. You can also run `just typecheck` for type checking.

### Releasing New Versions

> these notes are mostly for myself (or other contributors)

1. Run `just release` while your venv is active
2. paste the stored API key (If you're getting invalid password, verify that `~/.pypirc` is empty)
