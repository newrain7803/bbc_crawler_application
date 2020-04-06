from flask import abort, Blueprint, flash, g, redirect, render_template, request, url_for
from .db import get_client
from . import crochet
import pymongo
from bson.objectid import ObjectId
from scrapy.crawler import CrawlerRunner
from .bbc_crawler.bbc_crawler.spiders.articlescrawler import ArticleSpider
import re

bp = Blueprint('views', __name__)


@bp.route('/', methods = ('GET', 'POST'))
def index():
    client = get_client()
    collection = client['news']
    if request.method == 'POST':
        search = request.form.get('search')
        if search:
            research = re.compile('.*' + search + '.*', re.IGNORECASE)
            articles = collection.articles_final1.find({"$or" : [{"title_s" : research}, {"author" : research}, {"content_s" : research}]}, {"_id" : 1,"title" : 1, "author" : 1, "date" : 1}).sort("date_s", pymongo.DESCENDING)
            return render_template('index.html', datas = articles, search = search)
        else:
            flash('검색하신 입력값이 없습니다.')

    articles = collection.articles_final1.find({}, {"_id" : 1, "title" : 1, "author" : 1, "date" : 1}).sort([("date_s", pymongo.DESCENDING), ("_id", pymongo.DESCENDING)])
    return render_template('index.html', datas = articles, search = None)


@bp.route('/crawling')
def crawling():
    scrape_with_crochet()
    return render_template('crawling.html')


@crochet.run_in_reactor
def scrape_with_crochet():
    runner = CrawlerRunner().crawl(ArticleSpider)


@bp.route('/articles/<_id>')
def articles(_id):
    collection = get_client()['news']
    article = collection.articles_final1.find_one({'_id' : ObjectId(_id)}, {"title" : 1, "author" : 1, "date" : 1, "content_r" : 1, "url" : 1})
    return render_template('articles.html', article = article)