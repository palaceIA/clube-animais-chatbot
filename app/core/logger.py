import logging
import logging.config

from app.core.logger_config import LOGGING_CONFIG  # importa o config central

# Aplica a configuração no momento da importação
logging.config.dictConfig(LOGGING_CONFIG)


def get_logger(name: str) -> logging.Logger:
    """Retorna um logger já configurado com o nome do módulo."""
    return logging.getLogger(name)
