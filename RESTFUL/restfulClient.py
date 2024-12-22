import json
import subprocess
import requests


#curlCmd='curl http://127.0.0.1:8000/ -d \"{\\\"id\\\":1}\" PUT  -H "Content-Type: application/json" -v'

#result = subprocess.run(curlCmd,shell=True,capture_output=True, text=True)

#print(result.stdout)

#jsonstr = json.loads(result.stdout)

#tmp=dict()
#tmp['nnn'] = 2

#jsonstr.append(tmp)


print("get")

url = 'http://127.0.0.1:8000/'
res = requests.get(url)
print(res.text)

print("post")
data = {'id':2}
headers = {'Content-Type':'application/json'}
res = requests.post(url, data=json.dumps(data),headers=headers)
print(res.text)

print("put")
res = requests.put(url, data=json.dumps(data),headers=headers)
print(res.text)

print("dele")
res = requests.delete(url,  data=json.dumps(data), headers=headers)
print(res.text)
