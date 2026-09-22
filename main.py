from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from motor_ia import EngineMestreDeJogo

app = FastAPI(title="EduQuest AI - Backend")
mestre_ia = EngineMestreDeJogo()

# Modelo de dados para receber a requisição
class SubmissaoCodigo(BaseModel):
    codigo: str
    desafio: str
    nivel_atual: str # 'Iniciante', 'Intermediário', 'Avançado'

@app.get("/")
def home():
    return {"status": "Plataforma EduQuest Online", "mestre_ia": "Ativo"}

@app.post("/api/v1/submeter")
def submeter_desafio(dados: SubmissaoCodigo):
    if not dados.codigo.strip():
        raise HTTPException(status_code=400, detail="O código não pode estar vazio.")
        
    # Dispara o motor de IA para julgar o código
    resultado = mestre_ia.avaliar_codigo_e_adaptar(
        codigo_usuario=dados.codigo,
        desafio_contexto=dados.desafio,
        nivel_atual=dados.nivel_atual
    )
    
    return resultado
