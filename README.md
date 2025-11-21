# 🐾 Chatbot Inteligente – Clube dos Animais  
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-05998b?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Milvus](https://img.shields.io/badge/Milvus-2.3.6-red?style=for-the-badge&logo=milvus&logoColor=white)](https://milvus.io/)
[![Docker](https://img.shields.io/badge/Docker-24.0.5-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)

**RAG • Milvus • FastAPI • Embeddings E5-Large • Groq LLM**

---

Um chatbot construído com técnicas modernas de **IA generativa** e **busca semântica**, capaz de responder perguntas utilizando documentos do domínio **clubedosanimais.com.br**.  
O projeto combina **embeddings**, **Milvus**, **FastAPI** e **LLMs** para criar um sistema rápido, modular e altamente escalável.

---

## 🚀 Tecnologias Utilizadas

* **Python 3.10+**
* **FastAPI** (API REST)
* **Milvus** (banco vetorial)
* **Docker + Docker Compose**
* **Groq LLM API**
* **Modelo de Embeddings:** `intfloat/multilingual-e5-large`
* **HuggingFace Datasets**

---

## 📌 Arquitetura do Sistema

O sistema segue o padrão **Retrieval-Augmented Generation (RAG)**:

```mermaid
graph TD
    A[Usuário: Envia Query] --> B(API FastAPI)
    B --> C{Geração de Embedding: E5-Large}
    C --> D[Busca Semântica no Milvus]
    D --> E{Contexto Encontrado?}
    E -- Sim --> F[LLM Groq: Gera Resposta Contextualizada]
    E -- Não --> G[Guardrails: Mensagem Segura/Padrão]
    F --> H[Resposta para o Usuário]
    G --> H
````

-----

## 🛠️ Pré-requisitos

Antes de iniciar, certifique-se de ter instalado:

  * **Docker & Docker Compose**
  * **Python 3.10** ou superior
  * **Git**

-----

## ⚙️ Instalação e Execução

Siga os passos abaixo para rodar o projeto:

-----

### **1️⃣ Clone o repositório**

```bash
git clone [https://github.com/seu-user/seu-repo.git](https://github.com/seu-user/seu-repo.git)
cd seu-repo
```

-----

### **2️⃣ Suba os serviços do Milvus**

O `docker-compose.yml` inicia a stack do Milvus (Milvus, MinIO, etcd).

```bash
docker compose up -d
```

**Serviços iniciados:**

  * **Milvus** (Vector Database)
  * **MinIO** (Storage)
  * **etcd** (Metadata Service)

-----

### **3️⃣ Crie o ambiente virtual**

```bash
python3 -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

-----

### **4️⃣ Instale as dependências**

```bash
pip install -r requirements.txt
```

-----

### **6️⃣ Inicie o projeto**

Execute o script `start.sh`:

```bash
./start.sh
```

Ou, se precisar especificar o interpretador:

```bash
bash start.sh
```

A API estará disponível em:
👉 [http://localhost:8000](https://www.google.com/search?q=http://localhost:8000)

Documentação automática (Swagger UI/ReDoc):
👉 [http://localhost:8000/docs](https://www.google.com/search?q=http://localhost:8000/docs)

-----

## 🧠 Sobre o Dataset

Foi utilizado o dataset de perguntas e respostas em Português para popular o banco vetorial.

📦 **qa-portuguese-small**
🔗 [https://huggingface.co/datasets/Jpzinn654/qa-portuguese-small](https://huggingface.co/datasets/Jpzinn654/qa-portuguese-small)

Com filtragem específica para o domínio: `clubedosanimais.com.br`.

-----

## 🐾 Funcionalidades

  * ✔️ Busca semântica em documentos reais do Clube dos Animais (RAG)
  * ✔️ Respostas contextualizadas usando **Groq LLM** (Latência ultrabaixa)
  * ✔️ Guardrails para evitar alucinações de forma controlada
  * ✔️ API rápida e escalável com **FastAPI**
  * ✔️ Suporte a grandes volumes de dados e alta performance via **Milvus**

-----

## 📂 Estrutura do Projeto (Resumo)

```
.
├── 📁 app/
│   ├── api/          # Definições de rotas da API
│   ├── services/     # Lógica de negócio (LLM, RAG)
│   ├── vectorstore/  # Configurações do Milvus/Embeddings
│   ├── models/       # Pydantic models
│   └── core/         # Configurações, settings
├── 📁 milvus/         # Arquivos de configuração do Milvus
├── 📁 scripts/        # Scripts auxiliares
├── 📄 .env.example
├── 📄 docker-compose.yml # Para subir o Milvus
├── 📄 requirements.txt
├── 📄 start.sh          # Script de inicialização da API
└── 📄 README.md
```

