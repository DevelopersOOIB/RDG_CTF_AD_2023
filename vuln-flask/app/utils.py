from elasticsearch import Elasticsearch

from app import elasticsearch


def es_wrapper(data: dict) -> list:
    try:
        return [i['_source'] for i in data['hits']['hits']]
    except (KeyError, TypeError):
        return []


def insert(doc, index_name='flags') -> dict:
    response = elasticsearch.index(index=index_name, document=doc)
    return {
        'id': response['_id'],
        'result': response['result']
    }


def search(_id: str, index_name='flags') -> dict:
    search_object = {'query': {'ids': {'values': [_id]}}}
    response = elasticsearch.search(index=index_name, body=search_object)
    if len(response['hits']['hits']) > 0:
        return response['hits']['hits'][0]['_source']
    return {}
