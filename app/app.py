import json
import re
import sqlite3
import subprocess

import eventlet
from flask import Flask, render_template
from flask_mqtt import Mqtt
from flask_socketio import SocketIO

eventlet.monkey_patch()

app = Flask(__name__)
app.config["SECRET"] = "my secret key"
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["MQTT_BROKER_URL"] = "127.0.0.1"

app.config["MQTT_BROKER_PORT"] = 1883
app.config["MQTT_CLIENT_ID"] = ""
app.config["MQTT_USERNAME"] = ""
app.config["MQTT_PASSWORD"] = ""
app.config["MQTT_KEEPALIVE"] = 5
app.config["MQTT_TLS_ENABLED"] = False
app.config["MQTT_LAST_WILL_TOPIC"] = "home/lastwill"
app.config["MQTT_LAST_WILL_MESSAGE"] = "bye"
app.config["MQTT_LAST_WILL_QOS"] = 2

mqtt = Mqtt(app)
socketio = SocketIO(app)


@app.route("/")
def index():
    return render_template(
        "index.html"
    )


@app.route("/register")
def register():
    return render_template(
        "register.html"
    )


@socketio.on("publish")
def handle_publish(json_str):
    data = json.loads(json_str)
    mqtt.publish(data["topic"], data["message"], data["qos"])


@socketio.on("subscribe")
def handle_subscribe(json_str):
    data = json.loads(json_str)
    mqtt.subscribe(data["topic"], data["qos"])


@socketio.on("unsubscribe_all")
def handle_unsubscribe_all():
    mqtt.unsubscribe_all()


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=message.payload.decode(),
        qos=message.qos,
    )
    socketio.emit("mqtt_message", data=data)


@mqtt.on_log()
def handle_logging(client, userdata, level, buf):
    pass

mqtt.subscribe(topic='stat/heater/RESULT')
mqtt.subscribe(topic='stat/light/RESULT')


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, use_reloader=True, debug=True)
