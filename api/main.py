from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routers import dados, modelos, predicao, metricas

app = FastAPI(
    title="API de Queimadas — LightGBM",
    description=(
        "API para análise de queimadas com Machine Learning. "
        "Permite consulta do dataset bdqueimadas_completo.parquet, "
        "listagem de modelos LightGBM, predição de intensidade/ocorrência "
        "e avaliação de eficiência dos modelos."
    ),
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(dados.router)
app.include_router(modelos.router)
app.include_router(predicao.router)
app.include_router(metricas.router)


@app.get("/", tags=["Status"])
def root():
    return {
        "status": "online",
        "docs": "/docs",
        "versao": "1.0.0",
        "descricao": "API de Queimadas com LightGBM",
    }


@app.get("/health", tags=["Status"])
def health():
    return {"status": "healthy"}