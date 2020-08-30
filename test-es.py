from elasticsearch import Elasticsearch
es = Elasticsearch(host="es01", port=9200, timeout=30, max_retries=10, retry_on_timeout=True)
if not es.ping():
  print("error")
else:
  print("connected")
