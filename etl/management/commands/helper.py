import datetime


from django.core.management.base import BaseCommand

from etl.servises.db_updater import DBUpdater
from etl.servises.defines import MOVIES_INDEX, MOVIES, \
    LAST_EXTRACT_DATA_FOR_FILM_WORK
from etl.servises.extractor import Extractor
from etl.servises.loader import Loader
from movies.models import FilmWork


class Command(BaseCommand):
    help = 'Add country values to db from file'

    def handle(self, *args, **options):
        updater = DBUpdater()
        updater.update_data_in_elasticsearch()



        # a = Extractor()
        # a.film_new_date = datetime.datetime.now()
        # a.genre_new_date = datetime.datetime.now()
        # a.person_new_date = datetime.datetime.now()
        # a.set_last_data()
        # print(a._get_last_data(LAST_EXTRACT_DATA_FOR_FILM_WORK))




        # from django.conf import settings
        # hosts = '127.0.0.1:9200'
        # from datetime import datetime
        # from elasticsearch import Elasticsearch, helpers
        # es = Elasticsearch('http://localhost:9200')
        # mapping = '''{
        #     "settings": {
        #         "number_of_shards": 1
        #     },
        #     "mappings": {
        #         "properties": {
        #             "field1": {"type": "text"}
        #             }
        #         }
        #     }'''
        # # a = es.info()
        # # print(a)
        # # res = es.indices.create(index="rrrrrr", ignore=400, body=mapping)
        # # # print(res)
        # # a = es.indices.get("rrrrrr")
        # # # print(a)
        # res = es.index(index=MOVIES, document={
        #     "number_of_shards": '2374'
        # })
        # # print(res)
        # a = es.indices.get(MOVIES)
        # # print(a)
        # query = {
        #     "match": {
        #         "number_of_shards": "23"
        #     }
        # }
        # a = es.update(
        #     index=MOVIES,
        #     id='KceRUIUBOj-ROrMmciEU',
        #     body={"doc": {"number_of_shards": "11111111111"}}
        # )
        # print(a)
        #
        # from elasticsearch import Elasticsearch, helpers
        # res = helpers.bulk(
        #     es,
        #     [{"number_of_shards": "33333333"}],
        #     index=MOVIES
        # )
        #
        # res = helpers.bulk(
        #     es,
        #     [{
        #         '_index': MOVIES,
        #         '_op_type': 'update',
        #         '_id': 'SceqUIUBOj-ROrMm6SHq',
        #         'doc': {'number_of_shards': '1000000'}
        #     }]
        # )
        #
        # res = helpers.bulk(
        #     es,
        #     [{
        #         '_index': MOVIES,
        #         '_op_type': 'create',
        #         'doc': {'number_of_shards': '12300000'}
        #     }]
        # )
        #
        # print(es.search(index=MOVIES, size=1000))
