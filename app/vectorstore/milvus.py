from pymilvus import (
    Collection,
    CollectionSchema,
    DataType,
    FieldSchema,
    connections,
    utility
)

from typing import Optional
from pydantic import BaseModel

from app.core.config import settings 
from app.core.logger import get_logger
from app.services.embeddings import embedding_service


logging = get_logger(__name__)

class Text(BaseModel):
    id: str
    text: str
    score: float


class VectorStoreMilvus:
    def __init__(self):
        self.host = settings.MILVUS_HOST
        self.port = settings.MILVUS_PORT
        self.collection_name = settings.COLLECTION

        self.collection: Optional[Collection] = None

        self.connect()
        self.init_collection()

    def connect(self):
        try:
            logging.info("[VECTORSTORE] Estabelecendo conexão com Milvus...")
            connections.connect(
                alias="default",
                host=self.host,
                port=self.port
            )
            logging.info("[VECTORSTORE] Milvus conectado com sucesso!")
        except Exception as e:
            logging.error(f"[VECTORSTORE] Erro ao conectar: {e}", exc_info=True)
            raise

    def init_collection(self):
        try:
            logging.info("[VECTORSTORE] Inicializando coleção...")

            if self.collection_name in utility.list_collections():
                self.collection = Collection(self.collection_name)
                self.collection.load()
                logging.info("[VECTORSTORE] Coleção carregada.")
                return

            fields = [
                FieldSchema(
                    name="id",
                    dtype=DataType.VARCHAR,
                    is_primary=True,
                    auto_id=False,
                    max_length=150
                ),
                FieldSchema(
                    name="text",
                    dtype=DataType.VARCHAR,
                    max_length=4096,
                ),
                FieldSchema(
                    name="embeddings",
                    dtype=DataType.FLOAT_VECTOR,
                    dim=1024   
                )
            ]

            schema = CollectionSchema(fields=fields)
            self.collection = Collection(self.collection_name, schema=schema)

            self.collection.create_index(
                field_name="embeddings",
                index_params={
                    "metric_type": "COSINE",
                    "index_type": "HNSW",
                    "params": {"M": 32, "efConstruction": 500}
                }
            )

            self.collection.load()

            logging.info("[VECTORSTORE] Coleção criada e carregada com sucesso!")

        except Exception as e:
            logging.error(f"[VECTORSTORE] Erro ao inicializar coleção: {e}", exc_info=True)
            raise

    def insert_batch(self, records: list[dict]):
        if not self.collection:
            logging.error("[VECTORSTORE] Coleção não carregada.")
            return

        try:
            self.collection.insert(records)
            self.collection.flush()

            logging.info(f"[VECTORSTORE] {len(records)} registros inseridos com sucesso.")

        except Exception as e:
            logging.error(f"[VECTORSTORE] Erro ao inserir dados: {e}", exc_info=True)
            raise

    def search_similarity(self, query: str):
        query_emb = embedding_service.generate_embedding(query)

        results = self.collection.search(
            data=[query_emb],
            anns_field="embeddings",
            param={"ef": 500},
            limit=3,
            output_fields=["id", "text"]
        )

        matches = []
        for hit in results[0]:
            matches.append(
                Text(
                    id=hit.entity.get("id"),
                    text=hit.entity.get("text"),
                    score=hit.distance
                )
            )

        return matches


vectostore = VectorStoreMilvus()
