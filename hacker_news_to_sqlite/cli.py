import click
import requests
import sqlite_utils
import tqdm


@click.group()
@click.version_option()
def cli():
    "Save data from Hacker News to a SQLite database"


@cli.command()
@click.argument(
    "db_path",
    type=click.Path(file_okay=True, dir_okay=False, allow_dash=False),
    required=True,
)
@click.argument("username")
def user(db_path, username):
    "Fetch all content submitted by this user"
    db = sqlite_utils.Database(db_path)
    user = requests.get(
        "https://hacker-news.firebaseio.com/v0/user/{}.json".format(username)
    ).json()
    submitted = user.pop("submitted", None) or []
    with db.conn:
        db["users"].upsert(
            user, column_order=("id", "created", "karma", "about"), pk="id"
        )
    # Only do IDs we have not yet fetched
    done = set()
    if db["items"].exists():
        done = set(
            r[0]
            for r in db.conn.execute(
                "select id from items where id in ({})".format(
                    ", ".join(map(str, submitted))
                )
            ).fetchall()
        )
    to_do = [id for id in submitted if id not in done]
    for id in tqdm.tqdm(to_do, desc="Importing items"):
        item = requests.get(
            "https://hacker-news.firebaseio.com/v0/item/{}.json".format(id)
        ).json()
        with db.conn:
            db["items"].upsert(
                item, column_order=("id", "type", "by", "time"), pk="id", alter=True
            )


@cli.command()
@click.argument(
    "db_path",
    type=click.Path(file_okay=True, dir_okay=False, allow_dash=False),
    required=True,
)
@click.argument("item_ids", type=int, nargs=-1)
def trees(db_path, item_ids):
    "Retrieve all content from the trees of which any item_id is a member"
    db = sqlite_utils.Database(db_path)
    to_fetch = set(item_ids)
    done_count = 0
    while to_fetch:
        id = to_fetch.pop()
        try:
            db["items"].get(id)
            continue
        except sqlite_utils.db.NotFoundError:
            pass
        item_url = "https://hacker-news.firebaseio.com/v0/item/{}.json".format(id)
        item = requests.get(item_url).json()
        done_count += 1
        if item is None:
            continue
        with db.conn:
            db["items"].upsert(
                item, column_order=("id", "type", "by", "time"), pk="id", alter=True
            )
            print("done: {}, todo: {}".format(done_count, len(to_fetch)))
        # Anything else we should fetch?
        if (
            "parent" in item
            and not db.conn.execute(
                "select id from items where id = ?", [item["parent"]]
            ).fetchall()
        ):
            to_fetch.add(item["parent"])
        if "kids" in item:
            # Which of these need to be fetched?
            already_saved = [
                r[0]
                for r in db.conn.execute(
                    """
                select id from items where id in ({})
            """.format(
                        ", ".join(map(str, item["kids"]))
                    )
                )
            ]
            to_fetch.update(k for k in item["kids"] if k not in already_saved)
    # Set up foreign key
    try:
        db["items"].add_foreign_key("parent", "items", "id")
    except sqlite_utils.db.AlterError:
        pass  # Foreign key already exists
