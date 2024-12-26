from lib.rabbit import Queue
from flask import Flask, request, jsonify
from time import sleep
from dotenv import load_dotenv
import signal
import sys,os,json
load_dotenv()
import argparse

# import atexit sprawdzic DOTO

STATE = False


def signal_handler(signal, frame):
    print("You pressed Ctrl+C!")
    global STATE
    STATE = True

app = Flask(__name__)

# signal.signal(signal.SIGINT, signal_handler)

# parser = argparse.ArgumentParser()
# parser.add_argument("host", help="host rabbitmq")
# args = parser.parse_args()
objectQ = Queue(host=os.environ.get("RABBITMQ_HOST"), queue=os.environ.get("RABBITMQ_QUEUE_NAME"))

@app.route("/<name>",methods=['POST'])
def hello(name):
    content = request.json
    json_data = json.dumps(content)
    objectQ.send(json_data)
    return jsonify({"name":name})

# def main():
#     c = 1
#     while True:
#         if STATE:
#             break
#         c = c + 1
        
#         sleep(0.1)
#         print(f"Send msg")


# if __name__ == "__main__":
#     main()

#     print("normal end")
