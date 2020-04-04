from flask import Flask, jsonify
from flask_pymongo import PyMongo
from pymongo import MongoClient


app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'news'
app.config['MONGO_URI'] = "mongodb://root:tlsdbstjr1+@192.168.111.139/news?authSource=admin"
mongo = PyMongo(app)
client = MongoClient(host = '192.168.111.139', username = 'root', password = 'tlsdbstjr1+', port = 27017, authSource = 'admin')
# client = MongoClient("mongodb://root:tlsdbstjr1+@192.168.111.139:27017/?authSource=admin")

@app.route('/viewNews', methods=['GET'])
def get_all_news():
    articles = client['news'].articles
    # articles = mongo.db.article

    articles_list = []

    article = articles.find()

    for i in article:
        i.pop('_id')
        articles_list.append(i)

    return jsonify(articles_list)


@app.route('/search/<keyword>', methods=['GET'])
def get_news_by_keyword(keyword):
    articles = client['news'].articles
    # articles = mongo.db.article

    articles_list = []
    article = articles.find()
    keyword = keyword.lower()

    for i in article:
        if keyword in i['artivle_text'] or keyword in  i['title']:
            i.pop('_id')
            articles_list.append(i)


    return jsonify(articles_list)