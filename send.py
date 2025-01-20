from lib.rabbit import Queue
from lib.schema import PayloadSchemaBad
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os, json
from lib.mysql import TMySql

load_dotenv()

app = Flask(__name__)
payload_Schema = PayloadSchemaBad()
object_fanout = Queue(
    host=os.environ.get("RABBITMQ_HOST"),
    user=os.environ.get("RABBITMQ_USER"),
    password=os.environ.get("RABBITMQ_PASS"),
    arguments={"x-queue-type": "quorum"},

    logger=app.logger,
    exchange="logs",
    exchange_type="fanout",
)

objectQ_direct = Queue(
    host=os.environ.get("RABBITMQ_HOST"),
    queue=os.environ.get("RABBITMQ_QUEUE_NAME"),
    routing_key=os.environ.get("RABBITMQ_QUEUE_NAME"),
    user=os.environ.get("RABBITMQ_USER"),
    password=os.environ.get("RABBITMQ_PASS"),
    arguments={"x-queue-type": "quorum"},
    logger=app.logger,
)

objectQ_topic= Queue(
    host=os.environ.get("RABBITMQ_HOST"),
    queue=os.environ.get("RABBITMQ_QUEUE_NAME"),
    user=os.environ.get("RABBITMQ_USER"),
    password=os.environ.get("RABBITMQ_PASS"),
    routing_key="",
    arguments={"x-queue-type": "quorum"},
    logger=app.logger,
    exchange="logs_topic",
    exchange_type="topic",
)

cnx= TMySql(user="client", password="client", host="10.0.0.184", database="cloud")

@app.route("/db", methods=["GET"])
def db():
    data=cnx.get("select count(*) from task")
    app.logger.info(f"LOG SQL: {data}")
    return {}


@app.route("/logs", methods=["POST"])
def logs():

    json_data = request.get_json()

    app.logger.info("test log")
    error = payload_Schema.validate(json_data)
    if error:
        return error, 422
    json_data = json.dumps(json_data)
    status = object_fanout.send(message=json_data,routing_key="")
    return jsonify({"status": status})


@app.route("/direct", methods=["POST"])
def direct():

    json_data = request.get_json()

    app.logger.info("test log")
    error = payload_Schema.validate(json_data)
    if error:
        return error, 422
    json_data = json.dumps(json_data)
    status = objectQ_direct.send(message=json_data,routing_key="")
    return jsonify({"status": status})

@app.route("/topic", methods=["POST"])
def topic():

    json_data = request.get_json()

    app.logger.info("test log")
    error = payload_Schema.validate(json_data)
    if error:
        return error, 422
    json_data = json.dumps(json_data)
    status = objectQ_topic.send(message=json_data ,routing_key="")
    return jsonify({"status": status})

if __name__ == "__main__":
    app.run(debug=True)
