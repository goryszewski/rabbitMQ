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

objectQ_topic = Queue(
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

cnx1 = TMySql(
    user=os.environ.get("SQL_USER"),
    password=os.environ.get("SQL_PASS"),
    host="node01.autok8s.xyz",
    database=os.environ.get("SQL_DB"),
)
cnx2 = TMySql(
    user=os.environ.get("SQL_USER"),
    password=os.environ.get("SQL_PASS"),
    host="node02.autok8s.xyz",
    database=os.environ.get("SQL_DB"),
)
cnx3 = TMySql(
    user=os.environ.get("SQL_USER"),
    password=os.environ.get("SQL_PASS"),
    host="node03.autok8s.xyz",
    database=os.environ.get("SQL_DB"),
)


@app.route("/db", methods=["GET"])
def db():
    output = {}
    output["01"] = cnx1.get("select count(*) from task")
    output["02"] = cnx2.get("select count(*) from task")
    output["03"] = cnx3.get("select count(*) from task")
    app.logger.info(f"LOG SQL: {output}")
    return output


@app.route("/logs", methods=["POST"])
def logs():

    json_data = request.get_json()

    app.logger.info("test log")
    error = payload_Schema.validate(json_data)
    if error:
        return error, 422
    json_data = json.dumps(json_data)
    status = object_fanout.send(message=json_data, routing_key="")
    return jsonify({"status": status})


@app.route("/direct", methods=["POST"])
def direct():

    json_data = request.get_json()

    app.logger.info("test log")
    error = payload_Schema.validate(json_data)
    if error:
        return error, 422
    json_data = json.dumps(json_data)
    status = objectQ_direct.send(message=json_data, routing_key="")
    return jsonify({"status": status})


@app.route("/topic", methods=["POST"])
def topic():

    json_data = request.get_json()

    app.logger.info("test log")
    error = payload_Schema.validate(json_data)
    if error:
        return error, 422
    json_data = json.dumps(json_data)
    status = objectQ_topic.send(message=json_data, routing_key="")
    return jsonify({"status": status})


if __name__ == "__main__":
    app.run(debug=True)
