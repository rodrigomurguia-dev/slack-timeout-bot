import re
import logging

logger = logging.getLogger(__name__)

def extract_integrator(text: str) -> str | None:
    """
    Extrae el integrador del mensaje.
    Ejemplo: "Nombre de la Integracion/Brand: INTUIPOSPAV2SELFM/ Snack Fit Me"
    Retorna: "INTUIPOSPAV2SELFM"
    """
    match = re.search(r"Nombre de la Integracion/Brand:\s*([^/\s]+)", text)
    if match:
        integrator = match.group(1).strip()
        logger.info(f"🔍 Integrador extraído: {integrator}")
        return integrator
    logger.warning("⚠️ No se encontró integrador en el mensaje")
    return None
