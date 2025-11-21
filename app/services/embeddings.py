from typing import List

from sentence_transformers import SentenceTransformer
from app.core.config import settings
from app.core.logger import get_logger


logging = get_logger(__name__)

class EmbeddingService:
    def __init__(self):
        self.model = None
        self.load_model()
        
    def load_model(self) -> None:
        try:
            logging.info(
                f"[EMBEDDING] Carregando modelo de embeddings: {settings.EMBEDDINGS_MODEL_PATH} "
                f"[EMBEDDING] (dispositivo: {settings.EMBEDDINGS_DEVICE})"
            )

            model = SentenceTransformer(
                settings.EMBEDDINGS_MODEL_PATH, device=settings.EMBEDDINGS_DEVICE
            )

            self.model = model
        except Exception as e:
            raise RuntimeError(f"[EMBEDDING] Erro ao carregar o modelo de embeddings: {e}")

    def generate_embedding(self, text: str) -> List[float]:
        try:
            embedding = self.model.encode(text, convert_to_numpy=True).tolist()
            return embedding
        except Exception as e:
            logging.error(f"[EMBEDDING] Erro ao gerar embedding: {e}", exc_info=True)
            raise RuntimeError(f"[EMBEDDING] Erro ao gerar embedding: {e}")

    def get_model(self) -> SentenceTransformer:
        return self.model


embedding_service = EmbeddingService()
