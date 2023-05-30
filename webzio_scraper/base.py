import json
from abc import ABCMeta, abstractmethod
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional

from webzio_scraper.browser import ChromeBrowser


@dataclass
class Author:
    name: str
    joined_since: str
    num_posts: int


@dataclass
class ForumMessage:
    message_text: str
    post_date: str
    author: Author


@dataclass
class DiscussionThread:
    title: str
    url: str
    num_posts: int
    num_views: int
    messages: list[ForumMessage] = field(default_factory=list)


class ForumScraperBase(metaclass=ABCMeta):

    def __init__(self, url):
        self.url = url
        self.browser = ChromeBrowser()
        self.discussion_threads = None
        self.parallelization = 2  # num of threads to scrape in parallel

    @abstractmethod
    def get_discussion_thread_messages(self, url: str) -> Optional[list[ForumMessage]]:
        ...

    @abstractmethod
    def get_discussion_threads(self) -> Optional[list[DiscussionThread]]:
        ...

    def scrape(self):
        self.discussion_threads = self.get_discussion_threads()
        with ThreadPoolExecutor(max_workers=self.parallelization) as executor:
            tasks = []
            for discussion_thread in self.discussion_threads:
                tasks.append((discussion_thread,
                              executor.submit(self.get_discussion_thread_messages, url=discussion_thread.url)))
            for discussion_thread, get_thread_messages_result in tasks:
                discussion_thread.messages = get_thread_messages_result.result(timeout=15)

    def save_discussion_threads_as_json(self, path_to_json_file: Path):
        discussion_threads = [asdict(discussion_thread) for discussion_thread in self.discussion_threads]
        with path_to_json_file.open("w") as json_file:
            json.dump(obj=discussion_threads, fp=json_file)
