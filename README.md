# Forum Scraper
## Scrape threads and messages from different forums
Currently supported
- For Eternia

## Installation
### Install poetry
```
curl -sSL https://install.python-poetry.org | python
```
### Install dependencies
```
poetry install
```

## Example:
```
./scrape_forums.py foreternia --path-to-json /tmp/foreternia.json
```