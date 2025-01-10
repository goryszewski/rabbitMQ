import requests, time

url: str = "http://127.0.0.1:5000/name"
headers = {"Content-Type": "application/json"}
data = {"data1": 1}
while True:
    try:
        response = requests.post(url=url, headers=headers, json=data)
        print(f"Code: {response.status_code}")
        # print(f"Headers: {response.headers}")
        print(f"Headers: {response.json()}")
    except Exception as e:
        print(e)
    time.sleep(0.1)
