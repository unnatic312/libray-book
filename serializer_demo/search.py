from elasticsearch_dsl import DocType, Text, Float
from elasticsearch_dsl.connections import connections
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch
from . import models

connections.create_connection()

class ProductIndex(DocType):
    name = Text()
    price = Float()
    creator = Text()
    description = Text()

    class Meta:
        index='product-index'


def bulk_indexing():
    ProductIndex.init()
    es = Elasticsearch()
    bulk(
        client=es, actions=(
            b.indexing() for b in models.ProductSerializerModel.objects.all().iterator()
        )
    )