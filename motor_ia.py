import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class EngineMestreDeJogo:
    def __init__(self):
        # Inicializa o cliente da API
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def avaliar_codigo_e_adaptar(self, codigo_usuario: str, desafio_contexto: str, nivel_atual: str) -> dict:
        """
        Envia o código para a IA e retorna um JSON estruturado com a avaliação.
        """
        
        prompt_sistema = (
            "Você é o Mestre de Jogo de uma plataforma gamificada de programação corporativa. "
            "Sua função é avaliar o código de desenvolvedores juniores sob a ótica estrita de "
            "Clean Code (código limpo, legibilidade, boas práticas) e Cibersegurança (vulnerabilidades, "
            "ataques de injeção, vazamento de dados). "
            "Você deve responder EXCLUSIVAMENTE com um objeto JSON válido."
        )

        prompt_usuario = f"""
        [CONTEXTO DO DESAFIO]: {desafio_contexto}
        [NÍVEL ATUAL DO USUÁRIO]: {nivel_atual}
        
        [CÓDIGO SUBMETIDO PELO USUÁRIO]:
        ---
        {codigo_usuario}
        ---
        
        Instruções de Saída:
        Gere um JSON com a seguinte estrutura exata:
        {{
            "aprovado": true/false,
            "feedback": "Uma mensagem curta, motivadora e no estilo gamificado explicando o erro ou acerto.",
            "xp_ganho": int (de 0 a 100),
            "proxima_dificuldade": "subir", "manter" ou "descer" (Baseado nos erros/acertos)
        }}
        """

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                response_format={"type": "json_object"}, # Força o retorno em JSON estável
                messages=[
                    {"role": "system", "content": prompt_sistema},
                    {"role": "user", "content": prompt_usuario}
                ],
                temperature=0.2 # Baixa temperatura para respostas mais técnicas e consistentes
            )
            
            # Converte a string de resposta de volta para um dicionário Python
            return json.loads(response.choices.message.content)
            
        except Exception as e:
            return {
                "aprovado": False,
                "feedback": f"Erro crítico na comunicação com o Mestre de Jogo: {str(e)}",
                "xp_ganho": 0,
                "proxima_dificuldade": "manter"
            }
