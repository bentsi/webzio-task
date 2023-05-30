import requests
from abc import abstractmethod, ABCMeta


class BrowserBase(metaclass=ABCMeta):

    @abstractmethod
    def headers(self) -> str:
        ...

    def get_html(self, url: str) -> str:
        response = requests.get(url, headers=self.headers())
        response.raise_for_status()
        return response.text


class ChromeBrowser(BrowserBase):

    def headers(self) -> dict:
        return {
            "User-Agent": "Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) "
                          "CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1"
        }

