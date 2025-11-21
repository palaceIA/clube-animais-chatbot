from pydantic_settings import BaseSettings

import os 


class Settings(BaseSettings) : 

    COLLECTION : str = os.getenv("COLLECTION")
    MILVUS_HOST : str = os.getenv("MILVUS_HOST")
    MILVUS_PORT : str = os.getenv("MILVUS_PORT")

    EMBEDDINGS_DEVICE : str = os.getenv("EMBEDDINGS_DEVICE")
    EMBEDDINGS_MODEL_PATH : str = os.getenv("EMBEDDING_MODEL_PATH")
    DATA_JSON : str = os.getenv("DATA_JSON")

    GROQ_MODEL : str = os.getenv("GROQ_MODEL")
    GROQ_API_KEY : str = os.getenv("GROQ_API_KEY")

    class Config : 
        env = ".env"


settings = Settings()