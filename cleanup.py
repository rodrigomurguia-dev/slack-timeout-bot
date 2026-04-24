import schedule
import time
import threading
import logging
from handlers.yaml_handler import cleanup_old_threads

logger = logging.getLogger(__name__)

def start_cleanup_scheduler():
    schedule.every(14).days.do(cleanup_old_threads)
    
    def run():
        logger.info("🕐 Scheduler de limpieza iniciado (cada 14 días)")
        while True:
            schedule.run_pending()
            time.sleep(3600)  # revisa cada hora

    thread = threading.Thread(target=run, daemon=True)
    thread.start()
