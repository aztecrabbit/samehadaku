import requests
from .utils.utils import utils
from bs4 import BeautifulSoup


class samehadaku(object):
    def __init__(self):
        super(samehadaku, self).__init__()

        self.requests = requests.Session()
        self.libutils = utils(__file__)
        self.post_link = {}
        self.post_link_id = 1
        self.download_link = {}
        self.page = 1
        self.page_paginate = 2

    def log(self, value, color='[G1]', type=1):
        self.liblog.log(value, color=color, type=type)

    def rotate_list(self, data: list) -> (str, int):
        data.append(data.pop(0))

        return data[-1]

    def request(self, method, url, **kwargs):
        while True:
            try:
                return self.requests.request(method, url, timeout=(10, 30), **kwargs)
            except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
                self.liblog.sleep(7, value_resumming=None, color='[R1]')

    def get_post_list(self):
        for i in range(self.page_paginate):
            self.log(f"Requesting Page {self.page}")
            url = 'https://samehadaku.tv' + ('' if self.page == 1 else f"/page/{self.page}")
            response = self.request('GET', url)
            # response = open(self.libutils.real_path('/samehadaku.html')).read()
            response = BeautifulSoup(response.text, 'html.parser')
            for item_post in response.select('div.updateanime>ul>li>.dtl'):
                self.post_link[str(self.post_link_id)] = item_post.h2.a.get('href')
                item_post_title, _, item_post_episode = item_post.h2.a.get('title').rpartition(' Episode ')
                self.log(
                    f"[Y1]Episode{item_post_episode:.>10}[CC] "
                    f"[P1]{self.post_link_id:>3}[CC] "
                    f"[G1]{item_post_title}[CC]"
                )
                self.post_link_id = self.post_link_id + 1
            self.page = self.page + 1

    def view_post(self, post_link_id: str, colors: list = ['[G1]', '[G2]'], i: int = 0):
        if not self.post_link.get(post_link_id, False):
            self.log(f"Post {post_link_id} not found!", color='[R1]')
            return
        self.log(f"Requesting Post {post_link_id}")
        response = self.request('GET', self.post_link.get(post_link_id))
        # response = open(self.libutils.real_path('/samehadaku-post-view.html')).read()
        response = BeautifulSoup(response.text, 'html.parser')
        for item_format in response.select('.download-eps>ul>li'):
            item_format_text = item_format.strong.text.strip()
            item_format_link_values = [f"{item_format_text:>6}"]
            for item_format_link in item_format.select('span>a'):
                if not item_format_link.get('href', False):
                    self.log(item_format_link, color='[R1]')
                download_link_id = f"{post_link_id}:{i}"
                self.download_link[download_link_id] = item_format_link['href']
                item_format_link_values.append(
                    '{:.<3}{:.>10}'.format(item_format_link.text, f"({download_link_id})")
                )
                i = i + 1

            self.log(" | ".join(item_format_link_values), color=self.rotate_list(colors))
