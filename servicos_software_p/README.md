# Projeto Final - Serviços de Software

## Descrição

Este projeto consiste em uma aplicação baseada em arquitetura de
microserviços containerizados utilizando Docker. A solução é composta
por dois serviços principais:

-   **Backend**: responsável pelo processamento das requisições e
    execução dos modelos de Inteligência Artificial.
-   **Frontend**: responsável pela interface com o usuário.

A comunicação entre os serviços é realizada por meio de **APIs REST**.

------------------------------------------------------------------------

## Funcionalidades

A aplicação permite:

-   🎤 **Transcrição automática de áudio** utilizando o modelo de IA
    Whisper
-   🧠 **Análise de sentimento** do texto (positivo, negativo, neutro)
-   🔄 **Processamento integrado** (áudio → texto → sentimento) em um
    único endpoint

------------------------------------------------------------------------

## Arquitetura

Usuário → Frontend (Gradio) → Backend (FastAPI + Whisper)

-   O usuário envia um áudio pela interface web
-   O frontend envia a requisição para o backend
-   O backend:
    1.  Transcreve o áudio
    2.  Analisa o sentimento do texto
    3.  Retorna o resultado

------------------------------------------------------------------------

## Tecnologias Utilizadas

-   Python
-   FastAPI
-   Gradio
-   Whisper (OpenAI)
-   Docker / Docker Compose

------------------------------------------------------------------------

## Endpoints da API

### GET /

Verifica se o servidor está ativo

### POST /transcrever

Recebe um arquivo de áudio e retorna o texto transcrito

### POST /analyze

Recebe um texto e retorna a análise de sentimento

### POST /transcrever-e-analisar

Recebe um áudio e retorna: - Texto transcrito - Sentimento - Score

------------------------------------------------------------------------

## Como executar

``` bash
git clone https://github.com/SEU_USUARIO/servicos-software-2026-1.git
cd servicos-software-2026-1
docker compose up --build
```

Acesse: http://localhost:7860

------------------------------------------------------------------------

## Estrutura do Projeto

backend-json/ → API (FastAPI + IA) gradio-json/ → Interface do usuário
(Gradio) compose.yaml → Orquestração dos containers

------------------------------------------------------------------------

## Conclusão

O projeto demonstra a integração entre serviços independentes utilizando
containers Docker, comunicação via APIs REST e aplicação de modelos de
Inteligência Artificial em um fluxo completo de processamento de dados.
