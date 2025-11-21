from app.vectorstore.milvus import vectostore
from app.core.logger import get_logger

logging = get_logger(__name__)

class SearchSimilarity:
    @staticmethod
    def similarity(query: str, min_score: float = 0.81):

        logging.info(f"[SIMILARITY] Pergunta do usuário : {query}")

        results = vectostore.search_similarity(query)
        if not results:
            logging.info("[GUARDRAILS] Ativado proteção de conteúdo")
            return None

        filtered = [r for r in results if getattr(r, "score", 0) >= min_score]
        if not filtered:
            logging.info("[GUARDRAILS] Ativado proteção de conteúdo")
            return None

        return filtered

    @staticmethod
    def similarity_llm(query: str):
        context = SearchSimilarity.similarity(query)
        if not context:
            return None

        formatted_context = []
        for r in context:
            texto = getattr(r, "text", None)
            if texto is None:
                try:
                    texto = r.entity.get("text", str(r))
                except AttributeError:
                    texto = str(r)
            formatted_context.append(texto)

        return "\n\n".join(formatted_context)