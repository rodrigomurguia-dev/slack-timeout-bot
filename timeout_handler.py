import logging
from config.channel_config import get_listen_channel, get_notify_channel
from handlers.message_parser import extract_integrator
from handlers.yaml_handler import (
    get_user_for_integrator,
    is_thread_processed,
    mark_thread_processed
)

logger = logging.getLogger(__name__)

def handle_timeout_event(message, client):
    channel   = message["channel"]
    thread_ts = message.get("thread_ts") or message["ts"]
    text      = message.get("text", "")

    # ── Validar canal correcto ────────────────────────────
    if channel != get_listen_channel():
        logger.info(f"⏭️ Mensaje ignorado, canal no monitoreado: {channel}")
        return

    # ── Anti-duplicate ────────────────────────────────────
    if is_thread_processed(thread_ts):
        logger.info(f"🔁 Thread ya procesado, ignorando: {thread_ts}")
        return

    # ── Extraer integrador ────────────────────────────────
    integrator = extract_integrator(text)
    if not integrator:
        logger.warning("⚠️ Timeout sin integrador identificado")
        return

    # ── Buscar usuario asignado ───────────────────────────
    user = get_user_for_integrator(integrator)

    # ── Marcar thread como procesado ─────────────────────
    mark_thread_processed(thread_ts, channel)

    # ── Responder en el hilo ─────────────────────────────
    client.chat_postMessage(
        channel=channel,
        thread_ts=thread_ts,
        text=f"Hola, el tema lo estará siguiendo {user}"
    )
    logger.info(f"💬 Respuesta en hilo enviada → {user}")

    # ── Notificar en Canal B ──────────────────────────────
    permalink = client.chat_getPermalink(
        channel=channel,
        message_ts=thread_ts
    )["permalink"]

    client.chat_postMessage(
        channel=get_notify_channel(),
        text=f"Nuevo error de timeout {user}\n🔗 {permalink}"
    )
    logger.info(f"📣 Notificación enviada a canal B")
