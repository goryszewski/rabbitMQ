from lib.rabbit import Queue
from time import sleep

import signal
import sys

import argparse

#import atexit sprawdzic DOTO

STATE=False

def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')
    global STATE
    STATE =True


signal.signal(signal.SIGINT, signal_handler)

parser = argparse.ArgumentParser()
parser.add_argument("host", help="host rabbitmq")
args=parser.parse_args()


def main():
    objectQ = Queue(host=args.host,queue="hello")
    c=1
    while True:
        if STATE:
            break;
        c=c+1
        objectQ.send(f"test1{c}")
        sleep(0.1)
        print(f"Send msg")




if __name__ == "__main__":
    main()

    print("normal end")