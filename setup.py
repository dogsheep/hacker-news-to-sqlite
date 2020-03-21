from setuptools import setup
import os

VERSION = "0.3"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="hacker-news-to-sqlite",
    description="Create a SQLite database containing data pulled from Hacker News",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Simon Willison",
    url="https://github.com/dogsheep/hacker-news-to-sqlite",
    license="Apache License, Version 2.0",
    version=VERSION,
    packages=["hacker_news_to_sqlite"],
    entry_points="""
        [console_scripts]
        hacker-news-to-sqlite=hacker_news_to_sqlite.cli:cli
    """,
    install_requires=["sqlite-utils", "click", "requests", "tqdm"],
    extras_require={"test": ["pytest", "requests-mock"]},
    tests_require=["hacker-news-to-sqlite[test]"],
)
