import requests
from .utils.utils import utils
from bs4 import BeautifulSoup

class samehadaku(object):
    def __init__(self):
        super(samehadaku, self).__init__()

        self.requests = requests.Session()
        self.libutils = utils(__file__)
        self.postlink = {}
        self.postlink_id = 1
        self.download_link = {}
        self.page = 0
        self.page_next = 1
        self.page_show = 2

    def log(self, value, color='[G1]', type=1):
        self.liblog.log(value, color=color, type=type)

    def post_list(self):
        self.page_end = self.page + self.page_show
        while self.page < self.page_end:
            self.page = self.page_next

            self.log(f'Requesting page {self.page}')
            response = self.requests.get('https://samehadaku.tv' + ('' if self.page == 1 else f'/page/{self.page}/'))
            #response = open(self.libutils.real_path('/samehadaku.html')).read()
            response = BeautifulSoup(response.text, 'html.parser')
            for element in response.select('div.updateanime>ul>li>.dtl'):
                self.postlink[str(self.postlink_id)] = element.h2.a.get('href')
                title, _, episode = element.h2.a.get('title').rpartition(' Episode ')
                episode = f'Episode.{episode:.>9}'

                self.log(f'[Y1]{episode}[CC] [P1]{self.postlink_id:>3}[CC] [G1]{title}')
                self.postlink_id += 1

            self.page_next = int(response.find('div', class_='pagination').find('a', class_='next page-numbers').get('href').split('/')[-2])
    
    def post_view(self, postlink_id, i=1):
        postlink = self.postlink.get(postlink_id)
        if not postlink:
            self.log('Postlink not found!')
            return
        response = self.requests.get(postlink)
        # response = open(self.libutils.real_path('/samehadaku-post-view.html')).read()
        response = BeautifulSoup(response.text, 'html.parser')
        colors = ['[G1]','[G2]','[G2]']
        for li in response.select('.download-eps>ul>li'):
            try:
                text = f'{li.strong.text.strip():>6}'
                for a in li.select('span>a'):
                    self.download_link[f'{postlink_id}{i}'] = a.get('href')
                    text += ' | {:.<3}{:.>10}'.format(a.text, f'({postlink_id}{i})')
                    i += 1
                color = colors.pop(0)
                colors.append(color)
                self.log(text, color=color)
            except Exception as exception:
                self.log(exception, color='[R1]')

