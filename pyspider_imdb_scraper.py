from pyspider.libs.base_handler import *


class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('https://www.imdb.com/', callback=self.index_page,validate_cert=False)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('a[href^="http"]').items():
            if "coming-soon" in each.attr.href:
                self.crawl(each.attr.href, callback=self.detail_page,validate_cert=False)

    @config(priority=2)
    def detail_page(self, response):
        coming_movies_list = []
        for i in response.doc('.overview-top h4 a'):
            coming_movies_dict = {}
            coming_movies_dict["movie_name"] = i.text.split("(")[0]
            coming_movies_dict["year"] = i.text.split("(")[1].strip(")")
            coming_movies_dict["url"]  = response.url
            coming_movies_list.append(coming_movies_dict)
           
        return coming_movies_list
