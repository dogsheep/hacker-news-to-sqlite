import pytest
import sqlite_utils
from click.testing import CliRunner
from hacker_news_to_sqlite import cli
import json


def test_import_user(tmpdir, requests_mock):
    db_path = str(tmpdir / "data.db")
    requests_mock.get(
        "https://hacker-news.firebaseio.com/v0/user/simonw.json",
        text=json.dumps(
            {
                "about": "JSK Fellow 2019. Creator of Datasette, co-creator of Django. Co-founder of Lanyrd, YC Winter 2011.",
                "created": 1193660603,
                "id": "simonw",
                "karma": 14637,
                "submitted": [22490556],
            }
        ),
    )
    requests_mock.get(
        "https://hacker-news.firebaseio.com/v0/item/22490556.json",
        text=json.dumps(
            {
                "by": "simonw",
                "id": 22490556,
                "kids": [
                    22491039,
                    22490633,
                    22491277,
                    22492319,
                    22490883,
                    22491996,
                    22502812,
                    22491049,
                    22491052,
                    22491001,
                    22490704,
                ],
                "parent": 22485489,
                "text": "The approach that has worked best for me is...",
                "time": 1583377246,
                "type": "comment",
            }
        ),
    )
    result = CliRunner().invoke(cli.cli, ["user", db_path, "simonw"])
    assert not result.exception, result.exception
    db = sqlite_utils.Database(db_path)
    assert {"users", "items"} == set(db.table_names())
    users = list(db["users"].rows)
    items = list(db["items"].rows)
    assert [
        {
            "id": "simonw",
            "created": 1193660603,
            "karma": 14637,
            "about": "JSK Fellow 2019. Creator of Datasette, co-creator of Django. Co-founder of Lanyrd, YC Winter 2011.",
        }
    ] == users
    assert [
        {
            "id": 22490556,
            "type": "comment",
            "by": "simonw",
            "time": 1583377246,
            "kids": "[22491039, 22490633, 22491277, 22492319, 22490883, 22491996, 22502812, 22491049, 22491052, 22491001, 22490704]",
            "parent": 22485489,
            "text": "The approach that has worked best for me is...",
        }
    ] == items
