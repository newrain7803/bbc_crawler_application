import scrapy
import json
from dateutil.parser import parse
from pymongo import MongoClient

class ArticleSpider(scrapy.Spider):
    name = "articles"

    start_urls = [
        'https://www.bbc.com/news',
    ]

    urls = []
    articles = {}
    num = 0

    client = MongoClient(
        host = '192.168.111.139',
        username = 'root',
        password = 'tlsdbstjr1+',
        port = 27017,
        authSource = 'admin',
    )

    collection = client['news'].articles_final1

    def parse(self, response):
        for article in response.css('a.gs-c-promo-heading'):
            article_url = article.css('::attr(href)').get()

            if article_url.find('https://www.bbc') == -1:
                article_url = 'https://www.bbc.com' + article_url
            self.urls.append(article_url)

        self.urls = list(dict.fromkeys(self.urls))

        for url in self.urls:
            if url is not None:
                yield scrapy.Request(url = url, callback = self.parse_articles)


    def parse_articles(self, response):
        content_s = ""
        if '/news/' in response.request.url:
            if response.css('div.story-body'):
                for i in response.css('div.story-body__inner p::text').getall():
                    content_s += i

                author = 'Unknown' if response.css('span.byline__name::text').get() is None else response.css('span.byline__name::text').get()

                self.articles.update({
                    str(self.num) : {
                        'url' : response.request.url,
                        'author' : author,
                        'title' : response.css('h1.story-body__h1::text').get(),
                        'title_s' : response.css('h1.story-body__h1::text').get().lower(),
                        'date' : response.css('div.date::text').get(),
                        'date_s' : parse(response.css('div.date::text').get()).strftime('%Y-%m-%d'),
                        'content_r' : response.css('div.story-body__inner').get(),
                        'content_s' : content_s
                    }
                })
                self.num += 1
        elif '/sport/' in response.request.url:
            if response.css('article.component'):
                for i in response.css('div.sp-story-body p::text').getall():
                    content_s += i

                author = 'Unknown' if response.css('p.gel-long-primer::text').get() is None or response.css('p.gel-long-primer::text').get() == ' ' else response.css('p.gel-long-primer::text').get()

                self.articles.update({
                    str(self.num) : {
                        'url' : response.request.url,
                        'author' : author,
                        'title' : response.css('h1.story-headline::text').get(),
                        'title_s' : response.css('h1.story-headline::text').get().lower(),
                        'date' : response.css('abbr.abbr-on span::text').get(),
                        'date_s' : parse(response.css('abbr.abbr-on span::text').get()).strftime('%Y-%m-%d'),
                        'content_r' : response.css('div.sp-story-body').get(),
                        'content_s' : content_s
                    }
                })
                self.num += 1
        elif '/future/' in response.request.url or '/worklife/' in response.request.url:
            if response.css('article.article_main'):
                content_r = ""
                for i, j in zip(response.css('div.body-text-card__text p::text').getall(), response.css('div.body-text').getall()):
                    content_s += i
                    content_r += j

                author = 'Unknown' if response.css('p.gel-long-primer::text').get() is None else response.css('p.gel-long-primer::text').get()

                self.articles.update({
                    str(self.num) : {
                        'url' : response.request.url,
                        'author' : author,
                        'title' : response.css('h1.story-headline::text').get(),
                        'title_s' : response.css('h1.story-headline::text').get().lower(),
                        'date' : response.css('abbr.abbr-on span::text').get(),
                        'date_s' : parse(response.css('abbr.abbr-on span::text').get()).strftime('%Y-%m-%d'),
                        'content_r' : response.css('div.body-text-card').getall(),
                        'content_s' : content_s
                    }
                })
                self.num += 1
        elif '/travel/' in response.request.url or '/culture/' in response.request.url:
            if response.css('div#story-content'):
                for i in response.css('div.body-content p').getall():
                    content_s += i

                author = 'Unknown' if response.css('span.index-body::text').get() is None else response.css('span.index-body::text').get()
                try:
                    _date = response.css('span.publication-date::text')[1].get()
                except IndexError as e:
                    _date = response.css('span.publication-date::text').get()

                self.articles.update({
                    str(self.num) : {
                        'url' : response.request.url,
                        'author' : author,
                        'title' : response.css('h1.primary-heading::text').get(),
                        'title_s' : response.css('h1.primary-heading::text').get().lower(),
                        'date' : _date,
                        'date_s' : parse(_date).strftime('%Y-%m-%d'),
                        'content_r' : response.css('div.body-content').get(),
                        'content_s' : content_s
                    }
                })
                self.num += 1
        else:
            # url이 /news/extra/~ or /news/live/~ or /sound/~ ...
            pass



    def closed(self, reason):
        for i in range(len(self.articles)):
            self.collection.insert(dict(self.articles[str(i)]))
        self.client.close()