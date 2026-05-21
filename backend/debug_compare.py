import requests
import time

url = 'http://127.0.0.1:8001/api/compare'
print('REQUEST', url)
start = time.time()
try:
    r = requests.post(url, json={'product': 'iPhone 15'}, timeout=60)
    print('STATUS', r.status_code)
    print(r.text[:400])
except Exception as e:
    print('ERROR', type(e).__name__, e)
print('ELAPSED', time.time() - start)
