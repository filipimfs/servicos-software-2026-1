import os
import shutil
import uuid
import re
import whisper

from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel

app = FastAPI()

print("Carregando modelo de IA (Whisper)...")
model = whisper.load_model("base")
print("Modelo carregado!")


# =========================
# ROTA TESTE
# =========================
@app.get("/")
def diz_ola():
    return {"Olá": "Mundo"}


# =========================
# TRANSCRIÇÃO
# =========================
@app.post("/transcrever")
async def transcrever_audio(file: UploadFile = File(...)):
    caminho_temp = f"temp_{uuid.uuid4()}.wav"

    with open(caminho_temp, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        resultado = model.transcribe(caminho_temp, language="pt")
        texto = resultado["text"].strip()
    finally:
        if os.path.exists(caminho_temp):
            os.remove(caminho_temp)

    return {"texto": texto}


# =========================
# MODELO DE ENTRADA
# =========================
class TextoEntrada(BaseModel):
    text: str


# =========================
# FUNÇÃO DE SENTIMENTO (REUTILIZÁVEL)
# =========================
def calcular_sentimento(texto: str):
    texto = texto.lower()

    positivas = [
        "bom", "ótimo", "excelente", "gostei", "legal", "incrível",
        "perfeito", "maravilhoso", "fantástico", "amei", "top"
    ]

    negativas = [
        "ruim", "péssimo", "horrível", "odiei", "terrível",
        "lixo", "horroroso", "fraco", "decepcionante", "ridículo"
    ]

    intensificadores = ["muito", "extremamente", "super", "bem"]
    negacoes = ["não", "nunca", "jamais"]

    # Melhor tokenização (remove pontuação)
    palavras = re.findall(r'\b\w+\b', texto)

    score = 0

    for i, palavra in enumerate(palavras):
        peso = 1

        if i > 0 and palavras[i - 1] in intensificadores:
            peso = 2

        negado = False
        if i > 0 and palavras[i - 1] in negacoes:
            negado = True

        if palavra in positivas:
            score += -peso if negado else peso

        elif palavra in negativas:
            score += peso if negado else -peso

    if score > 1:
        sentimento = "muito positivo"
    elif score == 1:
        sentimento = "positivo"
    elif score == 0:
        sentimento = "neutro"
    elif score == -1:
        sentimento = "negativo"
    else:
        sentimento = "muito negativo"

    return sentimento, score


# =========================
# ANÁLISE DE TEXTO
# =========================
@app.post("/analyze")
def analisar_texto(entrada: TextoEntrada):
    sentimento, score = calcular_sentimento(entrada.text)

    return {
        "texto": entrada.text,
        "sentimento": sentimento,
        "score": score
    }


# =========================
# TRANSCRIÇÃO + ANÁLISE
# =========================
@app.post("/transcrever-e-analisar")
async def transcrever_e_analisar(file: UploadFile = File(...)):
    caminho_temp = f"temp_{uuid.uuid4()}.wav"

    with open(caminho_temp, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        resultado = model.transcribe(caminho_temp, language="pt")
        texto = resultado["text"].strip()

        sentimento, score = calcular_sentimento(texto)

    finally:
        if os.path.exists(caminho_temp):
            os.remove(caminho_temp)

    return {
        "texto": texto,
        "sentimento": sentimento,
        "score": score
    }
