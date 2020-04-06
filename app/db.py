from pymongo import MongoClient
from flask import g

def get_client():
    if 'client' not in g:
        g.client = MongoClient(
            host = '192.168.111.139',
            port = 27017,
            username = 'root',
            password = 'tlsdbstjr1+',
            authSource = 'admin',
        )

    return g.client


def close_client(e = None):
    client = g.pop("client", None)

    if client is not None:
        client.close()

