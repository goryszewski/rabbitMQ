from lib.rabbit import Queue
from lib.schema import PayloadSchemaBad
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os, json

load_dotenv()

app = Flask(__name__)
app.debug = True
payload_Schema = PayloadSchemaBad()
objectQ = Queue(
    host=os.environ.get("RABBITMQ_HOST"),
    queue=os.environ.get("RABBITMQ_QUEUE_NAME"),
    user=os.environ.get("RABBITMQ_USER"),
    password=os.environ.get("RABBITMQ_PASS"),
    arguments={"x-queue-type": "quorum"},
)


@app.route("/<name>", methods=["POST"])
def hello(name):

    json_data = request.get_json()

    print("DEBUG:", json_data)
    error = payload_Schema.validate(json_data)
    if error:
        return error, 422
    json_data = json.dumps(json_data)
    objectQ.send(json_data)
    return jsonify({"status": "ok"})
