import os
from dotenv import load_dotenv

load_dotenv()

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")
SLACK_SIGNING_SECRET = os.getenv("SLACK_SIGNING_SECRET")
NOTIFY_CHANNEL_ID = os.getenv("NOTIFY_CHANNEL_ID")

TIMEOUT_TRIGGER = "Tipo de error: Timeout"

DB_PATH = "db/"
INTEGRATORS_FILE = f"{DB_PATH}integrators.yaml"
PROCESSED_THREADS_FILE = f"{DB_PATH}processed_threads.yaml"
