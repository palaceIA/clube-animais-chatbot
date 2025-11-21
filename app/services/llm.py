from langchain_groq import ChatGroq

from app.core.config import settings
from app.services.rag import SearchSimilarity
from app.core.logger import get_logger

logging = get_logger(__name__)

class AgentRag :
    def __init__(self):
        pass

    def get_llm(self) :
        try :  
            logging.info("[LLM] Carregando modelo...")
            llm = ChatGroq(
                model= settings.GROQ_MODEL , 
                api_key= settings.GROQ_API_KEY , 
                temperature=0.8
            )
            logging.info("[LLM] Modelo carregado recuperado com sucesso!")
            return llm 
        except Exception as e :
            logging.error("[LLM] erro ao recuperar modelo")
            return None 
        
    def get_guardrails(self, query: str) -> str:
        response_guardrail = (
            f"🐾CLUBE DOS ANIMAIS🐾 : Infelizmente não possuímos nada que se relacione com '{query}' em nosso site, "
            f"mas caso queira contribuir com informações, acesse www.clubedosanimais.com "
            f"e nos ajude a engajar nosso conteúdo. Lembrando que sua contribuição está sujeita "
            f"à avaliação de conteúdo. Muito obrigado!"
        )
        return response_guardrail.strip()


    def get_prompt(self) : 
        prompt = """
            Você é um Agente de RAG responsável por responder perguntas do usuário
            sobre o Clube dos Animais **exclusivamente** com base no contexto fornecido.

            ⭐ REGRAS ABSOLUTAS (siga SEMPRE)

            1. A resposta deve usar **apenas** as informações presentes no contexto.  
            - Não invente informações.  
            - Não faça suposições.  
            - Não use conhecimento externo.

            2. Se o contexto estiver com Guardrails , responda de forma gentil que:
            “Eu sou a Assistente do Clube dos animais e não posso responder perguntas que não estejam no meu escopo”

            3. Sua postura deve ser sempre gentil, acolhedora e amigável — como alguém que cuida bem dos pets.

            4. Seja **direto e objetivo**, mas sem perder a cordialidade.
            ---
            Agora responda à pergunta do usuário usando APENAS o contexto:

            **CONTEXTO**  
            {contexto}

            **PERGUNTA**  
            {query}
        """
        return prompt
    
    async def response_message(self,query : str) :
        context = SearchSimilarity.similarity_llm(query)

        if context is None : 
            return self.get_guardrails(query)

        llm = self.get_llm()
        prompt = self.get_prompt()

        try : 
            logging.info("[LLM] Respondendo a pergunta do usuário...")
            prompt_full = prompt.format(
                query=query ,
                contexto=context 
            )
            message = [("system",prompt_full)]
            response = await llm.ainvoke(message)
            content  = "🐾CLUBE DOS ANIMAIS🐾 : " + response.content
            logging.info("[LLM] Pergunta respondida com sucesso!")
            return content
        
        except Exception as e :
            logging.error(f"[LLM] Erro ao responder pergunta do usuário : {e}")
            return None


agent = AgentRag()