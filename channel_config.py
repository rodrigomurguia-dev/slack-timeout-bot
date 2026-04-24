import yaml
import logging

logger = logging.getLogger(__name__)

def load_channels():
    with open("config/channels.yaml", "r") as f:
        return yaml.safe_load(f)

def get_listen_channel() -> str:
    return load_channels()["listen_channel"]

def get_notify_channel() -> str:
    return load_channels()["notify_channel"]
