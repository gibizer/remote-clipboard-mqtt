import argparse
import cryptography.fernet
from cryptography import fernet
from dataclasses import dataclass
import logging
from paho.mqtt import client as mqtt_client
import pyperclip
import sys
import uuid


@dataclass
class ConnectionInfo:
    broker: str
    port: int
    username: str
    password: str
    topic: str
    token: cryptography.fernet.Fernet


class ClipboardHandler:
    def __init__(self, connection_info):
        self.connection_info = connection_info
        self.client = mqtt_client.Client()
        self.client.username_pw_set(
            connection_info.username, connection_info.password)
        self.client.on_connect = self.on_connect
        self.client.connect(connection_info.broker, connection_info.port)
        self.local_clipboard_content = pyperclip.paste()
        logging.debug(
            f"Initialized from local clipboard content:"
            f"|{self.local_clipboard_content}|")

        self.client.subscribe(self.connection_info.topic)
        self.client.on_message = self.on_message

        while True:
            self.check_for_local_update()
            self.client.loop(timeout=1.0)

    def check_for_local_update(self):
        current: str = pyperclip.paste()
        if self.local_clipboard_content != current:
            msg = self.connection_info.token.encrypt(current.encode())
            self.client.publish(self.connection_info.topic, msg)
            logging.info(f"Published local clipboard content:|{current}|")
            logging.debug(f"Data sent: {msg}")
            self.local_clipboard_content = current

    def on_message(self, client, userdata, msg: mqtt_client.MQTTMessage):
        payload = msg.payload
        logging.debug(f"Data received: {payload}")
        new_clipboard = self.connection_info.token.decrypt(payload).decode()
        logging.info(f"Changing local clipboard to:|{new_clipboard}|")
        self.local_clipboard_content = new_clipboard
        pyperclip.copy(new_clipboard)

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            logging.info("Connected to the shared clipboard server.")
        else:
            logging.error("Failed to connect, return code %d.", rc)
            sys.exit(1)


def create(clipboard_name, key: str):
    if clipboard_name is None:
        clipboard_name = str(uuid.uuid4())
    if key is None:
        key = fernet.Fernet.generate_key()
    else:
        key = key.encode()

    token = fernet.Fernet(key)

    logging.info(
        f"To join to this clipboard from another machine use:\n"
        f"remote_clipboard --name {clipboard_name}, --key {key.decode()}")

    info = ConnectionInfo(
        # this is a free and public mqtt server
        broker="broker.emqx.io",
        port=1883,
        username="emqx",
        password="public",
        topic=clipboard_name,
        token=token,
    )

    ClipboardHandler(info)


def parse_args():
    arg_parser = argparse.ArgumentParser(
        usage="Connect to a shared, remote clipboard.\n\n"
              "If called without parameter then a new shared clipboard is "
              "created and instruction is printed to connect to it from "
              "another machine."
    )
    arg_parser.add_argument(
        "-k",
        "--key",
        type=str,
        default=None,
        help="The encryption key the clipboard uses. If not provided a new "
             "is generated and printed.",
    )
    arg_parser.add_argument(
        "-n",
        "--name",
        type=str,
        default=None,
        help="The name of the shared clipboard to join to. If not provided a "
             "new shared clipboard with a random name is created and printed.",
    )
    arg_parser.add_argument(
        "-d",
        "--debug",
        action='store_true',
        help="Print more logs",
    )
    return arg_parser.parse_args()


def main():
    args = parse_args()
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
        logging.debug('String with debug logging')
    else:
        logging.basicConfig(level=logging.INFO)
    create(clipboard_name=args.name, key=args.key)


if __name__ == "__main__":
    main()
