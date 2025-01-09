from lib.rabbit import Queue
from lib.schema import PayloadSchemaBad
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os, json

load_dotenv()

app = Flask(__name__)
payload_Schema = PayloadSchemaBad()
objectQ = Queue(
    host=os.environ.get("RABBITMQ_HOST"),
    queue=os.environ.get("RABBITMQ_QUEUE_NAME"),
    user=os.environ.get("RABBITMQ_USER"),
    password=os.environ.get("RABBITMQ_PASS"),
    arguments={"x-queue-type": "quorum"},
    logger=app.logger,
)


@app.route("/<name>", methods=["POST"])
def hello(name):

    json_data = request.get_json()

    app.logger.info("test log")
    error = payload_Schema.validate(json_data)
    if error:
        return error, 422
    json_data = json.dumps(json_data)
    status = objectQ.send(json_data)
    return jsonify({"status": status})


if __name__ == "__main__":
    app.run(debug=True)
