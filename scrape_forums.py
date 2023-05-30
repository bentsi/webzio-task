#!/bin/env python
import typer
from pathlib import Path

from webzio_scraper.foreternia import ForeterniaForumScraper

app = typer.Typer()


@app.command()
def version():
    with open("VERSION") as version_file:
        print(version_file.read())


@app.command()
def foreternia(path_to_json: Path = Path("./foreternia.json")):
    ffs = ForeterniaForumScraper(url="https://foreternia.com/community/announcement-forum")
    ffs.scrape()
    ffs.save_discussion_threads_as_json(path_to_json_file=path_to_json)


if __name__ == '__main__':
    app()
