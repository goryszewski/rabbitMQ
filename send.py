from lib.rabbit import Queue
from flask import Flask
from time import sleep
from dotenv import load_dotenv
import signal
import sys,os
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

@app.route("/<name>")
def hello(name):
    objectQ.send(f"test1  -{name}")
    return "done"

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
