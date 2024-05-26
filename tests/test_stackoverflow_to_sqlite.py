from click.testing import CliRunner
from sqlite_utils import Database

from stackoverflow_to_sqlite.cli import cli


def test_version():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ["--version"])
        assert 0 == result.exit_code
        assert result.output.startswith("cli, version ")


def test_full_backup(questions_response, tmp_db_path, tmp_db: Database):
    result = CliRunner().invoke(cli, ["user", "123", "--db", tmp_db_path])
    assert result.exit_code == 0
    # TODO: assertions
