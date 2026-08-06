"""
API de gestão da escola

Uma aplicação FastAPI simples que permite aos estudantes visualizar e se
inscrever em atividades extracurriculares da Escola Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="API da Escola Mergington High School",
              description="API para visualizar e se inscrever em atividades extracurriculares")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# Banco de dados em memória das atividades
activities = {
    "Clube de Xadrez": {
        "description": "Aprenda estratégias e participe de torneios de xadrez",
        "schedule": "Sextas-feiras, 15:30 - 17:00",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Aula de Programação": {
        "description": "Aprenda fundamentos de programação e construa projetos de software",
        "schedule": "Terças e quintas-feiras, 15:30 - 16:30",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Aula de Educação Física": {
        "description": "Educação física e atividades esportivas",
        "schedule": "Segundas, quartas e sextas-feiras, 14:00 - 15:00",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Time de Basquete": {
        "description": "Entre para o nosso time competitivo de basquete para treinos e jogos",
        "schedule": "Segundas e quintas-feiras, 16:00 - 17:30",
        "max_participants": 15,
        "participants": ["alex@mergington.edu"]
    },
    "Clube de Futebol": {
        "description": "Jogue futebol com colegas e desenvolva suas habilidades",
        "schedule": "Terças e sextas-feiras, 15:30 - 17:00",
        "max_participants": 22,
        "participants": ["lucas@mergington.edu"]
    },
    "Clube de Teatro": {
        "description": "Atue em peças e musicais escolares",
        "schedule": "Quartas e sábados, 15:00 - 17:00",
        "max_participants": 25,
        "participants": ["isabella@mergington.edu", "jacob@mergington.edu"]
    },
    "Banda de Música": {
        "description": "Tocando na banda da escola e se apresentando em concertos",
        "schedule": "Segundas e quartas-feiras, 15:30 - 16:30",
        "max_participants": 30,
        "participants": ["mia@mergington.edu"]
    },
    "Clube de Ciências": {
        "description": "Explore a ciência por meio de experimentos e projetos",
        "schedule": "Quintas-feiras, 15:30 - 16:30",
        "max_participants": 18,
        "participants": ["noah@mergington.edu", "ava@mergington.edu"]
    },
    "Time de Debate": {
        "description": "Desenvolva habilidades de fala em público e pensamento crítico",
        "schedule": "Terças-feiras, 16:00 - 17:30",
        "max_participants": 16,
        "participants": ["ethan@mergington.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return JSONResponse(content=activities, headers={"Cache-Control": "no-store"})


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Inscrever um estudante em uma atividade"""
    # Validar se a atividade existe
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Atividade não encontrada")

    # Obter a atividade específica
    activity = activities[activity_name]

    # Validar se o estudante já está inscrito
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Estudante já está inscrito nesta atividade")

    # Adicionar estudante
    activity["participants"].append(email)
    return {"message": f"Inscrição realizada para {email} na atividade {activity_name}"}


@app.delete("/activities/{activity_name}/participants/{email}")
def remove_participant(activity_name: str, email: str):
    """Remover um estudante de uma atividade"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Atividade não encontrada")

    activity = activities[activity_name]
    if email not in activity["participants"]:
        raise HTTPException(status_code=404, detail="Participante não encontrado")

    activity["participants"].remove(email)
    return {"message": f"Removido {email} da atividade {activity_name}"}
