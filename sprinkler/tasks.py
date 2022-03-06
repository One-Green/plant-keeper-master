"""
Celery + Redis async tasks
"""

from line_protocol_parser import parse_line
from django.core.exceptions import ObjectDoesNotExist
from core.controller import BinaryController
from sprinkler.models import Sprinklers
from sprinkler.dict_def import SprinklerCtrlDict
from project.settings import MQTT_HOST
from project.settings import MQTT_PORT
from project.settings import MQTT_USERNAME
from project.settings import MQTT_PASSWORD
from project.settings import MQTT_SPRINKLER_CONTROLLER_TOPIC
from project.settings import DEFAULT_WATER_DEVICE
from celery import shared_task
import paho.mqtt.client as mqtt
import orjson as json
from posixpath import join

mqtt_client = mqtt.Client()
mqtt_client.username_pw_set(username=MQTT_USERNAME, password=MQTT_PASSWORD)
mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)


@shared_task(name="sprinkler_control")
def node_controller(message):
    """
    async task : read message from mqtt,
    apply controller rules
    write on message on MQTT topic
    :param message:
    :return:
    """

    mqtt_client.reconnect()

    d: dict = parse_line(message + b" 0")
    tag: str = d["tags"]["tag"]
    print(d)
    s = Sprinklers()
    ctl = BinaryController()
    s.add_tag_in_registry(tag)
    try:
        s.get_config(tag)
    except ObjectDoesNotExist:
        s.update_config(
            tag=tag,
            soil_moisture_min_level=30,
            soil_moisture_max_level=70,
            water_tag_link=DEFAULT_WATER_DEVICE,
        )
        s.get_config(tag)
    ctl.set_conf(
        _min=s.soil_moisture_min_level, _max=s.soil_moisture_max_level, reverse=False
    )

    # ---- actuator control
    force_controller = Sprinklers().get_controller_force(tag)
    if force_controller["force_water_valve_signal"]:
        water_valve_signal = int(force_controller["water_valve_signal"])
    else:
        water_valve_signal = int(ctl.get_signal(d["fields"]["soil_moisture"]))

    s.update_controller(tag=tag, water_valve_signal=bool(water_valve_signal))

    mqtt_client.publish(
        join(MQTT_SPRINKLER_CONTROLLER_TOPIC, tag),
        json.dumps(
            SprinklerCtrlDict(
                controller_type="sprinkler",
                tag=tag,
                water_valve_signal=water_valve_signal,
                soil_moisture_min_level=s.soil_moisture_min_level,
                soil_moisture_max_level=s.soil_moisture_max_level,
            )
        ),
    )
