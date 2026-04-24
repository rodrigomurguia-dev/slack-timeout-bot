import yaml
import logging
from datetime import datetime, timedelta
from config.settings import INTEGRATORS_FILE, PROCESSED_THREADS_FILE

logger = logging.getLogger(__name__)

# ── INTEGRATORS ──────────────────────────────────────────
def load_integrators():
    with open(INTEGRATORS_FILE, "r") as f:
        return yaml.safe_load(f) or {}

def get_user_for_integrator(integrator_id: str) -> str:
    integrators = load_integrators()
    return integrators.get(integrator_id, "@soporte-general")

# ── PROCESSED THREADS ─────────────────────────────────────
def load_processed():
    with open(PROCESSED_THREADS_FILE, "r") as f:
        data = yaml.safe_load(f) or {}
        return data.get("threads", [])

def save_processed(threads):
    with open(PROCESSED_THREADS_FILE, "w") as f:
        yaml.dump({"threads": threads}, f)

def is_thread_processed(thread_ts: str) -> bool:
    return any(t["thread_ts"] == thread_ts for t in load_processed())

def mark_thread_processed(thread_ts: str, channel: str):
    threads = load_processed()
    threads.append({
        "thread_ts": thread_ts,
        "channel": channel,
        "timestamp": datetime.now().isoformat()
    })
    save_processed(threads)
    logger.info(f"📝 Thread marcado: {thread_ts}")

# ── LIMPIEZA CADA 14 DÍAS ─────────────────────────────────
def cleanup_old_threads():
    threads = load_processed()
    cutoff = datetime.now() - timedelta(days=14)
    cleaned = [
        t for t in threads
        if datetime.fromisoformat(t["timestamp"]) > cutoff
    ]
    removed = len(threads) - len(cleaned)
    save_processed(cleaned)
    logger.info(f"🧹 Limpieza: {removed} threads eliminados")
