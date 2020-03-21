# hacker-news-to-sqlite

[![PyPI](https://img.shields.io/pypi/v/hacker-news-to-sqlite.svg)](https://pypi.org/project/hacker-news-to-sqlite/)
[![CircleCI](https://circleci.com/gh/dogsheep/hacker-news-to-sqlite.svg?style=svg)](https://circleci.com/gh/dogsheep/hacker-news-to-sqlite)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/dogsheep/hacker-news-to-sqlite/blob/master/LICENSE)

Create a SQLite database containing data fetced from [Hacker News](https://news.ycombinator.com/).

## How to install

    $ pip install hacker-news-to-sqlite

## Usage

    $ hacker-news-to-sqlite user hacker-news.db your-username
    Importing items:  37%|███████████                        | 845/2297 [05:09<11:02,  2.19it/s]

Imports all of your Hacker News submissions and comments into a SQLite database called `hacker-news.db`.

    $ hacker-news-to-sqlite trees hacker-news.db 22640038 22643218

Fetches the entire comments tree in which any of those content IDs appears.
