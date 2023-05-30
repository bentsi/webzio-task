from pathlib import Path
from typing import Optional

from bs4 import BeautifulSoup

from webzio_scraper.base import ForumScraperBase, DiscussionThread, ForumMessage, Author


class ForeterniaForumScraper(ForumScraperBase):

    def get_discussion_thread_messages(self, url) -> Optional[list[ForumMessage]]:
        html = self.browser.get_html(url)
        soup = BeautifulSoup(html)
        post_elements = soup.find_all(name="div", attrs={"class": "post-wrap"})
        messages = []
        for post_element in post_elements:
            messages.append(ForumMessage(
                message_text=post_element.find(attrs={"class": "wpforo-post-content"}).text,
                post_date=post_element.find(attrs={"class": "wpf-post-date"}).text,
                author=Author(
                    name=post_element.find(attrs={"class": "author-name"}).find(name="a").text,
                    joined_since=post_element.find(attrs={"class": "author-joined"}).text,
                    num_posts=post_element.find(attrs={"class": "author-posts"}).text,
                )
            ))
        return messages

    def get_discussion_threads(self) -> Optional[list[DiscussionThread]]:
        html = self.browser.get_html(self.url)
        soup = BeautifulSoup(html)
        threads_elements = soup.find_all(name="div", attrs={"class": "wpforo-topic"})
        discussion_threads = []
        for thread_element in threads_elements:
            title_element = thread_element.find(name="p", attrs={"class": "wpforo-topic-title"})
            link_element = title_element.find("a")
            discussion_url = link_element.get("href")
            discussion_threads.append(DiscussionThread(
                title=link_element.text,
                url=discussion_url,
                num_posts=int(thread_element.find(attrs={"class": "wpforo-topic-stat-posts"}).text),
                num_views=int(thread_element.find(attrs={"class": "wpforo-topic-stat-views"}).text),
            ))
        return discussion_threads
