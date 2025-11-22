# **Relatório – Chatbot para o Clube dos Animais**

## **1. Problema Escolhido: Chatbot para o Clube dos Animais**

O projeto consiste no desenvolvimento de um **chatbot interativo baseado em Recuperação de Informação (RAG – Retrieval-Augmented Generation)**. Ele utiliza um **banco de dados vetorial** para busca semântica e um **LLM** para geração da resposta final, integrados por meio de uma **API REST desenvolvida com FastAPI**.

Os dados utilizados foram extraídos do dataset disponível no Hugging Face:

- **Dataset:** Jpzinn654/qa-portuguese-small  
- **Modelo de Embeddings:** intfloat/multilingual-e5-large  

O dataset possui aproximadamente **500 mil registros** provenientes de diversos domínios. Para este projeto, o domínio **clubedosanimais.com.br** foi selecionado como tema principal. A filtragem dos dados foi realizada utilizando o seguinte script:

```python
from datasets import load_dataset
import json

ds = load_dataset("Jpzinn654/qa-portuguese-small", split="train")
filtro = ds.filter(lambda x: x["domain"] == "clubedosanimais.com.br")
lista_json = [dict(item) for item in filtro]

with open("clubedosanimais.json", "w", encoding="utf-8") as f:
    json.dump(lista_json, f, ensure_ascii=False, indent=2)
```

A escolha do modelo **E5-large** se deve à sua robustez, capacidade multilíngue e excelente desempenho em tarefas de similaridade semântica. Ele também possui ampla adoção, com mais de 2,7 milhões de downloads até a data de 21/11/2025.

## **2. Tecnologias Utilizadas Python**

    -Milvus (banco de dados vetorial)
    -Docker
    -FastAPI
    -IA Generativa – API Groq
    -Modelo open-source de embeddings (E5-large)

## **3. que são Embeddings?**
Embeddings são representações vetoriais de alta dimensionalidade que capturam o significado semântico de textos ou imagens. Esses vetores permitem que elementos semelhantes ocupem posições próximas no espaço vetorial.

Modelos como o E5-large são especializados na geração desses vetores, sendo altamente eficientes em tarefas como:

    -Similaridade semântica
    -Recuperação de documentos
    -Classificação textual
    -Busca contextual

## **4. Banco de Dados Vetorial – Milvus**
O Milvus foi escolhido por oferecer:

    -Alta velocidade de busca e indexação
    -Suporte a vários tipos de índices (HNSW, IVF, etc.)
    -Escalabilidade horizontal
    -Flexibilidade no armazenamento de coleções

Os documentos do domínio Clube dos Animais foram convertidos em embeddings e armazenados no Milvus, permitindo consultas rápidas e precisas.

## **5. Arquitetura da Solução**
A arquitetura segue o padrão RAG (Retrieval-Augmented Generation):

        Usuário pergunta  
                ↓  
        Geração do embedding da pergunta  
                ↓  
        Busca semântica no Milvus  
                ↓  
        Documentos encontrados?  
        ↙                   ↘  
      Sim                      Não  
       │                         │    
     Resposta via LLM          Guardrails de fallback

Características principais:

    -Sem memória conversacional (interações curtas)
    -Fluxo direto e objetivo
    -LLM acionado apenas quando há contexto relevante
    -Guardrails para evitar respostas inventadas

## **6. Busca Semântica**

A busca semântica funciona da seguinte forma:

    1.A entrada do usuário é convertida em um embedding.
    2.Esse vetor é comparado com os documentos armazenados.
    3.A busca retorna os vetores mais semelhantes com base em métricas como Inner Product ou Cosine Similarity.Isso garante que o chatbot funcione pelo significado, e não por simples correspondência de palavras.

## **7. Resultados Obtidos**

✔ Recuperação eficiente
Respostas geralmente em menos de 50 ms

✔ Coerência nas respostas
LLM da Groq gerou respostas contextualizadas com base nos documentos recuperados

✔ Embeddings E5-large aumentaram a assertividade

✔ Pipeline robusto -> Arquitetura modular (embeddings → Milvus → LLM)

✔ Fácil manutenção e expansão

✔ Baixa taxa de alucinações - Guardrails evitaram respostas fora do contexto

✔ Escalabilidade - Pode ser ampliado com novos agentes ou memória
