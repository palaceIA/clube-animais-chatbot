import json
from typing import List, Dict, Any

from app.services.embeddings import embedding_service
from app.vectorstore.milvus import vectostore
from app.core.config import settings
from app.core.logger import get_logger

logging = get_logger(__name__)

def normalize_field(text: str) -> str:
    if not text or text.strip() == "-" or text.strip() == "":
        return ""
    return text.strip()


class KnowledgeStore:
    DATA_JSON = settings.DATA_JSON  

    def __init__(self):
        self.vectorstore = vectostore


    def load_json_file(self, file_path: str) -> List[Dict[str, Any]]:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            if isinstance(data, dict):
                data = [data]

            logging.info(
                f"[KNOWLEDGE] Carregado JSON: {file_path} ({len(data)} registros)"
            )
            return data

        except Exception as e:
            logging.error(f"[KNOWLEDGE] Erro ao ler JSON {file_path}: {e}", exc_info=True)
            return []

    def build_text(self, item: Dict[str, Any]) -> str:
        question_title = normalize_field(item.get("question_title", ""))
        question_text  = normalize_field(item.get("question_text", ""))
        answer_text    = normalize_field(item.get("answer_text", ""))

        parts = [question_title, question_text, answer_text]
        parts = [p for p in parts if p]  

        return "\n".join(parts).strip()
    
    def prepare_batch(self, items: List[Dict[str, Any]]) -> Dict[str, List]:
        ids, texts, embeddings = [], [], []

        for item in items:
            text = self.build_text(item)

            if not text:  
                continue

            emb = embedding_service.generate_embedding(text)

            ids.append(item["id"])
            texts.append(text)
            embeddings.append(emb)

        return {
            "ids": ids,
            "texts": texts,
            "embeddings": embeddings,
        }

    def insert_rag_batch(self, items: List[Dict[str, Any]]):
        try:
            total = len(items)
            logging.info(f"[KNOWLEDGE] Processando batch de {total} registros...")

            batch = self.prepare_batch(items)

            if not batch["ids"]:
                logging.warning("[KNOWLEDGE] Batch vazio — nada para inserir.")
                return

            rows = [batch["ids"], batch["texts"], batch["embeddings"]]

            self.vectorstore.insert_batch(rows)

            logging.info(
                f"[KNOWLEDGE] Inserido batch com {len(batch['ids'])}/{total} vetores."
            )

        except Exception as e:
            logging.error(f"[KNOWLEDGE] Erro ao inserir no Milvus: {e}", exc_info=True)
            raise


knowledge_service = KnowledgeStore()
