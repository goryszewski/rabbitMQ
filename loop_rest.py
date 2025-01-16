import requests, time

direct: str = "http://127.0.0.1:5000/direct"
logs: str = "http://127.0.0.1:5000/logs"
topic: str = "http://127.0.0.1:5000/topic"
headers = {"Content-Type": "application/json"}
count: int = 0

while True:
    try:
        count += 1
        data = {"data1": count}
        response = requests.post(url=direct, headers=headers, json=data)
        print(f"Code: {response.status_code}")
        # print(f"Headers: {response.headers}")
        print(f"Headers: {response.json()}")

        count += 1
        data = {"data1": count}

        response = requests.post(url=logs, headers=headers, json=data)
        print(f"Code: {response.status_code}")
        # print(f"Headers: {response.headers}")
        print(f"Headers: {response.json()}")

        count += 1
        data = {"data1": count}

        response = requests.post(url=topic, headers=headers, json=data)
        print(f"Code: {response.status_code}")
        # print(f"Headers: {response.headers}")
        print(f"Headers: {response.json()}")
    except Exception as e:
        print(e)
        time.sleep(5)
    time.sleep(0.1)
