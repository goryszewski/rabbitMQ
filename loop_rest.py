import requests,time

url:str="http://127.0.0.1:5000/name"
headers = {"Content-Type": "application/json" }
data={"data1":1}
while True:
    
    test = requests.post(url=url,headers=headers,json=data)
    print("ping")
    time.sleep(1)