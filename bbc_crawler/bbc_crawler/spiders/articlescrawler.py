import scrapy
import json


class ArticleSpider(scrapy.Spider):
    name = "articles"

    start_urls = [
        'https://www.bbc.com/news',
    ]

    urls = []
    articles = {}
    completed = False
    index = 0


    def parse(self, response):

        if self.completed == False:
            for article in response.css('a.gs-c-promo-heading'):
                article_url = article.css('::attr(href)').get()

                if article_url.find('www.bbc') == -1 and article_url.count('/') == 2:
                    article_url = article_url.replace('/news', '', 1)

                    self.urls.append(self.start_urls[0] + article_url)
                    self.urls = list(dict.fromkeys(self.urls))

            for url in self.urls:
                if url is not None:
                    yield scrapy.Request(url = url, callback = self.parse)

            self.completed = True

        if response.css('div.story-body h1::text').get() is not None:
            text = ""

            for j in range(0, len(response.css('div.story-body__inner p::text'))):
                text += response.css('div.story-body__inner p::text')[j].get()

            author = 'Unknown' if (response.css('span.byline__name::text').get() is None) else response.css('span.byline').get()
            self.articles.update({
                str(self.index) : {
                    'url' : response.request.url,
                    'author' : author,
                    'title' : str(response.css('div.story-body h1::text').get()).lower(),
                    'date' : response.css('div.date::attr(data-datetime)').get(),
                    'story_body' : response.css('p.story-body__introduction::text').get(),
                    'artivle_text' : text.lower()
                }
            })
            self.index += 1

            if len(self.articles) == 20:
                print('testing!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                yield self.articles

        with open('article_news_3.json', 'w') as f:
            f.write(json.dumps(self.articles))