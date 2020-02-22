from elasticsearch import Elasticsearch

es = Elasticsearch(['http://localhost:9200/'])

doc = {
  "query" : {
    "match_all": {}
  }
}


res = es.search(index='products', doc_type='typename', body=doc,scroll='1m')

print(res)