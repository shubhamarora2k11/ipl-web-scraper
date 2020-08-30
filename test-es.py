from elasticsearch import Elasticsearch
from datetime import datetime
es = Elasticsearch(host="es01", port=9200, timeout=30, max_retries=10, retry_on_timeout=True)
if not es.ping():
  print("error")
else:
  print("connected")

doc = {
    'author': 'kimchy',
    'text': 'Elasticsearch: cool. bonsai cool.',
    'timestamp': datetime.now(),
}
res = es.index(index="test-index", id=1, body=doc)
print(res['result'])
