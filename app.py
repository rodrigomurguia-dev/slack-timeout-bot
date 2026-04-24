import logging
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from config.settings import SLACK_BOT_TOKEN, SLACK_APP_TOKEN, TIMEOUT_TRIGGER
from handlers.timeout_handler import handle_timeout_event
from handlers.cleanup import start_cleanup_scheduler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = App(token=SLACK_BOT_TOKEN)

@app.message(TIMEOUT_TRIGGER)
def handle_timeout(message, client):
    handle_timeout_event(message, client)

if __name__ == "__main__":
    start_cleanup_scheduler()
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    logger.info("🤖 Bot iniciado - escuchando eventos...")
    handler.start()
